import keyboard
import MngcoIO
from Functions import *


class Listener:
    def __init__(self):
        hotkeysLists = subset('@hotkeys', '@editor', MngcoIO.read()[0])
        self.hotkeys = {}
        for h, hotkey in enumerate(hotkeysLists[0]):
            self.hotkeys[hotkey] = hotkeysLists[1][h]

        self.actions = []
        for hotkey in self.hotkeys:
            keyboard.add_hotkey(hotkey, self.record, args=(self, self.hotkeys[hotkey]))

    def record(self, *args):
        self.actions.append(args[1])
