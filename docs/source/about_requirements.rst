.. _requirements:

Requirements of the framework
===================================

A *twine* must describe a digital twin, and have multiple roles. It must:

#. Define what data is required by a digital twin, in order to run
#. Define what data will be returned by the twin following a successful run
#. Define the formats of these data, in such a way that incoming data can be validated
#. Define what other (1st or 3rd party) twins / services are required by this one in order for it to run.

If this weren't enough, the description:

#. Must be trustable (i.e. a *twine* from an untrusted, corrupt or malicious third party should be safe to at least read)
#. Must be machine-readable *and machine-understandable* [1]_
#. Must be human-readable *and human-understandable* [1]_
#. Must be discoverable (that is, searchable/indexable) otherwise people won't know it's there in orer to use it.

Fortunately for digital twin developers, several of these requirements have already been seen for data interchange
formats developed for the web. **twined** uses ``JSON`` and ``JSONSchema`` to help interchange data.

If you're not already familiar with ``JSONSchema`` (or wish to know why **twined** uses ``JSON`` over the seemingly more
appropriate ``XML`` standard), see :ref:`introducing_json_schema`.


.. Footnotes:

.. [1] *Understandable* essentially means that, once read, the machine or human knows what it actually means and what to do with it.

