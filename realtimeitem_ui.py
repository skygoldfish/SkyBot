# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'realtimeitem.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(312, 794)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 271, 631))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 251, 591))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_cm_fut_price = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_fut_price.setFont(font)
        self.checkBox_cm_fut_price.setObjectName("checkBox_cm_fut_price")
        self.verticalLayout.addWidget(self.checkBox_cm_fut_price)
        self.checkBox_cm_fut_quote = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_fut_quote.setFont(font)
        self.checkBox_cm_fut_quote.setObjectName("checkBox_cm_fut_quote")
        self.verticalLayout.addWidget(self.checkBox_cm_fut_quote)
        self.checkBox_cm_opt_price = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_opt_price.setFont(font)
        self.checkBox_cm_opt_price.setObjectName("checkBox_cm_opt_price")
        self.verticalLayout.addWidget(self.checkBox_cm_opt_price)
        self.checkBox_cm_opt_price_1 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_opt_price_1.setFont(font)
        self.checkBox_cm_opt_price_1.setObjectName("checkBox_cm_opt_price_1")
        self.verticalLayout.addWidget(self.checkBox_cm_opt_price_1)
        self.checkBox_cm_opt_quote = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_opt_quote.setFont(font)
        self.checkBox_cm_opt_quote.setObjectName("checkBox_cm_opt_quote")
        self.verticalLayout.addWidget(self.checkBox_cm_opt_quote)
        self.checkBox_cm_opt_quote_1 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_cm_opt_quote_1.setFont(font)
        self.checkBox_cm_opt_quote_1.setObjectName("checkBox_cm_opt_quote_1")
        self.verticalLayout.addWidget(self.checkBox_cm_opt_quote_1)
        self.checkBox_nm_fut_price = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_fut_price.setFont(font)
        self.checkBox_nm_fut_price.setObjectName("checkBox_nm_fut_price")
        self.verticalLayout.addWidget(self.checkBox_nm_fut_price)
        self.checkBox_nm_fut_quote = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_fut_quote.setFont(font)
        self.checkBox_nm_fut_quote.setObjectName("checkBox_nm_fut_quote")
        self.verticalLayout.addWidget(self.checkBox_nm_fut_quote)
        self.checkBox_nm_opt_price = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_opt_price.setFont(font)
        self.checkBox_nm_opt_price.setObjectName("checkBox_nm_opt_price")
        self.verticalLayout.addWidget(self.checkBox_nm_opt_price)
        self.checkBox_nm_opt_quote = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_opt_quote.setFont(font)
        self.checkBox_nm_opt_quote.setObjectName("checkBox_nm_opt_quote")
        self.verticalLayout.addWidget(self.checkBox_nm_opt_quote)
        self.checkBox_nm_opt_quote_1 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_opt_quote_1.setFont(font)
        self.checkBox_nm_opt_quote_1.setObjectName("checkBox_nm_opt_quote_1")
        self.verticalLayout.addWidget(self.checkBox_nm_opt_quote_1)
        self.checkBox_kospi_kosdaq = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_kospi_kosdaq.setFont(font)
        self.checkBox_kospi_kosdaq.setObjectName("checkBox_kospi_kosdaq")
        self.verticalLayout.addWidget(self.checkBox_kospi_kosdaq)
        self.checkBox_supply_demand = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_supply_demand.setFont(font)
        self.checkBox_supply_demand.setObjectName("checkBox_supply_demand")
        self.verticalLayout.addWidget(self.checkBox_supply_demand)
        self.checkBox_dow = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_dow.setFont(font)
        self.checkBox_dow.setObjectName("checkBox_dow")
        self.verticalLayout.addWidget(self.checkBox_dow)
        self.checkBox_sp500 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_sp500.setFont(font)
        self.checkBox_sp500.setObjectName("checkBox_sp500")
        self.verticalLayout.addWidget(self.checkBox_sp500)
        self.checkBox_nasdaq = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nasdaq.setFont(font)
        self.checkBox_nasdaq.setObjectName("checkBox_nasdaq")
        self.verticalLayout.addWidget(self.checkBox_nasdaq)
        self.checkBox_oil = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_oil.setFont(font)
        self.checkBox_oil.setObjectName("checkBox_oil")
        self.verticalLayout.addWidget(self.checkBox_oil)
        self.checkBox_eurofx = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_eurofx.setFont(font)
        self.checkBox_eurofx.setObjectName("checkBox_eurofx")
        self.verticalLayout.addWidget(self.checkBox_eurofx)
        self.checkBox_hangseng = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_hangseng.setFont(font)
        self.checkBox_hangseng.setObjectName("checkBox_hangseng")
        self.verticalLayout.addWidget(self.checkBox_hangseng)
        self.checkBox_gold = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_gold.setFont(font)
        self.checkBox_gold.setObjectName("checkBox_gold")
        self.verticalLayout.addWidget(self.checkBox_gold)
        self.checkBox_news = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_news.setFont(font)
        self.checkBox_news.setObjectName("checkBox_news")
        self.verticalLayout.addWidget(self.checkBox_news)
        self.groupBox_1 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 720, 271, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_1.setFont(font)
        self.groupBox_1.setObjectName("groupBox_1")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_1)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 251, 22))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_plot = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_plot.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_plot.setObjectName("lineEdit_plot")
        self.horizontalLayout.addWidget(self.lineEdit_plot)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 650, 271, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 30, 251, 22))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_mp = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEdit_mp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_mp.setObjectName("lineEdit_mp")
        self.horizontalLayout_2.addWidget(self.lineEdit_mp)
        self.label_1 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_2.addWidget(self.label_1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "실시간 설정"))
        self.groupBox.setTitle(_translate("Dialog", "실시간요청 항목"))
        self.checkBox_cm_fut_price.setText(_translate("Dialog", "본월물 선물가격"))
        self.checkBox_cm_fut_quote.setText(_translate("Dialog", "본월물 선물호가"))
        self.checkBox_cm_opt_price.setText(_translate("Dialog", "본월물 옵션가격(전체)"))
        self.checkBox_cm_opt_price_1.setText(_translate("Dialog", "본월물 옵션가격"))
        self.checkBox_cm_opt_quote.setText(_translate("Dialog", "본월물 옵션호가(전체)"))
        self.checkBox_cm_opt_quote_1.setText(_translate("Dialog", "본월물 옵션호가"))
        self.checkBox_nm_fut_price.setText(_translate("Dialog", "차월물 선물가격"))
        self.checkBox_nm_fut_quote.setText(_translate("Dialog", "차월물 선물호가"))
        self.checkBox_nm_opt_price.setText(_translate("Dialog", "차월물 옵션가격"))
        self.checkBox_nm_opt_quote.setText(_translate("Dialog", "차월물 옵션호가(전체)"))
        self.checkBox_nm_opt_quote_1.setText(_translate("Dialog", "차월물 옵션호가"))
        self.checkBox_kospi_kosdaq.setText(_translate("Dialog", "KOSPI/KOSDAQ 지수"))
        self.checkBox_supply_demand.setText(_translate("Dialog", "투자자별 매매현황"))
        self.checkBox_dow.setText(_translate("Dialog", "DOW"))
        self.checkBox_sp500.setText(_translate("Dialog", "SP500"))
        self.checkBox_nasdaq.setText(_translate("Dialog", "NASDAQ"))
        self.checkBox_oil.setText(_translate("Dialog", "WTI OIL"))
        self.checkBox_eurofx.setText(_translate("Dialog", "EUROFX"))
        self.checkBox_hangseng.setText(_translate("Dialog", "HANGSENG"))
        self.checkBox_gold.setText(_translate("Dialog", "GOLD"))
        self.checkBox_news.setText(_translate("Dialog", "NEWS"))
        self.groupBox_1.setTitle(_translate("Dialog", "Plot 갱신주기"))
        self.label.setText(_translate("Dialog", "msec"))
        self.groupBox_2.setTitle(_translate("Dialog", "Data 갱신주기"))
        self.label_1.setText(_translate("Dialog", "msec"))

