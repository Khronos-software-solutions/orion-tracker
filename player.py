from io import BytesIO
import struct
from typing import Any
import pygame.mixer as mixer
import threading
import wave

from extended_module import XMReader
from module_data import Pattern

def save_samples(r: XMReader):
    instruments: list[list[dict[str, Any]]] = []
    c = 0
    for i in r.instruments:
        l: list[dict[str, Any]] = []
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

            with wave.open(f'./temp/samples/{c}_{s['index']}_{s['relative_note']}.wav', 'wb') as f:
                f.setparams((1, 2, 8363, 0, 'NONE', 'NONE'))
                f.writeframes(real_sample)

            l.append({
                'id': c,
                'index': s['index'],
                'name': s['name'],
                'path': f'./temp/samples/{c}_{s['index']}_{s['relative_note']}.wav',
            })
        instruments.append(l)
        c += 1
    return instruments
