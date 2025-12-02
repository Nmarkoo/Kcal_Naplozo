
# -*- coding: utf-8 -*-


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


EDZESFORMAK_MET = {
    "Kardió": {
        "Futás": 10.0,
        "Gyaloglás / Séta": 3.5,
        "Kerékpár": 7.0,
    },
    "Erősítés / Izomépítés": {
        "Súlyzós edzés / Erősítés": 5.0,
        "Guggolás": 5.0,
    },
}

NAPLO_FILENEV = "edzes_naplo.json"

class EdzesKcalNaplo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fejlett Edzés & Kcal Naplózó")
        self.setGeometry(100, 100, 750, 750)  

        self.naplo = []

        fo_layout = QVBoxLayout()
        
        self.setLayout(fo_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdzesKcalNaplo()
    window.show()
    sys.exit(app.exec())