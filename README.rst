============
pyimaprotect
============


.. image:: https://img.shields.io/pypi/v/pyimaprotect.svg
        :target: https://pypi.python.org/pypi/pyimaprotect

.. image:: https://img.shields.io/travis/pcourbin/pyimaprotect.svg
        :target: https://travis-ci.com/pcourbin/pyimaprotect

.. image:: https://readthedocs.org/projects/pyimaprotect/badge/?version=latest
        :target: https://pyimaprotect.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/pcourbin/pyimaprotect/shield.svg
     :target: https://pyup.io/repos/github/pcourbin/pyimaprotect/
     :alt: Updates

| Get alarms status information from your `IMA Protect Alarm`_.
| It only allows to **get status**, **not to change** the status.

This work is originally developed for use with `Home Assistant`_ and the *custom component* `imaprotect`_.


* Free software: MIT license
* Documentation: https://pyimaprotect.readthedocs.io.

Features
--------

Parameters
==========

- `username`: Username used to connect to https://pilotageadistance.imateleassistance.com
- `password`: Password used to connect to https://pilotageadistance.imateleassistance.com

Properties
==========

- `first_name`: Firstname used in your contract
- `last_name`: Lastname used in your contract
- `email`: Email used in your contract
- `offer`: Offercurrently defined in your contract. Example: `tout-inclus`
- `contract_number`: Reference number of your contract
- `alerts_enabled`: Indicates whether the alarm is currently triggered (Boolean).

You can add properties using jsonpath, see method `add_property`

Methods
=======

- `get_all_info`: return the full JSON from the IMA Protect API "me" endpoint.
- `add_property`: allow to add a property to your object. This property will be stored the first time the API is called and each time you call `get_all_info`.
- `get_status`: return the current status of your IMA Protect Alarm. See next table to understand the values returned.

.. list-table:: List of Alarm status values
   :widths: auto
   :header-rows: 1

   * - Alarm Value
     - State
   * - `-1`
     - `UNKNOWN`
   * - `0`
     - `OFF`
   * - `1`
     - `PARTIAL`
   * - `2`
     - `ON`

Credits
-------

| This work is based on the work of `lplancke`_ for `Jeedom`_.
| This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`IMA Protect Alarm`: https://www.imaprotect.com/
.. _`Home Assistant`: https://www.home-assistant.io/
.. _`imaprotect`: https://github.com/pcourbin/imaprotect
.. _`lplancke`: https://github.com/lplancke/jeedom_alarme_IMA
.. _`Jeedom`: https://www.jeedom.com
..