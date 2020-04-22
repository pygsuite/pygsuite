from dataclasses import dataclass


@dataclass
class Link:
    url: str
    bookmark_id: str
    heading_id: str

    def render(self) -> dict:
        out = {}
        if self.url:
            out = {"url": self.url}
        elif self.bookmark_id:
            out = {"bookmark_id": self.bookmark_id}
        elif self.heading_id:
            out = {"heading_id": self.heading_id}
        return out
