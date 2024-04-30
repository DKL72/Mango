import queue

import Error_Handling
import MngcoIO
import StrCo
import sys
import threading
import traceback
from colorama import Fore, init
from cryptography.fernet import Fernet
from datetime import datetime
from io import StringIO

from Functions import *


class Script:
    def __init__(self, name: str = 'main'):
        self.name = name
        self.code = ""
        self.dicts, self.lists = MngcoIO.read()
        self.assembled = ''
        self.messages = []
        self.running = False
        self.vars = {}

        for var in MngcoIO.read()[1]['@builtin']:
            self.vars[var.split(' = ')[0]] = var.split(' = ')[1]

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
                builtIns = MngcoIO.read()[1]['@builtin']

                for builtIn in builtIns:
                    self.assembled = f'{builtIn};\n{self.assembled}'

                exec(self.assembled, globals(), self.vars)
                self.vars['__prints'].append('*Finished')
            except Exception as e:
                self.messages.append(Error_Handling.sort(e, self.code, self.name))
                self.running = False
