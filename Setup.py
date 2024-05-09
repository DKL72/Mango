import sys
import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime

import Editor


def log(text: str):
    current = datetime.datetime.now()
    console.insert(tk.END, f'{current.hour}:{current.minute}:{current.second} | {text}\n')


window = tk.Tk()
window.overrideredirect(True)
window.configure(background='#3b3a3a')
window.iconbitmap('C:\\Users\\nekta\\OneDrive\\Pictures\\Saved Pictures\\mngImage.ico')
window.title('Mango Project Setup')
window.geometry('900x500+500+300')

console = tk.scrolledtext.ScrolledText(window, width=100, height=40, background='#525252', foreground='white')
console.pack(padx=20, pady=40)

if len(sys.argv) > 1:
    path = sys.argv[1]
    folder = path[:path.rfind('\\')]
    requirements = ['mngco-path', 'main-file']
    defaults = ['mango-constants.mngco', 'Main.mng']

    satisfied = [False for _ in range(len(requirements))]

    if os.path.exists(f'{folder}\\settings.txt'):
        log('settings.txt found - checking current settings')
        with open(f'{folder}\\settings.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.split(' : ')[0] in requirements:
                satisfied[requirements.index(line.split(' : ')[0])] = True

    else:
        log('settings.txt not found')
        with open(f'{folder}\\settings.txt', 'w') as file:
            log('settings.txt created')

    for c, check in enumerate(satisfied):
        if not check:
            log(f'settings.txt missing "{requirements[c]}"')
            log(f'Generating default "{requirements[c]}" setting')
            with open(f'{folder}\\settings.txt', 'a') as file:
                file.write(f'{requirements[c]} : {defaults[c]}\n')
    log('settings.txt check complete')

    window.update()
    time.sleep(2)

    window.destroy()
    Editor.main(folder)
