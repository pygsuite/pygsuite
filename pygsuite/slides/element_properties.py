from dataclasses import dataclass
from enum import Enum
from typing import Union


class MeasurementUnit(Enum):
    PT = 1
    EMU = 2

MARGIN = .95
PT_TO_INCH = 72

# DEFAULT SLIDE RATIO
# TODO: genericize
SLIDE_WIDTH = PT_TO_INCH *10
SLIDE_HEIGHT = PT_TO_INCH *5.63

def process_dimension(dim, FULL):
    if isinstance(dim, str):
        if dim.endswith('%'):
            return int(dim[0:-1])*.01*FULL
        else:
            return int(dim)
    else:
        return dim


@dataclass
class ElementProperties:
    x:Union[int,str]
    y:Union[int,str]
    width:Union[int,str]
    height:Union[int,str]
    object_id = None
    unit_type = 'PT'

    def __post_init__(self):
        self.x = process_dimension(self.x, SLIDE_WIDTH)
        self.y = process_dimension(self.y, SLIDE_HEIGHT)
        self.width = process_dimension(self.width, SLIDE_WIDTH)
        self.height = process_dimension(self.height, SLIDE_HEIGHT)
    def to_slides_json(self, page_id):
        base = {
            "pageObjectId":page_id,
            "size": {
                "width": {
                    "magnitude": self.width,
                    "unit": 'PT'
                },
                "height": {
                    "magnitude": self.height,
                    "unit": self.unit_type
                }
            },
            "transform": {
                "scaleX": 1,
                "scaleY": 1,
                # "shearX": 1,
                # "shearY": 1,
                "translateX": self.x,
                "translateY": self.y,
                "unit": self.unit_type
            }
        }


        return base