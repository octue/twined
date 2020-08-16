.. _credentials_strand:

==================
Credentials Strand
==================

In order to:

- GET/POST data from/to an API,
- query a database, or
- connect to a socket (for receiving Values or emitting Values, Monitors or Logs),

A digital twin must have *access* to it. API keys, database URIs, etc must be supplied to the digital twin but
treated with best practice with respect to security considerations. The purpose of the ``credentials`` strand is to
dictate what credentials the twin requires in order to function.

.. _defining_the_credentials_strand:

Defining the Credentials Strand
===============================

This is the simplest of the strands, containing a list of credentials (whose ``NAMES_SHOULD_BE_SHOUTY_SNAKE_CASE``) with
a reminder of the purpose. Defaults can also be provided, useful for running on local or closed networks.

.. code-block:: javascript

   {
     "credentials": [
       {
         "name": "SECRET_THE_FIRST",
         "purpose": "Token for accessing a 3rd party API service"
       },
       {
         "name": "SECRET_THE_SECOND",
         "purpose": "Token for accessing a 3rd party API service"
       },
       {
         "name": "SECRET_THE_THIRD",
         "purpose": "Usually a big secret but sometimes has a convenient non-secret default, like a sandbox or local database",
         "default": "postgres://pguser:pgpassword@localhost:5432/pgdb"
       }
     ]
   }

.. _supplying_credentials:

Supplying Credentials
=====================

.. ATTENTION::

   *Credentials should never be hard-coded into application code*

   Do you trust the twin code? If you insert credentials to your own database into a digital twin
   provided by a third party, you better be very sure that twin isn't going to scrape all that data out then send
   it elsewhere!

   Alternatively, if you're building a twin requiring such credentials, it's your responsibility to give the end
   users confidence that you're not abusing their access.

   There'll be a lot more discussion on these issues, but it's outside the scope of **twined** - all we do here is
   make sure a twin has the credentials it requires.

Credentials should be securely managed by whatever system is managing the twin, then made accessible to the twin
in the form of environment variables:

.. code-block:: javascript

   SERVICE_API_KEY=someLongTokenTHatYouProbablyHaveToPayTheThirdPartyProviderLoadsOfMoneyFor

Credentials may also reside in a ``.env`` file in the current directory, either in the format above
(with a new line for each variable) or, for convenience, as bash exports like:

.. code-block:: javascript

   export SERVICE_API_KEY=someLongTokenTHatYouProbablyHaveToPayTheThirdPartyProviderLoadsOfMoneyFor

The ``validate_credentials()`` method of the ``Twine`` class checks for their presence and, where contained in a
``.env`` file, ensures they are loaded into the environment.
