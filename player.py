import struct
import os

# Set environment variable before importing sounddevice. Value is not important.
os.environ["SD_ENABLE_ASIO"] = "1"
import sounddevice as sd
import threading
import numpy as np


from extended_module import XMReader

def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

if __name__ == "__main__":
    reader = XMReader('amblight.xm')
    reader.load_file()
    sample = reader.instruments[0]['samples'][0]
    delta = [struct.unpack('<b', sample['data'][i:i+1])[0] for i in range(sample['length'])]
    old = 0
    raw = []
    for i in delta:
        old += i
        raw.append(old)
    print(len(delta))
