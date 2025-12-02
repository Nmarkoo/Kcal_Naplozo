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
        self.setStyleSheet(self._get_style_sheet()) 

        self.naplo = []
        self._betolt_naplot() 

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

        datum_kereso_layout = QHBoxLayout()
        datum_kereso_layout.addWidget(QLabel("Dátum (szűrés):"))
        self.szuro_datum = QDateEdit(QDate.currentDate())
        self.szuro_datum.setCalendarPopup(True)
        self.szuro_datum.setDate(QDate.currentDate())
        self.szuro_datum.dateChanged.connect(self._frissit_naplo_listat_szurve)
        datum_kereso_layout.addWidget(self.szuro_datum)

        self.kereso_mezo = QLineEdit()
        self.kereso_mezo.setPlaceholderText("Keresés az edzések között...")
        datum_kereso_layout.addWidget(self.kereso_mezo)
        fo_layout.addLayout(datum_kereso_layout)

        osszes_edzes_plain = [] 
        self.edzes_combo = QComboBox()
        self.combo_model = QStandardItemModel()
        self.edzes_combo.setModel(self.combo_model) 
        
        self._populate_combo_box(self.edzes_combo, EDZESFORMAK_MET, osszes_edzes_plain)
        self.edzes_combo.currentTextChanged.connect(self._frissit_extra_mezo)
            
        fo_layout.addWidget(self.edzes_combo)
        
        kieg = QCompleter(osszes_edzes_plain)
        kieg.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.kereso_mezo.setCompleter(kieg)
        self.kereso_mezo.textChanged.connect(self.szures)

        extra_layout = QHBoxLayout()
        self.extra_label = QLabel("Kiegészítő adat:")
        self.extra_input = QLineEdit()
        self.extra_input.setPlaceholderText("Adj meg Sebességet (km/h) a biciklihez")
        self.extra_input.setValidator(QDoubleValidator(1.0, 99.9, 1))
        
        extra_layout.addWidget(self.extra_label)
        extra_layout.addWidget(self.extra_input)
        fo_layout.addLayout(extra_layout)
        
        self._frissit_extra_mezo(self.edzes_combo.currentText())

        ido_layout = QHBoxLayout()
        self.ido_label = QLabel("Időtartam (perc):")
        self.ido_input = QLineEdit()
        self.ido_input.setPlaceholderText("Pozitív egész szám")
        self.ido_input.setValidator(QIntValidator(1, 999))
        ido_layout.addWidget(self.ido_label)
        ido_layout.addWidget(self.ido_input)
        fo_layout.addLayout(ido_layout)
        
        gombok_layout = QHBoxLayout()
        self.hozzaad_gomb = QPushButton("✅ Hozzáadás a naplóhoz")
        self.hozzaad_gomb.clicked.connect(self.hozzaad_edzest)
        self.torles_gomb = QPushButton("❌ Kijelölt törlése")
        self.torles_gomb.clicked.connect(self._torol_kijeloltet)
        gombok_layout.addWidget(self.hozzaad_gomb)
        gombok_layout.addWidget(self.torles_gomb)
        fo_layout.addLayout(gombok_layout)

        self.naplo_list = QListWidget() 
        fo_layout.addWidget(self.naplo_list)

        self.ossz_kcal_label = QLabel("Összesített kcal a mai napra: 0.0 kcal")
        self.ossz_kcal_label.setObjectName("OsszKcalLabel")
        fo_layout.addWidget(self.ossz_kcal_label)
        
        self.setLayout(fo_layout)
        self._frissit_naplo_listat_szurve()


    def _populate_combo_box(self, combo_box, edzes_data, plain_list):
        self.combo_model.clear()
        
        for csoport_nev, edzesek in edzes_data.items():
            item_sepa = QStandardItem(f"--- {csoport_nev.upper()} ---")
            item_sepa.setFlags(item_sepa.flags() & ~Qt.ItemFlag.ItemIsSelectable) 
            self.combo_model.appendRow(item_sepa)
            
            for edzes in edzesek.keys():
                item_edzes = QStandardItem(edzes)
                self.combo_model.appendRow(item_edzes)
                plain_list.append(edzes)

    def _frissit_extra_mezo(self, edzes):
        if edzes in ["Kerékpár", "Szobabicikli"]:
            self.extra_label.setText("Sebesség (km/h):")
            self.extra_input.setPlaceholderText("Kerékpározás sebessége km/h-ban")
            self.extra_label.setVisible(True)
            self.extra_input.setVisible(True)
        else:
            self.extra_label.setText("Kiegészítő adat:")
            self.extra_input.setPlaceholderText("Csak a Kerékpározáshoz szükséges")
            self.extra_label.setVisible(False)
            self.extra_input.setVisible(False)
            self.extra_input.clear()

    def _betolt_naplot(self):
        try:
            with open(NAPLO_FILENEV, 'r', encoding='utf-8') as f:
                self.naplo = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.naplo = []

    def _ment_naplot(self):
        try:
            with open(NAPLO_FILENEV, 'w', encoding='utf-8') as f:
                json.dump(self.naplo, f, indent=4)
        except IOError:
            QMessageBox.warning(self, "Hiba", "Nem sikerült elmenteni a naplót a lemezre!")
    
    def _frissit_naplo_listat_szurve(self):
        kivalasztott_datum = self.szuro_datum.date().toString(Qt.DateFormat.ISODate)
        
        self.naplo_list.clear()
        napi_osszeg = 0.0
        
        for i, bejegyzes in enumerate(self.naplo):
            if bejegyzes['datum'] == kivalasztott_datum:
                kcal = bejegyzes['kcal']
                ido = bejegyzes['perc']
                edzes = bejegyzes['edzes']
                
                extra_info = ""
                if bejegyzes.get('sebesseg') is not None:
                    extra_info = f", {bejegyzes['sebesseg']:.1f} km/h"
                        
                list_item_text = (
                    f"({edzes}) [MET: {bejegyzes.get('met_ertek', '?'):.1f}] - "
                    f"{bejegyzes['testsuly']:.1f} kg ({bejegyzes.get('nem', '?')})"
                    f"{extra_info} - "
                    f"{ido} perc - "
                    f"**{kcal:.1f} kcal**"
                )
                
                item = QListWidgetItem(list_item_text)
                item.setData(Qt.ItemDataRole.UserRole, i) 
                self.naplo_list.addItem(item)
                
                napi_osszeg += kcal
                
        self.ossz_kcal_label.setText(f"Összesített kcal a {kivalasztott_datum} napra: {napi_osszeg:.1f} kcal")
        
        if not self.naplo_list.count():
            self.naplo_list.addItem(f"Nincs bejegyzés a(z) {kivalasztott_datum} napon.")

    def _torol_kijeloltet(self):
        kijelolt_elem = self.naplo_list.currentItem()
        
        if kijelolt_elem is None:
            QMessageBox.information(self, "Információ", "Kérjük, válassz ki egy elemet a törléshez.")
            return

        eredeti_index = kijelolt_elem.data(Qt.ItemDataRole.UserRole)
        
        if eredeti_index is not None and eredeti_index >= 0 and eredeti_index < len(self.naplo):
            del self.naplo[eredeti_index]
            self._ment_naplot() 
            self._frissit_naplo_listat_szurve()
        else:
            QMessageBox.warning(self, "Hiba", "Nem található a kijelölt bejegyzés az adatbázisban.")
    
    def szures(self, szoveg):
        self.edzes_combo.blockSignals(True) 
        self.combo_model.clear()
        
        szurt_talalat = False
        osszes_edzes_plain = []
        
        for csoport_nev, edzesek in EDZESFORMAK_MET.items():
            szurt_csoport = [edz for edz in edzesek.keys() if szoveg.lower() in edz.lower()]
            
            if szurt_csoport:
                szurt_talalat = True
                
                item_sepa = QStandardItem(f"--- {csoport_nev.upper()} ---")
                item_sepa.setFlags(item_sepa.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.combo_model.appendRow(item_sepa)
                
                for edzes in szurt_csoport:
                    item_edzes = QStandardItem(edzes)
                    self.combo_model.appendRow(item_edzes)
            
        if not szurt_talalat and not szoveg:
              self._populate_combo_box(self.edzes_combo, EDZESFORMAK_MET, osszes_edzes_plain)
        elif not szurt_talalat:
              self.combo_model.appendRow(QStandardItem("Nincs találat"))

        self.edzes_combo.blockSignals(False)


    def hozzaad_edzest(self):
        edzes = self.edzes_combo.currentText()
        
        if edzes.startswith("---") or edzes == "Nincs találat":
            QMessageBox.warning(self, "Hiba", "Válassz ki egy érvényes edzésformát!")
            return

        try:
            perc = float(self.ido_input.text())
            testsuly = float(self.suly_input.text())
            magassag = float(self.magassag_input.text())
            if perc <= 0 or testsuly <= 0 or magassag <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hiba", "Ellenőrizd a bemenetet! Az összes alap numerikus mezőnek pozitív számnak kell lennie.")
            return

        met_ertek = 0
        sebesseg = None
        
        if edzes in ["Kerékpár", "Szobabicikli"]:
            try:
                sebesseg = float(self.extra_input.text())
                if sebesseg <= 0: raise ValueError
                
                if sebesseg < 16: 
                    met_ertek = 4.0
                elif sebesseg < 24: 
                    met_ertek = 8.0
                else: 
                    met_ertek = 12.0
            except ValueError:
                QMessageBox.warning(self, "Hiba", "Kérjük, adj meg érvényes sebességet (km/h) a kerékpározáshoz!")
                return
        else:
            for csoport in EDZESFORMAK_MET.values():
                if edzes in csoport:
                    met_ertek = csoport[edzes]
                    break
        
        if met_ertek == 0:
              QMessageBox.warning(self, "Hiba", "Nem található MET érték ehhez az edzéshez.")
              return

        ido_ora = perc / 60
        kcal = met_ertek * testsuly * ido_ora * 1.05
        
        naplo_item = {
            'datum': self.szuro_datum.date().toString(Qt.DateFormat.ISODate),
            'edzes': edzes,
            'testsuly': testsuly,
            'magassag': magassag, 
            'nem': self.nem_combo.currentText(),
            'perc': perc,
            'kcal': kcal,
            'met_ertek': met_ertek,
            'sebesseg': sebesseg
        }
        self.naplo.append(naplo_item)
        self._ment_naplot() 
        
        self._frissit_naplo_listat_szurve()
        
        QMessageBox.information(self, "Sikeres Rögzítés", 
                                f"Rögzítve: {edzes} ({perc} perc) - {kcal:.1f} kcal elégetve.")
        
        self.ido_input.clear()
        self.extra_input.clear()
        self.kereso_mezo.clear()

    def closeEvent(self, event):
        self._ment_naplot()
        event.accept()

    def _get_style_sheet(self):
        return """
            QWidget {
                background-color: #f0f4f8;
                color: #333;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#OsszKcalLabel {
                font-size: 18px;
                font-weight: bold;
                color: #007bff;
                padding: 8px;
                border: 1px solid #007bff;
                border-radius: 5px;
                margin-top: 10px;
                background-color: #e6f0ff;
                text-align: center;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QComboBox, QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
                selection-background-color: #007bff;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background: white;
                min-height: 200px;
            }
            QComboBox QAbstractItemView::item {
                padding: 5px;
            }
            QComboBox::item:has-text(---) {
                background-color: #333;
                color: white;
                font-weight: bold;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdzesKcalNaplo()
    window.show()
    sys.exit(app.exec())