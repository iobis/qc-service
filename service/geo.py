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

if __name__ == '__main__':
    import random
    random.seed(42)
    xy = [(random.uniform(-180, 180), random.uniform(-90, 90)) for _ in range(1000000)]
    print(get_centroid(xy))
    import cProfile
    cProfile.runctx('get_centroid(xy)', globals(), locals())
    cProfile.runctx('get_centroid_fast(xy)', globals(), locals())
