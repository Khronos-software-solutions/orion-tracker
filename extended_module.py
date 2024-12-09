from typing import Any

class XMReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header: dict[str, Any] = {}
        self.patterns: list[dict[str, Any]] = []
        self.samples: list[dict[str, Any]] = []

    def load_file(self):
        self.read_header(self.file_path)

    def read_header(self, file: str):
        with open(file, 'rb') as f:
            id_text = f.read(17).decode('ascii')
            name = f.read(20).decode('ascii').strip()
            null_terminator = f.read(1)
            tracker_name = f.read(20).decode('ascii').strip()
            version = "v" + '.'.join(map(str, list(f.read(2))[::-1]))
            header_size = int.from_bytes(f.read(4).strip(b'\x00'))
            song_length = f.read(2)
            song_restart = f.read(2)
            channel_number = int.from_bytes(f.read(2).strip(b'\x00'))
            pattern_number = int.from_bytes(f.read(2).strip(b'\x00'))
            instrument_number = int.from_bytes(f.read(2).strip(b'\x00'))
            self.header.update({
                'id_text': id_text,
                'name': name,
                'null_terminator': null_terminator,
                'tracker_name': tracker_name,
                'version': version,
                'header_size': header_size,
                'song_length': song_length,
                'song_restart': song_restart,
                'channel_number': channel_number,
                'pattern_number': pattern_number,
                'instrument_number': instrument_number
            })
        print(self.header)