.. _deployment:

==========
Deployment
==========


.. _deploying_with_octue:

Deploying with Octue
====================

`Octue <https://www.octue.com>`_ provides automated deployment to a cloud provider (like GCP or Azure), along with
permissions and user management, monitoring, logging and data storage management out of the box.

There are also a whole bunch of collaborative helper tools, like the graphical
`twine builder <https://app.octue.com/twined>`_ and manifesting tools, designed to speed up the process of building
and using twines.

The full set of services is in early beta, `get in touch <https://www.octue.com/contact>`_ and we can help you
architect systems - from small data services to large networks of :ref:`digital_twins`.


.. _deploying_with_doctue:

Coming Soon - Deploying with doctue
===================================

Once we've bedded down our services internally at Octue, we'll be open-sourcing more parts of our build/deploy process,
including docker containers with pre-configured servers to run and monitor twine-based services and digital twins.

This will allow services to be easily spun up on GCP, Azure Digital Ocean etc., and be a nice halfway house between
fully managed system on Octue and running your own webserver. Of course,
without all the collaborative and data management features that Octue provides ;)

We're looking for commercial sponsors for this part of the process - if that could be you, please
`get in touch <https://www.octue.com/contact>`_


.. _deploying_as_a_cli:

Deploying as a command-line application
=======================================

Use the open-source `octue app template <https://github.com/octue/octue-app-python>`_ as a guide. Write your new
python code (or call your existing tools/libraries) within it. It's set up to wrap and check configuration, inputs and
outputs using twined. Follow the instructions there to set up your inputs, and your files, and run an analysis.


.. _deployment_with_a_web_server:

Deploying with your own web server
==================================

You can use any python based web server (need another language? see :ref:`language_choice`):

- Add ``configuration_values_data`` to your webserver config
- Set up an endpoint to allow.
- Set up an endpoint to handle incoming requests / socket messages - these will be ``input_values_data``.
- Treat these requests / messages as events which trigger a task.
- In your task framework (e.g. your celery task), either:
     - Use **twined** directly to validate the ``input_values_data``/``output_values_data`` (and, on startup, the
       ``configuration_values_data``) and handle running any required analysis yourself, or
     - import your analysis app (as built in :ref:`deploying_as_a_cli`) and call it with the configuration and input
       data in your task framework.
- Return the result to the client.
