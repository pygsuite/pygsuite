class BaseFormItem(object):
    def __init__(self, object_info):
        self._info = object_info

    def __repr__(self):
        # output = []
        # for key, value in self._info.items():
        #     output.append(f'{key}: {getattr(self, key, None)}')
        # final_string = '\n'.join(output)
        return str(self._info)
