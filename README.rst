===========================================================
pyimaprotect - Python `IMA Protect Alarm`_ *UNOFFICIAL*
===========================================================


.. image:: https://img.shields.io/pypi/v/pyimaprotect.svg
        :target: https://pypi.python.org/pypi/pyimaprotect

.. image:: https://img.shields.io/pypi/pyversions/pyimaprotect.svg
        :target: https://pypi.python.org/pypi/pyimaprotect

.. image:: https://img.shields.io/travis/pcourbin/pyimaprotect.svg
        :target: https://travis-ci.com/pcourbin/pyimaprotect

.. image:: https://readthedocs.org/projects/pyimaprotect/badge/?version=latest
        :target: https://pyimaprotect.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pcourbin/pyimaprotect/shield.svg
     :target: https://pyup.io/repos/github/pcourbin/pyimaprotect/
     :alt: Updates

.. image:: https://codecov.io/gh/pcourbin/pyimaprotect/branch/main/graph/badge.svg
     :target: https://codecov.io/gh/pcourbin/pyimaprotect

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen
     :target: `pre-commit`_
     :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: `black`_
     :alt: Black

.. image:: https://img.shields.io/badge/maintainer-%40pcourbin-blue.svg
     :target: `user_profile`_
     :alt: Project Maintenance

.. image:: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
     :target: `buymecoffee`_
     :alt: BuyMeCoffee


| Get and set alarm status from your `IMA Protect Alarm`_.
| You can get and set the status, get the list of contacts and download your images.

This work is originally developed for use with `Home Assistant`_ and the *custom component* `imaprotect`_.


* Free software: MIT license
* Documentation: https://pyimaprotect.readthedocs.io.

Features
--------

Since the last update of IMAProtect "API" (05/2021), this plugin allows you to:

- **get the status** of your alarm:

.. code-block:: python

  from pyimaprotect import IMAProtect, STATUS_NUM_TO_TEXT
  ima = IMAProtect('myusername','mysuperpassword')

  print("# Get Status")
  imastatus = ima.status
  print("Current Alarm Status: %d (%s)" % (imastatus,STATUS_NUM_TO_TEXT[imastatus]))

- **set the status** of your alarm:

.. code-block:: python

  from pyimaprotect import IMAProtect
  ima = IMAProtect('myusername','mysuperpassword')

  print("# Set Status")
  ima.status = 0 # 0 to OFF, 1 to PARTIAL and 2 to On


- **get** the list and information of your **registered contacts**:

.. code-block:: python

  from pyimaprotect import IMAProtect
  ima = IMAProtect('myusername','mysuperpassword')

  print("# Get Contact List")
  contact_list = ima.get_contact_list()
  for contact in contact_list:
      print(contact)

- **download the images/photos** taken with your connected elements:

.. code-block:: python

  from pyimaprotect import IMAProtect
  ima = IMAProtect('myusername','mysuperpassword')

  print("# Download Images")
  ima.download_images() # Download images to 'Images/' folder. One subfolder per camera.
  ima.download_images("MyImages/") # Download images to a defined directory 'MyImages/' folder.

Parameters
==========

- `username`: Username used to connect to https://www.imaprotect.com/
- `password`: Password used to connect to https://www.imaprotect.com/

Methods
=======

- `login()`: open a session with the IMA Protect Alarm website
- `logout()`: close the session with the IMA Protect Alarm website
- `status`: property to get or set the status of your IMA Protect Alarm. See the next table to understand the values.
- `get_contact_list()`: get a JSON with the list and information about your registered contacts.
- `download_images()`: download the images/photos taken with your connected elements.

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

| This work was based on the work of `lplancke`_ and `chris94440`_ for `Jeedom`_.
| This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`IMA Protect Alarm`: https://www.imaprotect.com/
.. _`Home Assistant`: https://www.home-assistant.io/
.. _`imaprotect`: https://github.com/pcourbin/imaprotect
.. _`lplancke`: https://github.com/lplancke/jeedom_alarme_IMA
.. _`Jeedom`: https://www.jeedom.com
.. _`chris94440`: https://github.com/chris94440
.. _`pre-commit`: https://github.com/pre-commit/pre-commit
.. _`black`: https://github.com/psf/black
.. _`user_profile`: https://github.com/pcourbin
.. _`buymecoffee`: https://www.buymeacoffee.com/pcourbin
