from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygsuite.forms.info import Info


class UpdateFormInfoRequest(object):
    def __init__(self, info: "Info", ):
        self.info = info

    @property
    def request(self):
        return {"updateFormInfo": {
            "info": self.info._info,
            "updateMask": ','.join([key for key in self.info._info.keys()])
        }}
