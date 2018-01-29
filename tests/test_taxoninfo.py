import vcr
from service import taxoninfo


test_aphiaid = 141433


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_qc_stats.yaml')
def test_fetch_taxon_qc():
    """taxoninfo - qc stats"""
    stats = taxoninfo.qc_stats(test_aphiaid)
    assert stats['id'] == 395450
    assert 'bathymetry' in stats
    assert 'sssalinity' in stats
    assert 'sstemperature' in stats
    assert 'count' in stats and stats['count'] > 0
    assert 'spatial' in stats and len(stats['spatial']) == 5


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_get_taxonid.yaml')
def test_fetch_taxon_get_taxonid():
    """taxoninfo - qc stats"""
    taxonid = taxoninfo._get_taxonid(test_aphiaid)
    assert taxonid == 395450


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_qc_stats_missing_species.yaml')
def test_fetch_taxon_qc_missing_species():
    """taxoninfo - qc stats missing species"""
    stats = taxoninfo.qc_stats(-1)
    assert stats is None


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_qc_stats_data_poor_species.yaml')
def test_fetch_taxon_qc_missing_species():
    """taxoninfo - qc stats data poor species"""
    stats = taxoninfo.qc_stats(495041) # Sargassum desvauxii: 1 record
    assert stats['count'] == 1
