
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QComboBox,
)


class UI_Teacher_Dialog(QDialog):
    def setupUi(self, Dialog):
        self.roiGroups = {}
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(358, 126)
        self.verticalLayout = QVBoxLayout(self.Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.subjectlabel = QLabel(self.Dialog)
        self.subjectlabel.setObjectName("subjectlabel")
        self.horizontalLayout_3.addWidget(self.subjectlabel)
        self.teacherlabel = QLabel(self.Dialog)
        self.teacherlabel.setObjectName("roomlabel")
        self.horizontalLayout_3.addWidget(self.teacherlabel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.teacherlineedit = QLineEdit(self.Dialog)
        self.teacherlineedit.setObjectName("teacherlineedit")
        self.horizontalLayout_2.addWidget(self.teacherlineedit)
        self.subjectlineedit = QLineEdit(self.Dialog)
        self.subjectlineedit.setObjectName("subjectlineedit")
        self.horizontalLayout_2.addWidget(self.subjectlineedit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QPushButton(self.Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self.Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.pushButton.clicked.connect(self.return_cancel)
        self.pushButton_2.clicked.connect(self.return_accept)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.teacherlabel.setText(_translate("Dialog", "Имя преподавателя"))
        self.subjectlabel.setText(_translate("Dialog", "Название предмета"))
        self.pushButton_2.setText(_translate("Dialog", "Сохранить"))
        self.pushButton.setText(_translate("Dialog", "Отменить"))

    def return_accept(self):
        self.roiGroups["accept"] = True
        self.roiGroups["full_name"] = self.teacherlineedit.text()
        self.roiGroups["subject"] = self.subjectlineedit.text()
        self.Dialog.accept()

    def return_cancel(self):
        self.roiGroups["accept"] = False
        self.Dialog.accept()


class UI_Subject_Dialog(QDialog):
    def setupUi(self, Dialog, subject_records, time_records):
        self.roiGroups = {}
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(358, 126)
        self.verticalLayout = QVBoxLayout(self.Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.subjectlabel = QLabel(self.Dialog)
        self.subjectlabel.setObjectName("subjectlabel")
        self.horizontalLayout_3.addWidget(self.subjectlabel)
        self.roomlabel = QLabel(self.Dialog)
        self.roomlabel.setObjectName("roomlabel")
        self.horizontalLayout_3.addWidget(self.roomlabel)
        self.timelabel = QLabel(self.Dialog)
        self.timelabel.setObjectName("timelabel")
        self.horizontalLayout_3.addWidget(self.timelabel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.subject_selector = QComboBox()
        self.subject_selector.setFixedWidth(150)
        self.times_selector = QComboBox()
        self.subject_selector.addItems(subject_records)
        self.times_selector.addItems(time_records)
        self.roomlineedit = QLineEdit(self.Dialog)
        self.roomlineedit.setObjectName("roomlineedit")
        self.horizontalLayout_2.addWidget(self.subject_selector)
        self.horizontalLayout_2.addWidget(self.roomlineedit)
        self.horizontalLayout_2.addWidget(self.times_selector)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QPushButton(self.Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self.Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.pushButton.clicked.connect(self.return_cancel)
        self.pushButton_2.clicked.connect(self.return_accept)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.roomlineedit.setText(_translate("Dialog", "Кабинет"))
        self.pushButton_2.setText(_translate("Dialog", "Сохранить"))
        self.pushButton.setText(_translate("Dialog", "Отменить"))

    def return_accept(self):
        self.roiGroups["accept"] = True
        self.roiGroups["room"] = self.roomlineedit.text()
        self.roiGroups["subject"] = self.subject_selector.currentText()
        self.roiGroups["time"] = self.times_selector.currentText()
        self.Dialog.accept()

    def return_cancel(self):
        self.roiGroups["accept"] = False
        self.Dialog.accept()