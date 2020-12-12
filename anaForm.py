#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import os
from edefter import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
import sqlite3

###########################################################################
class AnaForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(AnaForm, self).__init__()
        self.data = pd.DataFrame()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonListeCek.clicked.connect(self.listeCek)
        #self.listeCek()
        self.ui.buttonKaydet.clicked.connect(self.EKLE)
        #self.Kaydet()
        
        
        #VERİTABANI OLUŞTUR
        global curs
        global conn
        conn =sqlite3.connect('okul.db')
        curs =conn.cursor()

        sorguCreTblDersler=("CREATE TABLE IF NOT EXISTS Dersler(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                 Sinif TEXT NOT NULL,                        \
                 Ogradi TEXT NOT NULL,                          \
                 Dersadi TEXT NOT NULL,                       \
                 Konukazanim TEXT NOT NULL,                           \
                 Tarih TEXT NOT NULL)")
        curs.execute(sorguCreTblDersler)
        conn.commit()

    def listeCek(self):
        # print('Dosya yolu alınır')
        dosyaAdi = QtWidgets.QFileDialog.getOpenFileName(self, 'dosya aranıyor', os.getenv('Masaüstü'))
        # print(dosyaAdi)

        self.excell_file =  dosyaAdi[0] #'5a.XLS'  ## excel dosya yolu
        self.sinif_listesi = pd.read_excel(self.excell_file)  ## pandas ile excel okunur
        self.boslukTemizle()  ## Boş sütunlar temizlenir.

    def boslukTemizle(self):  # gereksiz hücreler temizlenir
        satirSayisi = self.sinif_listesi.shape[0]
        self.data = self.sinif_listesi.iloc[0:satirSayisi - 2]  # son 2 satır silindi
        self.data = self.data[['S.No', 'Öğrenci No', 'Adı', 'Soyadı', 'Cinsiyeti']]  ## gerekli sütunlar alındı
        self.tableLoad()  ## ANA FORMA LİSTELERİ YAZMA

    def tableLoad(self):
        self.data = self.data.values.tolist()

        self.ui.tableWSinifListele.setRowCount(len(self.data))
        self.ui.tableWSinifListele.setColumnCount(5)
        self.ui.tableWSinifListele.setHorizontalHeaderLabels(('Öğrenci No','Adı', 'Soyadı', 'Cinsiyeti','GELMEDİ'))
        self.ui.tableWSinifListele.setColumnWidth(0,100)
        self.ui.tableWSinifListele.setColumnWidth(1,100)

        rowIndex = 0
        for i in self.data:
            ono = str(int(i[1]))
            adi = i[2]
            soyadi = i[3]
            cinsiyeti = i[4]
        
            self.ui.tableWSinifListele.setItem(rowIndex, 0, QTableWidgetItem(ono))
            self.ui.tableWSinifListele.setItem(rowIndex, 1, QTableWidgetItem(adi))
            self.ui.tableWSinifListele.setItem(rowIndex, 2, QTableWidgetItem(soyadi))
            self.ui.tableWSinifListele.setItem(rowIndex, 3, QTableWidgetItem(cinsiyeti))
            rowIndex += 1
    
    
    def EKLE(self):
        sinif = self.ui.comboSinif.currentText()
        ogrAdi = self.ui.lineOgrtAdi.text()
        dersAdi =self.ui.lineDersAdi.text()
        konuKazanim = self.ui.lineKonu.text()
        tarih = self.ui.lineTarih.text()
    
        curs.execute("INSERT INTO Dersler \
                     (Sinif,Ogradi,Dersadi,Konukazanim,Tarih) \
                      VALUES (?,?,?,?,?)", \
                      (sinif,ogrAdi,dersAdi,konuKazanim,tarih))
        conn.commit()
        print("Kayıt Başarılı")
        QMessageBox.about(self, "e-defter-DATABASE", "Kayıt işlemi başarılı..")
    

def anaform():
    app = QtWidgets.QApplication(sys.argv)
    win = AnaForm()
    win.setWindowTitle("E-Defter")
    win.show()
    sys.exit(app.exec_())

anaform()



