import sys

import extended_module
from module_data import Pattern
from ui import App

reader = extended_module.XMReader('./amblight.xm')
reader.load_file()

if __name__ == "__main__":
    assert sys.version_info >= (3, 12) # see bug bpo-45155

    rows = reader.patterns[6]['row_number']
    channels = reader.header['channel_number']
    pattern = Pattern(channels, rows)
    pattern.from_byte_pattern(reader.patterns[6]['data'])
