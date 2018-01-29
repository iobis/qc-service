import numpy as np
import math
from service import geo


def _median(sorted_values):
    even = (2 if len(sorted_values) % 2 == 0 else 1)
    middle = (len(sorted_values) - 1) // 2
    return sum(sorted_values[middle:middle + even]) / float(even)


def _mad(median_value, sorted_values):
    if len(sorted_values) > 1:
        return np.median(np.absolute(np.subtract(sorted_values, median_value)))
    else:
        return None

def _q1q3(sorted_values):
    def quartile(q):
        if len(sorted_values) >= 20:
            k = (len(sorted_values)-1) * q * 0.25
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return sorted_values[int(k)]
            else:
                return (sorted_values[int(f)] + sorted_values[int(c)]) / 2.0
        else:
            return None

    q1 = quartile(1)
    q3 = quartile(3)
    return q1, q3


def get_values_stats(values):
    values = np.sort(values)
    #values.sort()
    #values = np.float_(values)
    median_value = _median(values)
    return (median_value, _mad(median_value, values)) + _q1q3(values)  # (median, mad, q1, q3)


def get_distance_stats(points):
    centroid = geo.get_centroid(points)
    distances = geo.gc_distance_points(centroid, points)
    return (geo.point_ewkt(centroid),) + get_values_stats(distances)


if __name__ == '__main__':
    import random

    random.seed(42)
    v = [random.uniform(0,100) for _ in range(1000000)]

    def numpy_get_values_stats(values):
        median = np.median(values)
        q1 = np.percentile(values, 25, interpolation='midpoint')
        q3 = np.percentile(values, 75, interpolation='midpoint')
        mad = np.median(np.absolute(np.subtract(values, median)))
        return median, mad, q1, q3

    import cProfile
    cProfile.runctx('get_values_stats(v)', globals(), locals())
    cProfile.runctx('numpy_get_values_stats(v)', globals(), locals())
