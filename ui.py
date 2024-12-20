from tkinter import Entry, Label, Menu, Tk, Button, Frame, Canvas, Scrollbar
import tkinter.filedialog as fd
from tkinter.ttk import Notebook

from module_data import Note
from frame import ScrollableFrame

class Table(Frame):
    contents: list[list[Label]] = [[]]
    def __init__(self, master: Tk | Frame):
        Frame.__init__(self, master)       
    def testgrid(self, height: int, width: int):
        for i in range(0, height):
            self.contents.append([])
            for j in range(0, width):
                self.contents[i].append(Label(self, width=7, text=f'test {i} {j}', borderwidth=1, relief='sunken'))
                self.contents[i][j]['bg'] = '#eee'
                self.contents[i][j].grid(row=i, column=j)
    def set_contents(self, c: list[list[Note]]):
        self.contents = [[]]
        self.contents[0].append(Label(self, width=3, text=' ', borderwidth=1, relief='raised'))
        for i in range(len(c[0])):
            self.contents[0].append(Label(self, width=3, text=f'{str(i)}', borderwidth=1, relief='raised'))
            self.contents[0][i].grid(row=i, column=0)
        for i in range(1, len(c)):
            self.contents.append([])
            self.contents[i].append(Label(self, width=15, text=f'Channel {str(i)}', borderwidth=1, relief='raised'))
            self.contents[i][0].grid(row=0, column=i)
            for j in range(1, len(c[i])):
                self.contents[i].append(Label(self, width=15, text=f'{str(c[i-1][j-1])}', borderwidth=1, relief='sunken'))
                self.contents[i][j]['bg'] = '#eee'
                self.contents[i][j].configure(font=('Courier', 8))
                self.contents[i][j].grid(row=j, column=i)
        self.update()

class PatternSelector(Frame):
    indices: list[int] = []
    buttons: list[Button] = []
    def __init__(self, master: Tk | Frame, indices: list[int] = []):
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
        for i in range(len(self.indices)):
            index = i
            self.buttons.append(Button(self.inner_frame, text=str(self.indices[i]), width=4, relief='groove', command=lambda index=index: self.on_pattern_change(index)))
            self.buttons[index].grid(column=index, row=0, sticky='ew')
        self.on_pattern_change(0)
        self.update_canvas_height()

    def on_pattern_change(self, index: int):
        for i in self.buttons:
            i['relief'] = 'groove'
        self.buttons[index]['relief'] = 'sunken'
        self.load_pattern(self.indices[index])
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
        self.add_info('channel_number', 'Channels', 3)
        self.add_info('pattern_number', 'Patterns', 4)
        self.add_info('instrument_number', 'Instruments', 5)


class App(Tk):
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
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.config(menu=self.menu)

        self.main = Notebook(self)
        self.main.grid(row=0, column=0, sticky='nsew')

        self.info = InfoPanel(self)
        self.patterns = PatternEditor(self)

        self.main.add(self.info, text='Info')
        self.main.add(self.patterns, text='Patterns')

    def open_file(self):
        self.openedfile = fd.askopenfilename(filetypes=[("Extended Module", "*.xm")])
        self.load(self.openedfile)

    def load(self, filepath: str):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
