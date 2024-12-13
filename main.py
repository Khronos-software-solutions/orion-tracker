import extended_module
from module import Pattern
from ui import App

reader = extended_module.XMReader('./amblight.xm')
reader.load_file()

if __name__ == "__main__":
    rows = reader.patterns[9]['row_number']
    channels = reader.header['channel_number']
    pattern = Pattern(channels, rows)
    pattern.from_byte_pattern(reader.patterns[9]['data'])