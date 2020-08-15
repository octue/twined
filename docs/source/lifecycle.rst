
..

      Data matching the ``configuration_values_schema`` is supplied to the digital twin / data service at
      startup.

      It's generally used to define control parameters relating to what the service should do, or how it should operate.
      For example, should it produce output images as low resolution PNGs or as SVGs? How many iterations of a fluid
      flow solver should be used? What is the acceptable error level on an classifier algorithm?

   Input Values

      Once configuration data supplied to a service has been validated, it can accept inputs and run analyses
      using them.

      Depending on the way it's deployed (see :ref:`deployment`), the ``input_values`` might come in from a web request,
      over a websocket or called directly from the command line or another library.

      However it comes, new ``input_values``, which are in ``JSON`` format, are checked against the
      ``input_values_schema`` strand of the twine. If they match, then analysis can proceed.

   Output Values

      Once a service has Data matching the ``output_values_schema`` is supplied to the service while it's running.  Depending on the way
      it's deployed, the values might come in from a web request, over a websocket or called directly from
      another library

      Input For example current rotor speed, or forecast wind direction.

      Values might be passed at instantiation of a twin (typical application-like process) or via a socket.
