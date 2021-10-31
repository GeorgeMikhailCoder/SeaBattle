class DictClass:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    def __str__(self):
        str = ""
        for attr in dir( self ):
            if attr[0] != '_' and attr[0:5] != "html_":
                str+= attr.__str__() + ": " + \
                      getattr(self, attr.__str__()).__str__() + " \n"
        return str

    def __from_dict__(self, d):
        for key, value in d.items():
            setattr(self, key, value)
        return self


    def __from_json__(self, str):
        import json
        return self.__from_dict__(dict(json.loads(str)))


    def __as_dict__(self):
        res = dict()
        for attr in vars( self ):
            if attr[0] != '_':
                res[attr.__str__()] = getattr(self, attr.__str__())
        return res

    def __as_json__(self):
        import json
        return json.dumps(self.__as_dict__())