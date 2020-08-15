.. _anatomy:

=========================
Anatomy Of The Twine File
=========================

The main point of **twined** is to enable engineers and scientists to easily (and rigorously) define a digital twin
or data service.

This is done by adding a ``twine.json`` file to the repository containing your code. Adding a *twine* means you can:

- communicate (to you or a colleague) what data is required by this service
- communicate (to another service / machine) what data is required
- deploy services automatically with a provider like `Octue <https://www.octue.com>`_.

To just get started building a *twine*, check out the :ref:`quick_start`. To learn more about twines in general,
see :ref:`about`. Here, we describe the parts of a *twine* ("strands") and what they mean.

.. _strands:

Strands
=======

A *twine* has several sections, called *strands*. Each defines a different kind of data required (or produced) by the
twin.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Strand
     - Describes the twin's requirements for...
   * - :ref:`Configuration Values <values_based_strands>`
     - Data, in JSON form, used for configuration of the twin/service.
   * - :ref:`Configuration Manifest <manifest_strands>`
     - Files/datasets required by the twin at configuration/startup
   * - :ref:`Input Values <values_based_strands>`
     - Data, in JSON form, passed to the twin in order to trigger an analysis
   * - :ref:`Input Manifest <manifest_strands>`
     - Files/datasets passed with Input Values to trigger an analysis
   * - :ref:`Output Values <values_based_strands>`
     - Data, in JSON form, that will be produced by the twin (in response to inputs)
   * - :ref:`Output Manifest <manifest_strands>`
     - Files/datasets that will be produced by the twin (in response to inputs)
   * - :ref:`Credentials <credentials_strand>`
     - Credentials that are required by the twin in order to access third party services
   * - :ref:`Children <children_strand>`
     - Other twins, access to which are required for this twin to function
   * - :ref:`Monitors <monitors_strand>`
     - Visual and progress outputs from an analysis


.. toctree::
   :maxdepth: 1
   :hidden:

   anatomy_values
   anatomy_manifest
   anatomy_credentials
   anatomy_monitors
   anatomy_children


.. _twine_file_schema:

Twine File Schema
=================

Because the ``twine.json`` file itself is in ``JSON`` format with a strict structure, **twined** uses a schema to make
that twine files are correctly written (a "schema-schema", if you will, since a twine already contains schema). Try not
to think about it. But if you must, the *twine* schema is
`here <https://github.com/octue/twined/blob/master/twined/schema/twine_schema.json>`_.

The first thing **twined** always does is check that the ``twine.json`` file itself is valid, and give you a
descriptive error if it isn't.


.. _other_external_io:

Other External I/O
==================

A twin might:

- GET/POST data from/to an external API,
- query/update a database,
- upload files to an object store,
- trigger events in another network, or
- perform pretty much any interaction you can think of with other applications over the web.

However, such data exchange may not be controllable by **twined** (which is intended to operate at the boundaries of the
twin) unless the resulting data is returned from the twin (and must therefore be compliant with the schema).

So, there's nothing for **twined** to do here, and no need for a strand in the *twine* file. However, interacting with
third party APIs or databases might require some credentials. See :ref:`credentials_strand` for help with that.

.. NOTE::
   This is actually a very common scenario. For example, the purpose of the twin might be to fetch data (like a weather
   forecast) from some external API then return it in the ``output_values`` for use in a network of digital twins.
   But its the twin developer's job to do the fetchin' and make sure the resulting data is compliant with the
   ``output_values_schema`` (see :ref:`values_based_strands`).