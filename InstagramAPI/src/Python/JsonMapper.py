class JsonMapper():
    def __init__(self):
        self.bStrictNullTypes = False
        self.bExceptionOnUndefinedProperty = False # TODO implement

    def is_primitive(self, obj):
        return type(obj) in [str, int, float, bool]

    def map(self, root, obj):
        if root is None:
            obj = None
            return obj

        if type(root) is list:
            keys = list(obj.__dict__.keys())

            for i in range(len(root)):
                obj.__dict__[keys[i]] = root[i]

            return obj
        elif self.is_primitive(root):
            obj = root
            return obj

        for key in root:
            if "_types" in obj.__dict__ and key in obj._types:
                if type(obj._types[key]) is list:
                    obj.__dict__[key] = []

                    # TODO: check if root[key] is list
                    for i in range(len(root[key])):
                        obj.__dict__[key].append(obj._types[key][0]())
                        obj.__dict__[key][i] = self.map(root[key][i], obj.__dict__[key][i])
                else:
                    obj.__dict__[key] = obj._types[key]()
                    obj.__dict__[key] = self.map(root[key], obj.__dict__[key])
            else:
                obj.__dict__[key] = root[key]

        return obj
