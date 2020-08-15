.. _monitors_strand:

===============
Monitors Strand
===============

The ``configuration_values_schema``, ``input_values_schema`` and ``output_values_schema`` strands are *values-based*,
meaning the data that matches these strands is in JSON form.

Each of these strands is a *json schema* which describes that data.

.. tabs::

   .. group-tab:: Monitors Strand

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



Let's look at basic examples for twines containing each of these strands:


.. tabs::

   .. group-tab:: Monitors Strand

      **Monitor data (output)**

      **Log data (output)**

