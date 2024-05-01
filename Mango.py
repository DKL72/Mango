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
        self.running = False
        self.errors = []
        self.vars = {}

        for var in MngcoIO.read()[1]['@builtin']:
            self.vars[var.split(' = ')[0]] = eval(var.split(' = ')[1])

    def error(self, error: str, line: str, location: tuple[int, int]):
        message = f'!EXCEPTION [{datetime.now().strftime("%H:%M:%S")}] | Terminated Process - {self.name}\n\n{error} ERROR: "{line}" @ {location}\nSeverity: {self.dicts[error]}'
        self.errors.append(message)
        if self.dicts[error] == 'FULL-ERROR':
            quit()

    def run(self, interpreter: str = 'alpha'):
        removed = self.lists['@removed']
        self.vars['__prints'] = []

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

                for e, error in enumerate(self.errors):
                    self.vars['__prints'].insert(e, error)
                    print(self.vars['__prints'])
                self.vars['__prints'].append('*Finished')
            except Exception as e:
                self.errors.append(Error_Handling.sort(e, self.code, self.name))
