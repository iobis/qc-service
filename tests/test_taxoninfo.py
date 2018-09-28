from service import taxoninfo


test_aphiaid = 141433


def test_fetch_taxon_qc():
    """taxoninfo - qc stats"""
    stats = taxoninfo.qc_stats(test_aphiaid)
    assert stats['id'] == 141433
    for env in ['bathymetry', 'sssalinity', 'sstemperature']:
        assert env in stats and len(stats[env]) == 4

    assert 'count' in stats and stats['count'] > 0
    assert 'spatial' in stats and len(stats['spatial']) == 5



def test_fetch_taxon_qc_missing_species():
    """taxoninfo - qc stats missing species"""
    stats = taxoninfo.qc_stats(-1)
    assert stats is None


def test_fetch_taxon_qc_missing_species():
    """taxoninfo - qc stats data poor taxon"""

    stats = taxoninfo.qc_stats(145552)  # Sargassum baccularia: 7 records
    assert stats['count'] > 0
    centroid, median, mad, q1, q3 = stats['spatial']
    assert len(centroid) == 2
    assert median > 0
    assert mad > 0
    assert q1 is None
    assert q3 is None
    for env in ['sssalinity', 'sstemperature']:
        median, mad, q1, q3 = stats[env]
        assert median is not None
        assert mad > 0
        assert q1 is None
        assert q3 is None