import falcon
import simplejson as json
import umsgpack as msgpack
import numpy as np
from service import outliers, taxoninfo


class QcResource(object):

    @staticmethod
    def _validate_coef(coef, param):
        try:
            if coef is not None:
                coef = float(coef)
        except ValueError:
            raise falcon.HTTPInvalidParam('%s not numeric' % param, param)
        if coef < 0:
            raise falcon.HTTPInvalidParam('Invalid %s: cannot be smaller then 0' % param, param)
        return coef

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
        else:
            x = req.get_param_as_list('x')
            y = req.get_param_as_list('y')
            aphiaid = req.get_param_as_int('aphiaid')
            mad_coef = req.get_param_as_float('mad_coef')
            iqr_coef = req.get_param_as_float('iqr_coef')
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

        return points, aphiaid, mad_coef, iqr_coef

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


class QcSpeciesResource(QcResource):
    @staticmethod
    def _qc_species(req):
        points, aphiaid, mad_coef, iqr_coef = QcResource._parse_request(req)
        try:
            qcstats = None
            if aphiaid is not None:
                qcstats = taxoninfo.qc_stats(aphiaid)
            qc = outliers.environmental(points, mad_coef, iqr_coef, qcstats)
            qc['spatial'] = outliers.spatial(points, mad_coef, iqr_coef, qcstats)
            return qc
        except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error looking up data for provided points', str(ex))

    def on_get(self, req, resp):
        results = self._qc_species(req)
        self._prepare_response(results, req, resp)

    def on_post(self, req, resp):
        results = self._qc_species(req)
        self._prepare_response(results, req, resp)


class QcDatasetResource(QcResource):
    @staticmethod
    def _qc_dataset(req):
        points, _, mad_coef, iqr_coef = QcResource._parse_request(req)
        try:
            return outliers.spatial(points, mad_coef, iqr_coef)
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error looking up data for provided points', str(ex))

    def on_get(self, req, resp):
        results = self._qc_dataset(req)
        self._prepare_response(results, req, resp)

    def on_post(self, req, resp):
        results = self._qc_dataset(req)
        self._prepare_response(results, req, resp)


api = falcon.API()
api.add_route('/outliersspecies', QcSpeciesResource())
api.add_route('/outliersdataset', QcDatasetResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
