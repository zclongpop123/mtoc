# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widgets.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(434, 120)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, -1, -1, -1)
        self.cbx_exp_abc = QCheckBox(self.centralwidget)
        self.cbx_exp_abc.setObjectName(u"cbx_exp_abc")
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(11)
        self.cbx_exp_abc.setFont(font)
        self.cbx_exp_abc.setChecked(True)

        self.verticalLayout.addWidget(self.cbx_exp_abc)

        self.cbx_exp_json = QCheckBox(self.centralwidget)
        self.cbx_exp_json.setObjectName(u"cbx_exp_json")
        self.cbx_exp_json.setFont(font)
        self.cbx_exp_json.setChecked(True)

        self.verticalLayout.addWidget(self.cbx_exp_json)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.btn_export = QPushButton(self.centralwidget)
        self.btn_export.setObjectName(u"btn_export")
        self.btn_export.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setWeight(50)
        self.btn_export.setFont(font1)

        self.verticalLayout_2.addWidget(self.btn_export)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.btn_import = QPushButton(self.centralwidget)
        self.btn_import.setObjectName(u"btn_import")
        self.btn_import.setMinimumSize(QSize(0, 30))
        self.btn_import.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_import)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.cbx_exp_abc.setText(QCoreApplication.translate("MainWindow", u"Alembic (.abc)", None))
        self.cbx_exp_json.setText(QCoreApplication.translate("MainWindow", u"Json (.json)", None))
        self.btn_export.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.btn_import.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165", None))
    # retranslateUi

