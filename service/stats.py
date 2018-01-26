import numpy as np
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
            return sorted_values[int(round(q*0.25*(len(sorted_values)+1)))-1]
        else:
            return None

    q1 = quartile(1, sorted_values)
    q3 = quartile(3, sorted_values)
    return q1, q3


def get_values_stats(values):
    values.sort()
    values = np.float_(values)
    median_value = _median(values)
    return (median_value, _mad(median_value, values)) + _q1q3(values)  # (median, mad, q1, q3)


# def get_distance_stats(position_ids, positions):
#     def safe_distance(A, B):
#         try:
#             if A == B: return 0.0
#             else: return gc_distance(A,B)
#         except:
#             print("Distance A:%s to B:%s failed" % (A,B))
#             raise
#
#     points = [Point(positions[id]) for id in position_ids if positions.has_key(id)]
#     centroid = get_centroid(points)
#     distances = [safe_distance(centroid, p) * radius for p in points]
#     del points
#     return (centroid.to_ewkt(),) + get_values_stats(distances)