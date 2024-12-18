from io import BytesIO
import struct
import pygame.mixer as mixer
import threading
import wave

from extended_module import XMReader
from module_data import Pattern

if __name__ == "__main__":
    r = XMReader('./amb-nrg.xm')
    r.load_file()
    c = 0
    for i in r.instruments:
        for s in i['samples']:
            bit_depth = (int.from_bytes(s['type']) >> 4) & 1
            data: bytes = s['data']
            length = s['length']
            old: int = 0
            real_sample = b''
            d = BytesIO(data)
            print('working...')

            for j in range(length):
                old += struct.unpack('<b', d.read(1))[0]
                real_sample += old.to_bytes(2, signed=True)

            if bit_depth == 0:
                bit_depth = 1
            else:
                bit_depth = 2

            with wave.open(f'./{c}_{s['index']}.wav', 'wb') as f:
                f.setparams((1, 2, 8363, 0, 'NONE', 'NONE'))
                f.writeframes(real_sample)
        c += 1