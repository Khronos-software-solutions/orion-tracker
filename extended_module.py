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
            self.read_instruments(f)

    def read_header(self, f: BufferedReader):
        id_text = f.read(17).decode('ascii') # Should be "Extended Module: "
        module_name = f.read(20).decode('ascii').strip()
        null_terminator = f.read(1) # Always \x1a. Not used anywhere else.
        tracker_name = f.read(20).decode('ascii').strip() # Name of the tracker used to create the module
                                                          # .XM files were introduced with FastTracker v2.00

        version = "v" + '.'.join(map(str, list(f.read(2))[::-1])) # Almost always v1.4

        header_size = unpack('<I',f.read(4))[0] # The length of the header in bytes. The remaining part is padded with zeroes.
        song_length = unpack('<H', f.read(2))[0] # The amount of patterns in this file.
        song_restart = unpack('<H', f.read(2))[0] # The pattern to go to when reaching the end

        channel_number = unpack('<H', f.read(2))[0] # 
        pattern_number = unpack('<H', f.read(2))[0] # The number of patterns. Though not the amount of patterns used in sequence.
        instrument_number = unpack('<H', f.read(2))[0] # Amount of instruments, may contain empty or unused instruments.

        flags = f.read(2)
        default_tempo = unpack('<H', f.read(2))[0] # Starting tempo in rows per beat  
        default_bpm = unpack('<H', f.read(2))[0] # Starting beats per minute
        pattern_table = f.read(header_size - 20).strip(b'\x00') # Pattern order by index
        self.pattern_order = [int.from_bytes(pattern_table[i:i+1]) for i in range(0, len(pattern_table))]

        self.header.update({
            'id_text': id_text,
            'name': module_name,
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
    
    def read_patterns(self, f: BufferedReader):
        for i in range(self.header['pattern_number']):
            pattern_header_size = unpack('<I', f.read(4))[0] # Normally \x09, which is the minimum
            packing_type = f.read(1) # Should be \x00, unused
            row_number = unpack('<H', f.read(2))[0]
            data_size = unpack('<H', f.read(2))[0]

            if pattern_header_size > 9:
                f.read(pattern_header_size - 9) # We only read the data because we need to skip it

            pattern_data = f.read(data_size)

            self.patterns.append({
                'index': i,
                'packing_type': packing_type,
                'row_number': row_number,
                'data': pattern_data
            })
    
    def read_instruments(self, f: BufferedReader):
        for i in range(self.header['instrument_number']):
            instr_size = unpack('<I', f.read(4))[0]
            instr_name = unpack('<22s', f.read(22))[0].decode('CP437') # Decode using cp437 for regional text compatibility 
            instr_type = f.read(1) # Almost always \x00, doesn't mean anything
            num_samples = unpack('<H', f.read(2))[0]
            samples: list[dict[str, int | bytes | bool]] = []
            sample_header: list[dict[str, int | bytes]] = []

            if num_samples != 0:
                # Samples are stored like this:
                #    Sample 1 header
                #    ...
                #    Sample n header
                #    end of headers
                #    Sample 1 data
                #    ...
                #    Sample n data
                #    end of file
                
                for j in range(num_samples):
                    sample_header_size = unpack('<I', f.read(4))[0]
                    keymap = f.read(96) # Describes which keys trigger which sample. 
                                        # Most people do not use this feature, instead using different instruments.
                    volume_envelope = f.read(48)
                    panning_envelope = f.read(48)
                    num_volume_points = unpack('<B', f.read(1))[0]
                    num_panning_points = unpack('<B', f.read(1))[0]
                    volume_sus_point = unpack('<B', f.read(1))[0]
                    volume_loop_start = unpack('<B', f.read(1))[0]
                    volume_loop_end = unpack('<B', f.read(1))[0]
                    panning_sus_point = unpack('<B', f.read(1))[0]
                    panning_loop_start = unpack('<B', f.read(1))[0]
                    panning_loop_end = unpack('<B', f.read(1))[0]
                    volume_type = unpack('<B', f.read(1))[0]
                    panning_type = unpack('<B', f.read(1))[0]
                    vibrato_type = unpack('<B', f.read(1))[0]
                    vibrato_sweep = unpack('<B', f.read(1))[0]
                    vibrato_depth = unpack('<B', f.read(1))[0]
                    vibrato_rate = unpack('<B', f.read(1))[0]
                    volume_fadeout = unpack('<H', f.read(2))[0]

                    sample_header.append({
                        'id': i,
                        'header_size': sample_header_size,
                        'keymap': keymap,
                        'volume_envelope': volume_envelope,
                        'num_volume_points': num_volume_points,
                        'volume_type' : volume_type,
                        'volume_sus_point': volume_sus_point,
                        'volume_loop_start': volume_loop_start,
                        'volume_loop_end': volume_loop_end,
                        'panning_envelope': panning_envelope,
                        'num_panning_points': num_panning_points,
                        'panning_type' : panning_type,
                        'panning_sus_point': panning_sus_point,
                        'panning_loop_start': panning_loop_start,
                        'panning_loop_end': panning_loop_end,
                        'vibrato_type' : vibrato_type,
                        'vibrato_sweep' : vibrato_sweep,
                        'vibrato_depth' : vibrato_depth,
                        'vibrato_rate' : vibrato_rate,
                        'volume_fadeout' : volume_fadeout
                    })

                for j in range(num_samples):
                    f.read(22)
                    sample_length = unpack('<I', f.read(4))[0]
                    sample_loop_start = unpack('<I', f.read(4))[0]
                    sample_loop_length = unpack('<I', f.read(4))[0] # If 0, sample does not loop

                    volume = unpack('<B', f.read(1))[0]
                    finetune = unpack('<B', f.read(1))[0]
                    sample_type = f.read(1)
                    panning = unpack('<B', f.read(1))[0]
                    rel_note_num = unpack('<b', f.read(1))[0]
                    ADPCM: bool = f.read(1) == b'\xad'
                    name = f.read(22)
                    sample_name = unpack('<22s', name)[0].decode('CP437')
                    sample_data = f.read(sample_length)
                    sample: dict[str, Any] = {
                        'index': j,
                        'name': sample_name,
                        'length': sample_length,
                        'loop_start': sample_loop_start,
                        'loop_length': sample_loop_length,
                        'volume': volume,
                        'finetune': finetune,
                        'type': sample_type,
                        'panning': panning,
                        'relative_note': rel_note_num,
                        'use_ADPCM?': ADPCM,
                        'data': sample_data
                    }

                    samples.append(sample)
            else:
                f.read(instr_size - 29) # If there are no samples, and the instrument size is more than 29, the data is padded with zeroes.

            self.instruments.append({
                'id': i,
                'name': instr_name,
                'type': instr_type,
                'samples': samples
            })

if __name__ == "__main__":
    xm = XMReader('./amb-nrg.xm')
    
    xm.load_file()