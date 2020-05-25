from collections import OrderedDict


class KeyList(list):
    def __init__(self, keys, values):
        self.key_dict = OrderedDict()
        for val in zip(keys, values):
            self.key_dict[val[0]] = val[1]
        super(KeyList, self).__init__(values)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.key_dict[item]
        else:
            return super().__getitem__(item)
