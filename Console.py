import os
import sys
import tkinter as tk
from tkinter import scrolledtext, filedialog
from colorama import init, Fore
from datetime import datetime

window = None
text = None


def main(messages: list[str]):
    global window, text

    if window is not None:
        window.lift()
    else:
        window = tk.Tk()
        window.configure(background='black')
        window.iconbitmap('C:\\Users\\nekta\\OneDrive\\Pictures\\Saved Pictures\\mngImage.ico')
        window.title('Mango Console')
        window.geometry('800x600')

        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=140, height=47, background='lightgrey')
        text.pack()
    # text.delete('1.0', tk.END)

    messages.insert(0, f'*Script started [{datetime.now().strftime("%H:%M:%S")}]\n')
    # messages.append(f'\n*Script finished [{datetime.now().strftime("%H:%M:%S")}]')

    text.config(state='normal')
    for message in messages:
        text.insert(tk.END, message, 'Error' if message.strip()[0:10] == '!EXCEPTION' else ('Info' if message.strip()[0:7] == '*Script' else 'Message'))

        text.tag_config('Error', foreground='darkred')
        text.tag_config('Info', foreground='green')

    text.config(state='disabled')

    def onClose():
        global window
        window.destroy()
        window = None

    window.protocol("WM_DELETE_WINDOW", onClose)

    window.update()
