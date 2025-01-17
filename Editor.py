import os
import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, filedialog
from types import *
import Console
import Hotkeys
import Mango
import MngcoIO
from Functions import *

program = Mango.Script()
listener = Hotkeys.Listener()


def refresh():
    global splits, old
    program.refresh()
    old = ''
    splits = MngcoIO.read2()[1]['@splits']


def run():
    refresh()

    program.code = text.get('1.0', tk.END)

    runtime = threading.Thread(target=program.run)
    runtime.start()

    while runtime.is_alive():
        cycle = str(Console.get(program))
        if cycle not in [None, 'None', '']:
            program.vars['__inputs'].append(cycle)

    cycle = Console.get(program)
    if cycle not in [None, 'None', '']:
        program.vars['__inputs'].append(cycle)


def delete():
    confirmation = tk.Tk()
    confirmation.title('Delete')
    confirmation.geometry('200x80')
    bottomRow = tk.Frame(confirmation)
    bottomRow.pack(side='bottom')

    cancel = tk.Button(bottomRow, text='Cancel', background='#A5E3F8', command=confirmation.destroy, font=('Arial', 12)
                       , width=6)
    delete = tk.Button(bottomRow, text='Delete', command=lambda: (os.remove(path), confirmation.destroy(), window.destroy()),
                       font=('Arial', 12), width=6)
    text = tk.Label(confirmation, font=('Arial', 16), text='Delete file?')
    text.pack(anchor='center')

    delete.pack(side='left', padx=4, pady=5)
    cancel.pack(side='left', padx=4, pady=5)

    confirmation.mainloop()
    # tk
    # os.remove(path)
    # window.destroy()


def config():
    os.startfile('C:\\Users\\nekta\\PycharmProjects\\Mango\\Project\\mango-constants.mngco')


def openMng():
    openFile = filedialog.askopenfilename(filetypes=[("Mango Files", "*.mng")])
    if openFile != '':
        os.startfile(openFile)


def save():
    if path != 'Null':
        with open(path, 'w') as file:
            file.write(text.get('1.0', 'end-1c'))

    program.code = text.get('1.0', 'end-1c')


def saveAs():
    fileSelected = filedialog.asksaveasfilename(defaultextension='.mng', filetypes=[('Mango Files', '*.mng')])
    if fileSelected != '':
        with open(fileSelected, 'w'):
            pass


def new():
    newFile = filedialog.asksaveasfilename(defaultextension=".mng", filetypes=[('Mango Files', '*.mng')])
    with open(newFile, 'w'):
        pass
    os.startfile(newFile)


def selectFile(*args):
    global path
    selPath = path.split('\\')[:-1]
    selPath.append(files.get(files.curselection()[0]))
    selPath = '\\'.join(selPath)
    path = selPath

    with open(selPath, 'r') as file:
        data = file.read()

    text.delete('1.0', tk.END)
    text.insert(tk.END, data)
    refresh()
    window.title('Mango Editor: ' + files.get(files.curselection()[0]))


if len(sys.argv) > 1:
    path = sys.argv[1]
    with open(path, 'r') as file:
        contents = file.read()
else:
    path = 'C:\\Users\\nekta\\PycharmProjects\\Mango\\Project\\Main.mng'

    with open(path, 'r') as file:
        contents = file.read()


def enter(event):
    event.widget.config(background='lightgrey')


def leave(event):
    event.widget.config(background='#B9B9B9')


settingsList = subset('@editor', '@builtin', MngcoIO.read()[0])
settings = {}
for s, setting in enumerate(settingsList[0]):
    settings[setting] = settingsList[1][s]

window = tk.Tk()
window.configure(background='#3b3a3a')
window.iconbitmap('C:\\Users\\nekta\\OneDrive\\Pictures\\Saved Pictures\\mngImage.ico')
window.title('Mango Editor: ' + path.split("\\")[-1])

window.geometry('1800x900')
buttons = ['Open', 'Save', 'Save As...', 'Run', 'Reload', 'New', 'Config', 'Delete', 'Quit']
# Create refresh button and put function program.refresh and remove some blank spaces
bFunctions = [openMng, save, saveAs, run, refresh, new, config, delete, window.destroy]

for i in range(53):
    buttons.append('')
    bFunctions.append('')

buttons.reverse()
bFunctions.reverse()

buttonObjects = []
topFrame = tk.Frame(window, width=1800, highlightbackground='black', highlightthickness=2)
topFrame.pack(side='top')

sidebar = tk.Frame(window, background='#3b3a3a', padx=10, pady=10, height=300, highlightbackground='black', highlightthickness=2)
sidebar.pack(side='left')

filesScroll = tk.Scrollbar(sidebar)
files = tk.Listbox(sidebar, background='#878a89', width=30, height=15, font=eval(settings['scriptFont']), bd=3)
files.config(yscrollcommand=filesScroll.set)
files.bind('<Double-1>', selectFile)

variablesScroll = tk.Scrollbar(sidebar)
variablesList = tk.Listbox(sidebar, background='#878a89', width=30, height=15, font=eval(settings['scriptFont']), bd=3)
variablesList.config(yscrollcommand=filesScroll.set)
variablesList.pack()

for file in os.scandir(path[:path.rfind('\\') + 1]):
    if file.name.split('.')[-1] in ['mng', 'txt']:
        files.insert('end', file.name)

files.pack()

for b, button in enumerate(buttons):
    if button != '':
        buttonObjects.append(tk.Button(topFrame, command=bFunctions[b], text=button, width=8, font=('Arial', 10), background='#B9B9B9', borderwidth=0))
        buttonObjects[b].bind('<Enter>', enter)
        buttonObjects[b].bind('<Leave>', leave)
    else:
        buttonObjects.append(tk.Button(topFrame, command=bFunctions[b], text=button, width=2, state='disabled', font=('Arial', 10), background='#B9B9B9', borderwidth=0))

    buttonObjects[b].pack(side='right')

text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=165, height=47, background='#525252', font=eval(settings['scriptFont']), foreground='white')
text.pack(side='left', padx=20)
text.insert(tk.END, contents)

variables = {}
old = ''

splits = MngcoIO.read2()[1]['@splits']

while True:
    window.update()
    for action in listener.actions:
        exec(f'{action}()')
    listener.actions = []

    variables = program.vars
    try:
        variablesList.delete(0, tk.END)
    except:
        sys.exit()

    for var in variables:
        if var[0:2] != '__' and type(variables[var]) in [str, int, float, list, tuple, bool, bytes, complex, dict, complex, map]:
            variablesList.insert('end', f'{var} : {str(variables[var])}')

    code = text.get('1.0', tk.END)

    highlights = {}

    if code != old:
        for tag in text.tag_names():
            text.tag_delete(tag)

        for l, line in enumerate(code.split('\n')):
            if len(line) > 0 and line[0] == '#':
                text.tag_config('comment', foreground='#a4cc9b')
                text.tag_add('comment', f'{l + 1}.0', f'{l + 1}.{line.find(";")}')

            for word in MngcoIO.read2()[0]['@highlighting']:
                start = 0

                while word in line[start:]:
                    location = line[start:].find(word)

                    text.tag_config(word, foreground=MngcoIO.read2()[0]['@highlighting'][word])

                    try:
                        valid = (line[location + start - 1] in splits or location + start == 0,
                                 line[location + start + len(word)] in splits or location + start + len(word) == 0)
                    except IndexError:
                        valid = [False, False]

                    if location != -1 and valid[0] and valid[1]:
                        text.tag_add(word, f'{l + 1}.{location + start}', f'{l + 1}.{location + start + len(word)}')

                    start = start + len(word)

    old = text.get('1.0', tk.END)
