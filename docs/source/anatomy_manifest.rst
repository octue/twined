.. _manifest_strands:

======================
Manifest-based Strands
======================

Frequently, twins operate on files containing some kind of data. These files need to be made accessible to the code
running in the twin, in order that their contents can be read and processed. Conversely, a twin might produce an output
dataset which must be understood by users.

The ``configuration_manifest``, ``input_manifest`` and ``output_manifest`` strands describe what kind of datasets (and
associated files) are required / produced.

.. NOTE::

   Files are always contained in datasets, even if there's only one file. It's so that we can keep nitty-gritty file
   metadata separate from the more meaningful, higher level metadata like what a dataset is for.

.. tabs::

   .. group-tab:: Configuration Manifest Strand

      This describes datasets/files that are required at startup of the twin / service. They typically contain a
      resource that the twin might use across many analyses.

      For example, a twin might predict failure for a particular component, given an image. It will require a trained
      ML model (saved in a ``*.pickle`` or ``*.json``). While many thousands of predictions might be done over the
      period that the twin is deployed, all predictions are done using this version of the model - so the model file is
      supplied at startup.

   .. group-tab:: Input Manifest Strand

      These files are made available for the twin to run a particular analysis with. Each analysis will likely have
      different input datasets.

      For example, a twin might be passed a dataset of LiDAR ``*.scn`` files and be expected to compute atmospheric flow
      properties as a timeseries (which might be returned in the :ref:`output values <values_based_strands>` for onward
      processing and storage).

   .. group-tab:: Output Manifest Strand

      Files are created by the twin during an analysis, tagged and stored as datasets for some onward purpose.
      This strand is not used for sourcing data; it enables users or other services to understand appropriate search
      terms to retrieve datasets produced.


.. _describing_manifests:

Describing Manifests
====================

Manifest-based strands are a **description of what files are needed**, NOT a list of specific files or datasets. This is
a tricky concept, but important, since services should be reusable and applicable to a range of similar datasets.

The purpose of the manifest strands is to provide a helper to a wider system providing datafiles to digital twins.

The manifest strands therefore use **tagging** - they contain a ``filters`` field, which should be valid
`Apache Lucene <https://lucene.apache.org/>`_ search syntax. This is a powerful syntax, whose tagging features allow
us to specify incredibly broad, or extremely narrow searches (even down to a known unique result). See the tabs below
for examples.


.. NOTE::

   Tagging syntax is extremely powerful. Below, you'll see how this enables a digital twin to specify things like:

   *"OK, I need this digital twin to always have access to a model file for a particular system, containing trained model data"*

   *"Uh, so I need an ordered sequence of files, that are CSV files from a meteorological mast."*

   This allows **twined** to check that the input files contain what is needed, enables quick and easy
   extraction of subgroups or particular sequences of files within a dataset, and enables management systems
   to map candidate datasets to twins that might be used to process them.



.. tabs::

   .. group-tab:: Configuration Manifest Strand

      Here we construct an extremely tight filter, which connects this digital twin to a specific
      system.

      .. accordion::

         .. accordion-row:: Show twine containing this strand

            .. literalinclude:: ../../examples/damage_classifier_service/twine.json
                :language: javascript

         .. accordion-row:: Show a matching file manifest

            .. literalinclude:: ../../examples/damage_classifier_service/data/configuration_manifest.json
                :language: javascript


   .. group-tab:: Input Manifest Strand

      Here we specify that two datasets (and all or some of the files associated with them) are
      required, for a service that cross-checks meteorological mast data and power output data for a wind farm.

      .. accordion::

         .. accordion-row:: Show twine containing this strand

            .. literalinclude:: ../../examples/met_mast_scada_service/strands/input_manifest_filters.json
                :language: javascript

         .. accordion-row:: Show a matching file manifest

            .. literalinclude:: ../../examples/met_mast_scada_service/data/input_manifest.json
                :language: javascript

   .. group-tab:: Output Manifest Strand

      Here we specify that two datasets (and all or some of the files associated with them) are
      required, for a service that cross-checks meteorological mast data and power output data for a wind farm.

      .. accordion::

         .. accordion-row:: Show twine containing this strand

            .. literalinclude:: ../../examples/met_mast_scada_service/strands/output_manifest_filters.json
                :language: javascript

         .. accordion-row:: Show a matching file manifest

            .. literalinclude:: ../../examples/met_mast_scada_service/data/output_manifest.json
                :language: javascript

..

    TODO - clean up or remove this section

    .. _how_filtering_works:

    How Filtering Works
    ===================

    It's the job of **twined** to make sure of two things:

    1. make sure the *twine* file itself is valid,


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
