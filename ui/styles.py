# -*- coding: utf-8 -*-

STYLE_SHEET = """
    QMainWindow { background-color: #ffffff; }
    
    #progressContainer { background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; }
    
    #exitBtn {
        background-color: #fee2e2;
        color: #ef4444;
        font-weight: 700;
        font-size: 13px;
        border-radius: 10px;
        border: 1px solid #fecaca;
    }
    #exitBtn:hover { background-color: #fecaca; }
    
    QLabel[active="true"] { color: #3b82f6; font-weight: 800; font-size: 16px; }
    QLabel[active="false"] { color: #94a3b8; font-weight: 400; font-size: 14px; }
    #stepArrow { color: #cbd5e1; font-size: 18px; margin: 0 10px; }
    
    #pageTitle { font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
    #pageDesc { font-size: 16px; color: #64748b; margin-bottom: 30px; }
    #statusLabel { font-size: 14px; color: #3b82f6; font-weight: 600; margin-bottom: 10px; }
    
    #methodRadio { font-size: 18px; font-weight: 700; color: #1e293b; padding: 10px; }
    #methodDetail { font-size: 14px; color: #64748b; padding-left: 35px; margin-bottom: 10px; }
    
    #mainBtn {
        background-color: #3b82f6;
        color: white;
        font-weight: 700;
        font-size: 18px;
        border-radius: 15px;
        padding: 20px;
        border: none;
    }
    #mainBtn:hover { background-color: #2563eb; }
    #mainBtn:disabled { background-color: #e2e8f0; color: #94a3b8; }
    
    #secondaryBtn {
        background-color: #ffffff;
        color: #64748b;
        font-weight: 600;
        font-size: 16px;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e2e8f0;
    }
    #secondaryBtn:hover { background-color: #f8fafc; }
    
    #actionBtn {
        background-color: #f1f5f9;
        color: #3b82f6;
        font-size: 20px;
        font-weight: 700;
        border: 2px dashed #cbd5e1;
        border-radius: 20px;
        margin-bottom: 10px;
    }
    #actionBtn:hover { background-color: #eff6ff; border-color: #3b82f6; }
    #actionBtn[drag-active="true"] { background-color: #dbeafe; border-color: #2563eb; }
    
    #fileInfo { font-size: 14px; color: #64748b; font-style: italic; }
    
    #fileListDisplay {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #475569;
    }
    
    #recordProgress {
        height: 10px;
        border-radius: 5px;
        background-color: #f1f5f9;
        border: none;
        margin-bottom: 10px;
    }
    #recordProgress::chunk {
        background-color: #3b82f6;
        border-radius: 5px;
    }
    
    #recordTimer {
        font-size: 24px;
        font-weight: 800;
        color: #ef4444;
        margin-bottom: 5px;
    }
    
    #resultCard {
        background-color: #f8fafc;
        border-radius: 30px;
        padding: 40px;
        margin-bottom: 20px;
    }
    #rateBig { font-size: 80px; font-weight: 800; }
    #rateStatus { font-size: 14px; font-weight: 700; color: #94a3b8; letter-spacing: 2px; }
    
    #resList { background: transparent; border: none; font-size: 14px; }
    
    QScrollBar:vertical { width: 8px; background: transparent; }
    QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 4px; }
"""

