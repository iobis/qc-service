import json
import requests
from functools import lru_cache


@lru_cache(maxsize=65536)
def qc_stats(aphiaid):
    """Returns the statistics needed for calculating the taxon related outlier QC flags.

    :param aphiaid: AphiaID as an integer
    :returns: QC outlier statistics, None if not found.
    """

    taxonid = _get_taxonid(aphiaid)

    if taxonid:
        r = requests.get('http://api.iobis.org/taxon/' + str(taxonid) + '/qc')
        if r.status_code == 200:
            stats = json.loads(r.content)
            # stats = {'id': 395450, 'count': 8338, 'depth_median': -8.0, 'depth_mad': 8.0, 'depth_q1': -18.5, 'depth_q3': -1.0, 'sss_median': 33.94, 'sss_mad': 0.96, 'sss_q1': 32.62, 'sss_q3': 34.71, 'sst_median': 11.34, 'sst_mad': 0.85, 'sst_q1': 9.97, 'sst_q3': 11.88, 'dist_median': 512327.059217, 'dist_mad': 169692.183572, 'dist_q1': 284043.647877, 'dist_q3': 610637.508068, 'latitude': 53.8879241369, 'longitude': 2.87435902914}
            qcstats = {'id': stats['id'], 'count': stats['count'],
                       'spatial': ((float(stats['longitude']), float(stats['latitude'])),
                                   _get_float(stats, 'dist_median'), _get_float(stats, 'dist_mad'),
                                   _get_float(stats, 'dist_q1'), _get_float(stats, 'dist_q3'))}
            prefixes = {'bathymetry': 'depth_', 'sssalinity': 'sss_', 'sstemperature': 'sst_'}
            for grid, v in prefixes.items():
                prefix = prefixes[grid]
                qcstats[grid] = [_get_float(stats, prefix+stat) for stat in ['median', 'mad', 'q1', 'q3']]
            return qcstats
    return None


def _get_taxonid(aphiaid):
    """Returns the OBIS identifier for an aphiaid.

    :param aphiaid: AphiaID as an integer
    :returns: OBIS identifier, None if not found.
    """
    r = requests.get('http://api.iobis.org/taxon', params={'aphiaid': aphiaid})

    if r.status_code == 200:
        tx = json.loads(r.content).get('results', None)
        if tx and len(tx) == 1:
            validid = tx[0].get('valid_id', None)
            return validid

    return None


def _get_float(d, key):
    v = d.get(key, None)
    if v is not None:
        v = float(v)
    return v
