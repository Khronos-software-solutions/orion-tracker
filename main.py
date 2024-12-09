import extended_module
from ui import App

reader = extended_module.XMReader('./amblight.xm')
reader.load_file()

if __name__ == "__main__":
    root = App()
    root.mainloop()