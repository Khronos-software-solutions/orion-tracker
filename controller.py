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
            self.app.patterns.pattern_selector.indices = self.module.reader.pattern_order
            self.app.patterns.pattern_selector.update_buttons()
            self.app.patterns.view.update_scrollregion()
            self.app.info.module_info = self.module.reader.header
            self.app.info.update_info()
            self.app.update()

        self.app.load = on_load

        def load_pattern(index: int):
            print(index)
            print(len(self.app.patterns.pattern_selector.indices))
            currentindex = self.app.patterns.pattern_selector.indices[index]
            self.app.patterns.table.set_contents(self.patterns[currentindex])
            self.app.patterns.view.update_scrollregion()
        
        

        self.app.patterns.pattern_selector.load_pattern = load_pattern
