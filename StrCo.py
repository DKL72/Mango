import ErrorHandling
from colorama import init, Fore


def search(string: str, substring: str, start: int = -1, end: int = -1) -> list[int]:
    end = len(string) if end == -1 else end
    old = start
    locations = []

    for i in range(string.count(substring)):
        old = string.find(substring, old + 1, end)
        locations.append(old)
    locations.reverse()
    return locations


def get(code: str):
    pairs = []
    locations = search(code, "'")

    if len(locations) % 2 != 0:
        Error_Handling.error('QUOTATIONS', 'N\\A', (-1, -1), 'Script')
        return [[-1, len(code)]]

    for l in range(len(locations)):
        if l % 2 == 0:
            pairs.append([locations[l + 1], locations[l]])

    return pairs


def isValid(index: int, code: str):
    for p, pair in enumerate(get(code)):
        if pair[0] < index < pair[1]:
            return False

    return True
