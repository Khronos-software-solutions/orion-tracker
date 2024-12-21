from tkinter import Frame, Label, Tk

from module_data import Note

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