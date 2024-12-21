from extended_module import XMReader
from module_data import Pattern
from player import save_samples

class Module:
    reader: XMReader = XMReader()
    patterns: list[Pattern]
    def __init__(self):
        pass
    def load_file(self, filename: str):
        self.reader.file_path = filename
        self.reader.load_file()
        self.patterns = []
        for i in self.reader.patterns:
            p = Pattern(self.reader.header['channel_number'], i['row_number'])
            p.from_byte_pattern(i['data'])
            self.patterns.append(p)
        save_samples(self.reader)

