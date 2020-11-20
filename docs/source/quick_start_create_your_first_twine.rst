.. _create_your_first_twine:

Create your first twine
=======================

Let's say we want a digital twin that accepts two values, uses them to make a calculation, then gives the result. Anyone connecting to the twin will need to know what values it requires, and what it responds with.

First, create a blank text file, call it `twine.json`. We'll give the twin a title and description.
Paste in the following:

.. code-block:: javascript

   {
	   "title": "My first digital twin... of an atomising discombobulator",
	   "description": "A simple example... estimates the `foz` value of an atomising discombobulator."
   }

Now, let's define an input values strand, to specify what values are required by the twin. For this we use a json schema
(you can read more about them in :ref:`introducing_json_schema`). Add the ``input_values`` field, so your twine looks like this:

.. code-block:: javascript

    {
        "title": "My first digital twin",
        "description": "A simple example to build on..."
        "input_values_schema": {
            "$schema": "http://json-schema.org/2019-09/schema#",
            "title": "Input Values schema for my first digital twin",
            "description": "These values are supplied to the twin by another program (often over a websocket, depending on your integration provider). So as these values change, the twin can reply with an update.",
            "type": "object",
            "properties": {
            	"foo": {
            		"description": "The foo value... speed of the discombobulator's input bobulation module, in m/s",
            		"type": "number",
            		"minimum": 10,
            		"maximum": 500
            	},
            	"baz": {
            		"description": "The baz value... period of the discombobulator's recombulation unit, in s",
            		"type": "number",
            		"minimum": 0,
            		"maximum": 1000
            	}
            }
        }
    }

Finally, let's define an output values strand, to define what kind of data is returned by the twin:

.. code-block:: javascript

        "output_values_schema": {
            "$schema": "http://json-schema.org/2019-09/schema#",
            "title": "Output Values schema for my first digital twin",
            "description": "The twin will output data that matches this schema",
            "type": "object",
            "properties": {
            	"foz": {
            		"description": "Estimate of the foz value... efficiency of the discombobulator in %",
            		"type": "number",
            		"minimum": 10,
            		"maximum": 500
            	}
            }
        }


.. _load_the_twine:

Load the twine
==============

**twined** provides a `Twine()` class to load a twine (from a file or a json string).
The loading process checks the twine itself is valid. It's as simple as:

.. code-block:: py

    from twined import Twine

    my_twine = Twine(source='twine.json')


.. _validate_some_inputs:

Validate some inputs
====================

Say we have some json that we want to parse and validate, to make sure it matches what's required for input values.

.. code-block:: py

    my_input_values = my_twine.validate_input_values(json='{"foo": 30, "baz": 500}')

You can read the values from a file too. Paste the following into a file named ``input_values.json``:

.. code-block:: javascript

    {
      "foo": 30,
      "baz": 500
    }

Then parse and validate directly from the file:

.. code-block:: py

    my_input_values = my_twine.validate_input_values(source="input_values.json")


.. ATTENTION::
    LIBRARY IS UNDER CONSTRUCTION! WATCH THIS SPACE FOR MORE!