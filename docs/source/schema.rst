.. _schema:

=====================
About Twines (Schema)
=====================

The core of **twined** is to provide and use schemas for digital twins.

Below, we set out requirements and a framework for creating a *schema* to represent a digital twin.
We call these schema "twines". To just get started building a **twine**, check out the :ref:`_quick_start`.


.. _requirements:

Requirements of digital twin schema
===================================

A *schema* defines a digital twin, and has multiple roles. It:

#. Defines what data is required by a digital twin, in order to run
#. Defines what data will be returned by the twin following a successful run
#. Defines the formats of these data, in such a way that incoming data can be validated

If this weren't enough, the schema:

#. Must be trustable (i.e. a schema from an untrusted, corrupt or malicious third party should be safe to at least read)
#. Must be machine-readable *and machine-understandable* [1]_
#. Must be human-readable *and human-understandable* [1]_
#. Must be searchable/indexable

Fortunately for digital twin developers, many of these requirements have already been seen for data interchange formats
developed for the web. **twined** uses ``JSON`` and ``JSONSchema`` to interchange data between digital twins.

If you're not already familiar with ``JSONSchema`` (or wish to know why **twined** uses ``JSON`` over the seemingly more
appropriate ``XML`` standard), see :ref:`introducing_json_schema`.

.. toctree::
   :maxdepth: 0
   :hidden:

   schema_introducing_json


.. _data_framework:

Data framework
==============

We cannot simply expect many developers to create digital twins with some schema, then to be able to connect them all
together - even if those schema are all fully valid (*readable*). **twined** makes things slightly more specific.

**twined** has an opinionated view on how incoming data is organised. This results in a top-level schema that is
extremely prescriptive (*understandable*), allowing digital twins to be introspected and connected.


.. _data_types:

Data types
----------

Let us review the classes of data i/o undertaken a digital twin:

.. tabs::

   .. group-tab:: Config

      **Configuration data (input)**

      Control parameters relating to what the twin should do, or how it should operate. For example, should a twin produce
      output images as low resolution PNGs or as SVGs? How many iterations of a fluid flow solver should be used? What is
      the acceptable error level on an classifier algorithm?

      *These values should always have defaults.*

   .. group-tab:: Values

      **Value data (input, output)**

      Raw values passed directly to/from a twin. For example current rotor speed, or forecast wind direction.

      Values might be passed at instantiation of a twin (typical application-like process) or via a socket.

      *These values should never have defaults.*

   .. group-tab:: Files

      **File data (input, output)**

      Twins frequently operate on file content - eg files on disc or objects in a cloud data store. For example,
      groups of ``.csv`` files can contain data to train a machine learning algorithm. There are four subclasses of file i/o
      that may be undertaken by digital twins:

      #. Input file (read) - eg to read input data from a csv file
      #. Temporary file (read-write, disposable) - eg to save intermediate results to disk, reducing memory use
      #. Cache file (read-write, persistent) - eg to save a trained classifier for later use in prediction
      #. Output file (write) - eg to write postprocessed csv data ready for the next twin, or save generated images etc.

   .. group-tab:: External

      **External service data (input, output)**

      A digital twin might:
         - GET/POST data from/to an external API,
         - query/update a database.

      Such data exchange may not be controllable by **twined** (which is intended to operate at the boundaries of the
      twin) unless the resulting data is returned from the twin and must therefore be schema-compliant.

   .. group-tab:: Credentials

      **Credentials (input)**

      In order to:
         - GET/POST data from/to an API,
         - query a database, or
         - connect to a socket (for receiving Values or emitting Values, Monitors or Logs)

      a digital twin must have *access* to it. API keys, database URIs, etc must be supplied to the digital twin but
      treated with best practice with respect to security considerations.

      *Credentials should never be hard-coded into application code, always passed in*

   .. group-tab:: Monitors/Logs

      There are two kinds of monitoring data required from a digital twin.

      **Monitor data (output)**

      Values for health and progress monitoring of the twin, for example percentage progress, iteration number and
      status - perhaps even residuals graphs for a converging calculation. Broadly speaking, this should be user-facing
      information.

      *This kind of monitoring data can be in a suitable form for display on a dashboard*

      **Log data (output)**

      Logged statements, typically in iostream form, produced by the twin (e.g. via python's ``logging`` module) must be
      capturable as an output for debugging and monitoring purposes. Broadly speaking, this should be developer-facing
      information.


.. _data_descriptions:

Data descriptions
-----------------

Here, we describe how each of these data classes is described by **twined**.


.. tabs::

   .. group-tab:: Config

      **Configuration data**

      Configuration data is supplied as a simple object, which of course can be nested (although we don't encourage deep
      nesting). The following is a totally hypothetical configuration...

      .. code-block:: javascript

         {
             "max_iterations": 0,
             "compute_vectors": True,
             "cache_mode": "extended",
             "initial_conditions": {
                 "intensity": 0.0,
                 "direction", 0.0
             }
         }

   .. group-tab:: Values

      **Value data (input, output)**

      For Values data, a twin will accept and/or respond with raw JSON (this could originate over a socket, be read from
      a file or API depending exactly on the twin) containing variables of importance:

      .. code-block:: javascript

         {
             "rotor_speed": 13.2,
             "wind_direction": 179.4
         }

   .. group-tab:: Files

      **File data (input, output)**

      Files are not streamed directly to the digital twin (this would require extreme bandwidth in whatever system is
      orchestrating all the twins). Instead, files should be made available on the local storage system; i.e. a volume
      mounted to whatever container or VM the digital twin runs in.

      Groups of files are described by a ``manifest``, where a manifest is (in essence) a catalogue of files in a
      dataset.

      A digital twin might receive multiple manifests, if it uses multiple datasets. For example, it could use a 3D
      point cloud LiDAR dataset, and a meteorological dataset.

      .. code-block:: javascript

         {
             "manifests": [
                 {
                     "type": "dataset",
                     "id": "3c15c2ba-6a32-87e0-11e9-3baa66a632fe",  // UUID of the manifest
                     "files": [
                         {
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",  // UUID of that file
                             "sha1": "askjnkdfoisdnfkjnkjsnd"  // for quality control to check correctness of file contents
                             "name": "Lidar - 4 to 10 Dec.csv",
                             "path": "local/file/path/to/folder/containing/it/",
                             "type": "csv",
                             "metadata": {
                             },
                             "size_bytes": 59684813,
                             "tags": "lidar, helpful, information, like, sequence:1",  // Searchable, parsable and filterable
                         },
                         {
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "Lidar - 11 to 18 Dec.csv",
                             "path": "local/file/path/to/folder/containing/it/",
                             "type": "csv",
                             "metadata": {
                             },
                             "size_bytes": 59684813,
                             "tags": "lidar, helpful, information, like, sequence:2",  // Searchable, parsable and filterable
                         },
                         {
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "Lidar report.pdf",
                             "path": "local/file/path/to/folder/containing/it/",
                             "type": "pdf",
                             "metadata": {
                             },
                             "size_bytes": 484813,
                             "tags": "report",  // Searchable, parsable and filterable
                         }
                     ]
                 },
                 {
                     // ... another dataset manifest ...
                 }
             ]
         }

      .. NOTE::

         Tagging syntax is extremely powerful. Below, you'll see how this enables a digital twin to specify things like:

        *"Uh, so I need an ordered sequence of files, that are CSV files, and are tagged as lidar."*

         This allows **twined** to check that the input files contain what is needed, enables quick and easy
         extraction of subgroups or particular sequences of files within a dataset, and enables management systems
         to map candidate datasets to twins that might be used to process them.


   .. group-tab:: External

      **External service data (input, output)**

      There's nothing for **twined** to do here!

      If the purpose of the twin (and this is a common scenario!) is simply
      to fetch data from some service then return it as values from the twin, that's perfect. But its
      the twin developer's job to do the fetchin', not ours ;)

      However, fetching from your API or database might require some credentials. See the following tab for help with
      that.

   .. group-tab:: Credentials

      **Credentials (input)**

      Credentials should be securely managed by whatever system is managing the twin, then made accessible to the twin
      in the form of environment variables:

      .. code-block:: javascript

         SERVICE_API_KEY=someLongTokenTHatYouProbablyHaveToPayTheThirdPartyProviderLoadsOfMoneyFor

      **twined** helps by providing a small shim to check for their presence and bring these environment variables
      into your configuration.

      .. ATTENTION::

         Do you trust the twin code? If you insert credentials to your own database into a digital twin
         provided by a third party, you better be very sure that twin isn't going to scrape all that data out then send
         it elsewhere!

         Alternatively, if you're building a twin requiring such credentials, it's your responsibility to give the end
         users confidence that you're not abusing their access.

         There'll be a lot more discussion on these issues, but it's outside the scope of **twined** - all we do here is
         make sure a twin has the credentials it requires.

   .. group-tab:: Monitors/Logs

      **Monitor data (output)**

      **Log data (output)**


.. ATTENTION::
    *What's the difference between Configuration and Values data? Isn't it the same?*

    No. Configuration data is supplied to a twin to initialise it, and always has defaults. Values data is ingested by a
    twin, maybe at startup but maybe also later (if the twin is working like a live server). In complex cases, which
    Values are required may also depend on the Configuration of the twin!

    Values data can also be returned from a twin whereas configuration data is not.

    Don't get hung up on this yet - in simple (most) cases, they are effectively the same. For a twin which is run as a
    straightforward analysis, both the Configuration and Values are processed at startup.



.. Footnotes:

.. [1] *Understandable* essentially means that, once read, the machine or human knows what it actually means and what to do with it.


.. toctree::
   :maxdepth: 0
   :hidden:

   schema_other_considerations
