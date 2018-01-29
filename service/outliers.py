import pyxylookup as xy
from service import stats
from service import geo

MAD_COEF = 6
IQR_COEF = 3


def environmental(points, mad_coef, iqr_coef, qcstats=None):
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
        ok_mad = (median - median + (mad * mad_coef)) < values < (median + (mad * mad_coef))
        ok_iqr = (q1 - ((q3 - q1) * iqr_coef)) < values < (q3 + ((q3 - q1) * iqr_coef))
        qc[grid] = {'ok_mad': ok_mad, 'ok_iqr': ok_iqr,
                    'median': median, 'mad': mad, 'q1': q1, 'q3': q3}
    return qc


def spatial(points, mad_coef, iqr_coef, qcstats=None):
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

    ok_mad = distances < median + (mad * mad_coef)
    ok_iqr = distances < q3 + ((q3-q1) * iqr_coef)

    return {'ok_mad': ok_mad, 'ok_iqr': ok_iqr,
            'centroid': geo.point_ewkt(centroid), 'median': median, 'mad': mad, 'q1': q1, 'q3': q3}


# * What with high sampling bias??? => Tracking data, ...
# Faster shoredistance:
# - identify hotspot points:
#     - points that are very often the nearest shore point
#     - store these in a separate datastructure
