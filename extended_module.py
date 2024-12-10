from io import BufferedReader
from struct import unpack
from typing import Any

class XMReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header: dict[str, Any] = {}
        self.patterns: list[dict[str, Any]] = []
        self.pattern_order: list[int] = []
        self.instruments: list[dict[str, Any]] = []

    def load_file(self):
        with open(self.file_path, 'rb') as f:
            self.read_header(f)
            self.read_patterns(f)

    def read_header(self, f: BufferedReader):
        id_text = unpack('<17s', f.read(17))[0].decode('ascii')
        name = f.read(20).decode('ascii').strip()
        null_terminator = f.read(1)
        tracker_name = f.read(20).decode('ascii').strip()
        version = "v" + '.'.join(map(str, list(f.read(2))[::-1]))
        header_size = unpack('<I',f.read(4))[0]
        song_length = unpack('<H', f.read(2))[0]
        song_restart = unpack('<H', f.read(2))[0]
        channel_number = unpack('<H', f.read(2))[0]
        pattern_number = unpack('<H', f.read(2))[0]
        instrument_number = unpack('<H', f.read(2))[0]
        flags = f.read(2)
        default_tempo = unpack('<H', f.read(2))[0]
        default_bpm = unpack('<H', f.read(2))[0]
        pattern_table = f.read(header_size - 20).strip(b'\x00')
        self.pattern_order = [int.from_bytes(pattern_table[i:i+1]) for i in range(0, len(pattern_table))]
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
            'instrument_number': instrument_number,
            'flags': flags,
            'tempo': default_tempo,
            'bpm': default_bpm
        })
        print(self.header)
    
    def read_patterns(self, f: BufferedReader):
        for i in range(self.header['pattern_number']):
            _pattern_header_size = unpack('<I', f.read(4))[0] # Normally \x09
            packing_type = f.read(1) # Should be \x00
            row_number = unpack('<H', f.read(2))[0]
            print(row_number)
            data_size = unpack('<H', f.read(2))[0]
            print(f'size : {data_size}')
            pattern_data = f.read(data_size)
            self.patterns.append({
                'index': i,
                'packing_type': packing_type,
                'row_number': row_number,
                'data': pattern_data
            })
    
    def read_instruments(self, f: BufferedReader):
        for _ in range(self.header['instrument_number']):
            instr_size = unpack('<I', f.read(4))[0]
            instr_name = unpack('<22s', f.read(22))[0]
            instr_type = f.read(1) # Almost always \x00, doesn't mean anything
            num_samples = unpack('<H', f.read(2))[0]
            if num_samples > 0:
                sample_header_size = unpack('<I', f.read(4))[0]
                
            


if __name__ == "__main__":
    xm = XMReader('./amb-nrg.xm')
    
    xm.load_file()