import vcr
from service import taxoninfo


test_aphiaid = 141433


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_qc_stats.yaml')
def test_fetch_taxon_qc():
    """taxoninfo - qc stats"""
    stats = taxoninfo.qc_stats(test_aphiaid)
    assert stats["id"] == 395450


@vcr.use_cassette('tests/vcr_cassettes/fetch_taxon_get_taxonid.yaml')
def test_fetch_taxon_get_taxonid():
    """taxoninfo - qc stats"""
    taxonid = taxoninfo._get_taxonid(test_aphiaid)
    assert taxonid == 395450
