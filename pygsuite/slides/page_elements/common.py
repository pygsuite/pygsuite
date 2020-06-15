from dataclasses import dataclass
from typing import Dict


@dataclass
class Text:
    base: Dict

    @property
    def text(self):
        base = ""
        for el in self.base.get("textElements") or []:
            if el.get("textRun"):
                base += el.get("textRun")["content"]
        return base
