import importlib.util
import json


# Determines whether numpy is available
_numpy_spec = importlib.util.find_spec('numpy')


class TwinedEncoder(json.JSONEncoder):
    """ A class which will cope with serialising numpy arrays, ndarrays and matrices in list form.

    Does not require installation of numpy - it'll only check and serialise if numpy is present.

    """
    def default(self, obj):
        if _numpy_spec is not None:
            import numpy
            if isinstance(obj, numpy.array) or isinstance(obj, numpy.ndarray) or isinstance(obj, numpy.matrix):
                return obj.tolist()
        return json.JSONEncoder.default(self, obj)

