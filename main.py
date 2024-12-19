import sys
from controller import Controller

if __name__ == "__main__":
    assert sys.version_info >= (3, 12) # see bug bpo-45155
    c = Controller()
    c.app.mainloop()
