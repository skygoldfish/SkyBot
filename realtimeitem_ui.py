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
        Dialog.resize(356, 891)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 317, 541))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 26, 291, 506))
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
        self.checkBox_nm_opt_price_1 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nm_opt_price_1.setFont(font)
        self.checkBox_nm_opt_price_1.setObjectName("checkBox_nm_opt_price_1")
        self.verticalLayout.addWidget(self.checkBox_nm_opt_price_1)
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
        self.checkBox_news = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_news.setFont(font)
        self.checkBox_news.setObjectName("checkBox_news")
        self.verticalLayout.addWidget(self.checkBox_news)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_sp500 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_sp500.setFont(font)
        self.checkBox_sp500.setObjectName("checkBox_sp500")
        self.horizontalLayout_5.addWidget(self.checkBox_sp500)
        self.checkBox_dow = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_dow.setFont(font)
        self.checkBox_dow.setObjectName("checkBox_dow")
        self.horizontalLayout_5.addWidget(self.checkBox_dow)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_nasdaq = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nasdaq.setFont(font)
        self.checkBox_nasdaq.setObjectName("checkBox_nasdaq")
        self.horizontalLayout_6.addWidget(self.checkBox_nasdaq)
        self.checkBox_hangseng = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_hangseng.setFont(font)
        self.checkBox_hangseng.setObjectName("checkBox_hangseng")
        self.horizontalLayout_6.addWidget(self.checkBox_hangseng)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox_oil = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_oil.setFont(font)
        self.checkBox_oil.setObjectName("checkBox_oil")
        self.horizontalLayout_7.addWidget(self.checkBox_oil)
        self.checkBox_gold = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_gold.setFont(font)
        self.checkBox_gold.setObjectName("checkBox_gold")
        self.horizontalLayout_7.addWidget(self.checkBox_gold)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.checkBox_eurofx = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_eurofx.setFont(font)
        self.checkBox_eurofx.setObjectName("checkBox_eurofx")
        self.horizontalLayout_8.addWidget(self.checkBox_eurofx)
        self.checkBox_yen = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_yen.setFont(font)
        self.checkBox_yen.setObjectName("checkBox_yen")
        self.horizontalLayout_8.addWidget(self.checkBox_yen)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.checkBox_adi = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_adi.setFont(font)
        self.checkBox_adi.setObjectName("checkBox_adi")
        self.horizontalLayout_9.addWidget(self.checkBox_adi)
        self.checkBox_reserved1 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_reserved1.setFont(font)
        self.checkBox_reserved1.setObjectName("checkBox_reserved1")
        self.horizontalLayout_9.addWidget(self.checkBox_reserved1)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.groupBox_1 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 720, 317, 57))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_1.setFont(font)
        self.groupBox_1.setObjectName("groupBox_1")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_1)
        self.layoutWidget1.setGeometry(QtCore.QRect(14, 24, 287, 21))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_drate_ratio = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_drate_ratio.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_drate_ratio.setObjectName("lineEdit_drate_ratio")
        self.horizontalLayout.addWidget(self.lineEdit_drate_ratio)
        self.lineEdit_tolerance = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_tolerance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_tolerance.setObjectName("lineEdit_tolerance")
        self.horizontalLayout.addWidget(self.lineEdit_tolerance)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_plot = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_plot.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_plot.setObjectName("lineEdit_plot")
        self.horizontalLayout.addWidget(self.lineEdit_plot)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Consolas")
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
        self.groupBox_2.setGeometry(QtCore.QRect(20, 658, 317, 55))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(14, 24, 289, 21))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_bb_period = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_bb_period.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_bb_period.setObjectName("lineEdit_bb_period")
        self.horizontalLayout_2.addWidget(self.lineEdit_bb_period)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_bb_1st_std = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_bb_1st_std.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_bb_1st_std.setObjectName("lineEdit_bb_1st_std")
        self.horizontalLayout_2.addWidget(self.lineEdit_bb_1st_std)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_bb_2nd_std = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_bb_2nd_std.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_bb_2nd_std.setObjectName("lineEdit_bb_2nd_std")
        self.horizontalLayout_2.addWidget(self.lineEdit_bb_2nd_std)
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.lineEdit_rsi_period = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_rsi_period.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_rsi_period.setObjectName("lineEdit_rsi_period")
        self.horizontalLayout_2.addWidget(self.lineEdit_rsi_period)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 2)
        self.horizontalLayout_2.setStretch(3, 4)
        self.horizontalLayout_2.setStretch(4, 2)
        self.horizontalLayout_2.setStretch(5, 2)
        self.horizontalLayout_2.setStretch(6, 3)
        self.horizontalLayout_2.setStretch(7, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 558, 317, 91))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(12, 60, 291, 22))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_put_itm = QtWidgets.QLabel(self.layoutWidget3)
        self.label_put_itm.setObjectName("label_put_itm")
        self.horizontalLayout_3.addWidget(self.label_put_itm)
        self.spinBox_put_itm = QtWidgets.QSpinBox(self.layoutWidget3)
        self.spinBox_put_itm.setObjectName("spinBox_put_itm")
        self.horizontalLayout_3.addWidget(self.spinBox_put_itm)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_put_otm = QtWidgets.QLabel(self.layoutWidget3)
        self.label_put_otm.setObjectName("label_put_otm")
        self.horizontalLayout_3.addWidget(self.label_put_otm)
        self.spinBox_put_otm = QtWidgets.QSpinBox(self.layoutWidget3)
        self.spinBox_put_otm.setObjectName("spinBox_put_otm")
        self.horizontalLayout_3.addWidget(self.spinBox_put_otm)
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget4.setGeometry(QtCore.QRect(12, 30, 291, 22))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_call_itm = QtWidgets.QLabel(self.layoutWidget4)
        self.label_call_itm.setObjectName("label_call_itm")
        self.horizontalLayout_4.addWidget(self.label_call_itm)
        self.spinBox_call_itm = QtWidgets.QSpinBox(self.layoutWidget4)
        self.spinBox_call_itm.setObjectName("spinBox_call_itm")
        self.horizontalLayout_4.addWidget(self.spinBox_call_itm)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.label_call_otm = QtWidgets.QLabel(self.layoutWidget4)
        self.label_call_otm.setObjectName("label_call_otm")
        self.horizontalLayout_4.addWidget(self.label_call_otm)
        self.spinBox_call_otm = QtWidgets.QSpinBox(self.layoutWidget4)
        self.spinBox_call_otm.setObjectName("spinBox_call_otm")
        self.horizontalLayout_4.addWidget(self.spinBox_call_otm)
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 782, 317, 83))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.widget1 = QtWidgets.QWidget(self.groupBox_4)
        self.widget1.setGeometry(QtCore.QRect(15, 25, 287, 48))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_periodic_plot = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_periodic_plot.setObjectName("checkBox_periodic_plot")
        self.verticalLayout_3.addWidget(self.checkBox_periodic_plot)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.checkBox_plot_sync = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_plot_sync.setObjectName("checkBox_plot_sync")
        self.horizontalLayout_10.addWidget(self.checkBox_plot_sync)
        self.checkBox_tts = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_tts.setObjectName("checkBox_tts")
        self.horizontalLayout_10.addWidget(self.checkBox_tts)
        self.checkBox_telegram = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_telegram.setObjectName("checkBox_telegram")
        self.horizontalLayout_10.addWidget(self.checkBox_telegram)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

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
        self.checkBox_nm_opt_price.setText(_translate("Dialog", "차월물 옵션가격(전체)"))
        self.checkBox_nm_opt_price_1.setText(_translate("Dialog", "차월물 옵션가격"))
        self.checkBox_nm_opt_quote.setText(_translate("Dialog", "차월물 옵션호가(전체)"))
        self.checkBox_nm_opt_quote_1.setText(_translate("Dialog", "차월물 옵션호가"))
        self.checkBox_kospi_kosdaq.setText(_translate("Dialog", "KOSPI/KOSDAQ 지수"))
        self.checkBox_supply_demand.setText(_translate("Dialog", "투자자별 매매현황"))
        self.checkBox_news.setText(_translate("Dialog", "NEWS"))
        self.checkBox_sp500.setText(_translate("Dialog", "S&&P 500"))
        self.checkBox_dow.setText(_translate("Dialog", "DOW"))
        self.checkBox_nasdaq.setText(_translate("Dialog", "NASDAQ"))
        self.checkBox_hangseng.setText(_translate("Dialog", "HANGSENG"))
        self.checkBox_oil.setText(_translate("Dialog", "WTI OIL"))
        self.checkBox_gold.setText(_translate("Dialog", "GOLD"))
        self.checkBox_eurofx.setText(_translate("Dialog", "EUROFX"))
        self.checkBox_yen.setText(_translate("Dialog", "YEN"))
        self.checkBox_adi.setText(_translate("Dialog", "ADI"))
        self.checkBox_reserved1.setText(_translate("Dialog", "Reserved"))
        self.groupBox_1.setTitle(_translate("Dialog", "선물vsSP500 등락율비, 허용오차, Plot 갱신주기"))
        self.label_2.setText(_translate("Dialog", "sec"))
        self.label.setText(_translate("Dialog", "msec"))
        self.groupBox_2.setTitle(_translate("Dialog", "볼린저(주기, 1st STD, 2nd STD), RSI 주기"))
        self.label_5.setText(_translate("Dialog", "B주기"))
        self.label_3.setText(_translate("Dialog", "1st"))
        self.label_4.setText(_translate("Dialog", "2nd"))
        self.label_6.setText(_translate("Dialog", "R주기"))
        self.groupBox_3.setTitle(_translate("Dialog", "내가, 외가 설정"))
        self.label_put_itm.setText(_translate("Dialog", "풋내가"))
        self.label_put_otm.setText(_translate("Dialog", "풋외가"))
        self.label_call_itm.setText(_translate("Dialog", "콜내가"))
        self.label_call_otm.setText(_translate("Dialog", "콜외가"))
        self.groupBox_4.setTitle(_translate("Dialog", "User Switch"))
        self.checkBox_periodic_plot.setText(_translate("Dialog", "Option Table Periodic Update"))
        self.checkBox_plot_sync.setText(_translate("Dialog", "Plot Sync"))
        self.checkBox_tts.setText(_translate("Dialog", "TTS"))
        self.checkBox_telegram.setText(_translate("Dialog", "Telegram"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

