import importlib.util
import json


# Determines whether numpy is available
_numpy_spec = importlib.util.find_spec("numpy")


class TwinedEncoder(json.JSONEncoder):
    """An encoder which will cope with serialising numpy arrays, ndarrays and matrices to JSON (in list form)

    This is designed to work "out of the box" to help people serialise the outputs from twined applications.
    It does not require installation of numpy - it'll work fine if numpy is not present, so can be used in a versatile
    tool in uncertain environments.

    Example use:
    ```
    from twined.utils import TwinedEncoder
    some_json = {"a": np.array([0, 1])}
    json.dumps(some_json, cls=TwinedEncoder)
    ```
    """

    def default(self, obj):
        """Convert the given object to python primitives.

        :param any obj:
        :return any:
        """
        if _numpy_spec is not None:
            import numpy

            if isinstance(obj, numpy.ndarray) or isinstance(obj, numpy.matrix):
                return obj.tolist()

        return json.JSONEncoder.default(self, obj)
