from tkinter import Frame, Tk
import wave
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WaveformDisplay(Frame):
    def __init__(self, master: Tk | Frame):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.figure = Figure(dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def load_waveform(self, filepath: str):
        with wave.open(filepath, 'rb') as wav_file:
            params = wav_file.getparams()
            n_channels, _, framerate, n_frames = params[:4]
            str_data = wav_file.readframes(n_frames)
            wave_data = np.frombuffer(str_data, dtype=np.int16)

            if n_channels == 2:
                wave_data = wave_data[::2]

            time = np.linspace(0, n_frames / framerate, num=n_frames)

            self.ax.clear()
            self.ax.set_facecolor('black')
            self.ax.plot(time, wave_data, linewidth=0.5, color='r')
            self.ax.get_yaxis().set_visible(False)
            self.canvas.draw()

if __name__ == "__main__":
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = WaveformDisplay(root)
    app.load_waveform('./samples/0_0_0.wav')
    app.grid(row=0, column=0, sticky='nsew')
    root.mainloop()
