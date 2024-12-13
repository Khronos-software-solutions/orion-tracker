from io import BytesIO

class Sample:
    def __init__(self, data: bytes | None = None, length: int | None = None, name: str | None = None, ADPCM: bool = False):
        pass
    
class Volume:
    volume_type: str
    volume: int
    def __init__(self, data: int):

        high_ord, low_ord = data >> 4, data & 0x0F

        if 0x1 <= high_ord < 0x5:
            self.volume_type = 'V'
            self.volume = data - 0x10
        elif 0x6 <= high_ord < 0x7:
            self.volume_type = 'D'
            self.volume = low_ord
        elif 0x7 <= high_ord < 0x8:
            self.volume_type = 'C'
            self.volume = low_ord
        elif 0x8 <= high_ord < 0x9:
            self.volume_type = 'B'
            self.volume = low_ord
        elif 0x9 <= high_ord < 0xA:
            self.volume_type = 'A'
            self.volume = low_ord
        elif 0xA <= high_ord < 0xB:
            self.volume_type = 'U'
            self.volume = low_ord
        elif 0xB <= high_ord < 0xC:
            self.volume_type = 'H'
            self.volume = low_ord
        elif 0xC <= high_ord < 0xD:
            self.volume_type = 'P'
            self.volume = low_ord
        elif 0xD <= high_ord < 0xE:
            self.volume_type = 'L'
            self.volume = low_ord
        elif 0xE <= high_ord < 0xF:
            self.volume_type = 'R'
            self.volume = low_ord
        elif 0xF <= high_ord:
            self.volume_type = 'G'
            self.volume = low_ord
    
    def __str__(self):
        return "{}{:02d}".format(self.volume_type.lower(), self.volume)
    
class Effect:
    effect_type: str
    parameter: int
    def __init__(self, effect, parameter):
        pass

class Note:
    tone: int | None # 0..97
    instrument: int | None # 0..128
    volume: int | None # 0..64, 255
    effect: int | None # 0..26
    effect_parameter: int | None # 0..255

    def __init__(
            self, 
            tone: int | None = None,
            instrument: int | None = None,
            volume: int | None = None,
            effect: int | None = None,
            effect_parameter: int | None = None
                ):

        self.tone = tone
        self.instrument = instrument
        self.volume = volume
        self.effect = effect
        self.effect_parameter = effect_parameter
    
    def from_bytes(self, data: bytes):
        if len(data) != 5:
            raise ValueError('invalid byte data for note.')

        self.tone, self.instrument, self.volume, \
            self.effect, \
            self.effect_parameter\
            = [int.from_bytes(data[i:i+1]) for i in range(5)]


    def __str__(self):
        if self.instrument:
            i = "{:02d}".format(self.instrument)
        else:
            i = '--'
        if self.volume:
            v = Volume(self.volume)
        else:
            v = ' --'
        if self.effect:
            e = hex(self.effect)
        else:
            e = '---'
        

        return "{} {}{} {}".format(self.to_readable(), i, v, e)

    def to_readable(self):
        if self.tone:
            notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            octave = (self.tone - 1) // 12 + 1
            note_index = (self.tone - 1) % 12
            return f'{notes[note_index].ljust(2, '-')}{octave}'
        return '---'
    

class Pattern:
    pattern: dict[str, list[Note]]
    rows: int
    channels: int
    def __init__(self, channels: int, rows: int):
        self.pattern = {}
        self.rows = rows
        self.channels = channels

        for channel in range(channels):
            self.pattern.update({
                f'ch_{channel+1}': [Note() for _ in range(rows)]
            })

    def from_data(self, data: bytes):
        data_notes = [data[i:i+5] for i in range(0, len(data), 5)]
        data_rows: list[list[bytes]] = []
        for i in range(0, len(data_notes), self.rows):
            data_rows.append(data_notes[i:i + self.rows])

    def from_byte_pattern(self, pattern: bytes):
        f = BytesIO(pattern)
        for row in range(self.rows):
            for note in range(self.channels):
                t = i = v = e = ep = None
                byte_1 = int.from_bytes(f.read(1))

                # Handle packing scheme
                if (byte_1 & 0x80) != 0:
                    if (byte_1 & 0x01) != 0: t = int.from_bytes(f.read(1))
                    if (byte_1 & 0x02) != 0: i = int.from_bytes(f.read(1))
                    if (byte_1 & 0x04) != 0: v = int.from_bytes(f.read(1))
                    if (byte_1 & 0x08) != 0: e = int.from_bytes(f.read(1))
                    if (byte_1 & 0x10) != 0: ep = int.from_bytes(f.read(1)) # Useless

                else:
                    t, i, v, e, ep = [int.from_bytes(f.read(1)) for _ in range(5)]

                self.pattern[f'ch_{note+1}'][row] = Note(t, i, v, e, ep)

                print(self.pattern[f'ch_{note+1}'][row], end=' | ')
            print()
