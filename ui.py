from tkinter import Canvas, Label, Menu, Tk, Button, Frame, Scrollbar
import tkinter.filedialog as fd

class ScrollableFrame(Frame):
    def __init__(self, master: Tk):
        super().__init__(master)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        def _on_scroll(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        canvas.bind_all("<MouseWheel>", _on_scroll)


class TkTable(Frame):
    contents: list[list[Label]] = [[]]
    def __init__(self, master: Tk | Frame, height: int, width: int):
        Frame.__init__(self, master, height=height, width=width)
        
    def testgrid(self, height: int, width: int):
        for i in range(0, height):
            self.contents.append([])
            for j in range(0, width):
                self.contents[i].append(Label(self, width=7, text=f'test {i} {j}', borderwidth=1, relief='sunken'))
                self.contents[i][j]['bg'] = '#eee'
                
                self.contents[i][j].grid(row=i, column=j)


class App(Tk):
    openedfile: str
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.menu = Menu(self)
        filemenu = Menu(self.menu)
        
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Quit', command=self.destroy)
        self.menu.add_cascade(label='File', menu=filemenu)
        self.config(menu=self.menu)
        self.button = Button(self, text='Play', command=self.play, anchor='w')
        self.button['width'] = 10
        self.button.grid(row=0, column=0, sticky='w')
        self.view = ScrollableFrame(self)
        self.table = TkTable(self.view.scrollable_frame, height=100, width=10)
        self.table.testgrid(100, 10)
        self.table.grid(row=0, column=0, sticky='nsew')
        self.view.grid(row=1, column=0, sticky='nsew')
        
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
