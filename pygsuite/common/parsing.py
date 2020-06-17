def parse_id(input_id: str) -> str:
    if "/" in input_id:
        portions = input_id.split("/")
        for idx, val in enumerate(portions):
            if val == "d":
                return portions[idx + 1]
        raise ValueError("Unable to parse ID from input")
    else:
        return input_id
