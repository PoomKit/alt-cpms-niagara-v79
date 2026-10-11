package com.alt.plant;

import com.alt.plant.logic.ZoneStats;
import javax.baja.nre.annotations.*;
import javax.baja.status.*;
import javax.baja.sys.*;

/**
 * Floor zone statistics: average / max / count above limit for temperature, RH and CO2 (up to 16 zones), see {@link ZoneStats}.
 * zonesValid = zones with any valid value; tempValid / rhValid / co2Valid = valid values per metric.
 * ALT Reference V7.9 - Niagara 4.15 runtime component.
 */
@NiagaraType
@NiagaraProperty(name = "scanRate", type = "BRelTime", defaultValue = "BRelTime.makeSeconds(10)", flags = 0)
@NiagaraProperty(name = "tempHigh", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(26)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "rhHigh", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(65)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "co2High", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(1000)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t01", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h01", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c01", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t02", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h02", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c02", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t03", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h03", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c03", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t04", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h04", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c04", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t05", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h05", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c05", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t06", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h06", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c06", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t07", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h07", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c07", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t08", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h08", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c08", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t09", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h09", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c09", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t10", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h10", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c10", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t11", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h11", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c11", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t12", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h12", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c12", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t13", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h13", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c13", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t14", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h14", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c14", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t15", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h15", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c15", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "t16", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "h16", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "c16", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0, BStatus.nullStatus)", flags = Flags.SUMMARY)
@NiagaraProperty(name = "zonesValid", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "tempValid", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "rhValid", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "co2Valid", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "tempAvg", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "tempMax", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "rhAvg", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "rhMax", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "co2Avg", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "co2Max", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "zonesHot", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "zonesHumid", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "zonesCo2High", type = "BStatusNumeric", defaultValue = "new BStatusNumeric(0)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraProperty(name = "anyAlarm", type = "BStatusBoolean", defaultValue = "new BStatusBoolean(false)", flags = Flags.SUMMARY | Flags.READONLY)
@NiagaraAction(name = "execute", flags = Flags.HIDDEN)
public class BZoneAggregator extends BComponent
{
/*+ ------------ BEGIN BAJA AUTO GENERATED CODE ------------ +*/

//region Property "scanRate"
  public static final Property scanRate = newProperty(0, BRelTime.makeSeconds(10), null);
  public BRelTime getScanRate() { return (BRelTime)get(scanRate); }
  public void setScanRate(BRelTime v) { set(scanRate, v, null); }
//endregion Property "scanRate"

//region Property "tempHigh"
  public static final Property tempHigh = newProperty(Flags.SUMMARY, new BStatusNumeric(26), null);
  public BStatusNumeric getTempHigh() { return (BStatusNumeric)get(tempHigh); }
  public void setTempHigh(BStatusNumeric v) { set(tempHigh, v, null); }
//endregion Property "tempHigh"

//region Property "rhHigh"
  public static final Property rhHigh = newProperty(Flags.SUMMARY, new BStatusNumeric(65), null);
  public BStatusNumeric getRhHigh() { return (BStatusNumeric)get(rhHigh); }
  public void setRhHigh(BStatusNumeric v) { set(rhHigh, v, null); }
//endregion Property "rhHigh"

//region Property "co2High"
  public static final Property co2High = newProperty(Flags.SUMMARY, new BStatusNumeric(1000), null);
  public BStatusNumeric getCo2High() { return (BStatusNumeric)get(co2High); }
  public void setCo2High(BStatusNumeric v) { set(co2High, v, null); }
//endregion Property "co2High"

//region Property "t01"
  public static final Property t01 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT01() { return (BStatusNumeric)get(t01); }
  public void setT01(BStatusNumeric v) { set(t01, v, null); }
//endregion Property "t01"

//region Property "h01"
  public static final Property h01 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH01() { return (BStatusNumeric)get(h01); }
  public void setH01(BStatusNumeric v) { set(h01, v, null); }
//endregion Property "h01"

//region Property "c01"
  public static final Property c01 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC01() { return (BStatusNumeric)get(c01); }
  public void setC01(BStatusNumeric v) { set(c01, v, null); }
//endregion Property "c01"

//region Property "t02"
  public static final Property t02 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT02() { return (BStatusNumeric)get(t02); }
  public void setT02(BStatusNumeric v) { set(t02, v, null); }
//endregion Property "t02"

//region Property "h02"
  public static final Property h02 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH02() { return (BStatusNumeric)get(h02); }
  public void setH02(BStatusNumeric v) { set(h02, v, null); }
//endregion Property "h02"

//region Property "c02"
  public static final Property c02 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC02() { return (BStatusNumeric)get(c02); }
  public void setC02(BStatusNumeric v) { set(c02, v, null); }
//endregion Property "c02"

//region Property "t03"
  public static final Property t03 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT03() { return (BStatusNumeric)get(t03); }
  public void setT03(BStatusNumeric v) { set(t03, v, null); }
//endregion Property "t03"

//region Property "h03"
  public static final Property h03 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH03() { return (BStatusNumeric)get(h03); }
  public void setH03(BStatusNumeric v) { set(h03, v, null); }
//endregion Property "h03"

//region Property "c03"
  public static final Property c03 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC03() { return (BStatusNumeric)get(c03); }
  public void setC03(BStatusNumeric v) { set(c03, v, null); }
//endregion Property "c03"

//region Property "t04"
  public static final Property t04 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT04() { return (BStatusNumeric)get(t04); }
  public void setT04(BStatusNumeric v) { set(t04, v, null); }
//endregion Property "t04"

//region Property "h04"
  public static final Property h04 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH04() { return (BStatusNumeric)get(h04); }
  public void setH04(BStatusNumeric v) { set(h04, v, null); }
//endregion Property "h04"

//region Property "c04"
  public static final Property c04 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC04() { return (BStatusNumeric)get(c04); }
  public void setC04(BStatusNumeric v) { set(c04, v, null); }
//endregion Property "c04"

//region Property "t05"
  public static final Property t05 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT05() { return (BStatusNumeric)get(t05); }
  public void setT05(BStatusNumeric v) { set(t05, v, null); }
//endregion Property "t05"

//region Property "h05"
  public static final Property h05 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH05() { return (BStatusNumeric)get(h05); }
  public void setH05(BStatusNumeric v) { set(h05, v, null); }
//endregion Property "h05"

//region Property "c05"
  public static final Property c05 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC05() { return (BStatusNumeric)get(c05); }
  public void setC05(BStatusNumeric v) { set(c05, v, null); }
//endregion Property "c05"

//region Property "t06"
  public static final Property t06 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT06() { return (BStatusNumeric)get(t06); }
  public void setT06(BStatusNumeric v) { set(t06, v, null); }
//endregion Property "t06"

//region Property "h06"
  public static final Property h06 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH06() { return (BStatusNumeric)get(h06); }
  public void setH06(BStatusNumeric v) { set(h06, v, null); }
//endregion Property "h06"

//region Property "c06"
  public static final Property c06 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC06() { return (BStatusNumeric)get(c06); }
  public void setC06(BStatusNumeric v) { set(c06, v, null); }
//endregion Property "c06"

//region Property "t07"
  public static final Property t07 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT07() { return (BStatusNumeric)get(t07); }
  public void setT07(BStatusNumeric v) { set(t07, v, null); }
//endregion Property "t07"

//region Property "h07"
  public static final Property h07 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH07() { return (BStatusNumeric)get(h07); }
  public void setH07(BStatusNumeric v) { set(h07, v, null); }
//endregion Property "h07"

//region Property "c07"
  public static final Property c07 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC07() { return (BStatusNumeric)get(c07); }
  public void setC07(BStatusNumeric v) { set(c07, v, null); }
//endregion Property "c07"

//region Property "t08"
  public static final Property t08 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT08() { return (BStatusNumeric)get(t08); }
  public void setT08(BStatusNumeric v) { set(t08, v, null); }
//endregion Property "t08"

//region Property "h08"
  public static final Property h08 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH08() { return (BStatusNumeric)get(h08); }
  public void setH08(BStatusNumeric v) { set(h08, v, null); }
//endregion Property "h08"

//region Property "c08"
  public static final Property c08 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC08() { return (BStatusNumeric)get(c08); }
  public void setC08(BStatusNumeric v) { set(c08, v, null); }
//endregion Property "c08"

//region Property "t09"
  public static final Property t09 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT09() { return (BStatusNumeric)get(t09); }
  public void setT09(BStatusNumeric v) { set(t09, v, null); }
//endregion Property "t09"

//region Property "h09"
  public static final Property h09 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH09() { return (BStatusNumeric)get(h09); }
  public void setH09(BStatusNumeric v) { set(h09, v, null); }
//endregion Property "h09"

//region Property "c09"
  public static final Property c09 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC09() { return (BStatusNumeric)get(c09); }
  public void setC09(BStatusNumeric v) { set(c09, v, null); }
//endregion Property "c09"

//region Property "t10"
  public static final Property t10 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT10() { return (BStatusNumeric)get(t10); }
  public void setT10(BStatusNumeric v) { set(t10, v, null); }
//endregion Property "t10"

//region Property "h10"
  public static final Property h10 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH10() { return (BStatusNumeric)get(h10); }
  public void setH10(BStatusNumeric v) { set(h10, v, null); }
//endregion Property "h10"

//region Property "c10"
  public static final Property c10 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC10() { return (BStatusNumeric)get(c10); }
  public void setC10(BStatusNumeric v) { set(c10, v, null); }
//endregion Property "c10"

//region Property "t11"
  public static final Property t11 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT11() { return (BStatusNumeric)get(t11); }
  public void setT11(BStatusNumeric v) { set(t11, v, null); }
//endregion Property "t11"

//region Property "h11"
  public static final Property h11 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH11() { return (BStatusNumeric)get(h11); }
  public void setH11(BStatusNumeric v) { set(h11, v, null); }
//endregion Property "h11"

//region Property "c11"
  public static final Property c11 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC11() { return (BStatusNumeric)get(c11); }
  public void setC11(BStatusNumeric v) { set(c11, v, null); }
//endregion Property "c11"

//region Property "t12"
  public static final Property t12 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT12() { return (BStatusNumeric)get(t12); }
  public void setT12(BStatusNumeric v) { set(t12, v, null); }
//endregion Property "t12"

//region Property "h12"
  public static final Property h12 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH12() { return (BStatusNumeric)get(h12); }
  public void setH12(BStatusNumeric v) { set(h12, v, null); }
//endregion Property "h12"

//region Property "c12"
  public static final Property c12 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC12() { return (BStatusNumeric)get(c12); }
  public void setC12(BStatusNumeric v) { set(c12, v, null); }
//endregion Property "c12"

//region Property "t13"
  public static final Property t13 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT13() { return (BStatusNumeric)get(t13); }
  public void setT13(BStatusNumeric v) { set(t13, v, null); }
//endregion Property "t13"

//region Property "h13"
  public static final Property h13 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH13() { return (BStatusNumeric)get(h13); }
  public void setH13(BStatusNumeric v) { set(h13, v, null); }
//endregion Property "h13"

//region Property "c13"
  public static final Property c13 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC13() { return (BStatusNumeric)get(c13); }
  public void setC13(BStatusNumeric v) { set(c13, v, null); }
//endregion Property "c13"

//region Property "t14"
  public static final Property t14 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT14() { return (BStatusNumeric)get(t14); }
  public void setT14(BStatusNumeric v) { set(t14, v, null); }
//endregion Property "t14"

//region Property "h14"
  public static final Property h14 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH14() { return (BStatusNumeric)get(h14); }
  public void setH14(BStatusNumeric v) { set(h14, v, null); }
//endregion Property "h14"

//region Property "c14"
  public static final Property c14 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC14() { return (BStatusNumeric)get(c14); }
  public void setC14(BStatusNumeric v) { set(c14, v, null); }
//endregion Property "c14"

//region Property "t15"
  public static final Property t15 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT15() { return (BStatusNumeric)get(t15); }
  public void setT15(BStatusNumeric v) { set(t15, v, null); }
//endregion Property "t15"

//region Property "h15"
  public static final Property h15 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH15() { return (BStatusNumeric)get(h15); }
  public void setH15(BStatusNumeric v) { set(h15, v, null); }
//endregion Property "h15"

//region Property "c15"
  public static final Property c15 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC15() { return (BStatusNumeric)get(c15); }
  public void setC15(BStatusNumeric v) { set(c15, v, null); }
//endregion Property "c15"

//region Property "t16"
  public static final Property t16 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getT16() { return (BStatusNumeric)get(t16); }
  public void setT16(BStatusNumeric v) { set(t16, v, null); }
//endregion Property "t16"

//region Property "h16"
  public static final Property h16 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getH16() { return (BStatusNumeric)get(h16); }
  public void setH16(BStatusNumeric v) { set(h16, v, null); }
//endregion Property "h16"

//region Property "c16"
  public static final Property c16 = newProperty(Flags.SUMMARY, new BStatusNumeric(0, BStatus.nullStatus), null);
  public BStatusNumeric getC16() { return (BStatusNumeric)get(c16); }
  public void setC16(BStatusNumeric v) { set(c16, v, null); }
//endregion Property "c16"

//region Property "zonesValid"
  public static final Property zonesValid = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getZonesValid() { return (BStatusNumeric)get(zonesValid); }
  public void setZonesValid(BStatusNumeric v) { set(zonesValid, v, null); }
//endregion Property "zonesValid"

//region Property "tempValid"
  public static final Property tempValid = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getTempValid() { return (BStatusNumeric)get(tempValid); }
  public void setTempValid(BStatusNumeric v) { set(tempValid, v, null); }
//endregion Property "tempValid"

//region Property "rhValid"
  public static final Property rhValid = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getRhValid() { return (BStatusNumeric)get(rhValid); }
  public void setRhValid(BStatusNumeric v) { set(rhValid, v, null); }
//endregion Property "rhValid"

//region Property "co2Valid"
  public static final Property co2Valid = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getCo2Valid() { return (BStatusNumeric)get(co2Valid); }
  public void setCo2Valid(BStatusNumeric v) { set(co2Valid, v, null); }
//endregion Property "co2Valid"

//region Property "tempAvg"
  public static final Property tempAvg = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getTempAvg() { return (BStatusNumeric)get(tempAvg); }
  public void setTempAvg(BStatusNumeric v) { set(tempAvg, v, null); }
//endregion Property "tempAvg"

//region Property "tempMax"
  public static final Property tempMax = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getTempMax() { return (BStatusNumeric)get(tempMax); }
  public void setTempMax(BStatusNumeric v) { set(tempMax, v, null); }
//endregion Property "tempMax"

//region Property "rhAvg"
  public static final Property rhAvg = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getRhAvg() { return (BStatusNumeric)get(rhAvg); }
  public void setRhAvg(BStatusNumeric v) { set(rhAvg, v, null); }
//endregion Property "rhAvg"

//region Property "rhMax"
  public static final Property rhMax = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getRhMax() { return (BStatusNumeric)get(rhMax); }
  public void setRhMax(BStatusNumeric v) { set(rhMax, v, null); }
//endregion Property "rhMax"

//region Property "co2Avg"
  public static final Property co2Avg = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getCo2Avg() { return (BStatusNumeric)get(co2Avg); }
  public void setCo2Avg(BStatusNumeric v) { set(co2Avg, v, null); }
//endregion Property "co2Avg"

//region Property "co2Max"
  public static final Property co2Max = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getCo2Max() { return (BStatusNumeric)get(co2Max); }
  public void setCo2Max(BStatusNumeric v) { set(co2Max, v, null); }
//endregion Property "co2Max"

//region Property "zonesHot"
  public static final Property zonesHot = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getZonesHot() { return (BStatusNumeric)get(zonesHot); }
  public void setZonesHot(BStatusNumeric v) { set(zonesHot, v, null); }
//endregion Property "zonesHot"

//region Property "zonesHumid"
  public static final Property zonesHumid = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getZonesHumid() { return (BStatusNumeric)get(zonesHumid); }
  public void setZonesHumid(BStatusNumeric v) { set(zonesHumid, v, null); }
//endregion Property "zonesHumid"

//region Property "zonesCo2High"
  public static final Property zonesCo2High = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusNumeric(0), null);
  public BStatusNumeric getZonesCo2High() { return (BStatusNumeric)get(zonesCo2High); }
  public void setZonesCo2High(BStatusNumeric v) { set(zonesCo2High, v, null); }
//endregion Property "zonesCo2High"

//region Property "anyAlarm"
  public static final Property anyAlarm = newProperty(Flags.SUMMARY | Flags.READONLY, new BStatusBoolean(false), null);
  public BStatusBoolean getAnyAlarm() { return (BStatusBoolean)get(anyAlarm); }
  public void setAnyAlarm(BStatusBoolean v) { set(anyAlarm, v, null); }
//endregion Property "anyAlarm"

//region Action "execute"
  public static final Action execute = newAction(Flags.HIDDEN, null);
  public void execute() { invoke(execute, null, null); }
//endregion Action "execute"

  @Override public Type getType() { return TYPE; }
  public static final Type TYPE = Sys.loadType(BZoneAggregator.class);
/*+ ------------ END BAJA AUTO GENERATED CODE -------------- +*/

  // Floor statistics for up to 16 zones (t = temperature, h = humidity, c = CO2).
  // Unlinked inputs keep null status and are ignored, so one block fits any floor size.

  private Clock.Ticket ticket;
  @Override public void started() throws Exception { super.started(); schedule(); }
  @Override public void stopped() throws Exception { if (ticket != null) ticket.cancel(); super.stopped(); }
  @Override public void changed(Property p, Context cx) { super.changed(p, cx); if (isRunning() && p == scanRate) schedule(); }
  private void schedule()
  {
    if (ticket != null) ticket.cancel();
    ticket = Clock.schedulePeriodically(this, BRelTime.make(Math.max(1000L, getScanRate().getMillis())), execute, null);
  }
  public void doExecute() { calculate(); }

  public void calculate()
  {
    double[][] v = new double[16][ZoneStats.METRICS]; boolean[][] ok = new boolean[16][ZoneStats.METRICS];
    for (int i = 1; i <= 16; i++)
    {
      String k = (i < 10 ? "0" : "") + i;
      String[] names = { "t" + k, "h" + k, "c" + k };
      for (int j = 0; j < ZoneStats.METRICS; j++)
      {
        BStatusNumeric x = (BStatusNumeric)get(names[j]);
        ok[i - 1][j] = x != null && x.getStatus().isValid();
        v[i - 1][j] = ok[i - 1][j] ? x.getValue() : 0;
      }
    }
    ZoneStats z = ZoneStats.of(v, ok, new double[] { lim(getTempHigh()), lim(getRhHigh()), lim(getCo2High()) });
    setZonesValid(new BStatusNumeric(z.zonesValid));
    setTempValid(new BStatusNumeric(z.valid[0])); setRhValid(new BStatusNumeric(z.valid[1])); setCo2Valid(new BStatusNumeric(z.valid[2]));
    setTempAvg(num(z.avg(0))); setRhAvg(num(z.avg(1))); setCo2Avg(num(z.avg(2)));
    setTempMax(num(z.maxOf(0))); setRhMax(num(z.maxOf(1))); setCo2Max(num(z.maxOf(2)));
    setZonesHot(new BStatusNumeric(z.high[0])); setZonesHumid(new BStatusNumeric(z.high[1])); setZonesCo2High(new BStatusNumeric(z.high[2]));
    setAnyAlarm(new BStatusBoolean(z.anyHigh()));
  }
  private static double lim(BStatusNumeric v) { return v.getStatus().isValid() ? v.getValue() : Double.NaN; }
  private static BStatusNumeric num(double x) { return Double.isNaN(x) ? new BStatusNumeric(0, BStatus.nullStatus) : new BStatusNumeric(x); }

  @Override public BIcon getIcon() { return icon; }
  private static final BIcon icon = BIcon.std("control/control.png");
}
