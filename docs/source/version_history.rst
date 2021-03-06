.. _version_history:

===============
Version History
===============

Origins
=======

**twined** began as an internal tool at Octue, enabling applications to be connected together in the Octue ecosystem.

The twined library is presently being ported out of Octue's SDKs as it became clear that it would be most beneficial to
open-source the framework we developed to connect applications and digital twins together.


.. _version_0.0.x:

0.0.x
=====

Initial library framework - development version. Highly unstable! Let's see what happens...

New Features
------------
#. Documentation
#. Travis- and RTD- based test and documentation build with Codecov integration
#. Load and validation of twine itself against twine schema
#. Main ``Twine()`` class with strands set as attributes
#. Validation of input, config and output values against twine
#. Validation of manifest json
#. Credential parsing from the environment and validation
#. Hook allowing instantiation of inputs and config to a given class e.g. ``Manifest``
#. Tests to cover the majority of functionality

Backward Incompatible API Changes
---------------------------------
#. n/a (Initial release)

Bug Fixes & Minor Changes
-------------------------
#. n/a (Initial Release)
