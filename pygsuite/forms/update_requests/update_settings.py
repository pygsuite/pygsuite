from pygsuite.forms.location import Location
from typing import TYPE_CHECKING

from typing import Union

if TYPE_CHECKING:
    from pygsuite.forms.item import Item
    from pygsuite.forms.form_settings import FormSettings

class UpdateSettingsRequest(object):
    def __init__(self, settings:"FormSettings",):
        self.settings = settings

    @property
    def request(self):
        return {"updateSettings":{
            "settings": self.settings._info,
            "updateMask": ','.join([key for key in self.settings._info.keys()])
        }}