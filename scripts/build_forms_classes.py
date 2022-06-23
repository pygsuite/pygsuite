"""This file contains the code used to generate base Forms classes off the provided google reference implementation."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from googleapiclient.discovery import Resource, build
from jinja2 import Template

file_template = Template(
    '''
from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem
{% if dependency %}
{% for item in dependency %}from pygsuite.forms.generated.{{item.snake}} import {{item.original}}
{% endfor %}{% endif %}

class {{target.class_name}}(BaseFormItem):
    """
    {{ target.description }}
    """
    def __init__(self, {% for arg in target.props if arg.read_only is false() %}
                {{arg.base}}: Optional[{% if not arg.is_basic_type %}"{{arg.type}}"{% else %}{{ arg.type }}{% endif %}] = None,{% endfor %}
                object_info: Optional[Dict] = None):
        generated:Dict = {}
        {% for arg in target.props if arg.read_only is false() %}
        if {{arg.base}} is not None:
            {% if arg.is_list %}generated['{{arg.camel_case}}'] = [{% if not arg.list_type_is_basic %} v._info {% else %} v {% endif %} for v in {{arg.base}}]{% else %}
            generated['{{arg.camel_case}}'] = {% if not arg.is_basic_type %} {{arg.base}}._info {% else %} {{ arg.base }} {% endif %}{% endif %}{% endfor %}
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    {% for prop in target.props %}
    @property
    def {{prop.base}}(self)->{% if prop.is_basic_type %}{{prop.type }}{% else %}"{{ prop.type }}"{% endif %}:
        {% if prop.is_list %}return [{% if prop.class_name %}{{prop.class_name}}(object_info=v){% else %}v{% endif %} for v in self._info.get('{{prop.camel_case}}')]
        {% else %}return {% if prop.is_basic_type %}self._info.get('{{prop.camel_case}}'){% else %}{{ prop.type }}(object_info=self._info.get('{{prop.camel_case}}')){% endif %}{% endif %}{% if not prop.read_only %}
    
    @{{prop.base}}.setter
    def {{prop.base}}(self, value: {% if prop.is_basic_type %}{{prop.type }}{% else %}"{{ prop.type }}"{% endif %}):
        if self._info.get('{{prop.camel_case}}',None) == value:
            return
        self._info['{{prop.camel_case}}'] = value
        {% endif %}
    {% endfor %}
    
    {% if target.class_name.endswith('Request') %}
    @property
    def wire_format(self)->dict:
        base = '{{target.class_name.replace('Request', '')}}'
        base = base[0].lower() + base[1:]
        {% if update_mask %}
        request = self._info
        components = '{{target.snake}}'.split('_')
        # if it's an update, we *may* need to provide an update mask
        # generate this automatically to include all fields
        # can be optionally overridden when creating synchronization method
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        {% endif %}
        return {base:self._info}
    {% endif %}

'''
)


@dataclass
class ArgInfo:
    original: str
    value: dict
    description: str
    # type: str
    # is_basic_type: bool
    # is_list: bool
    read_only: bool
    base: str = None
    camel_case: str = None

    def __post_init__(self):
        self.base = "_".join([z.lower() for z in re.split("(?=[A-Z])", self.original)])
        self.camel_case = self.original

    @property
    def is_basic_type(self):
        return self.value.get("$ref", False) is False

    @property
    def is_list(self) -> bool:
        return self.value.get("type", "str") == "array"

    @property
    def list_type_is_basic(self):
        if not self.is_list:
            return None
        return self.value['items'].get("$ref", False) is False

    @property
    def type(self):
        return build_type(self.value)

    @property
    def class_name(self):
        if not self.value.get("items"):
            return None
        return self.value["items"].get("$ref", None)


@dataclass
class Target:
    class_name: str
    description: str
    props: List[ArgInfo]
    snake: Optional[str] = None

    def __post_init__(self):
        self.snake = "_".join(
            [z.lower() for z in re.split("(?=[A-Z])", self.class_name.strip()) if z]
        )


@dataclass
class Dependency:
    original: str
    snake: str = None

    def __post_init__(self):
        self.snake = "_".join(
            [z.lower() for z in re.split("(?=[A-Z])", self.original.strip()) if z]
        )


def map_type(input: str):
    if input == "string":
        return "str"
    elif input == "array":
        return "list"
    elif input == "boolean":
        return "bool"
    elif input == "integer":
        return "int"
    elif input == "number":
        return "float"
    return input


def build_type(avalue: dict) -> str:
    basic_type = avalue.get("$ref", map_type(avalue.get("type", "str")))
    if basic_type == "list":
        detail = avalue["items"]
        return f"""List["{build_type(detail)}"]"""
    return basic_type


def build_classes(resource: Resource):
    all_classes = []
    base_path = Path(__file__)
    new_parent = base_path.parent.parent / "pygsuite" / "forms" / "generated"
    for key, value in resource._rootDesc["schemas"].items():
        print(key)
        print(value)
        # {'fileUploadAnswers': {'$ref': 'FileUploadAnswers', 'description': 'Output only. The answers to a file upload question.', 'readOnly': True}
        # 'questionId': {'description': "Output only. The question's ID. See also Question.question_id.", 'readOnly': True, 'type': 'string'}
        # 'items': {'description': "Required. A list of the form's items, which can include section headers, questions, embedded media, etc.", 'items': {'$ref': 'Item'}, 'type': 'array'}
        dependency = []
        for akey, avalue in value["properties"].items():
            if avalue.get("$ref"):
                dependency.append(Dependency(original=avalue["$ref"]))
            elif avalue.get("type", "str") == "array":
                if avalue["items"].get("$ref"):
                    dependency.append(Dependency(original=avalue["items"].get("$ref")))
        target = Target(
            description=value["description"],
            class_name=value["id"],
            props=[
                ArgInfo(
                    original=akey,
                    description=avalue["description"],
                    value=avalue,
                    read_only=avalue.get("readOnly", False),
                )
                for akey, avalue in value["properties"].items()
            ],
        )
        update_mask = any([x.base == 'update_mask' for x in target.props])
        rendered = file_template.render(dependency=dependency, target=target, update_mask=update_mask)

        with open(new_parent / f"{target.snake}.py", "w") as f:
            f.write(rendered)
        all_classes.append([target.snake, target.class_name])
    all_classes = [v for v in all_classes if v[0] != "form"]
    with open(new_parent / f"__init__.py", "w") as f:
        f.write("\n".join([f"from pygsuite.forms.generated.{v[0]} import {v[1]}" for v in all_classes]))
        f.write('\n')
        f.write('__all__ = [{}]'.format(','.join([f'"{v[1]}"' for v in all_classes])))


if __name__ == "__main__":
    from google.auth import default

    auth, project = default()

    x = build("forms", "v1", credentials=auth)

    build_classes(x)
