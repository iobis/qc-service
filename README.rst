qc-service
==========

|travis| |coverage|

QC service for checking data for and from OBIS

`Source on GitHub at iobis/qc-service <https://github.com/iobis/qc-service>`_

Installation
============

.. code-block:: shell

    TODO

Example usage
=============

.. code-block:: python

    TODO


Development environment installation
====================================

.. code-block:: shell

    pipenv --three
    pipenv install vcrpy
    pipenv install tox
    pipenv install nose
    pipenv install requests
    pipenv install pandas
    pipenv install sphinx sphinx-autobuild sphinx_rtd_theme
    pipenv install git+https://github.com/iobis/pyxylookup.git#egg=pyxylookup
    # enter virtual evironment
    pipenv shell

Meta
====

* License: MIT, see `LICENSE file <LICENSE>`_

.. |travis| image:: https://travis-ci.org/iobis/pyxylookup.svg
   :target: https://travis-ci.org/iobis/qc-service

.. |coverage| image:: https://coveralls.io/repos/iobis/pyxylookup/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/iobis/qc-service?branch=master