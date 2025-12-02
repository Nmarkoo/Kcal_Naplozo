# -*- coding: utf-8 -*-

import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QComboBox, QListWidget, QCompleter, QDateEdit, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QStandardItem, QStandardItemModel 

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
        
        felhasznalo_layout = QHBoxLayout()
        
        felhasznalo_layout.addWidget(QLabel("Testsúly (kg):"))
        self.suly_input = QLineEdit("70")
        self.suly_input.setFixedWidth(50)
        self.suly_input.setValidator(QDoubleValidator(10.0, 300.0, 1))
        felhasznalo_layout.addWidget(self.suly_input)
        
        felhasznalo_layout.addWidget(QLabel("Magasság (cm):"))
        self.magassag_input = QLineEdit("175")
        self.magassag_input.setFixedWidth(50)
        self.magassag_input.setValidator(QIntValidator(100, 250))
        felhasznalo_layout.addWidget(self.magassag_input)
        
        felhasznalo_layout.addWidget(QLabel("Nem:"))
        self.nem_combo = QComboBox()
        self.nem_combo.addItems(["Férfi", "Nő"])
        self.nem_combo.setFixedWidth(60)
        felhasznalo_layout.addWidget(self.nem_combo)
        
        felhasznalo_layout.addStretch(1)
        fo_layout.addLayout(felhasznalo_layout)

        ido_layout = QHBoxLayout()
        self.ido_label = QLabel("Időtartam (perc):")
        self.ido_input = QLineEdit()
        self.ido_input.setPlaceholderText("Pozitív egész szám")
        self.ido_input.setValidator(QIntValidator(1, 999))
        ido_layout.addWidget(self.ido_label)
        ido_layout.addWidget(self.ido_input)
        fo_layout.addLayout(ido_layout)
        
        gombok_layout = QHBoxLayout()
        fo_layout.addLayout(gombok_layout)
        
        self.setLayout(fo_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdzesKcalNaplo()
    window.show()
    sys.exit(app.exec())