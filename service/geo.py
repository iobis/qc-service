import math
import numpy as np

RADIUS = 6371.009


def get_centroid(points):
    xy = np.asarray(points)
    xy = np.radians(xy)
    lon, lat = xy[:, 0], xy[:, 1]
    avg_x = np.sum(np.cos(lat) * np.cos(lon)) / xy.shape[0]
    avg_y = np.sum(np.cos(lat) * np.sin(lon)) / xy.shape[0]
    avg_z = np.sum(np.sin(lat)) / xy.shape[0]
    center_lon = math.atan2(avg_y, avg_x)
    hyp = math.sqrt(avg_x * avg_x + avg_y * avg_y)
    center_lat = math.atan2(avg_z, hyp)
    return math.degrees(center_lon), math.degrees(center_lat)


def gc_distance_points(a, points):
    b = np.asarray(points)
    lat1, lng1 = np.radians(a[1]), np.radians(a[0])
    lat2, lng2 = np.radians(b[:, 1]), np.radians(b[:, 0])

    sin_lat1, cos_lat1 = np.sin(lat1), np.cos(lat1)
    sin_lat2, cos_lat2 = np.sin(lat2), np.cos(lat2)

    delta_lng = np.subtract(lng2, lng1)
    cos_delta_lng, sin_delta_lng = np.cos(delta_lng), np.sin(delta_lng)

    d = np.arctan2(np.sqrt((cos_lat2 * sin_delta_lng) ** 2 +
                 (cos_lat1 * sin_lat2 -
                  sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
                 sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)

    return RADIUS * d


def point_ewkt(point, srid = 4326):
    return "SRID=%s;POINT(%s %s)" % (srid, point[0], point[1])