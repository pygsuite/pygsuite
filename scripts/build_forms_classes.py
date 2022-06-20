from googleapiclient.discovery import Resource, build
from jinja2 import Template


basic = Template('''
from .base_object import BaseFormItem

class {{title}}(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)
{% for arg in args %}
    @property
    def {{ arg.snake }}(self):
        return self._info.get('{{ arg.original }}')
        
    @{{ arg.snake }}.setter
    def {{ arg.snake }}(self, value):
        self._info['{{ arg.original }}'] = value
        
{% endfor %}    
''')

'''{
  "includeTime": boolean,
  "includeYear": boolean
}'''
import re
from dataclasses import dataclass

@dataclass
class ArgInfo:
    snake:str
    original:str
title = 'DateQuestion'
args =  ['includeTime', 'includeYear']

processed_args = [ArgInfo('_'.join([z.lower() for z in re.split('(?=[A-Z])', v)]), v) for v in args]
t = basic.render(title=title,args= processed_args)
#t = basic.render(title= 'QuizSettings',args= ['isQuiz'])
#t = basic.render(title='FormSettings',args= ['quiz_settings'])
print(t)


def build_classes(resource:Resource):
    created = []
    for key, value in resource._rootDesc['schemas'].items():
        print(key)
        print(value)
        print('-----------')


if __name__ == "__main__":
    from google.auth import default

    auth, project = default(
    )

    x = build("forms", 'v1', credentials=auth)

    build_classes(x)