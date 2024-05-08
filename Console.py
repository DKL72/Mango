import os
import sys
import time
import tkinter as tk

import keyboard

import Mango
from tkinter import scrolledtext, filedialog
from colorama import init, Fore
from datetime import datetime

window = None
text = None
running = False


def get(program: Mango.Script):
    global window, text, running

    running = True

    if window is None:
        window = tk.Tk()

    if text is None:
        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=140, height=47, background='lightgrey')
        text.pack()

    window.configure(background='black')
    window.iconbitmap('C:\\Users\\nekta\\OneDrive\\Pictures\\Saved Pictures\\mngImage.ico')
    window.title('Mango Console')
    window.geometry('800x600')

    window.update()

    def onClose():
        global window, text
        window.destroy()
        window = None
        text = None

    window.protocol("WM_DELETE_WINDOW", onClose)

    messages = program.vars['__prints']

    if text is None:
        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=140, height=47, background='lightgrey')
        text.pack()

    text.config(state='normal')

    text.delete('1.0', tk.END)

    for message in messages:
        message = str(message)
        print(message)

        text.insert(tk.END, message + ('\n' if message != '>>' else ''), 'Error' if message.strip()[0:10] == '!EXCEPTION' else ('Info' if message.strip()[0] == '*' else 'Message'))
        text.see('end')

        text.tag_config('Error', foreground='darkred')
        text.tag_config('Info', foreground='green')

        window.update()

        if message == '*Finished' or message.strip()[0:10] == '!EXCEPTION':
            break
        elif message == '>>':
            while not keyboard.is_pressed('enter'):
                window.update()

            text.config(state='disabled')
            messages.remove(message)
            return text.get('1.0', tk.END).split('>>')[-1].strip()

    text.config(state='disabled')

    window.update()
