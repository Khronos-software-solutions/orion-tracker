from io import BytesIO
import struct
import pygame.mixer as mixer
import wave

from extended_module import XMReader
from module import Pattern


if __name__ == "__main__":
    r = XMReader('./amb-nrg.xm')
    r.load_file()
    s = r.instruments[0]['samples'][0]
    bit_depth = (int.from_bytes(s['type']) >> 4) & 1
    data: bytes = s['data']
    length = s['length']
    old: int = 0
    real_sample = b''
    d = BytesIO(data)
    print('working...')

    for i in range(length):
        old += struct.unpack('<b', d.read(1))[0]
        print(old)
        real_sample += old.to_bytes(2, signed=True)

    print(bit_depth)
    if bit_depth == 0:
        bit_depth = 1
    else:
        bit_depth = 2
        
    print(s['length'])
    print(real_sample)
    with wave.open('./sample1.wav', 'wb') as f:
        f.setparams((1, 2, 42200, 0, 'NONE', 'NONE'))
        f.writeframes(real_sample)