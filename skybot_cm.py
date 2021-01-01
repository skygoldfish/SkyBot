# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skybot_cm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 310)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("PNG/skybot_cm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_1 = QtWidgets.QMenu(self.menubar)
        self.menu_1.setObjectName("menu_1")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("PNG/로그인.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLogin.setIcon(icon1)
        self.actionLogin.setStatusTip("")
        self.actionLogin.setObjectName("actionLogin")
        self.actionLogout = QtWidgets.QAction(MainWindow)
        self.actionLogout.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("PNG/로그아웃.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLogout.setIcon(icon2)
        self.actionLogout.setStatusTip("")
        self.actionLogout.setObjectName("actionLogout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("PNG/종료.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon3)
        self.actionExit.setStatusTip("")
        self.actionExit.setObjectName("actionExit")
        self.actionAccountDialog = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("PNG/계좌조회.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAccountDialog.setIcon(icon4)
        self.actionAccountDialog.setObjectName("actionAccountDialog")
        self.actionUsage = QtWidgets.QAction(MainWindow)
        self.actionUsage.setObjectName("actionUsage")
        self.actionMustRead = QtWidgets.QAction(MainWindow)
        self.actionMustRead.setObjectName("actionMustRead")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionScoreBoard = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("PNG/당월물 옵션전광판.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionScoreBoard.setIcon(icon5)
        self.actionScoreBoard.setObjectName("actionScoreBoard")
        self.actionBigChart = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("PNG/수급.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBigChart.setIcon(icon6)
        self.actionBigChart.setObjectName("actionBigChart")
        self.menu.addAction(self.actionLogin)
        self.menu.addAction(self.actionLogout)
        self.menu.addSeparator()
        self.menu.addAction(self.actionAccountDialog)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)
        self.menu.addSeparator()
        self.menu_3.addAction(self.actionMustRead)
        self.menu_3.addAction(self.actionUsage)
        self.menu_3.addAction(self.actionVersion)
        self.menu_1.addAction(self.actionScoreBoard)
        self.menu_1.addSeparator()
        self.menu_1.addAction(self.actionBigChart)
        self.menu_1.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_1.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.menubar.triggered['QAction*'].connect(MainWindow.MENU_Action)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Skybot"))
        self.menu.setTitle(_translate("MainWindow", "세션"))
        self.menu_3.setTitle(_translate("MainWindow", "도움말"))
        self.menu_1.setTitle(_translate("MainWindow", "선물옵션"))
        self.menu_2.setTitle(_translate("MainWindow", "설정"))
        self.actionLogin.setText(_translate("MainWindow", "로그인"))
        self.actionLogout.setText(_translate("MainWindow", "로그아웃"))
        self.actionExit.setText(_translate("MainWindow", "종료"))
        self.actionAccountDialog.setText(_translate("MainWindow", "계좌조회"))
        self.actionUsage.setText(_translate("MainWindow", "사용법"))
        self.actionMustRead.setText(_translate("MainWindow", "꼭 읽어보세요"))
        self.actionVersion.setText(_translate("MainWindow", "버전"))
        self.actionScoreBoard.setText(_translate("MainWindow", "선물옵션 전광판"))
        self.actionBigChart.setText(_translate("MainWindow", "Big Chart"))
