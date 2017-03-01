import re

class AutoResponseFunctionSetter(object):
    def __call(self, function, args):
        underScoreNames = self.camelCaseToUnderScore(function)
        if "_" not in underScoreNames:
            return False
        _temp = underScoreNames.split('_', 2)
        functionType = _temp[0]
        propName = '_'.join(_temp[1:])

        if functionType == 'get':
            if propName not in self.__dict__:
                raise Exception("Wrong function " + function)
            return self.__dict__[propName]
        elif functionType == 'set':
            if propName not in self.__dict__:
                raise Exception("Wrong function " + function)
            self.__dict__[propName] = args[0]
        elif functionType == 'is':
            if underScoreNames not in self.__dict__:
                raise Exception("Wrong function " + function)
            return self.__dict__[underScoreNames]

    def camelCaseToUnderScore(self, input):
        matches = re.findall('([A-Z][A-Z0-9]*(?=$|[A-Z][a-z0-9])|[A-Za-z][a-z0-9]+)', input)
        ret = matches
        for match_i in range(len(ret)):
            match = ret[match_i]
            if match == match.upper():
                ret[match_i] = match.lower()
            else:
                ret[match_i] = match[0].lower() + match[1:]

        return '_'.join(ret)

    def __getattr__(self, name):
        def _temp_function(arg=None):
            return self.__call(name, [arg])
        return _temp_function
