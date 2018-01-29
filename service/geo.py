from math import atan2, sqrt, degrees
import numpy as np
from math import radians, sin, cos

RADIUS = 6371.009


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
    return degrees(center_lon), degrees(center_lat)


def gc_distance_points(a, points):
    b = np.asarray(points)
    lat1, lng1 = radians(a[1]), radians(a[0])
    lat2, lng2 = np.radians(b[:, 1]), np.radians(b[:, 0])

    sin_lat1, cos_lat1 = sin(lat1), cos(lat1)
    sin_lat2, cos_lat2 = np.sin(lat2), np.cos(lat2)

    delta_lng = np.subtract(lng2, lng1)
    cos_delta_lng, sin_delta_lng = np.cos(delta_lng), np.sin(delta_lng)

    d = np.arctan2(np.sqrt((cos_lat2 * sin_delta_lng) ** 2 +
                 (cos_lat1 * sin_lat2 -
                  sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
                 sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)

    return RADIUS * d
