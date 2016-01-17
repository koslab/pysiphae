class TraversableDict(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        try:
            result = self.data[key]
        except KeyError:
            raise AttributeError(key)
        if isinstance(result, dict):
            return TraversableDict(result)
        return result

    def __getitem__(self, key):
        return self.data[key]

