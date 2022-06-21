
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.grid import Grid
from pygsuite.forms.generated.image import Image
from pygsuite.forms.generated.question import Question


class QuestionGroupItem(BaseFormItem):
    """
    Defines a question that comprises multiple questions grouped together.
    """
    def __init__(self, 
                grid: Optional["Grid"] = None,
                image: Optional["Image"] = None,
                questions: Optional[List["Question"]] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if grid:
            generated['grid'] =  grid._info 
        if image:
            generated['image'] =  image._info 
        if questions:
            generated['questions'] =  questions 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def grid(self)->"Grid":
        return Grid(object_info=self._info.get('grid'))
    
    @grid.setter
    def grid(self, value: "Grid"):
        if self._info['grid'] == value:
            return
        self._info['grid'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def image(self)->"Image":
        return Image(object_info=self._info.get('image'))
    
    @image.setter
    def image(self, value: "Image"):
        if self._info['image'] == value:
            return
        self._info['image'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def questions(self)->List["Question"]:
        return [Question(object_info=v) for v in self._info.get('questions')]
        
    
    @questions.setter
    def questions(self, value: List["Question"]):
        if self._info['questions'] == value:
            return
        self._info['questions'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

