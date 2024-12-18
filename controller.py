from ui import App
from module_model import Module

class Controller:
    filepath: str

    def __init__(self):
        self.app = App(self)
        self.module = Module()
