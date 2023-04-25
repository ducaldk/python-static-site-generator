import re
from yaml import load, FullLoader
from collections.abc import Mapping

class Content(Mapping):
    # misspelled in the instructions, by the way...
    __delimiter = r"^(?:-|\+){3}\s*$"
    __regex = re.compile(__delimiter, re.MULTILINE)

    
    @classmethod
    def load(cls, string):
        # second argument they call 'depth' but I think it is 'maxsplit'
        _, fm, content = cls.__regex.split(string, 2)
        # this is the yaml.load
        # specification of metadata as return value was OMITTED from the instructions
        metadata = load(fm, Loader=FullLoader)
        return cls(metadata, content)

    # this step was out of order in the instructions - also very confusing
    def __init__(self, metadata, content):
        self.data = metadata
        self.data["content"] = content

    @property
    def body(self):
        return self.data["content"]

    @property
    def type(self):
        return self.data["type"] if "type" in self.data else None

    @type.setter
    def type(self, type):
        self.data["type"] = type

    def __getitem__(self, key):
        # but surely you will get a KeyError from time to time...
        return self.data[key]
        # return self.data[key] if key in self.data else None

    def __iter__(self):
        # so this just works, no need for an explicit return...
        self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        data = {}
        for key,value in self.data.items():
            if key != "content":
                data[key] = value
        return str(data)
    