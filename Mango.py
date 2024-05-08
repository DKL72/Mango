import queue
import ErrorHandling
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
        self.dicts, self.lists = MngcoIO.read2()
        self.assembled = ''
        self.running = False
        self.errors = []
        self.vars = MngcoIO.read2()[0]['@builtin']

    def refresh(self):
        self.dicts, self.lists = MngcoIO.read2()
        self.assembled = ''
        self.running = False
        self.errors = []
        self.vars = MngcoIO.read2()[0]['@builtin']

    def error(self, error: str, line: str, location: tuple[int, int]):
        message = f'!EXCEPTION [{datetime.now().strftime("%H:%M:%S")}] | Terminated Process - {self.name}\n\n{error} ERROR: "{line}" @ {location}\nSeverity: {self.dicts[error]}'
        self.errors.append(message)
        if self.dicts[error] == 'FULL-ERROR':
            quit()

    def run(self, interpreter: str = 'alpha'):
        removed = self.lists['@removed']
        self.vars['__prints'] = []
        self.vars['__inputs'] = []

        if interpreter == 'alpha':
            for rem in removed:
                for l, line in enumerate(self.code.splitlines()):
                    if rem in line:
                        self.error('SYNTAX', line, (l, line.find(rem)))
                    elif line != '' and line[-1] not in [':', ';']:
                        self.error('ENDING', line, (l, len(line)))

            replacements = self.dicts['@interpreter']

            self.assembled = self.code
            for r, repl in enumerate(replacements):
                while repl in self.assembled and StrCo.isValid(self.assembled.find(repl), self.assembled):
                    self.assembled = self.assembled.replace(repl, replacements[repl], 1)

            for var in self.vars:
                self.assembled = f'{var} = {self.vars[var]};\n{self.assembled}'

            try:
                # exec(compile(self.assembled, '', 'exec'), globals(), self.vars)
                exec(self.assembled, globals(), self.vars)

                self.vars['__prints'].extend(self.errors)
                self.vars['__prints'].append('*Finished')

            except Exception as e:
                self.errors.append(ErrorHandling.sort(e, self.code, self.name))
