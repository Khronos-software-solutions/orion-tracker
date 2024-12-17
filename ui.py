from tkinter import Label, Menu, Tk, Button, Frame
import tkinter.filedialog as fd
from controller import Controller
from frame import ScrollableFrame

class TkTable(Frame):
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


class App(Tk):
    openedfile: str
    def __init__(self, controller: Controller):
        super().__init__()
        self.geometry('800x600')
        self.menu = Menu(self)
        filemenu = Menu(self.menu)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Quit', command=self.destroy)
        self.menu.add_cascade(label='File', menu=filemenu)
        
        self.main_table = Frame(self)
        
        self.config(menu=self.menu)
        self.button = Button(self, text='Play', command=self.play, anchor='w')
        self.button['width'] = 10
        self.button.grid(row=0, column=0, sticky='w')
        self.view = ScrollableFrame(self.main_table)
        self.table = TkTable(self.view.inner_frame)
        self.table.testgrid(100, 16)
        self.main_table.grid(row=1, column=0, sticky='nsew')
        self.table.grid(row=0, column=0, sticky='nsew')
        
    def open_file(self):
        self.openedfile = fd.askopenfilename(filetypes=[("Extended Module", "*.xm")])
        self.load()

    def load(self):
        print(f'loaded {self.openedfile}')
        pass

    def play(self):
        self.button['text'] = 'Stop'
        self.button['command'] = self.stop

    def stop(self):
        self.button['text'] = 'Play'
        self.button['command'] = self.play

if __name__ == "__main__":
    app = App()
    app.mainloop()
