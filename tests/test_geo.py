from service import geo
import numpy as np
import random


def test_get_centroid():
    """geo - get centroid"""
    random.seed(42)
    xy = [(random.uniform(-180, 180), random.uniform(-90, 90)) for _ in range(100)]
    p = geo.get_centroid(xy)
    assert -180 <= p[0] <= 180 and -90 <= p[0] <= 90

    p = geo.get_centroid([[1,2]])
    assert round(p[0],6) == 1 and round(p[1],6) == 2

    xy = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(100000)]
    p = geo.get_centroid(np.asarray(xy))
    assert round(p[0], 2) == 0 and round(p[1], 2) == 0


def test_gc_distance_points():
    """geo - great circle distance from a point to an array of points"""
    random.seed(42)
    p = [3.4, 5.6]
    xy = [(random.uniform(-180, 180), random.uniform(-180, 180)) for _ in range(10)]
    actual = geo.gc_distance_points(p, xy)

    from geopy.distance import great_circle
    gc = great_circle()
    expected = [gc.measure(p, b) for b in xy]
    for i in range(len(xy)):
        assert round(actual[i], 3) == round(expected[i], 3)

# gc_distance_points
