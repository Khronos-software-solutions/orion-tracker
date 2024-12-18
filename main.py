import sys

import extended_module
from controller import Controller

reader = extended_module.XMReader('./amblight.xm')
reader.load_file()

if __name__ == "__main__":
    assert sys.version_info >= (3, 12) # see bug bpo-45155
    c = Controller()