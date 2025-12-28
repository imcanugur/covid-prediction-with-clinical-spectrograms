# 🏥 COVID-19 Diagnostic Wizard

Developed with ❤️ by **imcanugur**.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![AI Engine](https://img.shields.io/badge/AI-TensorFlow-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A state-of-the-art, clinical-grade desktop application designed to assist in **COVID-19 screening** through AI-driven spectrogram analysis. By processing clinical sounds like coughs and breathing patterns, the tool provides a rapid match-rate prediction using deep learning.

---

## 🌟 Key Highlights

### 🚀 High-Performance Architecture
*   **Multithreading Engine**: Heavy audio processing and AI inferences run on background threads, ensuring a buttery-smooth 60FPS UI experience.
*   **Asynchronous Processing**: Add 50 files at once? No problem. The app processes them in the background while you continue working.
*   **Model Pre-loading**: AI models are cached in memory upon startup to eliminate latency during analysis.

### 🎨 Modern & Intuitive UX
*   **Unified Diagnostic Wizard**: A clean, 3-step guided process that eliminates user error.
*   **Hybrid Input System**: Seamlessly mix live microphone recordings, various audio formats (`.mp3`, `.wav`, `.m4a`), and even raw spectrogram images in a single session.
*   **Smart Drag & Drop**: Just drop your files anywhere on the window to start the automated conversion and queuing.

### 🔍 Clinical Precision
*   **Spectrogram Visualization**: Advanced STFT (Short-Time Fourier Transform) converts audio into high-resolution spectral images for the AI to analyze.
*   **Live Per-Sample Feedback**: Watch results roll in one by one with individual match rates and a dynamically updated global average.
*   **Audio Verification**: Built-in media player to listen and verify samples before committing to analysis.

---

## 🛠️ Tech Stack

| Domain | Technology |
| :--- | :--- |
| **Frontend** | PyQt5, QSS (Custom Styling) |
| **AI/ML** | TensorFlow, Keras, OpenCV |
| **Audio Processing** | Librosa, SoundFile, SoundDevice |
| **Visuals** | Matplotlib (Agg Backend) |
| **Logic** | Python 3.9+ (Multithreaded) |

---

## 📦 Installation & Setup

### 1. Clone & Environment
Clone the repository and enter the project directory:
```bash
git clone https://github.com/imcanugur/covid-prediction-with-clinical-spectrograms.git
cd covid-prediction-with-clinical-spectrograms
```

### 2. Virtual Environment Setup (Python 3.9 Recommended)
It is highly recommended to use a virtual environment to avoid dependency conflicts. 

**Create the environment:**
*   **Standard:**
    ```bash
    python -m venv venv
    ```
*   **Specific Python Path (if you have multiple versions):**
    ```bash
    # Windows Example:
    C:\Path\To\Python39\python.exe -m venv venv
    
    # Linux/macOS Example:
    python3.9 -m venv venv
    ```

**Activate the environment:**
*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **Linux/macOS:**
    ```bash
    source venv/bin/activate
    ```

### 3. Dependency Management
Once the environment is active, install the optimized requirements:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. AI Model Deployment
The prediction engine requires the pre-trained weights:
1. Ensure a directory named `models` exists in the root.
2. Download the trained model from [this Kaggle Notebook](https://www.kaggle.com/code/aimerodriguez/covid19-sound-spectograms/).
3. Place your `best_mod.h5` inside the `models/` folder.

---

## 📖 Step-by-Step Usage

### 🟢 Phase 1: Initiation
Ensure your virtual environment is activated, then launch the app:
```bash
python main.py
```
The "Diagnostic Wizard" will greet you. Click **Start Diagnostic Session** to initialize the background engines.

### 🟡 Phase 2: Sample Acquisition
Populate your analysis queue using any of these methods:
*   **Microphone**: Press **🎙️ Record Audio** for a 3-second clinical capture. A live countdown will guide you.
*   **File Browser**: Use **📁 Browse Files** to select multiple audio or image files.
*   **Drag & Drop**: Drag a mix of folders or files directly onto the app.

> **Tip**: Use the **▶️ Listen** button to check recordings and **❌** to prune the list before analysis.

### 🔴 Phase 3: Global Analysis
Hit **Run Global Analysis 🚀**. Switch to the results page where you'll see:
*   Real-time status updates for each file.
*   Individual match-rate percentages.
*   A large, color-coded **Average Match Rate** that updates as each sample is processed.

---

## 📁 Modular Project Structure

```text
.
├── main.py              # App bootstrapper
├── core/                # The Brain
│   ├── audio.py         # Signal processing & recording threads
│   └── model.py         # AI inference & model management
├── ui/                  # The Face
│   ├── window.py        # Main wizard logic & layouts
│   └── styles.py        # Modern QSS theme definitions
├── models/              # AI Warehouse (best_mod.h5)
├── data/                # Transient storage for processed samples
└── requirements.txt     # Global dependencies
```

---

## ⚖️ License & Disclaimer
This software is provided under the **MIT License**. 
**Disclaimer**: This is a clinical-grade *tool* intended for research and supplementary screening purposes. It is not a replacement for professional medical diagnosis.

---
*Created by **imcanugur** - Advancing Digital Health through AI.*
