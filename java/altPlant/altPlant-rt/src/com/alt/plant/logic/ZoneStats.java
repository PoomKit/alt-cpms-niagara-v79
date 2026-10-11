package com.alt.plant.logic;

/**
 * Floor zone statistics - plain Java, no Niagara dependency (unit tested in CI).
 * Metric 0 = temperature, 1 = RH, 2 = CO2. Invalid / unlinked values are skipped; an invalid limit never alarms.
 */
public final class ZoneStats
{
  public static final int METRICS = 3;

  public final double[] sum = new double[METRICS], max = new double[METRICS];
  public final int[] valid = new int[METRICS], high = new int[METRICS];
  /** zones with at least one valid value (temperature, RH or CO2) */
  public int zonesValid;

  /**
   * @param v     v[zone][metric]
   * @param ok    ok[zone][metric] = value is valid
   * @param limit high limit per metric (NaN = no limit)
   */
  public static ZoneStats of(double[][] v, boolean[][] ok, double[] limit)
  {
    ZoneStats s = new ZoneStats();
    for (int j = 0; j < METRICS; j++) s.max[j] = Double.NEGATIVE_INFINITY;
    for (int z = 0; z < v.length; z++)
    {
      boolean any = false;
      for (int j = 0; j < METRICS; j++)
      {
        if (!ok[z][j]) continue;
        double x = v[z][j]; any = true;
        s.sum[j] += x; s.valid[j]++; s.max[j] = Math.max(s.max[j], x);
        if (!Double.isNaN(limit[j]) && x > limit[j]) s.high[j]++;
      }
      if (any) s.zonesValid++;
    }
    return s;
  }

  /** average rounded to 0.1, NaN when no zone is valid */
  public double avg(int j) { return valid[j] == 0 ? Double.NaN : Math.round(sum[j] / valid[j] * 10) / 10.0; }

  public double maxOf(int j) { return valid[j] == 0 ? Double.NaN : max[j]; }

  public boolean anyHigh() { return high[0] + high[1] + high[2] > 0; }
}
