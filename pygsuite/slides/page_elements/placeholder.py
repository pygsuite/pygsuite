from dataclasses import dataclass
from typing import Dict


@dataclass
class Placeholder:
    base: Dict
    type: str = None
    index: int = None
    parent_id: str = None

    def __post_init__(self):
        self.type = self.base.get("type")
        self.index = self.base.get("index")
        self.parent_id = self.base.get("parentObjectId")

    def __str__(self):
        if self.index:
            return f"{self.type}_{self.index}"
        else:
            return self.type

    @property
    def text(self):
        base = ""
        for el in self.base.get("textElements") or []:
            if el.get("textRun"):
                base += el.get("textRun")["content"]
        return base
