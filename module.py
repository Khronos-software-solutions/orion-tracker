from io import BytesIO

class Sample:
    def __init__(self, data: bytes | None = None, length: int | None = None, name: str | None = None, ADPCM: bool = False):
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
        l: list[str] = []
        for i in [self.instrument, self.volume, self.effect, self.effect_parameter]:
            if i:
                l.append(bytes([i]).hex())
            else:
                l.append('-')

        return self.to_readable() + " " +' '.join(l)

    def to_readable(self):
        if not self.tone:
            raise ValueError('tone not set.')

        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        octave = (self.tone - 1) // 12 + 1
        note_index = (self.tone - 1) % 12

        return f'{notes[note_index].ljust(2, '-')}{octave}'
    

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
        print(self.pattern)
        pass
    
    def from_data(self, data: bytes):
        data_notes = [data[i:i+5] for i in range(0, len(data), 5)]
        data_rows: list[list[bytes]] = []
        for i in range(0, len(data_notes), self.rows):
            data_rows.append(data_notes[i:i + self.rows])

    def from_byte_pattern(self, pattern: bytes):
        notes: list[Note] = []

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

                notes.append(Note(t, i, v, e, ep))