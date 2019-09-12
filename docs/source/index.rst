.. ATTENTION::
    This library is in very early stages. Like the idea of it? Please
    `star us on GitHub <https://github.com/octue/twined>`_ and contribute via the
    `issues board <https://github.com/octue/twined/issues>`_ and
    `roadmap <https://github.com/octue/twined/projects/1>`_.

.. image:: https://codecov.io/gh/octue/twined/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/octue/twined
  :alt: Code coverage
  :align: right
.. image:: https://readthedocs.org/projects/twined/badge/?version=latest
  :target: https://twined.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
  :align: right

======
Twined
======

**twined** is a library to help :ref:`digital_twins` talk to one another.

.. epigraph::
   *"Twined" [t-why-nd] ~ encircled, twisted together, interwoven*

A digital twin is a virtual representation of a real life being - a physical asset like a wind turbine or car - or even
a human. Like real things, digital twins need to interact, so can be connected together, but need a common communication
framework to do so. This is what is provided by **twined**.

.. figure:: images/digital_twin_hierarchy.svg
    :width: 350px
    :align: center
    :figclass: align-center
    :alt: Hierarchy of digital twins

    Digital twins connected in a hierarchy. Each blue circle represents a twin, coupled to its neighbours.
    Yellow nodes are where schema are used to connect twins.


.. _aims:

Aims
====

**twined** provides a toolkit to help create and validate ":ref:`schema`" - descriptions of a digital twin, what data it
requires, what it does and how it works.

The goals of **twined** are as follows:
    - Provide a clear framework for what a digital twin schema can and/or must contain
    - Provide functions to validate incoming data against a known schema
    - Provide functions to check that a schema itself is valid
    - Provide (or direct you to) tools to create schema describing what you require

Using :ref:`schema`, we can describe how digital twins connect and interact... building them together in hierarchies and
networks.

The scope of **twined** is not large. Many other libraries will deal with hosting and deploying digital twins, still
more will deal with the actual analyses done within them. **twined** purely deals with parsing and checking the
information exchanged.


.. _reason_for_being:

Raison d'etre
=============

Octue believes that a lynchpin of solving climate change is the ability for all engineering, manufacturing, supply
chain and infrastructure plant to be connected together, enabling strong optimisation and efficient use of these
systems.

To enable engineers and scientists to build, connect and run digital twins in large networks (or even in small teams!)
it is necessary for everyone to be on the same page - the :ref:`gemini_principles` are a great way to start with that,
which is why we've released this part of our technology stack as open source, to support those principles and help
develop a wider ecosystem.


.. _uses:

Uses
=====

At `Octue <https://www.octue.com>`_, **twined** is used as a core part of our application creation process:

  * As a tool to validate incoming data to digital twins
  * As a framework to help establish schema when designing digital twins
  * As a source of information on digital twins in our network, to help map and connect twins together

We'd like to hear about your use case. Please get in touch!

We use the `GitHub Issue Tracker <https://github.com/octue/twined>`_ to manage bug reports and feature requests.
Please note, this is not a "general help" forum; we recommend Stack Overflow for such questions. For really gnarly
issues or for help designing digital twin schema, Octue is able to provide application support services for those
building digital twins using **twined**.


.. _life_choices:

Life Choices
============

**twined** is presently released in python only. It won't be too hard to replicate functionality in other languages, and
we're considering other languages at present, so might be easily persuadable ;)

If you require implementation of **twined** in a different language,
and are willing to consider sponsorship of development and maintenance of that library, please
`get in touch <https://octue.com/contact>`_.


.. toctree::
   :maxdepth: 2
   :hidden:

   self
   digital_twins
   schema
   installation
   examples
   license
   version_history
