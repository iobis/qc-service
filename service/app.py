import falcon
import simplejson as json
import umsgpack as msgpack
import numpy as np
from service import outliers, taxoninfo


class QcResource(object):

    @staticmethod
    def _float_or_none(v):
        if v is None:
            return None
        return float(v)

    @staticmethod
    def _int_or_none(v):
        if v is None:
            return None
        return int(v)

    @staticmethod
    def _validate_coef(coef, param):
        try:
            if coef is not None:
                coef = float(coef)
                if coef < 0:
                    raise falcon.HTTPInvalidParam('Invalid %s: cannot be smaller then 0' % param, param)
        except ValueError:
            raise falcon.HTTPInvalidParam('%s not numeric' % param, param)
        return coef

    @staticmethod
    def _param_as_bool_with_default(req, paramname, default=False):
        v = req.get_param_as_bool(paramname, blank_as_true=default)
        if v is None:
            v = default
        return v

    @staticmethod
    def _parse_request(req):
        if req.method == "POST":
            try:
                raw_data = req.stream.read()
            except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error reading data from POST', str(ex))

            if req.content_type and req.content_type.lower() == falcon.MEDIA_MSGPACK:
                try:
                    data = msgpack.unpackb(raw_data, use_list=False)
                except Exception:
                    raise falcon.HTTPError(falcon.HTTP_400, 'Invalid msgpack',
                                           'Could not decode the request body. The msgpack was incorrect.')
            else:
                try:
                    data = json.loads(raw_data)
                except ValueError:
                    raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON',
                                           'Could not decode the request body. The ''JSON was incorrect.')
            if not data or type(data) is not dict or len(data) == 0:
                raise falcon.HTTPInvalidParam('Request POST data should be a JSON object/Python dictionary/R list',
                                              'POST body')
            points = data.get('points', None)
            if not points or len(points) == 0:
                raise falcon.HTTPInvalidParam('No points provided', 'points')
            aphiaid = data.get('aphiaid', None)
            mad_coef = data.get('mad_coef', None)
            iqr_coef = data.get('iqr_coef', None)
            return_values = data.get('returnvalues', False)
        else:
            x = req.get_param_as_list('x')
            y = req.get_param_as_list('y')
            aphiaid = QcResource._int_or_none(req.get_param_as_int('aphiaid', required=False))
            mad_coef = QcResource._float_or_none(req.get_param('mad_coef', required=False))
            iqr_coef = QcResource._float_or_none(req.get_param('iqr_coef', required=False))
            return_values = QcResource._param_as_bool_with_default(req, 'returnvalues', default=False)
            if not x or not y or len(x) == 0 or len(y) == 0:
                raise falcon.HTTPInvalidParam('Missing parameters x and/or y', 'x/y')
            elif len(x) != len(y):
                raise falcon.HTTPInvalidParam('Length of x parameter is different from length of y', 'x/y')
            points = list(zip(x, y))

        points = np.array(points)
        try:
            points = points.astype(float)
        except ValueError:
            raise falcon.HTTPInvalidParam('Coordinates not numeric', 'x/y points')
        mad_coef = QcResource._validate_coef(mad_coef, 'mad_coef')
        iqr_coef = QcResource._validate_coef(iqr_coef, 'iqr_coef')

        if not all([-180 <= p[0] <= 180 and -90 <= p[1] <= 90 for p in points]):
            raise falcon.HTTPInvalidParam('Invalid coordinates (xmin: -180, ymin: -90, xmax: 180, ymax: 90)', 'x/y points')

        return points, aphiaid, mad_coef, iqr_coef, return_values

    @staticmethod
    def _prepare_response(results, req, resp):
        if req.client_accepts_msgpack and req.content_type and req.content_type.lower() == falcon.MEDIA_MSGPACK:
            try:
                resp.data = msgpack.packb(results, use_bin_type=False)
                resp.content_type = falcon.MEDIA_MSGPACK
                resp.status = falcon.HTTP_200
            except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error creating msgpack response', str(ex))
        else:
            try:
                resp.body = json.dumps(results)
            except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error creating JSON response', str(ex))


class QcTaxonResource(QcResource):
    @staticmethod
    def _qc_taxon(req):
        points, aphiaid, mad_coef, iqr_coef, return_values = QcResource._parse_request(req)
        try:
            qcstats = None
            if aphiaid is not None:
                qcstats = taxoninfo.qc_stats(aphiaid)
            points, duplicate_indices = np.unique(points, return_inverse=True, axis=0)
            qc = outliers.environmental(points, duplicate_indices, mad_coef, iqr_coef, qcstats, return_values)
            qc['spatial'] = outliers.spatial(points, duplicate_indices, mad_coef, iqr_coef, qcstats, return_values)
            if qcstats is not None:
                qc['count'] = qcstats['count']
                qc['id'] = qcstats['id']
            else:
                qc['count'] = len(points)
                qc['id'] = None
            return qc
        except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error looking up data for provided points', str(ex))

    def on_get(self, req, resp):
        results = self._qc_taxon(req)
        self._prepare_response(results, req, resp)

    def on_post(self, req, resp):
        results = self._qc_taxon(req)
        self._prepare_response(results, req, resp)


class QcDatasetResource(QcResource):
    @staticmethod
    def _qc_dataset(req):
        points, _, mad_coef, iqr_coef, return_values = QcResource._parse_request(req)
        try:
            points, duplicate_indices = np.unique(points, return_inverse=True, axis=0)
            return {'spatial': outliers.spatial(points, duplicate_indices, mad_coef, iqr_coef, return_values=return_values),
                    'count': len(points)}
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error looking up data for provided points', str(ex))

    def on_get(self, req, resp):
        results = self._qc_dataset(req)
        self._prepare_response(results, req, resp)

    def on_post(self, req, resp):
        results = self._qc_dataset(req)
        self._prepare_response(results, req, resp)


def create():
    api = falcon.API()
    api.add_route('/outlierstaxon', QcTaxonResource())
    api.add_route('/outliersdataset', QcDatasetResource())
    return api


api = create()

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
