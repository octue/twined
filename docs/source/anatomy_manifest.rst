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

Manifest-based strands are a **description of what files are needed**. The purpose of the manifest strands is to
provide a helper to a wider system providing datafiles to digital twins.

.. tabs::

   .. group-tab:: Configuration Manifest Strand

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

            .. literalinclude:: ../../examples/met_mast_scada_service/strands/input_manifest.json
                :language: javascript

         .. accordion-row:: Show a matching file manifest

            .. literalinclude:: ../../examples/met_mast_scada_service/data/input_manifest.json
                :language: javascript

   .. group-tab:: Output Manifest Strand

      .. accordion::

         .. accordion-row:: Show twine containing this strand

            .. literalinclude:: ../../examples/met_mast_scada_service/strands/output_manifest.json
                :language: javascript

         .. accordion-row:: Show a matching file manifest

            .. literalinclude:: ../../examples/met_mast_scada_service/data/output_manifest.json
                :language: javascript



.. _file_tag_templates:

File tag templates
==================

Datafiles can be tagged with key-value pairs of relevant metadata that can be used in analyses. Certain datasets might
need one set of metadata on each file, while others might need a different set. The required (or optional) file tags can be
specified in the twine in the ``file_tags_template`` property of each dataset of any ``manifest`` strand. Each file in
the corresponding manifest strand is then validated against its dataset's file tag template to ensure the required tags
are present.

.. tabs::

    .. group-tab:: Manifest strand with file tag template

        The example below is for an input manifest, but the format is the same for configuration and output manifests.

        .. accordion::

            .. accordion-row:: Show twine containing a manifest strand with a file tag template

                .. code-block:: javascript

                   {
                     "input_manifest": {
                       "datasets": [
                         {
                           "key": "met_mast_data",
                           "purpose": "A dataset containing meteorological mast data",
                           "file_tags_template": {
                             "type": "object",
                             "properties": {
                               "manufacturer": {"type": "string"},
                               "height": {"type": "number"},
                               "is_recycled": {"type": "boolean"}
                             },
                             "required": ["manufacturer", "height", "is_recycled"]
                           }
                         }
                       ]
                     }
                   }

            .. accordion-row:: Show a matching file manifest

                .. code-block:: javascript

                   {
                     "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                     "datasets": [
                       {
                         "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                         "name": "met_mast_data",
                         "tags": {},
                         "labels": ["met", "mast", "wind"],
                         "files": [
                           {
                             "path": "input/datasets/7ead7669/file_1.csv",
                             "cluster": 0,
                             "sequence": 0,
                             "extension": "csv",
                             "labels": ["mykeyword1", "mykeyword2"],
                             "tags": {
                               "manufacturer": "vestas",
                               "height": 500,
                               "is_recycled": true
                             },
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "file_1.csv"
                           },
                           {
                             "path": "input/datasets/7ead7669/file_1.csv",
                             "cluster": 0,
                             "sequence": 1,
                             "extension": "csv",
                             "labels": [],
                             "tags": {
                               "manufacturer": "vestas",
                               "height": 500,
                               "is_recycled": true
                             },
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "file_1.csv"
                           }
                         ]
                       }
                     ]
                   }

    .. group-tab:: Manifest strand with a remote file tag template

        A remote reference can also be given for a file tag template. If the tag template somewhere public, this is
        useful for sharing the template between one or more teams working on the same type of data.

        The example below is for an input manifest, but the format is the same for configuration and output manifests.
        It also shows two different tag templates being specified for two different types of dataset required by the
        manifest.

        .. accordion::

            .. accordion-row:: Show twine using a remote tag template

                .. code-block:: javascript

                    {
                      "input_manifest": {
                        "datasets": [
                          {
                            "key": "met_mast_data",
                            "purpose": "A dataset containing meteorological mast data",
                            "file_tags_template": {
                              "$ref": "https://refs.schema.octue.com/octue/my-file-type-tag-template/0.0.0.json"
                            }
                          },
                          {
                            "key": "some_other_kind_of_dataset",
                            "purpose": "A dataset containing something else",
                            "file_tags_template": {
                              "$ref": "https://refs.schema.octue.com/octue/another-file-type-tag-template/0.0.0.json"
                            }
                          }
                        ]
                      }
                    }

            .. accordion-row:: Show a matching file manifest

                .. code-block:: javascript

                   {
                     "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                     "datasets": [
                       {
                         "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                         "name": "met_mast_data",
                         "tags": {},
                         "labels": ["met", "mast", "wind"],
                         "files": [
                           {
                             "path": "input/datasets/7ead7669/file_1.csv",
                             "cluster": 0,
                             "sequence": 0,
                             "extension": "csv",
                             "labels": ["mykeyword1", "mykeyword2"],
                             "tags": {
                               "manufacturer": "vestas",
                               "height": 500,
                               "is_recycled": true
                             },
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "file_1.csv"
                           },
                           {
                             "path": "input/datasets/7ead7669/file_1.csv",
                             "cluster": 0,
                             "sequence": 1,
                             "extension": "csv",
                             "labels": [],
                             "tags": {
                               "manufacturer": "vestas",
                               "height": 500,
                               "is_recycled": true
                             },
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "file_1.csv"
                           }
                         ]
                       },
                       {
                         "id": "7ead7669-8162-4f64-8cd5-4abe92509e29",
                         "name": "some_other_kind_of_dataset",
                         "tags": {},
                         "labels": ["my-label"],
                         "files": [
                           {
                             "path": "input/datasets/7eadpp9/interesting_file.dat",
                             "cluster": 0,
                             "sequence": 0,
                             "extension": "dat",
                             "labels": [],
                             "tags": {
                               "length": 864,
                               "orientation_angle": 85
                             },
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae9071",
                             "name": "interesting_file.csv"
                           },
                       }
                     ]
                   }


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
                             "tags": {"special_number": 1},
                             "labels": ["lidar", "helpful", "information", "like"],  // Searchable, parsable and filterable
                         },
                         {
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "Lidar - 11 to 18 Dec.csv",
                             "path": "local/file/path/to/folder/containing/it/",
                             "type": "csv",
                             "metadata": {
                             },
                             "size_bytes": 59684813,
                             "tags": {"special_number": 2},
                             "labels": ["lidar", "helpful", "information", "like"]  // Searchable, parsable and filterable
                         },
                         {
                             "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                             "name": "Lidar report.pdf",
                             "path": "local/file/path/to/folder/containing/it/",
                             "type": "pdf",
                             "metadata": {
                             },
                             "size_bytes": 484813,
                             "tags": {},
                             "labels": ["report"]  // Searchable, parsable and filterable
                         }
                     ]
                 },
                 {
                     // ... another dataset manifest ...
                 }
             ]
         }
