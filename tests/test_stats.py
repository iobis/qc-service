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
