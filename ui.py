import customtkinter as tk
import tkinter.filedialog as fd

from extended_module import XMReader

class App(tk.CTk):
    filepath: str
    def __init__(self):
        super().__init__()

        self.title('Orion Tracker')
        self.geometry('300x200')
        # self.menu = tk.CTkOptionMenu(self)
        # self.menu_file = tk.CTkOptionMenu(self.menu)
        # self.menu_file.add_command(label='Open', command=self.openFile)
        # self.menu.add_cascade(menu=self.menu_file, label='File')
        self.filebutton = tk.CTkButton(self, text="Open file", command=self.openFile)
        self.entry = tk.CTkTextbox(self)
        self.filebutton.grid(row=0,column=0,padx=20,pady=20)
        self.entry.grid(row=1,column=0,padx=20,pady=20,sticky='ew', columnspan=2)
        # self['menu'] = self.menu

    def openFile(self):
        self.filepath = fd.askopenfilename(filetypes=[('Extended Module file','*.xm'), ('Impulse Tracker file', '*.it')])
        self.readfile = XMReader(self.filepath)
        self.readfile.load_file()
        self.entry.insert(tk.END, str(self.readfile.header))
        self.entry.update()
