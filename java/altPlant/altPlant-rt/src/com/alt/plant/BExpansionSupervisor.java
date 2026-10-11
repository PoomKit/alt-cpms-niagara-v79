package com.alt.plant;

import javax.baja.nre.annotations.*;
import javax.baja.status.*;
import javax.baja.sys.*;

/**
 * Chiller expansion supervisor for slots CH03-CH06 (adds / removes expansion chillers by load).
 * ALT Reference V7.9 - Niagara 4.15 runtime component.
 */
@NiagaraType
@NiagaraProperty(name = "enable", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "plantStage", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "baseAvailable", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(2)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "averageLoad", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "upLoadPct", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(90)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "downLoadPct", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(75)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "stepDelay", type = "BRelTime", defaultValue = "BRelTime.makeMinutes(10)", flags = 0)
@NiagaraProperty(name = "scanRate", type = "BRelTime", defaultValue = "BRelTime.makeSeconds(5)", flags = 0)
@NiagaraProperty(name = "slot03Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "targetNum", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "stageAdd", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "baseAsked", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "chillersNeedingWater", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run03", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run04", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run05", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run06", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "statusText", type = "BString", defaultValue = "BString.make(\"\")", flags = Flags.SUMMARY | Flags.READONLY)
public class BExpansionSupervisor extends BComponent
{
/*+ ------------ BEGIN BAJA AUTO GENERATED CODE ------------ +*/

//region Property "enable"
  public static final Property enable = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getEnable() { return (BStatusBoolean)get(enable); }
  public void setEnable(BStatusBoolean v) { set(enable, v, null); }
//endregion Property "enable"

//region Property "plantStage"
  public static final Property plantStage = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getPlantStage() { return (BStatusNumeric)get(plantStage); }
  public void setPlantStage(BStatusNumeric v) { set(plantStage, v, null); }
//endregion Property "plantStage"

//region Property "baseAvailable"
  public static final Property baseAvailable = newProperty(Flags.SUMMARY, new BStatusNumeric(2), null);
  public BStatusNumeric getBaseAvailable() { return (BStatusNumeric)get(baseAvailable); }
  public void setBaseAvailable(BStatusNumeric v) { set(baseAvailable, v, null); }
//endregion Property "baseAvailable"

//region Property "averageLoad"
  public static final Property averageLoad = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getAverageLoad() { return (BStatusNumeric)get(averageLoad); }
  public void setAverageLoad(BStatusNumeric v) { set(averageLoad, v, null); }
//endregion Property "averageLoad"

//region Property "upLoadPct"
  public static final Property upLoadPct = newProperty(Flags.SUMMARY, new BStatusNumeric(90), null);
  public BStatusNumeric getUpLoadPct() { return (BStatusNumeric)get(upLoadPct); }
  public void setUpLoadPct(BStatusNumeric v) { set(upLoadPct, v, null); }
//endregion Property "upLoadPct"

//region Property "downLoadPct"
  public static final Property downLoadPct = newProperty(Flags.SUMMARY, new BStatusNumeric(75), null);
  public BStatusNumeric getDownLoadPct() { return (BStatusNumeric)get(downLoadPct); }
  public void setDownLoadPct(BStatusNumeric v) { set(downLoadPct, v, null); }
//endregion Property "downLoadPct"

//region Property "stepDelay"
  public static final Property stepDelay = newProperty(0, BRelTime.makeMinutes(10), null);
  public BRelTime getStepDelay() { return (BRelTime)get(stepDelay); }
  public void setStepDelay(BRelTime v) { set(stepDelay, v, null); }
//endregion Property "stepDelay"

//region Property "scanRate"
  public static final Property scanRate = newProperty(0, BRelTime.makeSeconds(5), null);
  public BRelTime getScanRate() { return (BRelTime)get(scanRate); }
  public void setScanRate(BRelTime v) { set(scanRate, v, null); }
//endregion Property "scanRate"

//region Property "slot03Installed"
  public static final Property slot03Installed = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot03Installed() { return (BStatusBoolean)get(slot03Installed); }
  public void setSlot03Installed(BStatusBoolean v) { set(slot03Installed, v, null); }
//endregion Property "slot03Installed"

//region Property "slot03Available"
  public static final Property slot03Available = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getSlot03Available() { return (BStatusBoolean)get(slot03Available); }
  public void setSlot03Available(BStatusBoolean v) { set(slot03Available, v, null); }
//endregion Property "slot03Available"

//region Property "slot04Installed"
  public static final Property slot04Installed = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot04Installed() { return (BStatusBoolean)get(slot04Installed); }
  public void setSlot04Installed(BStatusBoolean v) { set(slot04Installed, v, null); }
//endregion Property "slot04Installed"

//region Property "slot04Available"
  public static final Property slot04Available = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getSlot04Available() { return (BStatusBoolean)get(slot04Available); }
  public void setSlot04Available(BStatusBoolean v) { set(slot04Available, v, null); }
//endregion Property "slot04Available"

//region Property "slot05Installed"
  public static final Property slot05Installed = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot05Installed() { return (BStatusBoolean)get(slot05Installed); }
  public void setSlot05Installed(BStatusBoolean v) { set(slot05Installed, v, null); }
//endregion Property "slot05Installed"

//region Property "slot05Available"
  public static final Property slot05Available = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getSlot05Available() { return (BStatusBoolean)get(slot05Available); }
  public void setSlot05Available(BStatusBoolean v) { set(slot05Available, v, null); }
//endregion Property "slot05Available"

//region Property "slot06Installed"
  public static final Property slot06Installed = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot06Installed() { return (BStatusBoolean)get(slot06Installed); }
  public void setSlot06Installed(BStatusBoolean v) { set(slot06Installed, v, null); }
//endregion Property "slot06Installed"

//region Property "slot06Available"
  public static final Property slot06Available = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getSlot06Available() { return (BStatusBoolean)get(slot06Available); }
  public void setSlot06Available(BStatusBoolean v) { set(slot06Available, v, null); }
//endregion Property "slot06Available"

//region Property "targetNum"
  public static final Property targetNum = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getTargetNum() { return (BStatusNumeric)get(targetNum); }
  public void setTargetNum(BStatusNumeric v) { set(targetNum, v, null); }
//endregion Property "targetNum"

//region Property "stageAdd"
  public static final Property stageAdd = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getStageAdd() { return (BStatusNumeric)get(stageAdd); }
  public void setStageAdd(BStatusNumeric v) { set(stageAdd, v, null); }
//endregion Property "stageAdd"

//region Property "baseAsked"
  public static final Property baseAsked = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getBaseAsked() { return (BStatusNumeric)get(baseAsked); }
  public void setBaseAsked(BStatusNumeric v) { set(baseAsked, v, null); }
//endregion Property "baseAsked"

//region Property "chillersNeedingWater"
  public static final Property chillersNeedingWater = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getChillersNeedingWater() { return (BStatusNumeric)get(chillersNeedingWater); }
  public void setChillersNeedingWater(BStatusNumeric v) { set(chillersNeedingWater, v, null); }
//endregion Property "chillersNeedingWater"

//region Property "run03"
  public static final Property run03 = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getRun03() { return (BStatusBoolean)get(run03); }
  public void setRun03(BStatusBoolean v) { set(run03, v, null); }
//endregion Property "run03"

//region Property "run04"
  public static final Property run04 = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getRun04() { return (BStatusBoolean)get(run04); }
  public void setRun04(BStatusBoolean v) { set(run04, v, null); }
//endregion Property "run04"

//region Property "run05"
  public static final Property run05 = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getRun05() { return (BStatusBoolean)get(run05); }
  public void setRun05(BStatusBoolean v) { set(run05, v, null); }
//endregion Property "run05"

//region Property "run06"
  public static final Property run06 = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getRun06() { return (BStatusBoolean)get(run06); }
  public void setRun06(BStatusBoolean v) { set(run06, v, null); }
//endregion Property "run06"

//region Property "statusText"
  public static final Property statusText = newProperty(Flags.SUMMARY | Flags.READONLY, BString.make(""), null);
  public BString getStatusText() { return (BString)get(statusText); }
  public void setStatusText(BString v) { set(statusText, v, null); }
//endregion Property "statusText"

  @Override public Type getType() { return TYPE; }
  public static final Type TYPE = Sys.loadType(BExpansionSupervisor.class);
/*+ ------------ END BAJA AUTO GENERATED CODE -------------- +*/

  // ---------------------------------------------------------------- logic
  // Same rules as the V7.9 wire sheet (CHX_* blocks):
  //  * base chillers CH01-02 follow the plant stage: baseAsked = min(plantStage, baseAvailable)
  //  * when every base chiller asked is running and average load > upLoadPct for stepDelay -> add one expansion chiller
  //  * when average load < downLoadPct for stepDelay -> remove one
  //  * stageAdd never exceeds the number of installed + available slots 03-06
  //  * run03..run06 are given to installed + available slots in slot order
  //  * chillersNeedingWater = baseAsked + targetNum (used for pump / tower targets)

  private Clock.Ticket ticket;
  private long upSince = -1, downSince = -1;
  private int add;

  @Override public void started() throws Exception { super.started(); schedule(); }
  @Override public void stopped() throws Exception { if (ticket != null) ticket.cancel(); super.stopped(); }

  @Override public void changed(Property p, Context cx)
  {
    super.changed(p, cx);
    if (isRunning() && p == scanRate) schedule();
  }

  private void schedule()
  {
    if (ticket != null) ticket.cancel();
    long ms = Math.max(1000L, getScanRate().getMillis());
    ticket = Clock.schedulePeriodically(this, BRelTime.make(ms), execute, null);
  }

  public static final Action execute = newAction(Flags.HIDDEN, null);
  public void execute() { invoke(execute, null, null); }
  public void doExecute() { calculate(Clock.ticks()); }

  /** one scan; public for unit tests */
  public void calculate(long now)
  {
    boolean en = ok(getEnable()) && getEnable().getValue();
    BStatusBoolean[] inst = { getSlot03Installed(), getSlot04Installed(), getSlot05Installed(), getSlot06Installed() };
    BStatusBoolean[] avail = { getSlot03Available(), getSlot04Available(), getSlot05Available(), getSlot06Available() };
    int usable = 0;
    for (int i = 0; i < 4; i++) if (on(inst[i]) && on(avail[i])) usable++;

    int stage = (int)Math.round(num(getPlantStage()));
    int baseAsked = Math.max(0, Math.min(stage, (int)Math.round(num(getBaseAvailable()))));
    double load = num(getAverageLoad());
    long delay = getStepDelay().getMillis();

    if (!en || usable == 0) { add = 0; upSince = downSince = -1; }
    else
    {
      boolean baseFull = stage >= 2 && baseAsked >= 2;
      if (baseFull && load > num(getUpLoadPct())) { if (upSince < 0) upSince = now; } else upSince = -1;
      if (load < num(getDownLoadPct())) { if (downSince < 0) downSince = now; } else downSince = -1;
      if (upSince >= 0 && now - upSince >= delay && add < usable) { add++; upSince = now; }
      if (downSince >= 0 && now - downSince >= delay && add > 0) { add--; downSince = now; }
      if (!baseFull) add = 0;
      add = Math.min(add, usable);
    }

    BStatusBoolean[] run = new BStatusBoolean[4];
    int given = 0;
    for (int i = 0; i < 4; i++)
    {
      boolean r = en && on(inst[i]) && on(avail[i]) && given < add;
      if (r) given++;
      run[i] = new BStatusBoolean(r);
    }
    setRun03(run[0]); setRun04(run[1]); setRun05(run[2]); setRun06(run[3]);
    setStageAdd(new BStatusNumeric(add));
    setTargetNum(new BStatusNumeric(given));
    setBaseAsked(new BStatusNumeric(baseAsked));
    setChillersNeedingWater(new BStatusNumeric(baseAsked + given));
    setStatusText(BString.make(en ? ("usable " + usable + ", adding " + given + ", load " + Math.round(load) + "%") : "disabled"));
  }

  private static boolean ok(BStatusValue v) { return v != null && v.getStatus().isValid(); }
  private static boolean on(BStatusBoolean b) { return ok(b) && b.getValue(); }
  private static double num(BStatusNumeric n) { return ok(n) ? n.getValue() : 0; }

  @Override public BIcon getIcon() { return icon; }
  private static final BIcon icon = BIcon.std("control/control.png");
}
