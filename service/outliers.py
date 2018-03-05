import pyxylookup as xy
import numpy as np
from service import stats
from service import geo

MAD_COEF = 6
IQR_COEF = 3


def _values_qc(values, median, mad, q1, q3, mad_coef, iqr_coef, duplicate_indices, return_values):
    ok_mad = ok_iqr = np.full(len(values), True)
    mad_limits, iqr_limits = (None, None), (None, None)
    if median is not None and mad is not None:
        mad_limits = (median - (mad * mad_coef)), (median + (mad * mad_coef))
        ok_mad = (mad_limits[0] < values) & (values < mad_limits[1])
    if q1 is not None and q3 is not None:
        iqr_limits = (q1 - ((q3 - q1) * iqr_coef)), (q3 + ((q3 - q1) * iqr_coef))
        ok_iqr = (iqr_limits[0] < values) & (values < iqr_limits[1])
    qc = {'ok_mad': ok_mad[duplicate_indices].tolist(), 'ok_iqr': ok_iqr[duplicate_indices].tolist(),
          'median': median, 'mad': mad, 'q1': q1, 'q3': q3, 'mad_coef': mad_coef, 'iqr_coef': iqr_coef,
          'mad_limits':mad_limits, 'iqr_limits': iqr_limits}
    if return_values:
        qc['values'] = values[duplicate_indices].tolist()
    return qc


def environmental(points, duplicate_indices, mad_coef, iqr_coef, qcstats=None, return_values=False):
    if mad_coef is None:
        mad_coef = MAD_COEF
    if iqr_coef is None:
        iqr_coef = IQR_COEF
    env = xy.lookup(points, shoredistance=False, grids=True, areas=False, asdataframe=True)
    qc = {}
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        values = env.get(grid, np.full(len(points), np.nan))
        if qcstats is None:
            median, mad, q1, q3 = stats.get_values_stats(values)
        else:
            median, mad, q1, q3 = qcstats[grid]

        qc[grid] = _values_qc(values, median, mad, q1, q3, mad_coef, iqr_coef, duplicate_indices, return_values)
    return qc


def spatial(points, duplicate_indices , mad_coef, iqr_coef, qcstats=None, return_values=False):
    if mad_coef is None:
        mad_coef = MAD_COEF
    if iqr_coef is None:
        iqr_coef = IQR_COEF
    if qcstats is None:
        centroid = geo.get_centroid(points)
        distances = geo.gc_distance_points(centroid, points)
        median, mad, q1, q3 = stats.get_values_stats(distances)
    else:
        centroid, median, mad, q1, q3 = qcstats['spatial']
        distances = geo.gc_distance_points(centroid, points)

    qc = _values_qc(distances, median, mad, q1, q3, mad_coef, iqr_coef, duplicate_indices, return_values)
    qc['centroid'] = geo.point_ewkt(centroid)
    return qc


# * What with high sampling bias??? => Tracking data, ...
# Faster shoredistance:
# - identify hotspot points:
#     - points that are very often the nearest shore point
#     - store these in a separate datastructure
