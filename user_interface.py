import os
from tkinter import Entry, Label, Menu, Tk, Button, Frame, Canvas, Scrollbar, Toplevel
import tkinter.filedialog as fd
from tkinter.ttk import Notebook

from player import play_sample

from table import Table
from waveform import WaveformDisplay
from frame import ScrollableFrame
from selector_box import SelectorBox


class PatternSelector(Frame):
    indices: list[int] = []
    buttons: list[Button] = []

    def __init__(self, master: Tk | Frame, indices: list[int]):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.indices = indices
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.inner_frame = Frame(self.canvas)
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='ew')
        self.scrollbar.grid(row=1, column=0, sticky='ew')
        self.update_buttons()

    def update_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for i in enumerate(self.indices):
            index = i[0]
            self.buttons.append(Button(self.inner_frame, text=str(self.indices[index]), width=4, relief='groove', command=lambda index=index: self.on_pattern_change(index)))
            self.buttons[index].grid(column=index, row=0, sticky='ew')

        self.on_pattern_change(0)
        self.update_canvas_height()

    def on_pattern_change(self, index: int):
        for i in self.buttons:
            i['relief'] = 'groove'
        self.buttons[index]['relief'] = 'sunken'
        self.load_pattern(index)
        self.update()

    def load_pattern(self, index: int):
        pass

    def update_canvas_height(self):
        self.update_idletasks()
        self.canvas.config(height=self.inner_frame.winfo_height(), width=self.winfo_reqwidth())

class PatternEditor(Frame):
    def __init__(self, master: Tk | Frame):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pattern_selector = PatternSelector(self, [0])
        self.pattern_selector['bd'] = 1
        self.pattern_selector['relief'] = 'sunken'
        self.pattern_selector['padx'] = 2
        self.pattern_selector['pady'] = 2
        self.pattern_selector.grid(row=0, column=0, sticky='ew')

        self.main_table = Frame(self)
        self.main_table.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.view = ScrollableFrame(self.main_table)
        self.table = Table(self.view.inner_frame)
        self.table.grid(row=0, column=0, sticky='nsew')

class InfoPanel(Frame):
    module_info: dict[str, str] = {}
    def __init__(self, master: Tk | Frame):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.info = Label(self, text='Information')
        self.info.grid(row=0, column=0, sticky='w')       
        self.headerinfo = Frame(self, relief='sunken', bd=1)
        self.headerinfo.grid(row=1, column=0, sticky='nsew')

    def add_info(self, key: str, name: str, row: int = 0):
        if self.module_info[key]:
            label = Label(self.headerinfo, text=f'{name}: ')
            label.grid(row=row, column=0, sticky='w')
            entry = Entry(self.headerinfo)
            entry.insert(0, self.module_info[key])
            entry['state'] = 'readonly'
            entry.grid(row=row, column=1)

    def update_info(self):
        self.add_info('name', 'Name', 0)
        self.add_info('tracker_name', 'Tracker', 1)
        self.add_info('version', 'Version', 2)
        self.add_info('song_length', 'Song Length', 3)
        self.add_info('song_restart', 'Restart Position', 4)
        self.add_info('channel_number', 'Channels', 5)
        self.add_info('pattern_number', 'Patterns', 6)
        self.add_info('instrument_number', 'Instruments', 7)
        self.add_info('tempo', 'Tempo', 8)
        self.add_info('bpm', 'BPM', 9)

class SamplePanel(Frame):
    samplepaths: list[str] = []
    def __init__(self, master: Tk | Frame):
        super(SamplePanel, self).__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.playbutton = Button(self, text='Play', command=self.play_sample)
        self.playbutton.grid(row=0, column=1, sticky='w')
        self.selector = SelectorBox(self, 0, self.update_graph)
        self.graph = WaveformDisplay(self)
        self.graph['bd'] = 1
        self.graph['relief'] = 'sunken'
        self.selector.grid(row=0, column=0, sticky='w')
        self.graph.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def load_samples(self, filepath: str):
        if not os.path.exists(filepath) or not os.path.isdir(filepath):
            return
        self.samplepaths = [os.path.join(filepath, i) for i in os.listdir(filepath) if i.endswith('.wav')]
        self.selector.options = len(self.samplepaths)
        self.selector.selected = 0
        self.selector.entry.delete(0, 'end')
        self.selector.entry.insert(0, '0')
        self.selector.update()
        self.update_graph()

    def update_graph(self):
        self.graph.load_waveform(self.samplepaths[self.selector.selected])

    def play_sample(self):
        play_sample(self.samplepaths[self.selector.selected]) if self.samplepaths else None



class App(Tk):
    openedfile: str
    def __init__(self):
        super().__init__()
        self.title('XM Module Viewer')
        self.geometry('800x600')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.menu = Menu(self, tearoff=0)
        self.filemenu = Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label='Open', command=self.open_file)
        self.filemenu.add_command(label='Quit', command=self.destroy)
        self.helpmenu = Menu(self.menu, tearoff=0)
        self.helpmenu.add_command(label='About', command=self.about)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.config(menu=self.menu)

        self.main = Notebook(self)
        self.main.grid(row=0, column=0, sticky='nsew')

        self.info = InfoPanel(self)
        self.patterns = PatternEditor(self)
        self.samples = SamplePanel(self)

        self.main.add(self.info, text='Info')
        self.main.add(self.patterns, text='Patterns')
        self.main.add(self.samples, text='Samples')

    def about(self):
        t = Toplevel(self)
        t.title('About')
        t.geometry('175x155')
        t.columnconfigure(0, weight=1)
        f = Frame(t)
        f['relief'] = 'groove'
        f['bd'] = 2
        Label(f, text='Orion Tracker').grid(row=0, column=0, sticky='w')
        Label(f, text='Version 0.1').grid(row=1, column=0, sticky='w')
        Label(f, text='Authors: ').grid(row=2, column=0, sticky='w')
        Label(f, text='  - Ties Heijnis').grid(row=3, column=0, sticky='w')
        Label(f, text='  - Luuk Kalkman').grid(row=4, column=0, sticky='w')
        f.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        Button(t, text='Close', command=t.destroy).grid(row=1, column=0)
        t.mainloop()

    def open_file(self):
        self.openedfile = fd.askopenfilename(filetypes=[("Extended Module", "*.xm")])
        self.load(self.openedfile)

    def load(self, filepath: str):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
