==========================
Spotter Project
==========================

A Spotter project with recommendation.

==========

Setup
==========

Set environment variable for Django Secret Key, Debug, Allowed Host, Admin Path, Reset Timeout and Env. Also add configuration for
Database, and Defender.


.. code-block:: bash

    SECRET_KEY = '...'
    DEBUG = ..
    ALLOWED_HOSTS = '...'
    ADMIN_PATH = '...'
    DJANGO_ENV = '...'
    ADMIN_PATH = '...'
    AUTO_LOGOUT_IDLE_TIME = '...'

    ENGINE = '...'
    NAME = '...'
    HOST = '...'
    USER = '...'
    PASSWORD = '...'
    PORT = '...'

    # Defender Settings
    DEFENDER_LOGIN_FAILURE_LIMIT = '...'
    DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = '...'
    DEFENDER_COOLOFF_TIME = '...'
    DEFENDER_ATTEMPT_COOLOFF_TIME = '...'
    DEFENDER_LOCKOUT_TEMPLATE = '...'
    DEFENDER_LOCKOUT_URL = '...'
    DEFENDER_USERNAME_FORM_FIELD = '...'
    DEFENDER_STORE_ACCESS_ATTEMPTS = '...'
    DEFENDER_ACCESS_ATTEMPT_EXPIRATION = '...'
    DEFENDER_REDIS_URL = '...'
    DEFENDER_GET_USERNAME_FROM_REQUEST_PATH = '...'
    DEFENDER_REVERSE_PROXY_HEADER = '...'
    DEFENDER_BEHIND_REVERSE_PROXY = True'...'



Additional Setup
-----------------

Set config for *Sentry*.

.. code-block:: bash

    # Sentry
    SENTRY_DNS= '...'
    SENTRY_REPORT_URL = '...'

Running Project
----------------

Setup
^^^^^^^^^^^
.. code-block:: bash

    make setup


create Superuser
^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    make superuser


Load Fixtures
^^^^^^^^^^^
.. code-block:: bash

    make load-fixtures


Run Server
^^^^^^^^^^^
.. code-block:: bash

    make runserver

