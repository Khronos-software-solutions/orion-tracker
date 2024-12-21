from typing import Callable
from tkinter import Frame, Tk, Button, Entry

class SelectorBox(Frame):
    selected: int = 0
    options: int = 1
    def __init__(self, master: Tk | Frame, options: int, on_change: Callable[[], None] | None = None):
        super().__init__(master)
        self.on_change = on_change
        self.options = options
        self.columnconfigure(0, weight=1)
        self.entry = Entry(self)
        self.entry.grid(row=0, column=2, sticky='ew')
        self.up_button = Button(self, text='↑', command=self.up)
        self.up_button.grid(row=0, column=0, sticky='ew')
        self.down_button = Button(self, text='↓', command=self.down)
        self.down_button.grid(row=0, column=1, sticky='ew')

    def up(self):
        self.selected += 1
        if self.selected >= self.options:
            self.selected = 0
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(self.selected))
        if self.on_change:
            self.on_change()

    def down(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = self.options - 1
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(self.selected))
        if self.on_change:
            self.on_change()

if __name__ == "__main__":
    root = Tk()
    app = SelectorBox(root, 10)
    app.grid(row=0, column=0, sticky='nsew')
    root.mainloop()
