import random


def rand_xy_tuple(n, minx=-180, maxx=180, miny=-90, maxy=90, seed=42):
    random.seed(seed)
    return [random.uniform(minx, maxx) for _ in range(n)], [random.uniform(miny, maxy) for _ in range(n)]


def rand_xy_list(n, minx=-180, maxx=180, miny=-90, maxy=90, seed=42):
    x, y = rand_xy_tuple(n, minx, maxx, miny, maxy, seed)
    return list(zip(x, y))