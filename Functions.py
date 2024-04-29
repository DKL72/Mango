def subset(header1: str, header2: str, constants: dict):
    keys = list(constants.keys())
    values = list(constants.values())
    indexes = (keys.index(header1) + 1, keys.index(header2))

    return keys[keys.index(header1) + 1: keys.index(header2)], values[indexes[0]: indexes[1]]