qc-service
==========

|travis| |coverage|

QC service for checking data for and from OBIS

`Source on GitHub at iobis/qc-service <https://github.com/iobis/qc-service>`_


Parameters
==========

There are two endpoints: *outlierstaxon* and *outliersdatasets*.

The following parameters are GET request:

- **x**: longitude of the points
- **y**: latitude of the points
- mad_coef (optional): Coefficient to multiply the median absolute deviation (MAD) by in order to determine the range of valid values (default is 6)
- iqr_coef (optional): Coefficient to multiply the interquartile range (IQR) by in order to determine the range of valid values (default is 3)
- aphiaid (optional): Taxonomic identifier as provided by the world register of marine species (WoRMS), this is parameter is only used by the *outlierstaxon* endpoint
- returnvalues (optional): Return the values based on which the outlier analysis is done (default is false).

For a POST request a json or msgpack object with the following attributes is expected:

- **points**: nested list of longitude/latitude pairs
- mad_coef (optional): Coefficient to multiply the median absolute deviation (MAD) by in order to determine the range of valid values (default is 6)
- iqr_coef (optional): Coefficient to multiply the interquartile range (IQR) by in order to determine the range of valid values (default is 3)
- aphiaid (optional): taxonomic identifier as provided by the world register of marine species (WoRMS), this is parameter is only used by the *outlierstaxon* endpoint
- returnvalues (optional): Return the values based on which the outlier analysis is done (default is false).

Example usage
=============

.. code-block:: shell
    pipenv run app.py

GET outlierstaxon: http://api.iobis.org/outlierstaxon?x=50.1936,-170.9961,-80.9894,-99.6441,85.1296,63.6118,141.1846,-148.7020,-28.1081,-169.2730,-101.2903,1.9279,-170.4471,-108.4184,53.9584,16.1789,-100.6414,32.1356,111.3950,-177.6604&y=55.0475,35.6651,-28.7549,-62.0137,82.2984,-29.4130,-73.3057,-72.5911,62.5490,18.6707,55.2831,41.3517,6.5211,85.1608,-21.8638,9.3673,59.2928,21.3336,65.1072,13.9234

.. code-block:: json
    {"bathymetry": {"ok_mad": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "ok_iqr": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "median": 1659.8999999999999, "mad": 2232.5, "q1": -370.5, "q3": 4547.0}, "sssalinity": {"ok_mad": [false, true, true, true, true, true, false, true, true, true, false, false, true, false, true, false, false, false, false, true], "ok_iqr": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "median": 34.61073112487793, "mad": 0.5011653900146484, "q1": null, "q3": null}, "sstemperature": {"ok_mad": [false, true, true, true, true, true, false, true, true, true, false, false, true, true, true, false, false, false, false, true], "ok_iqr": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "median": 18.59064292907715, "mad": 9.223979949951172, "q1": null, "q3": null}, "spatial": {"ok_mad": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "ok_iqr": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "centroid": "SRID=4326;POINT(156.73819714431002 86.1317707629376)", "median": 7729884.218843833, "mad": 4223770.357516784, "q1": 3750079.9391325824, "q3": 12910808.479267936}}

GET outliersdataset: http://api.iobis.org/outliersdataset?x=50.1936,-170.9961,-80.9894,-99.6441,85.1296,63.6118,141.1846,-148.7020,-28.1081,-169.2730,-101.2903,1.9279,-170.4471,-108.4184,53.9584,16.1789,-100.6414,32.1356,111.3950,-177.6604&y=55.0475,35.6651,-28.7549,-62.0137,82.2984,-29.4130,-73.3057,-72.5911,62.5490,18.6707,55.2831,41.3517,6.5211,85.1608,-21.8638,9.3673,59.2928,21.3336,65.1072,13.9234

.. code-block:: json
    {"spatial": {"ok_mad": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "ok_iqr": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "centroid": "SRID=4326;POINT(156.73819714431002 86.1317707629376)", "median": 7729884.218843833, "mad": 4223770.357516784, "q1": 3750079.9391325824, "q3": 12910808.479267936}}

Development environment installation
====================================

.. code-block:: shell

    pipenv --three
    pipenv install vcrpy
    pipenv install tox
    pipenv install nose
    pipenv install requests
    pipenv install pandas
    pipenv install json-logging-py
    pipenv install gunicorn
    pipenv install sphinx sphinx-autobuild sphinx_rtd_theme
    pipenv install git+https://github.com/iobis/pyxylookup.git#egg=pyxylookup
    # enter virtual evironment
    pipenv shell

Tests
=====

Run tests

.. code-block:: shell

    pipenv run nosetests --with-coverage --cover-package=service

Run locally

.. code-block:: shell

    pipenv run gunicorn service.app:api

Call locally

.. code-block::shell

    echo '{"points":[[2.9,51.2]]}' | curl -d @- http://localhost:8000/outlierstaxon

Deploying
=========

1) (Optional) generate requirements.txt

.. code-block:: shell

    pipenv lock -r > requirements.txt

And remove git+https://github.com/iobis/pyxylookup.git#egg=pyxylookup from it.

2) Use docker-compose or build and start

.. code-block:: shell

    docker-compose up


Alternative is to build and start the Docker image

.. code-block:: shell

    docker build -t qc-service .
    docker run -e GUNICORN_WORKERS=4 -e GUNICORN_ACCESSLOG=- -p 8000:8000 qc-service

3) Configure the two endpoints (outlierstaxon and outliersdataset) in NGINX

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`_

.. |travis| image:: https://travis-ci.org/iobis/pyxylookup.svg
   :target: https://travis-ci.org/iobis/qc-service

.. |coverage| image:: https://coveralls.io/repos/iobis/pyxylookup/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/iobis/qc-service?branch=master
