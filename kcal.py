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
        "Futópadon futás": 10.0,
        "Gyaloglás / Séta": 3.5,
        "Kerékpár": 7.0, 
        "Szobabicikli": 7.0, 
        "Úszás": 8.0,
        "Görkorcsolya": 6.5,
        "Lépcsőzés": 6.0,
        "Lovaglás": 4.0,
        "Sielés": 7.0
    },
    "Erősítés / Izomépítés": {
        "Súlyzós edzés / Erősítés": 5.0,
        "Bicepszhajlítás": 4.0,
        "Fekvenyomás": 5.0,
        "Felülés": 4.0,
        "Plank": 4.0,
        "Guggolás": 5.0,
        "Kitörés": 4.5, 
        "Calisthenics": 6.0,
        "Edzőtermi edzés": 5.0,
        "Favágás": 6.0
    },
    "Küzdősport / Harcművészet": {
        "Birkózás": 8.5,
        "Boksz zsák ütögetés": 9.0,
        "Sparring": 10.0,
        "Karate": 8.0,
        "MMA": 10.0,
        "Kickbox": 9.0,
        "Dzudo": 9.0
    },
    "Szabadidős / Egyéb": {
        "Autoszerelés": 4.0,
        "Bowling": 3.0,
        "Darts": 2.0,
        "Tánc": 6.0,
        "Gimnasztika": 5.0,
        "Jóga": 3.0,
        "Röplabda": 5.0
    }
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
        
        osszes_edzes_plain = [] 
        self.edzes_combo = QComboBox()
        self.combo_model = QStandardItemModel()
        self.edzes_combo.setModel(self.combo_model) 
        
        self._populate_combo_box(self.edzes_combo, EDZESFORMAK_MET, osszes_edzes_plain)
            
        fo_layout.addWidget(self.edzes_combo)

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



    def _populate_combo_box(self, combo_box, edzes_data, plain_list):
        """Feltölti a ComboBoxot kategóriákkal és edzésekkel."""
        self.combo_model.clear()
        
        for csoport_nev, edzesek in edzes_data.items():
            item_sepa = QStandardItem(f"--- {csoport_nev.upper()} ---")
            
            item_sepa.setFlags(item_sepa.flags() & ~Qt.ItemFlag.ItemIsSelectable) 
            self.combo_model.appendRow(item_sepa)
            
            for edzes in edzesek.keys():
                item_edzes = QStandardItem(edzes)
                self.combo_model.appendRow(item_edzes)
                plain_list.append(edzes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdzesKcalNaplo()
    window.show()
    sys.exit(app.exec())