from tkinter import Label, Menu, Tk, Button, Frame, Scale
import tkinter.filedialog as fd

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
        for i in range(0, len(c)):
            self.contents.append([])
            for j in range(0, len(c[i])):
                self.contents[i].append(Label(self, width=7, text=f'{str(c[i][j])}', borderwidth=1, relief='sunken'))
                self.contents[i][j]['bg'] = '#eee'
                self.contents[i][j].grid(row=j, column=i)
        self.update()

class PatternSelector(Frame):
    indices: list[int] = []
    buttons: list[Button] = []
    def __init__(self, master: Tk | Frame, indices: list[int] = []):
        super().__init__(master)
        self.indices = indices
        self.update_buttons()

    def update_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for i in range(len(self.indices)):
            index = i
            self.buttons.append(Button(self, text=str(self.indices[i]), width=4, relief='groove', command=lambda index=index: self.on_pattern_change(index)))
            self.buttons[index].grid(column=index, row=0, sticky='ew')
        self.on_pattern_change(0)

    def on_pattern_change(self, index: int):
        for i in self.buttons:
            i['relief'] = 'groove'
        self.buttons[index]['relief'] = 'sunken'
        self.load_pattern(self.indices[index])
        self.update()
    
    def load_pattern(self, index: int):
        pass

class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.menu = Menu(self, tearoff=0)
        self.filemenu = Menu(self.menu)
        self.filemenu.add_command(label='Open', command=self.open_file)
        self.filemenu.add_command(label='Quit', command=self.destroy)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.config(menu=self.menu)
        
        self.pattern_selector = PatternSelector(self, [0])
        self.pattern_selector['bd'] = 1
        self.pattern_selector['relief'] = 'sunken'
        self.pattern_selector['padx'] = 2
        self.pattern_selector['pady'] = 2
        self.pattern_selector.grid(row=1, column=0, sticky='ew')

        self.main_table = Frame(self)
        self.main_table.grid(row=2, column=0, columnspan=2, sticky='nsew')
        
        self.view = ScrollableFrame(self.main_table)
        self.table = Table(self.view.inner_frame)
        self.table.grid(row=0, column=0, sticky='nsew')
        
        # volume_frame = Frame(self)
        # volume_frame.grid(row=0, column=1, sticky='ew')
        # self.volume_label = Label(volume_frame, text='Volume')
        # self.volume_label.pack(side='left')
        # self.volume_slider = Scale(volume_frame, from_=0, to_=100, orient='horizontal')
        # self.volume_slider.set(50)
        # self.volume_slider.pack(side='left', fill='x', expand=True)
    
    def open_file(self):
        self.openedfile = fd.askopenfilename(filetypes=[("Extended Module", "*.xm")])
        self.load(self.openedfile)

    def load(self, filepath: str):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()