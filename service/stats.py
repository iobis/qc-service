import numpy as np
from service import geo


def get_values_stats(values):
    median = np.median(values)
    mad, q1, q3 = None, None, None
    if len(values) > 1:
        mad = np.median(np.absolute(np.subtract(values, median)))
    if len(values) >= 20:
        q1 = np.percentile(values, 25, interpolation='midpoint')
        q3 = np.percentile(values, 75, interpolation='midpoint')
    return median, mad, q1, q3
