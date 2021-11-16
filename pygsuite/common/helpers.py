from enum import Enum
from typing import Any, Callable, Optional


def coerce_value_to_enum(
    value: Any,
    enum: Enum,
    transform: Optional[Callable] = None
) -> Enum:

    if transform:
        value = transform(value)

    try:
        out = enum(value)
    except ValueError:
        raise ValueError(
            f"{value} is not a valid input. Please use one of the following inputs instead:\n"
            f"[{', '.join(list(map(lambda e: e.value, enum)))}]\n"
            f"Or, use an input enumeration of the type: {enum.__name__}"
        )

    return out


if __name__ == "__main__":

    from pygsuite.enums import UserType

    print(coerce_value_to_enum(
        value="User",
        enum=UserType,
        transform=str.lower,
    ))

    print(coerce_value_to_enum(
        value="Robot",
        enum=UserType,
        transform=str.lower,
    ))
