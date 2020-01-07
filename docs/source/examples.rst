.. _examples:

========
Examples
========

Here, we look at example use cases for the library, and show how to use it in python.

It's also well worth looking at the unit test cases
copied straight from the unit test cases, so you can always check there to see how everything hooks up.


.. _example_equipment_installation_cost:

[Simple] Equipment installation cost
====================================

.. tabs::

   .. group-tab:: Scenario

      You need to provide your team with an estimate for installation cost of an equipment foundation.

      It's a straightforward calculation for you, but the Logistics Team keeps changing the installation position, to
      try and optimise the overall project logistics.

      Each time the locations change, the GIS team gives you an updated embedment depth, which is what you use
      (along with steel cost and foundation type), to calculate cost and report it back.

      This twine allows you to define to create a wrapper around your scripts that communicates to the GIS team what you
      need as an input, communicate to the logistics team what they can expect as an output.

      When deployed as a digital twin, the calculation gets automatically updated, leaving you free to get on with
      all the other work!

   .. group-tab:: Twine

      We specify the ``steel_cost`` and ``foundation_type`` as ``configuration`` values, which you can set on startup of the twin.

      Once the twin is running, it requires the ``embedment_depth`` as an ``input_value`` from the GIS team. A member
      of the GIS team can use your twin to get ``foundation_cost`` directly.

      .. code-block:: javascript

         {
             "title": "Foundation Cost Model",
             "description": "This twine helps compute the cost of an installed foundation.",
             "children": [
             ],
             "configuration_schema": {
                 "$schema": "http://json-schema.org/2019-09/schema#",
                 "title": "Foundation cost twin configuration",
                 "description": "Set config parameters and constants at startup of the twin.",
                 "type": "object",
                 "properties": {
                     "steel_cost": {
                         "description": "The cost of steel in GBP/m^3. To get a better predictive model, you could add an economic twin that forecasts the cost of steel using the project timetable.",
                         "type": "number",
                         "minimum": 0,
                         "default": 3000
                     },
                     "foundation_type": {
                         "description": "The type of foundation being used.",
                         "type": "string",
                         "pattern": "^(monopile|twisted-jacket)$",
                         "default": "monopile"
                     }
                 }
             },
             "input_values_schema": {
                 "$schema": "http://json-schema.org/2019-09/schema#",
                 "title": "Input Values schema for the foundation cost twin",
                 "description": "These values are supplied to the twin asynchronously over a web socket. So as these values change, the twin can reply with an update.",
                 "type": "object",
                 "properties": {
                     "embedment_depth": {
                         "description": "Embedment depth in metres",
                         "type": "number",
                         "minimum": 10,
                         "maximum": 500
                     }
                 }
             },
             "output_manifest": [
             ],
             "output_values_schema": {
                 "title": "Output Values schema for the foundation cost twin",
                 "description": "The response supplied to a change in input values will always conform to this schema.",
                 "type": "object",
                 "properties": {
                     "foundation_cost": {
                         "description": "The foundation cost.",
                         "type": "integer",
                         "minimum": 2
                     }
                 }
             }
         }
