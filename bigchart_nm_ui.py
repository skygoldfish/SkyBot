# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bigchart_nm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1747, 905)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/skybot_nm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_time = QtWidgets.QLabel(Dialog)
        self.label_time.setObjectName("label_time")
        self.horizontalLayout.addWidget(self.label_time)
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBox1 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox1.setFont(font)
        self.comboBox1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox1.setObjectName("comboBox1")
        self.horizontalLayout.addWidget(self.comboBox1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_41 = QtWidgets.QLabel(Dialog)
        self.label_41.setObjectName("label_41")
        self.horizontalLayout_17.addWidget(self.label_41)
        self.label_42 = QtWidgets.QLabel(Dialog)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_17.addWidget(self.label_42)
        self.label_43 = QtWidgets.QLabel(Dialog)
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_17.addWidget(self.label_43)
        self.label_44 = QtWidgets.QLabel(Dialog)
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_17.addWidget(self.label_44)
        self.label_45 = QtWidgets.QLabel(Dialog)
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_17.addWidget(self.label_45)
        self.label_46 = QtWidgets.QLabel(Dialog)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_17.addWidget(self.label_46)
        self.label_47 = QtWidgets.QLabel(Dialog)
        self.label_47.setObjectName("label_47")
        self.horizontalLayout_17.addWidget(self.label_47)
        self.label_48 = QtWidgets.QLabel(Dialog)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_17.addWidget(self.label_48)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem1)
        self.comboBox4 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox4.setFont(font)
        self.comboBox4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox4.setObjectName("comboBox4")
        self.horizontalLayout_17.addWidget(self.comboBox4)
        self.gridLayout.addLayout(self.horizontalLayout_17, 0, 1, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.plot1 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot1.setFont(font)
        self.plot1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot1.setObjectName("plot1")
        self.horizontalLayout_10.addWidget(self.plot1)
        self.groupBox1 = QtWidgets.QGroupBox(Dialog)
        self.groupBox1.setObjectName("groupBox1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBox_plot1_bband = QtWidgets.QCheckBox(self.groupBox1)
        self.checkBox_plot1_bband.setObjectName("checkBox_plot1_bband")
        self.verticalLayout_6.addWidget(self.checkBox_plot1_bband)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_plot1_oe = QtWidgets.QCheckBox(self.groupBox1)
        self.checkBox_plot1_oe.setObjectName("checkBox_plot1_oe")
        self.horizontalLayout_4.addWidget(self.checkBox_plot1_oe)
        self.checkBox_plot1_mama = QtWidgets.QCheckBox(self.groupBox1)
        self.checkBox_plot1_mama.setObjectName("checkBox_plot1_mama")
        self.horizontalLayout_4.addWidget(self.checkBox_plot1_mama)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.label_p1_1 = QtWidgets.QLabel(self.groupBox1)
        self.label_p1_1.setObjectName("label_p1_1")
        self.verticalLayout_6.addWidget(self.label_p1_1)
        self.label_p1_2 = QtWidgets.QLabel(self.groupBox1)
        self.label_p1_2.setObjectName("label_p1_2")
        self.verticalLayout_6.addWidget(self.label_p1_2)
        self.label_p1_3 = QtWidgets.QLabel(self.groupBox1)
        self.label_p1_3.setObjectName("label_p1_3")
        self.verticalLayout_6.addWidget(self.label_p1_3)
        self.label_p1_4 = QtWidgets.QLabel(self.groupBox1)
        self.label_p1_4.setObjectName("label_p1_4")
        self.verticalLayout_6.addWidget(self.label_p1_4)
        self.horizontalLayout_10.addWidget(self.groupBox1)
        self.gridLayout.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.plot4 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot4.setFont(font)
        self.plot4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot4.setObjectName("plot4")
        self.horizontalLayout_15.addWidget(self.plot4)
        self.groupBox1_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox1_3.setObjectName("groupBox1_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox1_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_plot4_bband = QtWidgets.QCheckBox(self.groupBox1_3)
        self.checkBox_plot4_bband.setObjectName("checkBox_plot4_bband")
        self.verticalLayout.addWidget(self.checkBox_plot4_bband)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.checkBox_plot4_oe = QtWidgets.QCheckBox(self.groupBox1_3)
        self.checkBox_plot4_oe.setObjectName("checkBox_plot4_oe")
        self.horizontalLayout_9.addWidget(self.checkBox_plot4_oe)
        self.checkBox_plot4_mama = QtWidgets.QCheckBox(self.groupBox1_3)
        self.checkBox_plot4_mama.setObjectName("checkBox_plot4_mama")
        self.horizontalLayout_9.addWidget(self.checkBox_plot4_mama)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.label_p4_1 = QtWidgets.QLabel(self.groupBox1_3)
        self.label_p4_1.setObjectName("label_p4_1")
        self.verticalLayout.addWidget(self.label_p4_1)
        self.label_p4_2 = QtWidgets.QLabel(self.groupBox1_3)
        self.label_p4_2.setObjectName("label_p4_2")
        self.verticalLayout.addWidget(self.label_p4_2)
        self.label_p4_3 = QtWidgets.QLabel(self.groupBox1_3)
        self.label_p4_3.setObjectName("label_p4_3")
        self.verticalLayout.addWidget(self.label_p4_3)
        self.label_p4_4 = QtWidgets.QLabel(self.groupBox1_3)
        self.label_p4_4.setObjectName("label_p4_4")
        self.verticalLayout.addWidget(self.label_p4_4)
        self.horizontalLayout_15.addWidget(self.groupBox1_3)
        self.gridLayout.addLayout(self.horizontalLayout_15, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_2.addWidget(self.label_21)
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_2.addWidget(self.label_22)
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_2.addWidget(self.label_23)
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_2.addWidget(self.label_24)
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_2.addWidget(self.label_25)
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_2.addWidget(self.label_26)
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_2.addWidget(self.label_27)
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_2.addWidget(self.label_28)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.comboBox2 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox2.setFont(font)
        self.comboBox2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox2.setObjectName("comboBox2")
        self.horizontalLayout_2.addWidget(self.comboBox2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_51 = QtWidgets.QLabel(Dialog)
        self.label_51.setObjectName("label_51")
        self.horizontalLayout_19.addWidget(self.label_51)
        self.label_52 = QtWidgets.QLabel(Dialog)
        self.label_52.setObjectName("label_52")
        self.horizontalLayout_19.addWidget(self.label_52)
        self.label_53 = QtWidgets.QLabel(Dialog)
        self.label_53.setObjectName("label_53")
        self.horizontalLayout_19.addWidget(self.label_53)
        self.label_54 = QtWidgets.QLabel(Dialog)
        self.label_54.setObjectName("label_54")
        self.horizontalLayout_19.addWidget(self.label_54)
        self.label_55 = QtWidgets.QLabel(Dialog)
        self.label_55.setObjectName("label_55")
        self.horizontalLayout_19.addWidget(self.label_55)
        self.label_56 = QtWidgets.QLabel(Dialog)
        self.label_56.setObjectName("label_56")
        self.horizontalLayout_19.addWidget(self.label_56)
        self.label_57 = QtWidgets.QLabel(Dialog)
        self.label_57.setObjectName("label_57")
        self.horizontalLayout_19.addWidget(self.label_57)
        self.label_58 = QtWidgets.QLabel(Dialog)
        self.label_58.setObjectName("label_58")
        self.horizontalLayout_19.addWidget(self.label_58)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem3)
        self.comboBox5 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox5.setFont(font)
        self.comboBox5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox5.setObjectName("comboBox5")
        self.horizontalLayout_19.addWidget(self.comboBox5)
        self.gridLayout.addLayout(self.horizontalLayout_19, 2, 1, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.plot2 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot2.setFont(font)
        self.plot2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot2.setObjectName("plot2")
        self.horizontalLayout_11.addWidget(self.plot2)
        self.groupBox2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox2.setObjectName("groupBox2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.checkBox_plot2_bband = QtWidgets.QCheckBox(self.groupBox2)
        self.checkBox_plot2_bband.setObjectName("checkBox_plot2_bband")
        self.verticalLayout_5.addWidget(self.checkBox_plot2_bband)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_plot2_oe = QtWidgets.QCheckBox(self.groupBox2)
        self.checkBox_plot2_oe.setObjectName("checkBox_plot2_oe")
        self.horizontalLayout_5.addWidget(self.checkBox_plot2_oe)
        self.checkBox_plot2_mama = QtWidgets.QCheckBox(self.groupBox2)
        self.checkBox_plot2_mama.setObjectName("checkBox_plot2_mama")
        self.horizontalLayout_5.addWidget(self.checkBox_plot2_mama)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.label_p2_1 = QtWidgets.QLabel(self.groupBox2)
        self.label_p2_1.setObjectName("label_p2_1")
        self.verticalLayout_5.addWidget(self.label_p2_1)
        self.label_p2_2 = QtWidgets.QLabel(self.groupBox2)
        self.label_p2_2.setObjectName("label_p2_2")
        self.verticalLayout_5.addWidget(self.label_p2_2)
        self.label_p2_3 = QtWidgets.QLabel(self.groupBox2)
        self.label_p2_3.setObjectName("label_p2_3")
        self.verticalLayout_5.addWidget(self.label_p2_3)
        self.label_p2_4 = QtWidgets.QLabel(self.groupBox2)
        self.label_p2_4.setObjectName("label_p2_4")
        self.verticalLayout_5.addWidget(self.label_p2_4)
        self.horizontalLayout_11.addWidget(self.groupBox2)
        self.gridLayout.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.plot5 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot5.setFont(font)
        self.plot5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot5.setObjectName("plot5")
        self.horizontalLayout_14.addWidget(self.plot5)
        self.groupBox2_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox2_3.setObjectName("groupBox2_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox2_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_plot5_bband = QtWidgets.QCheckBox(self.groupBox2_3)
        self.checkBox_plot5_bband.setObjectName("checkBox_plot5_bband")
        self.verticalLayout_2.addWidget(self.checkBox_plot5_bband)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.checkBox_plot5_oe = QtWidgets.QCheckBox(self.groupBox2_3)
        self.checkBox_plot5_oe.setObjectName("checkBox_plot5_oe")
        self.horizontalLayout_8.addWidget(self.checkBox_plot5_oe)
        self.checkBox_plot5_mama = QtWidgets.QCheckBox(self.groupBox2_3)
        self.checkBox_plot5_mama.setObjectName("checkBox_plot5_mama")
        self.horizontalLayout_8.addWidget(self.checkBox_plot5_mama)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.label_p5_1 = QtWidgets.QLabel(self.groupBox2_3)
        self.label_p5_1.setObjectName("label_p5_1")
        self.verticalLayout_2.addWidget(self.label_p5_1)
        self.label_p5_2 = QtWidgets.QLabel(self.groupBox2_3)
        self.label_p5_2.setObjectName("label_p5_2")
        self.verticalLayout_2.addWidget(self.label_p5_2)
        self.label_p5_3 = QtWidgets.QLabel(self.groupBox2_3)
        self.label_p5_3.setObjectName("label_p5_3")
        self.verticalLayout_2.addWidget(self.label_p5_3)
        self.label_p5_4 = QtWidgets.QLabel(self.groupBox2_3)
        self.label_p5_4.setObjectName("label_p5_4")
        self.verticalLayout_2.addWidget(self.label_p5_4)
        self.horizontalLayout_14.addWidget(self.groupBox2_3)
        self.gridLayout.addLayout(self.horizontalLayout_14, 3, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_31 = QtWidgets.QLabel(Dialog)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_3.addWidget(self.label_31)
        self.label_32 = QtWidgets.QLabel(Dialog)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_3.addWidget(self.label_32)
        self.label_33 = QtWidgets.QLabel(Dialog)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_3.addWidget(self.label_33)
        self.label_34 = QtWidgets.QLabel(Dialog)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_3.addWidget(self.label_34)
        self.label_35 = QtWidgets.QLabel(Dialog)
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_3.addWidget(self.label_35)
        self.label_36 = QtWidgets.QLabel(Dialog)
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_3.addWidget(self.label_36)
        self.label_37 = QtWidgets.QLabel(Dialog)
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_3.addWidget(self.label_37)
        self.label_38 = QtWidgets.QLabel(Dialog)
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_3.addWidget(self.label_38)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.comboBox3 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox3.setFont(font)
        self.comboBox3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox3.setObjectName("comboBox3")
        self.horizontalLayout_3.addWidget(self.comboBox3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_61 = QtWidgets.QLabel(Dialog)
        self.label_61.setObjectName("label_61")
        self.horizontalLayout_21.addWidget(self.label_61)
        self.label_62 = QtWidgets.QLabel(Dialog)
        self.label_62.setObjectName("label_62")
        self.horizontalLayout_21.addWidget(self.label_62)
        self.label_63 = QtWidgets.QLabel(Dialog)
        self.label_63.setObjectName("label_63")
        self.horizontalLayout_21.addWidget(self.label_63)
        self.label_64 = QtWidgets.QLabel(Dialog)
        self.label_64.setObjectName("label_64")
        self.horizontalLayout_21.addWidget(self.label_64)
        self.label_65 = QtWidgets.QLabel(Dialog)
        self.label_65.setObjectName("label_65")
        self.horizontalLayout_21.addWidget(self.label_65)
        self.label_66 = QtWidgets.QLabel(Dialog)
        self.label_66.setObjectName("label_66")
        self.horizontalLayout_21.addWidget(self.label_66)
        self.label_67 = QtWidgets.QLabel(Dialog)
        self.label_67.setObjectName("label_67")
        self.horizontalLayout_21.addWidget(self.label_67)
        self.label_68 = QtWidgets.QLabel(Dialog)
        self.label_68.setObjectName("label_68")
        self.horizontalLayout_21.addWidget(self.label_68)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem5)
        self.comboBox6 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox6.setFont(font)
        self.comboBox6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox6.setObjectName("comboBox6")
        self.horizontalLayout_21.addWidget(self.comboBox6)
        self.gridLayout.addLayout(self.horizontalLayout_21, 4, 1, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.plot3 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot3.setFont(font)
        self.plot3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot3.setObjectName("plot3")
        self.horizontalLayout_12.addWidget(self.plot3)
        self.groupBox3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox3.setObjectName("groupBox3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox_plot3_bband = QtWidgets.QCheckBox(self.groupBox3)
        self.checkBox_plot3_bband.setObjectName("checkBox_plot3_bband")
        self.verticalLayout_4.addWidget(self.checkBox_plot3_bband)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_plot3_oe = QtWidgets.QCheckBox(self.groupBox3)
        self.checkBox_plot3_oe.setObjectName("checkBox_plot3_oe")
        self.horizontalLayout_6.addWidget(self.checkBox_plot3_oe)
        self.checkBox_plot3_mama = QtWidgets.QCheckBox(self.groupBox3)
        self.checkBox_plot3_mama.setObjectName("checkBox_plot3_mama")
        self.horizontalLayout_6.addWidget(self.checkBox_plot3_mama)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.label_p3_1 = QtWidgets.QLabel(self.groupBox3)
        self.label_p3_1.setObjectName("label_p3_1")
        self.verticalLayout_4.addWidget(self.label_p3_1)
        self.label_p3_2 = QtWidgets.QLabel(self.groupBox3)
        self.label_p3_2.setObjectName("label_p3_2")
        self.verticalLayout_4.addWidget(self.label_p3_2)
        self.label_p3_3 = QtWidgets.QLabel(self.groupBox3)
        self.label_p3_3.setObjectName("label_p3_3")
        self.verticalLayout_4.addWidget(self.label_p3_3)
        self.label_p3_4 = QtWidgets.QLabel(self.groupBox3)
        self.label_p3_4.setObjectName("label_p3_4")
        self.verticalLayout_4.addWidget(self.label_p3_4)
        self.horizontalLayout_12.addWidget(self.groupBox3)
        self.gridLayout.addLayout(self.horizontalLayout_12, 5, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.plot6 = PlotWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.plot6.setFont(font)
        self.plot6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot6.setObjectName("plot6")
        self.horizontalLayout_13.addWidget(self.plot6)
        self.groupBox3_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox3_5.setObjectName("groupBox3_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox3_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_plot6_bband = QtWidgets.QCheckBox(self.groupBox3_5)
        self.checkBox_plot6_bband.setObjectName("checkBox_plot6_bband")
        self.verticalLayout_3.addWidget(self.checkBox_plot6_bband)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox_plot6_oe = QtWidgets.QCheckBox(self.groupBox3_5)
        self.checkBox_plot6_oe.setObjectName("checkBox_plot6_oe")
        self.horizontalLayout_7.addWidget(self.checkBox_plot6_oe)
        self.checkBox_plot6_mama = QtWidgets.QCheckBox(self.groupBox3_5)
        self.checkBox_plot6_mama.setObjectName("checkBox_plot6_mama")
        self.horizontalLayout_7.addWidget(self.checkBox_plot6_mama)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.label_p6_1 = QtWidgets.QLabel(self.groupBox3_5)
        self.label_p6_1.setObjectName("label_p6_1")
        self.verticalLayout_3.addWidget(self.label_p6_1)
        self.label_p6_2 = QtWidgets.QLabel(self.groupBox3_5)
        self.label_p6_2.setObjectName("label_p6_2")
        self.verticalLayout_3.addWidget(self.label_p6_2)
        self.label_p6_3 = QtWidgets.QLabel(self.groupBox3_5)
        self.label_p6_3.setObjectName("label_p6_3")
        self.verticalLayout_3.addWidget(self.label_p6_3)
        self.label_p6_4 = QtWidgets.QLabel(self.groupBox3_5)
        self.label_p6_4.setObjectName("label_p6_4")
        self.verticalLayout_3.addWidget(self.label_p6_4)
        self.horizontalLayout_13.addWidget(self.groupBox3_5)
        self.gridLayout.addLayout(self.horizontalLayout_13, 5, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Big Chart"))
        self.label_time.setText(_translate("Dialog", "TextLabel"))
        self.label_11.setText(_translate("Dialog", "TextLabel"))
        self.label_12.setText(_translate("Dialog", "TextLabel"))
        self.label_13.setText(_translate("Dialog", "TextLabel"))
        self.label_14.setText(_translate("Dialog", "TextLabel"))
        self.label_15.setText(_translate("Dialog", "TextLabel"))
        self.label_16.setText(_translate("Dialog", "TextLabel"))
        self.label_17.setText(_translate("Dialog", "TextLabel"))
        self.label_18.setText(_translate("Dialog", "TextLabel"))
        self.label_41.setText(_translate("Dialog", "TextLabel"))
        self.label_42.setText(_translate("Dialog", "TextLabel"))
        self.label_43.setText(_translate("Dialog", "TextLabel"))
        self.label_44.setText(_translate("Dialog", "TextLabel"))
        self.label_45.setText(_translate("Dialog", "TextLabel"))
        self.label_46.setText(_translate("Dialog", "TextLabel"))
        self.label_47.setText(_translate("Dialog", "TextLabel"))
        self.label_48.setText(_translate("Dialog", "TextLabel"))
        self.groupBox1.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot1_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot1_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot1_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p1_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p1_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p1_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p1_4.setText(_translate("Dialog", "TextLabel"))
        self.groupBox1_3.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot4_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot4_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot4_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p4_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p4_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p4_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p4_4.setText(_translate("Dialog", "TextLabel"))
        self.label_21.setText(_translate("Dialog", "TextLabel"))
        self.label_22.setText(_translate("Dialog", "TextLabel"))
        self.label_23.setText(_translate("Dialog", "TextLabel"))
        self.label_24.setText(_translate("Dialog", "TextLabel"))
        self.label_25.setText(_translate("Dialog", "TextLabel"))
        self.label_26.setText(_translate("Dialog", "TextLabel"))
        self.label_27.setText(_translate("Dialog", "TextLabel"))
        self.label_28.setText(_translate("Dialog", "TextLabel"))
        self.label_51.setText(_translate("Dialog", "TextLabel"))
        self.label_52.setText(_translate("Dialog", "TextLabel"))
        self.label_53.setText(_translate("Dialog", "TextLabel"))
        self.label_54.setText(_translate("Dialog", "TextLabel"))
        self.label_55.setText(_translate("Dialog", "TextLabel"))
        self.label_56.setText(_translate("Dialog", "TextLabel"))
        self.label_57.setText(_translate("Dialog", "TextLabel"))
        self.label_58.setText(_translate("Dialog", "TextLabel"))
        self.groupBox2.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot2_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot2_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot2_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p2_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p2_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p2_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p2_4.setText(_translate("Dialog", "TextLabel"))
        self.groupBox2_3.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot5_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot5_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot5_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p5_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p5_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p5_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p5_4.setText(_translate("Dialog", "TextLabel"))
        self.label_31.setText(_translate("Dialog", "TextLabel"))
        self.label_32.setText(_translate("Dialog", "TextLabel"))
        self.label_33.setText(_translate("Dialog", "TextLabel"))
        self.label_34.setText(_translate("Dialog", "TextLabel"))
        self.label_35.setText(_translate("Dialog", "TextLabel"))
        self.label_36.setText(_translate("Dialog", "TextLabel"))
        self.label_37.setText(_translate("Dialog", "TextLabel"))
        self.label_38.setText(_translate("Dialog", "TextLabel"))
        self.label_61.setText(_translate("Dialog", "TextLabel"))
        self.label_62.setText(_translate("Dialog", "TextLabel"))
        self.label_63.setText(_translate("Dialog", "TextLabel"))
        self.label_64.setText(_translate("Dialog", "TextLabel"))
        self.label_65.setText(_translate("Dialog", "TextLabel"))
        self.label_66.setText(_translate("Dialog", "TextLabel"))
        self.label_67.setText(_translate("Dialog", "TextLabel"))
        self.label_68.setText(_translate("Dialog", "TextLabel"))
        self.groupBox3.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot3_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot3_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot3_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p3_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p3_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p3_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p3_4.setText(_translate("Dialog", "TextLabel"))
        self.groupBox3_5.setTitle(_translate("Dialog", "TA 지표"))
        self.checkBox_plot6_bband.setText(_translate("Dialog", "볼린저밴드"))
        self.checkBox_plot6_oe.setText(_translate("Dialog", "OE"))
        self.checkBox_plot6_mama.setText(_translate("Dialog", "MAMA"))
        self.label_p6_1.setText(_translate("Dialog", "TextLabel"))
        self.label_p6_2.setText(_translate("Dialog", "TextLabel"))
        self.label_p6_3.setText(_translate("Dialog", "TextLabel"))
        self.label_p6_4.setText(_translate("Dialog", "TextLabel"))

from pyqtgraph import PlotWidget
