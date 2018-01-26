from math import atan2, sqrt, degrees
import numpy as np


def get_centroid(points):
    xy = np.asarray(points)
    xy = np.radians(xy)
    lon, lat = xy[:, 0], xy[:, 1]
    avg_x = np.sum(np.cos(lat) * np.cos(lon)) / xy.shape[0]
    avg_y = np.sum(np.cos(lat) * np.sin(lon)) / xy.shape[0]
    avg_z = np.sum(np.sin(lat)) / xy.shape[0]
    center_lon = atan2(avg_y, avg_x)
    hyp = sqrt(avg_x * avg_x + avg_y * avg_y)
    center_lat = atan2(avg_z, hyp)
    (degrees(center_lon), degrees(center_lat))

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
