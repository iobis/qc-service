import json
import requests
from functools import lru_cache


@lru_cache(maxsize=65536)
def qc_stats(aphiaid):
    """Returns the statistics needed for calculating the taxon related outlier QC flags.

    :param aphiaid: AphiaID as an integer
    :returns: QC outlier statistics, None if not found.
    """
    aphiaid = int(aphiaid)

    if aphiaid is not None:
        r = requests.get('http://api.iobis.org/v3/statistics/outliers?taxonid=' + str(aphiaid))
        if r.status_code == 200:
            stats = json.loads(r.content)
            qcstats = {'id': aphiaid, 'count': stats['count'],
                       'spatial': [(_get_float(stats, 'longitude'), _get_float(stats, 'latitude')),
                                   _get_float(stats, 'dist_median'), _get_float(stats, 'dist_mad'),
                                   _get_float(stats, 'dist_q1'), _get_float(stats, 'dist_q3')]}
            prefixes = {'bathymetry': 'depth_', 'sssalinity': 'sss_', 'sstemperature': 'sst_'}
            for grid, v in prefixes.items():
                prefix = prefixes[grid]
                qcstats[grid] = [_get_float(stats, prefix+stat) for stat in ['median', 'mad', 'q1', 'q3']]
            return qcstats
    return None


def _get_float(d, key):
    v = d.get(key, None)
    if v is not None and v != 'NaN':
        return float(v)
    return None
