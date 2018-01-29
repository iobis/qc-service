import random
from service import outliers

def test_spatial():
    """outliers - spatial"""
    random.seed(42)
    xy = [(random.uniform(-180, 180), random.uniform(-90, 90)) for _ in range(150)]
    qc = outliers.spatial(xy, None, None)
    assert len(qc['ok_mad']) == len(xy)
    assert len(qc['ok_iqr']) == len(xy)
    assert len(qc['centroid']) > 0 and "SRID=4326;POINT(" in qc['centroid']
    assert 16000 > qc['median'] > 4000
    assert 6000 > qc['mad'] > 1500
    assert 12000 > qc['q1'] > 2000
    assert 24000 > qc['q3'] > 6000
    xy = [(0, 0) for _ in range(100)]
    qc = outliers.spatial(xy, None, None)
    assert len(qc['ok_mad']) == len(xy)
    assert len(qc['ok_iqr']) == len(xy)
    assert qc['centroid'] == "SRID=4326;POINT(0.0 0.0)"
    assert qc['median'] == 0
    assert qc['mad'] == 0
    assert qc['q1'] == 0
    assert qc['q3'] == 0


## TODO: test with qcstats
## TODO: test with qcstats from a species with few records (1 record, <20 records)
