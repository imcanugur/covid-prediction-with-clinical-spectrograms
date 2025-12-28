# -*- coding: utf-8 -*-

import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QRadioButton, QButtonGroup, 
                             QFrame, QFileDialog, QCheckBox, QStatusBar,
                             QScrollArea, QListWidget, QListWidgetItem, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from core.audio import RecordThread, ProcessThread, processing
from core.model import AnalysisThread, ModelLoaderThread
from ui.styles import STYLE_SHEET

class ModernWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COVID-19 Diagnostic Wizard")
        self.setFixedSize(900, 750)
        self.setAcceptDrops(True)
        
        self.selected_files = []
        self.original_audio_files = []
        self.control = 0
        
        self.player = QMediaPlayer()
        
        self.init_ui()
        self.apply_styles()
        
        self.model_loader = ModelLoaderThread()
        self.model_loader.start()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and self.stack.currentIndex() == 1:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.handle_files_input(files)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top Bar
        self.progress_container = QWidget()
        self.progress_container.setObjectName("progressContainer")
        self.progress_layout = QHBoxLayout(self.progress_container)
        self.progress_layout.setContentsMargins(40, 20, 40, 20)
        
        steps_widget = QWidget()
        steps_layout = QHBoxLayout(steps_widget)
        steps_layout.setContentsMargins(0, 0, 0, 0)
        self.steps_labels = []
        for i, name in enumerate(["1. Start", "2. Input Samples", "3. Results"]):
            label = QLabel(name)
            label.setObjectName(f"stepLabel_{i}")
            label.setProperty("active", i == 0)
            steps_layout.addWidget(label)
            self.steps_labels.append(label)
            if i < 2: steps_layout.addWidget(QLabel("→"))
        
        self.progress_layout.addWidget(steps_widget, 1)
        self.btn_exit = QPushButton("✕ Exit")
        self.btn_exit.setObjectName("exitBtn")
        self.btn_exit.setFixedSize(80, 35)
        self.btn_exit.clicked.connect(self.close)
        self.progress_layout.addWidget(self.btn_exit)
        self.main_layout.addWidget(self.progress_container)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # PAGE 1: START
        self.page1 = QWidget()
        p1_layout = QVBoxLayout(self.page1)
        p1_layout.setContentsMargins(100, 60, 100, 60)
        p1_layout.addWidget(QLabel("COVID-19 Analysis", objectName="pageTitle", alignment=Qt.AlignCenter))
        p1_layout.addWidget(QLabel("Unified diagnostic tool for clinical voice and spectrogram analysis.", objectName="pageDesc", alignment=Qt.AlignCenter))
        
        info_box = QFrame(objectName="stepBox")
        info_layout = QVBoxLayout(info_box)
        info_layout.addWidget(QLabel("<b>Instructions:</b>", styleSheet="font-size: 16px; margin-bottom: 10px;"))
        info_layout.addWidget(QLabel("• You can record sounds directly via microphone."))
        info_layout.addWidget(QLabel("• You can upload WAV audio files."))
        info_layout.addWidget(QLabel("• You can upload existing spectrogram images."))
        info_layout.addWidget(QLabel("• Multiple samples can be analyzed simultaneously."))
        p1_layout.addWidget(info_box)
        
        p1_layout.addStretch()
        self.btn_start = QPushButton("Start Diagnostic Session 🚀", objectName="mainBtn")
        self.btn_start.clicked.connect(self.go_to_step2)
        p1_layout.addWidget(self.btn_start)
        self.stack.addWidget(self.page1)

        # PAGE 2: PREPARATION
        self.page2 = QWidget()
        p2_layout = QVBoxLayout(self.page2)
        p2_layout.setContentsMargins(80, 20, 80, 40)
        p2_layout.addWidget(QLabel("Add Clinical Samples", objectName="pageTitle"))
        
        btns_layout = QHBoxLayout()
        self.btn_record = QPushButton("🎙️ Record Audio", objectName="actionBtn", minimumHeight=80)
        self.btn_record.clicked.connect(self.handle_record)
        
        self.btn_browse = QPushButton("📁 Browse Files", objectName="actionBtn", minimumHeight=80)
        self.btn_browse.clicked.connect(self.handle_browse)
        
        btns_layout.addWidget(self.btn_record)
        btns_layout.addWidget(self.btn_browse)
        p2_layout.addLayout(btns_layout)
        
        self.record_timer_label = QLabel("", objectName="recordTimer", alignment=Qt.AlignCenter)
        self.record_timer_label.hide()
        p2_layout.addWidget(self.record_timer_label)
        
        self.record_progress = QtWidgets.QProgressBar(objectName="recordProgress", visible=False)
        p2_layout.addWidget(self.record_progress)
        
        self.file_list_display = QListWidget(objectName="fileListDisplay", minimumHeight=150)
        self.file_list_display.hide()
        p2_layout.addWidget(self.file_list_display)
        
        self.btn_clear_files = QPushButton("🗑️ Clear All Samples", objectName="secondaryBtn", visible=False)
        self.btn_clear_files.clicked.connect(self.clear_file_selection)
        p2_layout.addWidget(self.btn_clear_files)
        
        self.file_info = QLabel("Drag & Drop files here or use buttons above.", objectName="fileInfo", alignment=Qt.AlignCenter)
        p2_layout.addWidget(self.file_info)
        
        p2_layout.addStretch()
        nav2 = QHBoxLayout()
        self.btn_back2 = QPushButton("⬅️ Back", objectName="secondaryBtn")
        self.btn_back2.clicked.connect(self.go_to_step1)
        self.btn_next2 = QPushButton("Run Global Analysis 🚀", objectName="mainBtn", enabled=False)
        self.btn_next2.clicked.connect(self.go_to_step3)
        nav2.addWidget(self.btn_back2); nav2.addWidget(self.btn_next2)
        p2_layout.addLayout(nav2)
        self.stack.addWidget(self.page2)

        # PAGE 3: ANALYSIS
        self.page3 = QWidget()
        p3_layout = QVBoxLayout(self.page3)
        p3_layout.setContentsMargins(100, 20, 100, 60)
        p3_layout.addWidget(QLabel("Analysis Results", objectName="pageTitle"))
        self.status_label = QLabel("Preparing...", objectName="statusLabel")
        p3_layout.addWidget(self.status_label)
        
        result_card = QFrame(objectName="resultCard")
        rc_layout = QVBoxLayout(result_card)
        self.rate_label = QLabel("--", objectName="rateBig", alignment=Qt.AlignCenter)
        rc_layout.addWidget(self.rate_label)
        rc_layout.addWidget(QLabel("AVERAGE MATCH RATE", objectName="rateStatus", alignment=Qt.AlignCenter))
        p3_layout.addWidget(result_card)
        
        self.res_list = QListWidget(objectName="resList", maximumHeight=200)
        p3_layout.addWidget(self.res_list)
        p3_layout.addStretch()
        self.btn_reset = QPushButton("🔄 Start New Diagnostic", objectName="mainBtn", visible=False)
        self.btn_reset.clicked.connect(self.reset_all)
        p3_layout.addWidget(self.btn_reset)
        self.stack.addWidget(self.page3)

        self.setStatusBar(QStatusBar())

    def go_to_step1(self): self.stack.setCurrentIndex(0); self.update_progress(0)
    def go_to_step2(self): self.stack.setCurrentIndex(1); self.update_progress(1)
    def go_to_step3(self):
        self.stack.setCurrentIndex(2); self.update_progress(2)
        self.rate_label.setText("--")
        self.rate_label.setStyleSheet("color: #94a3b8; font-size: 80px; font-weight: 800;")
        self.res_list.clear()
        self.btn_reset.hide()
        self.analysis_thread = AnalysisThread(self.selected_files)
        self.analysis_thread.result_ready.connect(self.on_analysis_result)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.start()

    def handle_record(self):
        self.btn_record.setEnabled(False); self.btn_browse.setEnabled(False)
        self.record_progress.show(); self.record_timer_label.show()
        self.recorder = RecordThread(datetime.now().strftime("%H-%M-%S"))
        self.recorder.progress.connect(self.update_record_ui)
        self.recorder.finished.connect(self.on_record_finished)
        self.recorder.start()

    def handle_browse(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Audio or Images (*.wav *.mp3 *.ogg *.flac *.m4a *.jpg *.png *.jpeg)")
        if files: self.handle_files_input(files)

    def handle_files_input(self, files):
        audio_exts = ('.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aiff')
        img_exts = ('.jpg', '.png', '.jpeg')
        
        audio_files = [f for f in files if f.lower().endswith(audio_exts)]
        img_files = [f for f in files if f.lower().endswith(img_exts)]
        
        if audio_files:
            self.statusBar().showMessage(f"Processing {len(audio_files)} audio files...")
            self.process_thread = ProcessThread(audio_files)
            self.process_thread.finished.connect(self.add_file_to_selection)
            self.process_thread.finished.connect(self.update_file_visibility)
            self.process_thread.start()
        
        if img_files:
            for f in img_files: self.add_file_to_selection(f, None)
            self.update_file_visibility()

    def update_record_ui(self, v):
        self.record_progress.setValue(v)
        self.record_timer_label.setText(f"Recording: {max(0, 3.0-(v*0.03)):.1f}s")

    def on_record_finished(self, img, wav):
        self.add_file_to_selection(img, wav); self.record_progress.hide(); self.record_timer_label.hide()
        self.btn_record.setEnabled(True); self.btn_browse.setEnabled(True)
        self.update_file_visibility()

    def add_file_to_selection(self, img, wav):
        self.selected_files.append(img); self.original_audio_files.append(wav)
        item = QListWidgetItem(self.file_list_display)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        filename = os.path.basename(img if not wav else wav)
        layout.addWidget(QLabel(f"📄 {filename[:30]}..."))
        layout.addStretch()
        if wav:
            btn = QPushButton("▶️ Play")
            btn.setFixedSize(65, 28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("background:#10b981; color:white; border-radius:6px; font-size:11px; font-weight:700;")
            
            def toggle_play(_, p=wav, b=btn):
                if self.player.state() == QMediaPlayer.PlayingState and self.player.currentMedia().canonicalUrl().toLocalFile() == p:
                    self.player.stop()
                    b.setText("▶️ Play")
                    b.setStyleSheet("background:#10b981; color:white; border-radius:6px; font-size:11px; font-weight:700;")
                else:
                    self.play_audio(p)
                    for i in range(self.file_list_display.count()):
                        other_item = self.file_list_display.item(i)
                        other_widget = self.file_list_display.itemWidget(other_item)
                        if other_widget:
                            other_btn = other_widget.findChild(QPushButton)
                            if other_btn and other_btn.text() == "⏹️ Stop":
                                other_btn.setText("▶️ Play")
                                other_btn.setStyleSheet("background:#10b981; color:white; border-radius:6px; font-size:11px; font-weight:700;")
                    b.setText("⏹️ Stop")
                    b.setStyleSheet("background:#ef4444; color:white; border-radius:6px; font-size:11px; font-weight:700;")
            
            btn.clicked.connect(toggle_play)
            layout.addWidget(btn)
            
        rm_btn = QPushButton("❌")
        rm_btn.setFixedSize(28, 28)
        rm_btn.setCursor(Qt.PointingHandCursor)
        rm_btn.setStyleSheet("background:#f1f5f9; color:#ef4444; border-radius:6px; font-weight:800;")
        rm_btn.clicked.connect(lambda: self.remove_specific_file(item, img, wav))
        layout.addWidget(rm_btn)
        item.setSizeHint(widget.sizeHint()); self.file_list_display.setItemWidget(item, widget)

    def remove_specific_file(self, item, img, wav):
        self.file_list_display.takeItem(self.file_list_display.row(item))
        idx = self.selected_files.index(img)
        self.selected_files.pop(idx); self.original_audio_files.pop(idx)
        self.update_file_visibility()

    def play_audio(self, p):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(p)))
        self.player.play()
        self.player.stateChanged.connect(self.on_player_state_changed)

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            for i in range(self.file_list_display.count()):
                item = self.file_list_display.item(i)
                widget = self.file_list_display.itemWidget(item)
                if widget:
                    btn = widget.findChild(QPushButton)
                    if btn and btn.text() == "⏹️ Stop":
                        btn.setText("▶️ Play")
                        btn.setStyleSheet("background:#10b981; color:white; border-radius:6px; font-size:11px; font-weight:700;")
    
    def update_file_visibility(self):
        has_files = len(self.selected_files) > 0
        self.file_list_display.setVisible(has_files); self.btn_clear_files.setVisible(has_files)
        self.btn_next2.setEnabled(has_files)
        self.file_info.setText(f"✅ {len(self.selected_files)} sample(s) ready." if has_files else "Drag & Drop or use buttons above.")

    def on_analysis_result(self, i, path, rate):
        total_prev = sum([float(self.res_list.item(j).text().split('%')[1].split(' ')[0]) for j in range(self.res_list.count())])
        avg = (total_prev + rate) / (self.res_list.count() + 1)
        self.rate_label.setText(f"%{avg:.2f}")
        self.rate_label.setStyleSheet(f"color: {'#ef4444' if avg > 50 else '#10b981'}; font-size:80px; font-weight:800;")
        item = QListWidgetItem(f"✅ Sample {i+1}: %{rate:.2f}")
        item.setForeground(QtGui.QColor('#ef4444' if rate > 50 else '#10b981'))
        self.res_list.addItem(item); self.res_list.scrollToBottom()

    def on_analysis_finished(self): self.status_label.setText("✨ Analysis complete."); self.btn_reset.show()
    def clear_file_selection(self):
        self.selected_files = []; self.original_audio_files = []
        self.file_list_display.clear(); self.update_file_visibility(); self.player.stop()
    
    def reset_all(self):
        self.clear_file_selection()
        self.res_list.clear()
        self.rate_label.setText("--")
        self.rate_label.setStyleSheet("color: #94a3b8; font-size: 80px; font-weight: 800;")
        self.status_label.setText("Preparing...")
        self.go_to_step1()

    def update_progress(self, index):
        for i, label in enumerate(self.steps_labels):
            label.setProperty("active", i == index); label.style().unpolish(label); label.style().polish(label)
    def apply_styles(self): self.setStyleSheet(STYLE_SHEET)
