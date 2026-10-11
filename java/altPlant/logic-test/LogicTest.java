import com.alt.plant.logic.ExpansionLogic;
import com.alt.plant.logic.ZoneStats;

/**
 * Unit tests of the plain-Java logic in altPlant-rt (no Niagara jars needed).
 * run: javac -d out ../altPlant-rt/src/com/alt/plant/logic/*.java LogicTest.java && java -cp out LogicTest
 * Cases follow the offline wire-sheet tests in tools/v79tests.py (X01-X09) plus the cases found in the V7.9 review.
 */
public class LogicTest
{
  static int run, failed;
  static final long MIN = 60000L;

  static void check(String id, boolean ok, String what)
  {
    run++;
    if (!ok) failed++;
    System.out.println((ok ? "PASS " : "FAIL ") + id + "  " + what);
  }

  static ExpansionLogic.Inputs plant(int stage)
  {
    ExpansionLogic.Inputs in = new ExpansionLogic.Inputs();
    in.plantRunRequest = true; in.stage2Request = stage >= 2; in.plantStage = stage;
    in.baseRunCount = stage; in.baseLoadSum = 70 * stage;
    return in;
  }

  /** run the logic from t0 for `ms` in 5 s scans; returns the last outputs */
  static ExpansionLogic.Outputs runFor(ExpansionLogic L, ExpansionLogic.Inputs in, long t0, long ms)
  {
    ExpansionLogic.Outputs o = null;
    for (long t = t0; t <= t0 + ms; t += 5000) o = L.step(in, t);
    return o;
  }

  static boolean[] req(ExpansionLogic.Outputs o) { return o.request; }

  public static void main(String[] a)
  {
    // X01 nothing installed -> no expansion request
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2);
      in.baseLoadSum = 2 * 95; ExpansionLogic.Outputs o = runFor(L, in, 0, 30 * MIN);
      check("X01", o.target == 0 && !o.request[0] && !o.request[1], "no slot available -> target " + o.target + ", no request"); }

    // X02 base chiller missing -> deficit -> CH03 replaces it
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.base02Healthy = false; in.available[0] = true;
      ExpansionLogic.Outputs o = L.step(in, 0);
      check("X02", o.deficit == 1 && o.target == 1 && o.request[0], "CH02 missing at stage 2 -> deficit " + o.deficit + ", run03 " + o.request[0]); }

    // R1 (review finding) CH01 trips while stage 2 at high load -> expansion units must NOT all stop
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.available[0] = in.available[1] = true;
      in.baseLoadSum = 2 * 95; runFor(L, in, 0, 11 * MIN);                       // one unit added for load
      in.running[0] = true; in.loadPct[0] = 95; in.valveOpen[0] = true;
      runFor(L, in, 11 * MIN, MIN);
      in.base01Healthy = false; in.baseRunCount = 1; in.baseLoadSum = 95;         // CH01 trips
      ExpansionLogic.Outputs o = L.step(in, 13 * MIN);
      check("R1", o.request[0] && o.request[1] && o.target == 2, "CH01 trip: deficit " + o.deficit + " + added " + o.stageAdd + " -> run03 " + o.request[0] + ", run04 " + o.request[1]); }

    // X03 stage up after the delay (only one step), stage down after the down delay
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.available[0] = in.available[1] = true;
      in.baseLoadSum = 2 * 95;
      ExpansionLogic.Outputs o9 = runFor(L, in, 0, 9 * MIN);
      ExpansionLogic.Outputs o11 = runFor(L, in, 9 * MIN + 5000, 2 * MIN);
      ExpansionLogic.Outputs o30 = runFor(L, in, 11 * MIN + 5000, 19 * MIN);      // CH03 not running yet -> no second step
      check("X03a", o9.stageAdd == 0 && o11.stageAdd == 1 && o30.stageAdd == 1 && o30.request[0] && !o30.request[1],
            "95 % load: stage at 9 min " + o9.stageAdd + ", 11 min " + o11.stageAdd + ", 30 min " + o30.stageAdd + " (one unit only while it is not running)");
      in.running[0] = true; in.loadPct[0] = 40; in.baseLoadSum = 2 * 40;
      ExpansionLogic.Outputs d14 = runFor(L, in, 31 * MIN, 14 * MIN);
      ExpansionLogic.Outputs d16 = runFor(L, in, 45 * MIN + 5000, 2 * MIN);
      check("X03b", d14.stageAdd == 1 && d16.stageAdd == 0 && !d16.request[0], "40 % load: stage at 14 min " + d14.stageAdd + ", 16 min " + d16.stageAdd); }

    // CHWS high also adds a unit (load below the up limit)
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.available[0] = true; in.chwsHigh = true;
      ExpansionLogic.Outputs o = runFor(L, in, 0, 11 * MIN);
      check("R2", o.stageAdd == 1 && o.request[0], "CHWS above the stage-up limit -> stage " + o.stageAdd); }

    // load if one chiller less still too high -> no stage down
    { ExpansionLogic L = new ExpansionLogic(); L.setStageAdd(1); ExpansionLogic.Inputs in = plant(2); in.available[0] = true;
      in.running[0] = true; in.loadPct[0] = 60; in.baseLoadSum = 2 * 60;            // average 60 % but 3 -> 2 units = 90 %
      ExpansionLogic.Outputs o = runFor(L, in, 0, 30 * MIN);
      check("R3", o.stageAdd == 1, "average 60 %, with one less 90 % -> stays at " + o.stageAdd + " (no short cycling)"); }

    // X05 / X06 unavailable slot (failed / maintenance) is skipped
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.base02Healthy = false;
      in.available[0] = false; in.available[1] = true;
      ExpansionLogic.Outputs o = L.step(in, 0);
      check("X05", !o.request[0] && o.request[1], "CH03 not available -> run04 " + o.request[1]); }

    // X08 master switch
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.base02Healthy = false; in.available[0] = true; in.enable = false;
      check("X08", !L.step(in, 0).request[0], "enable off -> no request"); }

    // plant off -> step register cleared
    { ExpansionLogic L = new ExpansionLogic(); L.setStageAdd(2); ExpansionLogic.Inputs in = plant(2); in.plantRunRequest = false;
      check("R4", L.step(in, 0).stageAdd == 0, "plant run request off -> stage 0"); }

    // fail-safe: invalid load input holds the decision
    { ExpansionLogic L = new ExpansionLogic(); L.setStageAdd(1); ExpansionLogic.Inputs in = plant(2); in.available[0] = true;
      in.running[0] = true; in.loadValid[0] = false; in.baseLoadSum = 2 * 20;
      ExpansionLogic.Outputs o = runFor(L, in, 0, 30 * MIN);
      check("R5", o.fault && o.stageAdd == 1 && o.request[0], "load signal invalid for 30 min -> fault " + o.fault + ", stage held " + o.stageAdd);
      in.plantStageValid = false;
      ExpansionLogic.Outputs p = L.step(in, 31 * MIN);
      check("R6", p.fault && p.target == 1, "plant stage invalid -> target held " + p.target); }

    // rotation: fewest run hours first, running unit never displaced, slot order when rotation is off
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.base02Healthy = false;
      in.available[0] = in.available[1] = true; in.runHours[0] = 500; in.runHours[1] = 100;
      ExpansionLogic.Outputs o = L.step(in, 0);
      check("R7", !o.request[0] && o.request[1], "CH03 500 h, CH04 100 h -> CH04 starts");
      in.running[0] = true; in.loadPct[0] = 70;
      o = L.step(in, 5000);
      check("R8", o.request[0] && !o.request[1], "CH03 already running -> it keeps running (no swap)");
      in.running[0] = false; in.rotateByRuntime = false;
      o = L.step(in, 10000);
      check("R9", o.request[0] && !o.request[1], "rotation off -> slot order (CH03)"); }

    // stageAdd restored after restart
    { ExpansionLogic L = new ExpansionLogic(); L.setStageAdd(9);
      check("R10", L.getStageAdd() == ExpansionLogic.SLOTS, "persisted value clamped to " + L.getStageAdd()); }

    // water demand = max(valves open / post-run, asked)
    { ExpansionLogic L = new ExpansionLogic(); ExpansionLogic.Inputs in = plant(2); in.base02Healthy = false; in.available[0] = true;
      in.base01PostRun = true;
      ExpansionLogic.Outputs o = L.step(in, 0);
      check("R11", o.waterDemand == 2 && o.valvesOpen == 1, "1 base asked + 1 expansion asked -> water demand " + o.waterDemand + ", valves open " + o.valvesOpen); }

    // ---- zone statistics
    { double[][] v = { { 24, 50, 700 }, { 26, 70, 1200 }, { 99, 0, 0 } };
      boolean[][] ok = { { true, true, true }, { true, true, true }, { false, false, false } };
      ZoneStats z = ZoneStats.of(v, ok, new double[] { 25, 65, 1000 });
      check("Z1", z.zonesValid == 2 && z.avg(0) == 25.0 && z.maxOf(2) == 1200 && z.high[0] == 1 && z.high[1] == 1 && z.high[2] == 1 && z.anyHigh(),
            "2 valid zones: temp avg " + z.avg(0) + ", CO2 max " + z.maxOf(2) + ", high counts " + z.high[0] + "/" + z.high[1] + "/" + z.high[2]);
      double[][] w = { { 0, 55, 0 } }; boolean[][] wok = { { false, true, false } };
      ZoneStats y = ZoneStats.of(w, wok, new double[] { Double.NaN, Double.NaN, Double.NaN });
      check("Z2", y.zonesValid == 1 && y.valid[0] == 0 && Double.isNaN(y.avg(0)) && y.avg(1) == 55 && !y.anyHigh(),
            "RH-only zone counts as valid (" + y.zonesValid + "), temp avg null, no limit -> no alarm"); }

    System.out.println(run - failed + "/" + run + " PASS");
    if (failed > 0) System.exit(1);
  }
}
