package com.alt.plant;

import com.alt.plant.logic.ExpansionLogic;
import javax.baja.nre.annotations.*;
import javax.baja.status.*;
import javax.baja.sys.*;

/**
 * Chiller expansion supervisor for slots CH03-CH06: same rules as the V7.9 wire sheet blocks CHX_* in
 * ChillerPlant/Expansion/Supervisor (see {@link ExpansionLogic}). ALT Reference V7.9 - Niagara 4.15 runtime component.
 *
 * Inputs (link from the station):           PlantRunRequest, Stage2Request, PlantStage, PlantPermissive, CHX_Enable,
 *   CH01TrainHealthy / CH02TrainHealthy, CH01PostRun / CH02PostRun, CH_RunNum, ChillerLoadSum, ChwsAboveStageUpLimit,
 *   Stg_DownChwsOk, per slot: CHnn_Installed, CHnn_Avail, CHnnRunProof, CHnn_NeedNum (as boolean), CHnnLoadPct, CHnn_RuntimeHours.
 * Outputs: run03..run06 (= CHX_Req03..06), targetNum, stageAdd (kept over a restart), deficit, averageLoad,
 *   chillersNeedingWater (pump / tower demand), valvesOpen, fault (input invalid: last decision held).
 */
@NiagaraType
@NiagaraProperty(name = "enable", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "plantPermissive", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "plantRunRequest", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "stage2Request", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "plantStage", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "base01Healthy", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "base02Healthy", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "base01PostRun", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "base02PostRun", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "baseRunCount", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "baseLoadSum", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "chwsHigh", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "chwsDownOk", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "upLoadPct", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(90)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "downLoadPct", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(75)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "rotateByRuntime", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "upDelay", type = "BRelTime", defaultValue = "BRelTime.makeMinutes(10)", flags = 0)
@NiagaraProperty(name = "downDelay", type = "BRelTime", defaultValue = "BRelTime.makeMinutes(15)", flags = 0)
@NiagaraProperty(name = "scanRate", type = "BRelTime", defaultValue = "BRelTime.makeSeconds(5)", flags = 0)
@NiagaraProperty(name = "slot03Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03Running", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03ValveOpen", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03Load", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot03Hours", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Running", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04ValveOpen", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Load", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot04Hours", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Running", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05ValveOpen", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Load", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot05Hours", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Installed", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Available", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(true)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Running", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06ValveOpen", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Load", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "slot06Hours", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "deficit", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "stageAdd", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "targetNum", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "averageLoad", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "chillersNeedingWater", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "valvesOpen", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run03", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run04", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run05", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "run06", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "fault", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "statusText", type = "BString", defaultValue = "BString.make(\"\")", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraAction(name = "execute", flags = Flags.HIDDEN)
public class BExpansionSupervisor extends BComponent
{
/*+ ------------ BEGIN BAJA AUTO GENERATED CODE ------------ +*/

//region Property "enable"
  public static final Property enable = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getEnable() { return (BStatusBoolean)get(enable); }
  public void setEnable(BStatusBoolean v) { set(enable, v, null); }
//endregion Property "enable"

//region Property "plantPermissive"
  public static final Property plantPermissive = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getPlantPermissive() { return (BStatusBoolean)get(plantPermissive); }
  public void setPlantPermissive(BStatusBoolean v) { set(plantPermissive, v, null); }
//endregion Property "plantPermissive"

//region Property "plantRunRequest"
  public static final Property plantRunRequest = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getPlantRunRequest() { return (BStatusBoolean)get(plantRunRequest); }
  public void setPlantRunRequest(BStatusBoolean v) { set(plantRunRequest, v, null); }
//endregion Property "plantRunRequest"

//region Property "stage2Request"
  public static final Property stage2Request = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getStage2Request() { return (BStatusBoolean)get(stage2Request); }
  public void setStage2Request(BStatusBoolean v) { set(stage2Request, v, null); }
//endregion Property "stage2Request"

//region Property "plantStage"
  public static final Property plantStage = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getPlantStage() { return (BStatusNumeric)get(plantStage); }
  public void setPlantStage(BStatusNumeric v) { set(plantStage, v, null); }
//endregion Property "plantStage"

//region Property "base01Healthy"
  public static final Property base01Healthy = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getBase01Healthy() { return (BStatusBoolean)get(base01Healthy); }
  public void setBase01Healthy(BStatusBoolean v) { set(base01Healthy, v, null); }
//endregion Property "base01Healthy"

//region Property "base02Healthy"
  public static final Property base02Healthy = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getBase02Healthy() { return (BStatusBoolean)get(base02Healthy); }
  public void setBase02Healthy(BStatusBoolean v) { set(base02Healthy, v, null); }
//endregion Property "base02Healthy"

//region Property "base01PostRun"
  public static final Property base01PostRun = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getBase01PostRun() { return (BStatusBoolean)get(base01PostRun); }
  public void setBase01PostRun(BStatusBoolean v) { set(base01PostRun, v, null); }
//endregion Property "base01PostRun"

//region Property "base02PostRun"
  public static final Property base02PostRun = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getBase02PostRun() { return (BStatusBoolean)get(base02PostRun); }
  public void setBase02PostRun(BStatusBoolean v) { set(base02PostRun, v, null); }
//endregion Property "base02PostRun"

//region Property "baseRunCount"
  public static final Property baseRunCount = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getBaseRunCount() { return (BStatusNumeric)get(baseRunCount); }
  public void setBaseRunCount(BStatusNumeric v) { set(baseRunCount, v, null); }
//endregion Property "baseRunCount"

//region Property "baseLoadSum"
  public static final Property baseLoadSum = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getBaseLoadSum() { return (BStatusNumeric)get(baseLoadSum); }
  public void setBaseLoadSum(BStatusNumeric v) { set(baseLoadSum, v, null); }
//endregion Property "baseLoadSum"

//region Property "chwsHigh"
  public static final Property chwsHigh = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getChwsHigh() { return (BStatusBoolean)get(chwsHigh); }
  public void setChwsHigh(BStatusBoolean v) { set(chwsHigh, v, null); }
//endregion Property "chwsHigh"

//region Property "chwsDownOk"
  public static final Property chwsDownOk = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getChwsDownOk() { return (BStatusBoolean)get(chwsDownOk); }
  public void setChwsDownOk(BStatusBoolean v) { set(chwsDownOk, v, null); }
//endregion Property "chwsDownOk"

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

//region Property "rotateByRuntime"
  public static final Property rotateByRuntime = newProperty(Flags.SUMMARY, new BStatusBoolean(true), null);
  public BStatusBoolean getRotateByRuntime() { return (BStatusBoolean)get(rotateByRuntime); }
  public void setRotateByRuntime(BStatusBoolean v) { set(rotateByRuntime, v, null); }
//endregion Property "rotateByRuntime"

//region Property "upDelay"
  public static final Property upDelay = newProperty(0, BRelTime.makeMinutes(10), null);
  public BRelTime getUpDelay() { return (BRelTime)get(upDelay); }
  public void setUpDelay(BRelTime v) { set(upDelay, v, null); }
//endregion Property "upDelay"

//region Property "downDelay"
  public static final Property downDelay = newProperty(0, BRelTime.makeMinutes(15), null);
  public BRelTime getDownDelay() { return (BRelTime)get(downDelay); }
  public void setDownDelay(BRelTime v) { set(downDelay, v, null); }
//endregion Property "downDelay"

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

//region Property "slot03Running"
  public static final Property slot03Running = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot03Running() { return (BStatusBoolean)get(slot03Running); }
  public void setSlot03Running(BStatusBoolean v) { set(slot03Running, v, null); }
//endregion Property "slot03Running"

//region Property "slot03ValveOpen"
  public static final Property slot03ValveOpen = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot03ValveOpen() { return (BStatusBoolean)get(slot03ValveOpen); }
  public void setSlot03ValveOpen(BStatusBoolean v) { set(slot03ValveOpen, v, null); }
//endregion Property "slot03ValveOpen"

//region Property "slot03Load"
  public static final Property slot03Load = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot03Load() { return (BStatusNumeric)get(slot03Load); }
  public void setSlot03Load(BStatusNumeric v) { set(slot03Load, v, null); }
//endregion Property "slot03Load"

//region Property "slot03Hours"
  public static final Property slot03Hours = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot03Hours() { return (BStatusNumeric)get(slot03Hours); }
  public void setSlot03Hours(BStatusNumeric v) { set(slot03Hours, v, null); }
//endregion Property "slot03Hours"

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

//region Property "slot04Running"
  public static final Property slot04Running = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot04Running() { return (BStatusBoolean)get(slot04Running); }
  public void setSlot04Running(BStatusBoolean v) { set(slot04Running, v, null); }
//endregion Property "slot04Running"

//region Property "slot04ValveOpen"
  public static final Property slot04ValveOpen = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot04ValveOpen() { return (BStatusBoolean)get(slot04ValveOpen); }
  public void setSlot04ValveOpen(BStatusBoolean v) { set(slot04ValveOpen, v, null); }
//endregion Property "slot04ValveOpen"

//region Property "slot04Load"
  public static final Property slot04Load = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot04Load() { return (BStatusNumeric)get(slot04Load); }
  public void setSlot04Load(BStatusNumeric v) { set(slot04Load, v, null); }
//endregion Property "slot04Load"

//region Property "slot04Hours"
  public static final Property slot04Hours = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot04Hours() { return (BStatusNumeric)get(slot04Hours); }
  public void setSlot04Hours(BStatusNumeric v) { set(slot04Hours, v, null); }
//endregion Property "slot04Hours"

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

//region Property "slot05Running"
  public static final Property slot05Running = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot05Running() { return (BStatusBoolean)get(slot05Running); }
  public void setSlot05Running(BStatusBoolean v) { set(slot05Running, v, null); }
//endregion Property "slot05Running"

//region Property "slot05ValveOpen"
  public static final Property slot05ValveOpen = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot05ValveOpen() { return (BStatusBoolean)get(slot05ValveOpen); }
  public void setSlot05ValveOpen(BStatusBoolean v) { set(slot05ValveOpen, v, null); }
//endregion Property "slot05ValveOpen"

//region Property "slot05Load"
  public static final Property slot05Load = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot05Load() { return (BStatusNumeric)get(slot05Load); }
  public void setSlot05Load(BStatusNumeric v) { set(slot05Load, v, null); }
//endregion Property "slot05Load"

//region Property "slot05Hours"
  public static final Property slot05Hours = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot05Hours() { return (BStatusNumeric)get(slot05Hours); }
  public void setSlot05Hours(BStatusNumeric v) { set(slot05Hours, v, null); }
//endregion Property "slot05Hours"

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

//region Property "slot06Running"
  public static final Property slot06Running = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot06Running() { return (BStatusBoolean)get(slot06Running); }
  public void setSlot06Running(BStatusBoolean v) { set(slot06Running, v, null); }
//endregion Property "slot06Running"

//region Property "slot06ValveOpen"
  public static final Property slot06ValveOpen = newProperty(Flags.SUMMARY, new BStatusBoolean(false), null);
  public BStatusBoolean getSlot06ValveOpen() { return (BStatusBoolean)get(slot06ValveOpen); }
  public void setSlot06ValveOpen(BStatusBoolean v) { set(slot06ValveOpen, v, null); }
//endregion Property "slot06ValveOpen"

//region Property "slot06Load"
  public static final Property slot06Load = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot06Load() { return (BStatusNumeric)get(slot06Load); }
  public void setSlot06Load(BStatusNumeric v) { set(slot06Load, v, null); }
//endregion Property "slot06Load"

//region Property "slot06Hours"
  public static final Property slot06Hours = newProperty(Flags.SUMMARY, new BStatusNumeric(0), null);
  public BStatusNumeric getSlot06Hours() { return (BStatusNumeric)get(slot06Hours); }
  public void setSlot06Hours(BStatusNumeric v) { set(slot06Hours, v, null); }
//endregion Property "slot06Hours"

//region Property "deficit"
  public static final Property deficit = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getDeficit() { return (BStatusNumeric)get(deficit); }
  public void setDeficit(BStatusNumeric v) { set(deficit, v, null); }
//endregion Property "deficit"

//region Property "stageAdd"
  public static final Property stageAdd = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getStageAdd() { return (BStatusNumeric)get(stageAdd); }
  public void setStageAdd(BStatusNumeric v) { set(stageAdd, v, null); }
//endregion Property "stageAdd"

//region Property "targetNum"
  public static final Property targetNum = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getTargetNum() { return (BStatusNumeric)get(targetNum); }
  public void setTargetNum(BStatusNumeric v) { set(targetNum, v, null); }
//endregion Property "targetNum"

//region Property "averageLoad"
  public static final Property averageLoad = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getAverageLoad() { return (BStatusNumeric)get(averageLoad); }
  public void setAverageLoad(BStatusNumeric v) { set(averageLoad, v, null); }
//endregion Property "averageLoad"

//region Property "chillersNeedingWater"
  public static final Property chillersNeedingWater = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getChillersNeedingWater() { return (BStatusNumeric)get(chillersNeedingWater); }
  public void setChillersNeedingWater(BStatusNumeric v) { set(chillersNeedingWater, v, null); }
//endregion Property "chillersNeedingWater"

//region Property "valvesOpen"
  public static final Property valvesOpen = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getValvesOpen() { return (BStatusNumeric)get(valvesOpen); }
  public void setValvesOpen(BStatusNumeric v) { set(valvesOpen, v, null); }
//endregion Property "valvesOpen"

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

//region Property "fault"
  public static final Property fault = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getFault() { return (BStatusBoolean)get(fault); }
  public void setFault(BStatusBoolean v) { set(fault, v, null); }
//endregion Property "fault"

//region Property "statusText"
  public static final Property statusText = newProperty(Flags.SUMMARY | Flags.READONLY, BString.make(""), null);
  public BString getStatusText() { return (BString)get(statusText); }
  public void setStatusText(BString v) { set(statusText, v, null); }
//endregion Property "statusText"

//region Action "execute"
  public static final Action execute = newAction(Flags.HIDDEN, null);
  public void execute() { invoke(execute, null, null); }
//endregion Action "execute"

  @Override public Type getType() { return TYPE; }
  public static final Type TYPE = Sys.loadType(BExpansionSupervisor.class);
/*+ ------------ END BAJA AUTO GENERATED CODE -------------- +*/

  private final ExpansionLogic logic = new ExpansionLogic();
  private Clock.Ticket ticket;

  @Override public void started() throws Exception
  {
    super.started();
    if (getStageAdd().getStatus().isValid()) logic.setStageAdd((int)Math.round(getStageAdd().getValue()));   // persisted
    schedule();
  }

  @Override public void stopped() throws Exception { if (ticket != null) ticket.cancel(); super.stopped(); }

  @Override public void changed(Property p, Context cx)
  {
    super.changed(p, cx);
    if (isRunning() && p == scanRate) schedule();
  }

  private void schedule()
  {
    if (ticket != null) ticket.cancel();
    ticket = Clock.schedulePeriodically(this, BRelTime.make(Math.max(1000L, getScanRate().getMillis())), execute, null);
  }

  public void doExecute() { calculate(Clock.ticks()); }

  /** one scan */
  public void calculate(long now)
  {
    ExpansionLogic.Inputs in = new ExpansionLogic.Inputs();
    in.enable = on(getEnable()); in.plantPermissive = on(getPlantPermissive());
    in.plantRunRequest = on(getPlantRunRequest()); in.stage2Request = on(getStage2Request());
    in.plantStage = getPlantStage().getValue(); in.plantStageValid = ok(getPlantStage());
    in.base01Healthy = on(getBase01Healthy()); in.base02Healthy = on(getBase02Healthy());
    in.base01PostRun = on(getBase01PostRun()); in.base02PostRun = on(getBase02PostRun());
    in.baseRunCount = getBaseRunCount().getValue(); in.baseLoadSum = getBaseLoadSum().getValue();
    in.baseValid = ok(getBaseRunCount()) && ok(getBaseLoadSum());
    in.chwsHigh = on(getChwsHigh()); in.chwsDownOk = on(getChwsDownOk());
    in.upLoadPct = ok(getUpLoadPct()) ? getUpLoadPct().getValue() : 90;
    in.downLoadPct = ok(getDownLoadPct()) ? getDownLoadPct().getValue() : 75;
    in.upDelayMs = getUpDelay().getMillis(); in.downDelayMs = getDownDelay().getMillis();
    in.rotateByRuntime = on(getRotateByRuntime());
    BStatusBoolean[] inst = { getSlot03Installed(), getSlot04Installed(), getSlot05Installed(), getSlot06Installed() };
    BStatusBoolean[] avail = { getSlot03Available(), getSlot04Available(), getSlot05Available(), getSlot06Available() };
    BStatusBoolean[] run = { getSlot03Running(), getSlot04Running(), getSlot05Running(), getSlot06Running() };
    BStatusBoolean[] valve = { getSlot03ValveOpen(), getSlot04ValveOpen(), getSlot05ValveOpen(), getSlot06ValveOpen() };
    BStatusNumeric[] load = { getSlot03Load(), getSlot04Load(), getSlot05Load(), getSlot06Load() };
    BStatusNumeric[] hours = { getSlot03Hours(), getSlot04Hours(), getSlot05Hours(), getSlot06Hours() };
    for (int i = 0; i < ExpansionLogic.SLOTS; i++)
    {
      in.available[i] = on(inst[i]) && on(avail[i]);
      in.running[i] = on(inst[i]) && on(run[i]);
      in.valveOpen[i] = on(valve[i]);
      in.loadPct[i] = load[i].getValue(); in.loadValid[i] = ok(load[i]);
      in.runHours[i] = ok(hours[i]) ? hours[i].getValue() : 0;
    }

    ExpansionLogic.Outputs o = logic.step(in, now);
    BStatus st = o.fault ? BStatus.fault : BStatus.ok;
    setRun03(new BStatusBoolean(o.request[0])); setRun04(new BStatusBoolean(o.request[1]));
    setRun05(new BStatusBoolean(o.request[2])); setRun06(new BStatusBoolean(o.request[3]));
    setDeficit(new BStatusNumeric(o.deficit, st));
    setStageAdd(new BStatusNumeric(o.stageAdd));
    setTargetNum(new BStatusNumeric(o.target, st));
    setAverageLoad(new BStatusNumeric(Math.round(o.averageLoad * 10) / 10.0, st));
    setChillersNeedingWater(new BStatusNumeric(o.waterDemand));
    setValvesOpen(new BStatusNumeric(o.valvesOpen));
    setFault(new BStatusBoolean(o.fault));
    setStatusText(BString.make(o.text));
  }

  private static boolean ok(BStatusValue v) { return v != null && v.getStatus().isValid(); }
  private static boolean on(BStatusBoolean b) { return ok(b) && b.getValue(); }

  @Override public BIcon getIcon() { return icon; }
  private static final BIcon icon = BIcon.std("control/control.png");
}
