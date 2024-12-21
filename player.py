import os
import struct
import shutil
import wave

from typing import Any
from io import BytesIO

import pygame.mixer as mixer

from extended_module import XMReader

def save_samples(r: XMReader):
    shutil.rmtree('./samples', ignore_errors=True)
    os.makedirs('./samples', exist_ok=True)
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

            with wave.open(f'./samples/{c}_{s["index"]}_{s["relative_note"]}.wav', 'wb') as f:
                f.setparams((1, 2, 8363, 0, 'NONE', 'NONE'))
                f.writeframes(real_sample)

            l.append({
                'id': c,
                'index': s['index'],
                'name': s['name'],
                'path': f'./temp/samples/{c}_{s["index"]}_{s["relative_note"]}.wav',
            })
        instruments.append(l)
        c += 1

def play_sample(filepath: str):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()

if __name__ == '__main__':
    r = XMReader('./amb-nrg.xm')
    r.load_file()
    save_samples(r)
