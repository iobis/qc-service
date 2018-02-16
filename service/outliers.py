import pyxylookup as xy
import numpy as np
from service import stats
from service import geo

MAD_COEF = 6
IQR_COEF = 3


def environmental(points, mad_coef, iqr_coef, qcstats=None):
    points, duplicate_indices = np.unique(points, return_inverse=True, axis=0)
    if mad_coef is None:
        mad_coef = MAD_COEF
    if iqr_coef is None:
        iqr_coef = IQR_COEF
    env = xy.lookup(points, shoredistance=False, grids=True, areas=False, asdataframe=True)
    qc = {}
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        values = env[grid]
        if qcstats is None:
            median, mad, q1, q3 = stats.get_values_stats(values)
        else:
            median, mad, q1, q3 = qcstats[grid]
        ok_mad = ok_iqr = np.full(len(values), True)
        if median is not None and mad is not None:
            ok_mad = ((median - (mad * mad_coef)) < values) & (values < (median + (mad * mad_coef)))
        if q1 is not None and q3 is not None:
            ok_iqr = ((q1 - ((q3 - q1) * iqr_coef)) < values) & (values < (q3 + ((q3 - q1) * iqr_coef)))
        qc[grid] = {'ok_mad': ok_mad[duplicate_indices].tolist(), 'ok_iqr': ok_iqr[duplicate_indices].tolist(),
                    'median': median, 'mad': mad, 'q1': q1, 'q3': q3}
    return qc


def spatial(points, mad_coef, iqr_coef, qcstats=None):
    points, duplicate_indices = np.unique(points, return_inverse=True, axis=0)
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

    ok_mad = distances < (median + (mad * mad_coef))
    ok_iqr = distances < (q3 + ((q3-q1) * iqr_coef))

    return {'ok_mad': ok_mad[duplicate_indices].tolist(), 'ok_iqr': ok_iqr[duplicate_indices].tolist(),
            'centroid': geo.point_ewkt(centroid), 'median': median, 'mad': mad, 'q1': q1, 'q3': q3}


# * What with high sampling bias??? => Tracking data, ...
# Faster shoredistance:
# - identify hotspot points:
#     - points that are very often the nearest shore point
#     - store these in a separate datastructure
