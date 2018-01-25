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
            return json.loads(r.content)
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
