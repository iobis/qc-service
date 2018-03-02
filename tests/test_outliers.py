import random
import vcr
import numpy as np
from service import outliers
from service import taxoninfo
import tests as t


def test_spatial():
    """outliers - spatial"""
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.spatial(points, duplicate_indices, None, None)
    assert len(qc['ok_mad']) == len(points)
    assert len(qc['ok_iqr']) == len(points)
    assert len(qc['centroid']) > 0 and "SRID=4326;POINT(" in qc['centroid']
    assert 16000e3 > qc['median'] > 4000e3
    assert 6000e3 > qc['mad'] > 1500e3
    assert 12000e3 > qc['q1'] > 2000e3
    assert 24000e3 > qc['q3'] > 6000e3
    xy = [(random.uniform(-0.001, 0.001), random.uniform(-0.001, 0.001)) for _ in range(100)]
    duplicate_indices = list(range(100))
    qc = outliers.spatial(xy, duplicate_indices, None, None)
    assert len(qc['ok_mad']) == len(xy)
    assert len(qc['ok_iqr']) == len(xy)
    assert qc['centroid'].startswith('SRID=4326;POINT(')
    assert round(qc['median']/1000) == 0
    assert round(qc['mad']/1000) == 0
    assert round(qc['q1']/1000) == 0
    assert round(qc['q3']/1000) == 0


def test_spatial():
    """outliers - spatial return values"""
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.spatial(points, duplicate_indices, None, None, return_values=True)
    assert len(qc['values']) == len(points)


def test_spatial_few_points():
    """ outliers - spatial few points """
    points, duplicate_indices = [[1,2]], [0]
    qc = outliers.spatial(points, None, None)
    assert len(qc['ok_mad']) == len(points) and np.all(qc['ok_mad'])
    assert len(qc['ok_iqr']) == len(points) and np.all(qc['ok_iqr'])
    print(qc)
    assert qc['centroid'].startswith('SRID=4326;POINT(')
    x, y = [float(x) for x in qc['centroid'].replace('SRID=4326;POINT(', '').replace(')', '').split(' ')]
    assert abs(round(x) - 1) < 0.00001 and abs(round(y) - 2) < 0.00001
    assert abs(round(qc['median'])) < 0.00001
    for k in ['mad', 'q1', 'q3']:
        assert qc[k] is None


@vcr.use_cassette('tests/vcr_cassettes/outliers_environmental.yaml')
def test_environmental():
    """outliers - environmental"""
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.environmental(points, duplicate_indices, None, None)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        assert len(g['ok_mad']) == len(points)
        assert len(g['ok_iqr']) == len(points)
        for k in ['median', 'mad', 'q1', 'q3']:
            assert isinstance(g[k], float) and g[k] != 0


@vcr.use_cassette('tests/vcr_cassettes/outliers_environmental_return_values.yaml')
def test_environmental():
    """outliers - environmental return values"""
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.environmental(points, duplicate_indices, None, None, return_values=True)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        assert len(g['ok_mad']) == len(points)
        assert len(g['ok_iqr']) == len(points)
        assert len(g['values']) == len(points)
        for k in ['median', 'mad', 'q1', 'q3']:
            assert isinstance(g[k], float) and g[k] != 0


@vcr.use_cassette('tests/vcr_cassettes/outliers_environmental_few_points.yaml')
def test_environmental_few_points():
    """outliers - environmental few points"""

    points, duplicate_indices = t.rand_xy_list(1, -1, 1, -1, 1)
    qc = outliers.environmental(points, duplicate_indices, None, None)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        assert len(g['ok_mad']) == len(points) and np.all(g['ok_mad'])
        assert len(g['ok_iqr']) == len(points) and np.all(g['ok_iqr'])
        assert isinstance(g['median'], float) and g['median'] != 0
        for k in ['mad', 'q1', 'q3']:
            assert g[k] is None

    xy = t.rand_xy_list(10, -1, 1, -1, 1)
    qc = outliers.environmental(xy, mad_coef=1, iqr_coef=0.1)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        assert len(g['ok_mad']) == len(xy) and 0 < np.sum(g['ok_mad']) < len(xy)
        assert len(g['ok_iqr']) == len(xy) and np.all(g['ok_iqr'])
        assert isinstance(g['median'], float) and g['median'] != 0
        assert isinstance(g['mad'], float) and g['mad'] != 0
        assert g['q1'] is None
        assert g['q3'] is None

    random.seed(42)
    points, duplicate_indices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(21)], list(range(21))
    qc = outliers.environmental(points, mad_coef=1, iqr_coef=0.1)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        assert len(g['ok_mad']) == len(points) and 0 < np.sum(g['ok_mad']) < len(points)
        assert len(g['ok_iqr']) == len(points) and 0 < np.sum(g['ok_iqr']) < len(points)
        for k in ['median', 'mad', 'q1', 'q3']:
            assert isinstance(g[k], float) and g[k] != 0


@vcr.use_cassette('tests/vcr_cassettes/outliers_spatial_qcstats.yaml')
def test_spatial_qcstats():
    """outliers - spatial qc stats"""
    qcstats = taxoninfo.qc_stats(aphiaid=141433)
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.spatial(points, None, None, qcstats=qcstats)
    assert len(qc['ok_mad']) == len(points) and 0 < np.sum(qc['ok_mad']) < len(points)
    assert len(qc['ok_iqr']) == len(points) and 0 < np.sum(qc['ok_iqr']) < len(points)
    for i, k in enumerate(['median', 'mad', 'q1', 'q3']):
        assert isinstance(qc[k], float) and qc[k] == qcstats['spatial'][i+1]


@vcr.use_cassette('tests/vcr_cassettes/outliers_environmental_qcstats.yaml')
def test_environmental_qcstats():
    """outliers - environmental qc stats"""
    qcstats = taxoninfo.qc_stats(aphiaid=141433)
    points, duplicate_indices = t.rand_xy_list(150)
    qc = outliers.environmental(points, duplicate_indices, 12, 6, qcstats=qcstats)
    for grid in ['bathymetry', 'sssalinity', 'sstemperature']:
        g = qc[grid]
        print(grid)
        print(np.sum(g['ok_mad']))
        print(np.sum(g['ok_iqr']))
        assert len(g['ok_mad']) == len(points) and 0 < np.sum(g['ok_mad']) < len(points)
        assert len(g['ok_iqr']) == len(points) and 0 < np.sum(g['ok_iqr']) < len(points)
        for i, k in enumerate(['median', 'mad', 'q1', 'q3']):
            assert isinstance(g[k], float) and g[k] == qcstats[grid][i]
