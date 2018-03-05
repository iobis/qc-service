import numpy as np


def get_values_stats(values):
    values = np.asarray(values)
    values = values[~np.isnan(values)]
    median, mad, q1, q3 = None, None, None, None
    if len(values) > 0:
        median = np.median(values)
    if len(values) > 1:
        mad = np.median(np.absolute(np.subtract(values, median)))
    if len(values) >= 20:
        q1 = np.percentile(values, 25, interpolation='midpoint')
        q3 = np.percentile(values, 75, interpolation='midpoint')
    return median, mad, q1, q3
