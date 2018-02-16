import vcr
import json
import umsgpack as msgpack
import falcon
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


def _check_outliersspecies_result(result, content=None):
    assert result.status_code == 200
    if content is None:
        content = result.json
    assert 'spatial' in content
    assert 'bathymetry' in content
    assert 'sstemperature' in content
    assert 'sssalinity' in content


@vcr.use_cassette('tests/vcr_cassettes/api_species_get_works.yaml')
def test_api_species_get_works():
    """ api species - get works """
    x, y = t.rand_xy_tuple(150)
    qs = 'x={0}&y={1}'.format(','.join(map(str, x)), ','.join(map(str, y)))
    result = client.simulate_get('/outliersspecies', query_string=qs)
    _check_outliersspecies_result(result)


@vcr.use_cassette('tests/vcr_cassettes/api_species_post_works.yaml')
def test_api_species_post_works():
    """ api species - post works """
    points = t.rand_xy_list(150)
    body = json.dumps({'points': points})
    result1 = client.simulate_post('/outliersspecies', body=body)
    _check_outliersspecies_result(result1)
    body = msgpack.dumps({'points': points})
    result2 = client.simulate_post('/outliersspecies', body=body, headers={'Content-Type': falcon.MEDIA_MSGPACK})
    content = msgpack.loads(result2.content)
    _check_outliersspecies_result(result2, content)
    assert result1.json == content


def _check_outliersdataset_result(result, content=None):
    assert result.status_code == 200
    if content is None:
        content = result.json
    assert 'spatial' in content


@vcr.use_cassette('tests/vcr_cassettes/api_dataset_get_works.yaml')
def test_api_dataset_get_works():
    """ api dataset - get works """
    x, y = t.rand_xy_tuple(150)
    qs = 'x={0}&y={1}'.format(','.join(map(str, x)), ','.join(map(str, y)))
    result = client.simulate_get('/outliersdataset', query_string=qs)
    _check_outliersdataset_result(result)


@vcr.use_cassette('tests/vcr_cassettes/api_dataset_post_works.yaml')
def test_api_dataset_post_works():
    """ api dataset - post works """
    points = t.rand_xy_list(150)
    body = json.dumps({'points': points})
    result1 = client.simulate_post('/outliersdataset', body=body)
    _check_outliersdataset_result(result1)
    body = msgpack.dumps({'points': points})
    result2 = client.simulate_post('/outliersdataset', body=body, headers={'Content-Type': falcon.MEDIA_MSGPACK})
    content = msgpack.loads(result2.content)
    _check_outliersdataset_result(result2, content)
    assert result1.json == content
