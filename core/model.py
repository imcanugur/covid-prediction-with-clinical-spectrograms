# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PyQt5.QtCore import QThread, pyqtSignal

_MODEL_CACHE = None

def get_model():
    global _MODEL_CACHE
    model_path = os.path.join('models', 'best_mod.h5')
    if _MODEL_CACHE is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found.")
        _MODEL_CACHE = load_model(model_path)
    return _MODEL_CACHE

class ModelLoaderThread(QThread):
    """Pre-loads model in background to avoid lag on first prediction"""
    loaded = pyqtSignal()
    
    def run(self):
        try:
            get_model()
            self.loaded.emit()
        except:
            pass

class AnalysisThread(QThread):
    """Background inference thread to keep UI smooth during heavy ML tasks"""
    result_ready = pyqtSignal(int, str, float) # index, img_path, result
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, selected_files):
        super().__init__()
        self.selected_files = selected_files

    def run(self):
        try:
            model = get_model()
            for i, img_path in enumerate(self.selected_files):
                image = cv2.imread(img_path)
                if image is None: continue
                
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (224, 224))
                image = np.array(image).astype('float32') / 255
                image = image.reshape(1, 224, 224, 3)
                
                res = model.predict(image, verbose=0)
                match_rate = (1 - res[0][0]) * 100
                
                self.result_ready.emit(i, img_path, float(match_rate))
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
