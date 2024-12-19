from module_data import Note
from ui import App
from module_model import Module

class Controller:
    filepath: str
    patterns: list[list[list[Note]]] = []
    def __init__(self):
        self.app = App()
        self.module = Module()

        def on_load(filepath: str):
            self.module.load_file(filepath)
            index = 0
            for i in self.module.patterns:
                self.patterns.append([])
                for key in i.pattern:
                    self.patterns[index].append(i.pattern[key])
                index += 1
            self.app.pattern_selector.indices = self.module.reader.pattern_order
            self.app.pattern_selector.update_buttons()
            self.app.view.update_scrollregion()
            self.app.update()

        self.app.load = on_load

        def load_pattern(index: int):
            currentindex = self.app.pattern_selector.indices[index]
            self.app.table.set_contents(self.patterns[currentindex])
            self.app.view.update_scrollregion()

        self.app.pattern_selector.load_pattern = load_pattern
