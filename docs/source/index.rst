.. ATTENTION::
    This library is in very early stages. Like the idea of it? Please
    `star us on GitHub <https://github.com/octue/twined>`_ and contribute via the
    `issues board <https://github.com/octue/twined/issues>`_ and
    `roadmap <https://github.com/octue/twined/projects/1>`_.

======
Twined
======

**twined** is a library to help create and connect :ref:`digital_twins` and data services.

.. epigraph::
   *"Twined" [t-why-nd] ~ encircled, twisted together, interwoven*

A digital twin is a virtual representation of a real life being - a physical asset like a wind turbine or car - or even
a human. Like real things, digital twins need to interact, so can be connected together, but need a common communication
framework to do so.

**twined** helps you to define a single file, a "twine", that defines a digital twin / data service. It specifies
specifying its data interfaces, connections to other twins, and other requirements.

Any person, or any computer, can read a twine and understand *what-goes-in* and *what-comes-out*. That makes it easy to
collaborate with other teams, since everybody is crystal clear about what's needed.

.. figure:: images/digital_twin_hierarchy.svg
    :width: 350px
    :align: center
    :figclass: align-center
    :alt: Hierarchy of digital twins

    Digital twins / data services connected in a hierarchy. Each blue circle represents a twin, coupled to its neighbours.
    Yellow nodes are where schema are used to connect twins.


.. _aims:

Aims
====

**twined** provides a toolkit to help create and validate "twines" - descriptions of a digital twin, what data it
requires, what it does and how it works.

The goals of this **twined** library are as follows:
    - Provide a clear framework for what a *twine* can and/or must contain
    - Provide functions to validate incoming data against a known *twine*
    - Provide functions to check that a *twine* itself is valid
    - Provide (or direct you to) tools to create *twines* describing what you require

In :ref:`anatomy`, we describe the different parts of a twine (examining how digital twins connect and interact...
building them together in hierarchies and networks). But you may prefer to dive straight in with the :ref:`quick_start`
guide.

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

The main goal is to **help engineers and scientists focus on doing engineering and science** - instead of apis, data
cleaning/management, and all this cloud-pipeline-devops-test-ci-ml BS that takes up 90% of a scientist's time, when they
should be spending their valuable time researching migratory patterns of birds, or cell structures, or wind turbine
performance, or whatever excites them.

.. _uses:

Uses
=====

At `Octue <https://www.octue.com>`_, **twined** is used as a core part of our application creation process:

  * As a format to communicate requirements to our partners in research projects
  * As a tool to validate incoming data to digital twins
  * As a framework to help establish schema when designing digital twins
  * As a source of information on digital twins in our network, to help map and connect twins together

We'd like to hear about your use case. Please get in touch!

We use the `GitHub Issue Tracker <https://github.com/octue/twined>`_ to manage bug reports and feature requests.
Please note, this is not a "general help" forum; we recommend Stack Overflow for such questions. For really gnarly
issues or for help designing digital twin schema, Octue is able to provide application support services for those
building digital twins using **twined**.

.. toctree::
   :maxdepth: 2

   self
   quick_start
   anatomy
   about
   deployment
   license
   version_history
