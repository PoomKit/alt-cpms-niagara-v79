package com.alt.plant.logic;

/**
 * Expansion chiller supervisor for slots CH03-CH06 - plain Java, no Niagara dependency (unit tested in CI).
 * Same rules as the V7.9 wire sheet (tools/v79_scale.py supervisor() / ranks()):
 * <ul>
 *  <li>deficit   = max(0, plantStage - healthy base chillers)  (expansion units replace missing base units)</li>
 *  <li>stageAdd  += 1 when PlantRunRequest, Stage2Request, every wanted expansion unit runs, (average load &gt;= up % or CHWS high)
 *      and there is a free available slot, continuously for upDelay</li>
 *  <li>stageAdd  -= 1 when stageAdd &gt;= 1, the load would stay below down % with one chiller less, CHWS is OK
 *      and no more expansion units run than wanted, continuously for downDelay</li>
 *  <li>stageAdd  = 0 when the plant run request goes off; limited to 0..4</li>
 *  <li>target    = deficit + stageAdd; request = available AND rank &lt;= target AND permissive AND enable</li>
 *  <li>rank: running units first, then fewest run hours (rotateByRuntime), then slot order</li>
 *  <li>waterDemand = max(base post-run + expansion valves open, base asked + expansion requests)</li>
 * </ul>
 * Fail-safe: when a required input is invalid the last stageAdd / deficit are held and {@link Outputs#fault} is set.
 */
public final class ExpansionLogic
{
  public static final int SLOTS = 4;                  // CH03..CH06
  public static final double RUNNING_BIAS = 1.0e6;

  /** one scan of inputs; valid flags are the Niagara status (true = ok) */
  public static final class Inputs
  {
    public boolean enable = true, plantPermissive = true, plantRunRequest, stage2Request, chwsHigh, chwsDownOk = true;
    public double plantStage; public boolean plantStageValid = true;
    public boolean base01Healthy = true, base02Healthy = true, base01PostRun, base02PostRun;
    public double baseRunCount, baseLoadSum; public boolean baseValid = true;
    public double upLoadPct = 90, downLoadPct = 75;
    public long upDelayMs = 600000, downDelayMs = 900000;
    public boolean rotateByRuntime = true;
    public final boolean[] available = new boolean[SLOTS];
    public final boolean[] running = new boolean[SLOTS];
    public final boolean[] valveOpen = new boolean[SLOTS];
    public final double[] loadPct = new double[SLOTS];
    public final boolean[] loadValid = { true, true, true, true };
    public final double[] runHours = new double[SLOTS];
  }

  public static final class Outputs
  {
    public int deficit, stageAdd, target, availCount, expRunning;
    public double averageLoad, loadIfOneLess;
    public int waterDemand, valvesOpen;
    public final boolean[] request = new boolean[SLOTS];
    public final int[] rank = new int[SLOTS];
    public boolean fault;
    public String text = "";
  }

  private int stageAdd, deficit;
  private long upSince = -1, downSince = -1;

  public int getStageAdd() { return stageAdd; }
  /** restore the persisted value after a station restart */
  public void setStageAdd(int v) { stageAdd = Math.max(0, Math.min(SLOTS, v)); }

  public Outputs step(Inputs in, long now)
  {
    Outputs o = new Outputs();
    int baseAvail = (in.base01Healthy ? 1 : 0) + (in.base02Healthy ? 1 : 0);
    double expLoad = 0;
    boolean loadsOk = true;
    for (int i = 0; i < SLOTS; i++)
    {
      if (in.available[i]) o.availCount++;
      if (in.running[i]) { o.expRunning++; if (in.loadValid[i]) expLoad += in.loadPct[i]; else loadsOk = false; }
    }
    o.fault = !in.plantStageValid || !in.baseValid || !loadsOk;
    int stage = (int)Math.round(in.plantStage);

    if (o.fault)
    {                                                   // hold the last decision, no step while blind
      upSince = downSince = -1;
    }
    else
    {
      deficit = Math.max(0, stage - baseAvail);
      double totalRun = in.baseRunCount + o.expRunning, totalLoad = in.baseLoadSum + expLoad;
      o.averageLoad = totalLoad / Math.max(totalRun, 1);
      o.loadIfOneLess = totalLoad / Math.max(totalRun - 1, 1);
      int target = deficit + stageAdd;
      boolean allRunning = o.expRunning >= target;
      boolean needMore = o.averageLoad >= in.upLoadPct || in.chwsHigh;
      boolean up = in.plantRunRequest && in.stage2Request && allRunning && needMore && target < o.availCount;
      boolean down = stageAdd >= 1 && o.loadIfOneLess < in.downLoadPct && in.chwsDownOk && o.expRunning <= target;
      if (up) { if (upSince < 0) upSince = now; } else upSince = -1;
      if (down) { if (downSince < 0) downSince = now; } else downSince = -1;
      if (upSince >= 0 && now - upSince >= in.upDelayMs) { stageAdd++; upSince = -1; }
      else if (downSince >= 0 && now - downSince >= in.downDelayMs) { stageAdd--; downSince = -1; }
      if (!in.plantRunRequest) { stageAdd = 0; upSince = downSince = -1; }
      stageAdd = Math.max(0, Math.min(SLOTS, stageAdd));
    }
    o.deficit = deficit;
    o.stageAdd = stageAdd;
    o.target = deficit + stageAdd;

    double[] key = new double[SLOTS];
    for (int i = 0; i < SLOTS; i++)
      key[i] = (in.rotateByRuntime ? in.runHours[i] : 0) + (i + 3) / 1000.0 - (in.running[i] ? RUNNING_BIAS : 0);
    int requests = 0;
    for (int i = 0; i < SLOTS; i++)
    {
      int r = 1;
      for (int j = 0; j < SLOTS; j++) if (j != i && in.available[j] && key[j] < key[i]) r++;
      o.rank[i] = r;
      o.request[i] = in.available[i] && r <= o.target && in.plantPermissive && in.enable;
      if (o.request[i]) requests++;
    }

    int needNow = (in.base01PostRun ? 1 : 0) + (in.base02PostRun ? 1 : 0);
    for (int i = 0; i < SLOTS; i++) if (in.valveOpen[i]) needNow++;
    int asked = Math.max(0, Math.min(stage, baseAvail)) + requests;
    o.valvesOpen = needNow;
    o.waterDemand = Math.max(needNow, asked);
    o.text = (o.fault ? "FAULT input invalid - holding; " : "") + "deficit " + o.deficit + " + added " + o.stageAdd
           + " = target " + o.target + ", available " + o.availCount + ", load " + Math.round(o.averageLoad) + "%";
    return o;
  }
}
