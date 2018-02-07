import vcr
import random
from falcon import testing
import service.app as app
import tests as t

client = testing.TestClient(app.create())
endpoints = ['/outliersspecies', '/outliersdataset']


def test_api_missing_xy_get():
    """ api - get missing xy """
    for endpoint in endpoints:
        result = client.simulate_get(endpoint, query_string='')
        assert result.status_code == 400
        assert 'Invalid ' in result.json["title"]


def test_api_empty_body_post():
    """ api - post empty body """
    for endpoint in endpoints:
        result = client.simulate_post(endpoint, body='')
        assert result.status_code == 400
        assert 'Invalid ' in result.json["title"]


def test_api_empty_list_post():
    """ api - post empty list """
    for endpoint in endpoints:
        result = client.simulate_post(endpoint, body='[]')
        assert result.status_code == 400
        assert 'Invalid ' in result.json["title"]


# @vcr.use_cassette('tests/vcr_cassettes/api_species_get_works.yaml')
# def test_api_species_get_works():
#     """ api species - get works """
#     x, y = t.rand_xy_tuple(150)
#     result = client.simulate_get('/outliersspecies', query_string=qs)
#
#
# def test_api_species_post_works():
#     """ api species - post works """
#     return
#
#
# def test_api_dataset_get_works():
#     """ api dataset - get works """
#     result = client.simulate_get('/outliersdataset', query_string='')
#
#
#
# def test_api_dataset_post_works():
#     """ api dataset - post works """
#     result = client.simulate_get('/outliersdataset', query_string='')
#
#
# def test_api_species():
#     """ api species - """
#     return
#
#
# def test_api_dataset():
#     """ api dataset - """
#     result = client.simulate_get('/outliersdataset', query_string='')
#
# def test_api_dataset():
#     """ api dataset - """
#     return
#
# def test_api_dataset():
#     """ api dataset - """
#     return
#
# def test_api_dataset():
#     """ api dataset - """
#     return

"""
# Tests to implement

- get and post
- missing parameters
- valid parameters
- correct parameter parsing
- correct results e.g. datasets only spatial outliers
"""





