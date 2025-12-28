# -*- coding: utf-8 -*-

import os
import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa
import librosa.display
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from scipy.io import wavfile
from PyQt5.QtCore import QThread, pyqtSignal

matplotlib.use('Agg')

def generate_spectrogram(file_path):
    """Heavy STFT processing logic separated for thread usage"""
    try:
        # Use librosa.load for broad format support (mp3, m4a, wav, etc.)
        y, sr = librosa.load(file_path, sr=None)
        
        if len(y.shape) > 1:
            y = np.mean(y, axis=1)
            
        window_size = 1024
        window = np.hanning(window_size)
        stft = librosa.stft(y, n_fft=window_size, hop_length=512, window=window)
        out = 2 * np.abs(stft) / np.sum(window)
        
        fig = matplotlib.figure.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, cmap="nipy_spectral")
        ax.axis('off')
        fig.tight_layout(pad=0)
        
        if not os.path.exists("data"):
            os.makedirs("data")
            
        output_img = os.path.join("data", os.path.basename(file_path) + ".jpg")
        fig.savefig(output_img, bbox_inches='tight', pad_inches=0)
        return output_img
    except Exception as e:
        raise e

# Alias for backward compatibility
processing = generate_spectrogram

class ProcessThread(QThread):
    """Thread for processing existing audio files to spectrograms"""
    finished = pyqtSignal(str, str)
    error = pyqtSignal(str)

    def __init__(self, audio_paths):
        super().__init__()
        self.audio_paths = audio_paths

    def run(self):
        try:
            for path in self.audio_paths:
                img_path = generate_spectrogram(path)
                self.finished.emit(img_path, path)
        except Exception as e:
            self.error.emit(str(e))

class RecordThread(QThread):
    """Improved RecordThread with non-blocking processing"""
    finished = pyqtSignal(str, str)
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        try:
            fs = 44100
            seconds = 3
            
            # Start recording
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
            
            # Progress updates
            steps = 30
            for i in range(steps):
                self.msleep(100) 
                self.progress.emit(int((i + 1) / steps * 100))
            
            sd.wait()
            
            if not os.path.exists("data"):
                os.makedirs("data")
                
            wav_path = os.path.join("data", self.filename + ".wav")
            wavfile.write(wav_path, fs, myrecording)
            
            # Process to spectrogram
            img_path = generate_spectrogram(wav_path)
            self.finished.emit(img_path, wav_path)
        except Exception as e:
            self.error.emit(str(e))
