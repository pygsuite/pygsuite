from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union


class QueryTerm(Enum):
    """Enumeration representing query term fields that can be searched.

    More information here: https://developers.google.com/drive/api/v3/ref-search-terms#file_properties
    """

    NAME = "name"
    TEXT = "fullText"
    MIMETYPE = "mimeType"
    MODIFIED_TIME = "modifiedTime"
    LAST_VIEWED_TIME = "viewedByMeTime"
    TRASHED = "trashed"
    STARRED = "starred"
    PARENTS = "parents"
    OWNERS = "owners"
    WRITERS = "writers"
    READERS = "readers"
    SHARED_WITH_ME = "sharedWithMe"
    CREATED_TIME = "createdTime"
    PROPERTIES = "properties"
    ADD_PROPERTIES = "addProperties"
    VISIBILITY = "visibility"
    SHORTCUT_DETAILS_TARGET_ID = "shortcutDetails.targetId"
    # drive-specific query terms
    HIDDEN = "hidden"
    MEMBER_COUNT = "memberCount"
    ORGANIZER_COUNT = "organizerCount"


class Operator(Enum):
    """Enumeration representing comparison operators for a query string.

    More information here: https://developers.google.com/drive/api/v3/ref-search-terms#operators
    """

    CONTAINS = "contains"
    NOT_CONTAINS = "not {} contains"
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    IN = "in"
    AND = "and"
    OR = "or"
    NOT = "not"
    HAS = "has"


class Connector(Enum):
    AND = "and"
    OR = "or"


@dataclass
class QueryString:
    query_term: Union[QueryTerm, str]
    operator: Optional[Union[Operator, str]] = None
    value: Optional[str] = None

    def __post_init__(self):

        # convert strings to enums
        if isinstance(self.query_term, str):
            try:
                self.query_term = QueryTerm(self.query_term)
            except ValueError as e:
                raise ValueError(
                    f"{self.query_term} is an unsupported query term. Please see the docs for supported query terms: "
                    "https://developers.google.com/drive/api/v3/ref-search-terms"
                ) from e

        if isinstance(self.operator, str):
            try:
                self.operator = Operator(self.operator)
            except ValueError as e:
                raise ValueError(
                    f"{self.operator} is an unsupported operator. Please see the docs for supported operators: "
                    "https://developers.google.com/drive/api/v3/ref-search-terms"
                ) from e

        # convert bools to JSON-friendly capitalization
        if isinstance(self.value, bool):
            self.value = str(self.value).lower()
        # IN comparisons reverse order to value, operator, query_term
        # ex. 'test@example.org' in writers
        if self.operator == Operator.IN:
            self.formatted = f"'{self.value}' {self.operator.value} {self.query_term.value}"
        # NOT_CONTAINS comparisons wrap query term with operator
        # ex. not name contains 'hello'
        elif self.operator == Operator.NOT_CONTAINS:
            self.formatted = (
                self.operator.value.format(self.query_term.value) + f" {self.query_term.value}"
            )
        # all other operators are formatted: query_term, operator, value
        else:
            self.formatted = f"{self.query_term.value} {self.operator.value} '{self.value}'"


@dataclass
class QueryStringGroup:
    query_strings: List[Any]  # type: ignore
    connectors: Optional[List[Union[Connector, str]]] = None

    def __post_init__(self):

        self.formatted = ""

        if self.connectors is None:
            self.connectors = [Connector.AND] * (len(self.query_strings) - 1)

        # pad the first connector for iteration
        self.connectors.insert(0, None)

        zipped_list = zip(self.query_strings, self.connectors)

        for (query_string, connector) in zipped_list:
            self.formatted += (
                f"{connector.value if connector is not None else ''} {query_string.formatted} "
            )

        self.formatted = f"({self.formatted})"
