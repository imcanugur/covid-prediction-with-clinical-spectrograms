# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, QtGui
from ui.window import ModernWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
