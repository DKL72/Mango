import Error_Handling
import Mngco_IO
import StrCo
import sys
import threading
import traceback
from colorama import Fore, init
from cryptography.fernet import Fernet
from datetime import datetime
from Functions import *
from io import StringIO


class Script:
    def __init__(self, name: str = 'main'):
        self.name = name
        self.code = ""
        self.dicts, self.lists = Mngco_IO.read()
        self.assembled = ''
        self.messages = []
        self.running = False
        self.vars = {}

    def clear(self):
        self.messages = []

    def error(self, error: str, line: str, location: tuple[int, int]):
        message = f'{Fore.RED}!EXCEPTION [{datetime.now().strftime("%H:%M:%S")}] | Terminated Process - {self.name}\n\n{error} ERROR: "{line}" @ {location}\nSeverity: {self.dicts[error]}'
        self.messages.append(message)
        self.running = False

    def run(self, interpreter: str = 'alpha'):
        removed = self.lists['@removed']

        if interpreter == 'alpha':
            for rem in removed:
                for l, line in enumerate(self.code.splitlines()):
                    if rem in line:
                        self.error('SYNTAX', line, (l, line.find(rem)))
                    elif line != '' and line[-1] not in [':', ';']:
                        self.error('ENDING', line, (l, len(line)))

            replacements = subset('@interpreter', '@error-severity', self.dicts)

            self.assembled = self.code
            for r, repl in enumerate(replacements[0]):
                while repl in self.assembled and StrCo.isValid(self.assembled.find(repl), self.assembled):
                    if StrCo.isValid(self.assembled.find(repl), self.assembled):
                        self.assembled = self.assembled.replace(repl, replacements[1][r], 1)

            try:
                builtIns = Mngco_IO.read()[1]['@builtin']

                for builtIn in builtIns:
                    self.assembled = f'{builtIn};\n{self.assembled}'

                exec(self.assembled, globals(), self.vars)
            except Exception as e:
                self.messages.append(Error_Handling.sort(e, self.code, self.name))
                self.running = False
