.. _other_considerations:

====================
Other Considerations
====================

A variety of thoughts that arose whilst architecting **twined**.

.. _bash_style_stdio:

Bash-style stdio
----------------

Some thought was given to using a very old-school-unix approach to piping data between twins, via stdout.

Whilst attractive (as being a wildly fast way of piping data between twins on the same machine) it was felt this
was insufficiently general, eg:

 - where twins don't exist on the same machine or container, making it cumbersome to engineer common iostreams
 - where slight differences between different shells might lead to incompatibilities or changes in behaviour

And also unfriendly, eg:

 - engineers or scientists unfamiliar with subtleties of bash shell scripting encounter difficulty piping data around
 - difficult to build friendly web based tools to introspect the data and configuration
 - bound to be headaches on windows platforms, even though windows now supports bash
 - easy to corrupt using third party libraries (e.g. which print to stdout)


.. _Units:

Units
-----

Being used (mostly) for engineering and scientific analysis, it was tempting to add in a specified sub-schema for units.
For example, mandating that where values can be given in units, they be specified in a certain way, like:

.. code-block:: javascript

   {
       "wind_speed": {
           "value": 10.2,
           "units": "mph"
       }
   }

or (more succinct):

.. code-block:: javascript

   {
       "wind_speed": 10.2,
       "wind_speed_units": "mph"
   }

It's still extremely tempting to provide this facility; or at least provide some way of specifying in the schema
what units a value should be provided in. Thinking about it but don't have time right now.
If anybody wants to start crafting a PR with an extension or update to **twined** that facilitates this; please raise an
issue to start progressing it.


.. _variable_style:

Variable Style
--------------

A premptive stamp on the whinging...

Note that in the ``JSON`` descriptions above, all variables are named in ``snake_case`` rather than ``camelCase``. This
decision, more likely than even Brexit to divide opinions, is based on:
  - The reservation of snake case for the schema spec has the subtle advantage that in future, we might be able to use
    camelCase within the spec to denote class types in some useful way, just like in python. Not sure yet; just mulling.
  - The :ref:`requirements` mention human-readability as a must;
    `this paper <https://ieeexplore.ieee.org/document/5521745?tp=&arnumber=5521745&url=http:%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D5521745>`_
    suggests a 20% slower comprehension of camel case than snake.
  - The languages we anticipate being most popular for building twins seem to trend toward snake case (eg
    `python <https://www.python.org/dev/peps/pep-0008/>`_, `c++ <https://google.github.io/styleguide/cppguide.html>`_)
    although to be fair we might've woefully misjudged which languages start emerging.
  - We're starting in Python so are taking a lead from PEP8, which is bar none the most successful style guide on the
    planet, because it got everybody on the same page really early on.

If existing code that you're dropping in uses camelCase, please don't file that as an issue... converting property
names automatically after schema validation generation is trivial, there are tons of libraries (like
`humps <https://humps.readthedocs.io/en/latest/>`_) to do it.

We'd also consider a pull request for a built-in utility converting `to <https://pypi.org/project/camelcase/>`_ and
`from <>`_ that does this following validation and prior to returning results. Suggest your proposed approach on the
issues board.
