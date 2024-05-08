import traceback
from colorama import init, Fore
from datetime import datetime
import MngcoIO


def error(error: str, line: str, location: tuple[int, int], name: str):
    dicts, lists = MngcoIO.read()

    return f'!EXCEPTION [{datetime.now().strftime("%H:%M:%S")}] | Terminated Process - {name}\n\n{error} ERROR: "{line}" @ {location}\nSeverity: {dicts[error]}'


def sort(e: Exception, code: str, name: str):
    errorType = type(e).__name__
    lastError = traceback.extract_tb(e.__traceback__)[-1]

    if errorType == 'ModuleNotFoundError':
        line = traceback.extract_tb(e.__traceback__)[-1].lineno
        return error('INCLUDE', 'include ' + e.__str__().split("'")[1], (line - 1, 0), name)

    elif errorType == 'NameError':
        return error('NAME', code.split('\n')[lastError.lineno - len(MngcoIO.read2()[0]['@builtin']) - 1].strip(),
                     (lastError.lineno - len(MngcoIO.read2()[0]['@builtin']), 0), name)

    else:
        return e
