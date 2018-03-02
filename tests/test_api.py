import vcr
import json
import umsgpack as msgpack
import falcon
from falcon import testing
import service.app as app
import tests as t

client = testing.TestClient(app.create())
endpoints = ['/outlierstaxon', '/outliersdataset']


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


def _check_outlierstaxon_result(result, content=None, return_values=False):
    if content: print(content)
    else: print(result.json)
    assert result.status_code == 200
    if content is None:
        content = result.json
    assert 'spatial' in content
    assert 'bathymetry' in content
    assert 'sstemperature' in content
    assert 'sssalinity' in content

    for k in ['spatial', 'bathymetry', 'sstemperature', 'sssalinity']:
        for v in ['ok_mad', 'ok_iqr', 'median', 'mad', 'q1', 'q3']:
            assert v in content[k]
        if return_values:
            assert 'values' in content[k]
    return content


@vcr.use_cassette('tests/vcr_cassettes/api_taxon_get_works.yaml')
def test_api_taxon_get_works():
    """ api taxon - get works """
    x, y = t.rand_xy_tuple(150)
    qs = 'x={0}&y={1}'.format(','.join(map(str, x)), ','.join(map(str, y)))
    result = client.simulate_get('/outlierstaxon', query_string=qs)
    _check_outlierstaxon_result(result)
    for return_values in [True, False]:
        qs = 'x={0}&y={1}&returnvalues={2}'.format(','.join(map(str, x)), ','.join(map(str, y)), return_values)
        result = client.simulate_get('/outlierstaxon', query_string=qs)
        _check_outlierstaxon_result(result)


@vcr.use_cassette('tests/vcr_cassettes/api_taxon_get_few_points.yaml')
def test_api_taxon_get_few_points():
    """ api taxon - get few points """
    qs = 'x=1&y=2'
    result = client.simulate_get('/outlierstaxon', query_string=qs)
    _check_outlierstaxon_result(result)


@vcr.use_cassette('tests/vcr_cassettes/api_taxon_post_works.yaml')
def test_api_taxon_post_works():
    """ api taxon - post works """
    points, _ = t.rand_xy_list(150)
    points = points.tolist()
    body = json.dumps({'points': points})
    result1 = client.simulate_post('/outlierstaxon', body=body)
    _check_outlierstaxon_result(result1)
    body = msgpack.dumps({'points': points})
    result2 = client.simulate_post('/outlierstaxon', body=body, headers={'Content-Type': falcon.MEDIA_MSGPACK})
    content = msgpack.loads(result2.content)
    _check_outlierstaxon_result(result2, content)
    assert result1.json == content

    for return_values in [True, False]:
        body = json.dumps({'points': points, 'returnvalues': return_values})
        result1 = client.simulate_post('/outlierstaxon', body=body)
        _check_outlierstaxon_result(result1, return_values=return_values)
        body = msgpack.dumps({'points': points, 'returnvalues': return_values})
        result2 = client.simulate_post('/outlierstaxon', body=body, headers={'Content-Type': falcon.MEDIA_MSGPACK})
        content = msgpack.loads(result2.content)
        _check_outlierstaxon_result(result2, content, return_values=return_values)


def _check_outliersdataset_result(result, content=None, return_values=False):
    assert result.status_code == 200
    if content is None:
        content = result.json
    assert 'spatial' in content
    for v in ['ok_mad', 'ok_iqr', 'median', 'mad', 'q1', 'q3']:
        assert v in content['spatial']
    if return_values:
        assert 'values' in content['spatial']


@vcr.use_cassette('tests/vcr_cassettes/api_dataset_get_works.yaml')
def test_api_dataset_get_works():
    """ api dataset - get works """
    x, y = t.rand_xy_tuple(150)
    qs = 'x={0}&y={1}'.format(','.join(map(str, x)), ','.join(map(str, y)))
    result = client.simulate_get('/outliersdataset', query_string=qs)
    _check_outliersdataset_result(result)
    for return_values in [True, False]:
        qs = 'x={0}&y={1}&returnvalues={2}'.format(','.join(map(str, x)), ','.join(map(str, y)), return_values)
        result = client.simulate_get('/outliersdataset', query_string=qs)
        _check_outliersdataset_result(result, return_values=return_values)


@vcr.use_cassette('tests/vcr_cassettes/api_dataset_post_works.yaml')
def test_api_dataset_post_works():
    """ api dataset - post works """
    points, _ = t.rand_xy_list(150)
    points = points.tolist()
    body = json.dumps({'points': points})
    result1 = client.simulate_post('/outliersdataset', body=body)
    _check_outliersdataset_result(result1)
    body = msgpack.dumps({'points': points})
    result2 = client.simulate_post('/outliersdataset', body=body, headers={'Content-Type': falcon.MEDIA_MSGPACK})
    content = msgpack.loads(result2.content)
    _check_outliersdataset_result(result2, content)
    assert result1.json == content


@vcr.use_cassette('tests/vcr_cassettes/api_taxon_aphiaid_works.yaml')
def test_api_taxon_aphiaid_works():
    qs = 'x=1&y=2&aphiaid=144132'
    result = client.simulate_get('/outlierstaxon', query_string=qs)
    content = _check_outlierstaxon_result(result)
    assert content['count'] > 1
    assert content['bathymetry']['mad'] is not None
