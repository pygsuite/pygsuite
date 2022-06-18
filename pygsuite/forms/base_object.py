class BaseFormItem(object):
    def __init__(self, info, form):
        self._info = info
        self._form = form

    def __repr__(self):
        # output = []
        # for key, value in self._info.items():
        #     output.append(f'{key}: {getattr(self, key, None)}')
        # final_string = '\n'.join(output)
        return str(self._info)
