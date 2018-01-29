import random
import numpy as np
from service import stats


def test_get_values_stats():
    """stats - get values stats"""
    random.seed(42)
    values = [random.uniform(0,10) for _ in range(105)]
    median, mad, q1, q3 = stats.get_values_stats(values)
    assert median == np.median(values)
    assert 1 < mad < 4
    assert q1 == np.percentile(values, 25, interpolation='midpoint')
    assert q3 == np.percentile(values, 75, interpolation='midpoint')
    np.percentile(np.asarray(range(1, 101)), 25)


def test_get_values_stats_few_values():
    """stats - get values stats few values"""
    random.seed(42)
    values = [random.uniform(0,10) for _ in range(1)]
    median, mad, q1, q3 = stats.get_values_stats(values)
    assert median == np.median(values)
    assert mad is None
    assert q1 is None
    assert q3 is None
    values = [random.uniform(0, 10) for _ in range(5)]
    median, mad, q1, q3 = stats.get_values_stats(values)
    assert median == np.median(values)
    assert 1 < mad < 4
    assert q1 is None
    assert q3 is None


def test_get_distance_stats():
    """stats - get distance stats"""
    random.seed(42)
    xy = [(random.uniform(-180, 180), random.uniform(-90, 90)) for _ in range(150)]
    centroid, median, mad, q1, q3 = stats.get_distance_stats(xy)
    assert len(centroid) > 0 and "SRID=4326;POINT(" in centroid
    assert 16000 > median > 4000
    assert 6000 > mad > 1500
    assert 12000 > q1 > 2000
    assert 24000 > q3 > 6000
    xy = [(0, 0) for _ in range(100)]
    centroid, median, mad, q1, q3 = stats.get_distance_stats(xy)
    assert centroid == "SRID=4326;POINT(0.0 0.0)"
    assert median == 0
    assert mad == 0
    assert q1 == 0
    assert q3 == 0
