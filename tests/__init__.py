import numpy as np
import random


def rand_xy_tuple(n, minx=-180, maxx=180, miny=-90, maxy=90, seed=42):
    random.seed(seed)
    return [random.uniform(minx, maxx) for _ in range(n)], [random.uniform(miny, maxy) for _ in range(n)]


def rand_xy_list(n, minx=-180, maxx=180, miny=-90, maxy=90, seed=42):
    x, y = rand_xy_tuple(n, minx, maxx, miny, maxy, seed)
    points = list(zip(x, y))
    points, duplicate_indices = np.unique(points, return_inverse=True, axis=0)
    return points, duplicate_indices
