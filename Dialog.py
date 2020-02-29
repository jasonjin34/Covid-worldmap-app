# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(234, 209)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.countrylineEdit = QtWidgets.QLineEdit(Dialog)
        self.countrylineEdit.setMinimumSize(QtCore.QSize(120, 0))
        self.countrylineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.countrylineEdit.setObjectName("countrylineEdit")
        self.horizontalLayout_3.addWidget(self.countrylineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.ConfiredlineEdit = QtWidgets.QLineEdit(Dialog)
        self.ConfiredlineEdit.setMinimumSize(QtCore.QSize(120, 0))
        self.ConfiredlineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.ConfiredlineEdit.setObjectName("ConfiredlineEdit")
        self.horizontalLayout_4.addWidget(self.ConfiredlineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.DeathslineEdit = QtWidgets.QLineEdit(Dialog)
        self.DeathslineEdit.setMinimumSize(QtCore.QSize(120, 0))
        self.DeathslineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.DeathslineEdit.setObjectName("DeathslineEdit")
        self.horizontalLayout_2.addWidget(self.DeathslineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.RecoveredlineEdit = QtWidgets.QLineEdit(Dialog)
        self.RecoveredlineEdit.setMinimumSize(QtCore.QSize(120, 0))
        self.RecoveredlineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.RecoveredlineEdit.setObjectName("RecoveredlineEdit")
        self.horizontalLayout.addWidget(self.RecoveredlineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Location"))
        self.label_2.setText(_translate("Dialog", "Confirmed"))
        self.label_3.setText(_translate("Dialog", "Deaths"))
        self.label_4.setText(_translate("Dialog", "Recovered"))
