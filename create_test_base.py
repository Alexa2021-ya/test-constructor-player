from PyQt6 import QtCore, QtGui, QtWidgets
from create_test_questions import *
from db import *
from test import *

class Ui_FormCreateTest(object):
    def setupUi(self, FormCreateTest):
        FormCreateTest.setObjectName("FormCreateTest")
        FormCreateTest.resize(346, 150)
        self.gridLayout = QtWidgets.QGridLayout(FormCreateTest)
        self.gridLayout.setObjectName("gridLayout")
        self.label_title = QtWidgets.QLabel(parent=FormCreateTest)
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)
        self.label_name_test = QtWidgets.QLabel(parent=FormCreateTest)
        self.label_name_test.setObjectName("label_name_test")
        self.gridLayout.addWidget(self.label_name_test, 1, 0, 1, 1)
        self.lineEdit_name_test = QtWidgets.QLineEdit(parent=FormCreateTest)
        self.lineEdit_name_test.setObjectName("lineEdit_name_test")
        self.gridLayout.addWidget(self.lineEdit_name_test, 2, 0, 1, 1)
        
        self.pushButton_start = QtWidgets.QPushButton(parent=FormCreateTest)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout.addWidget(self.pushButton_start, 7, 0, 1, 1)

        self.retranslateUi(FormCreateTest)
        QtCore.QMetaObject.connectSlotsByName(FormCreateTest)

    def retranslateUi(self, FormCreateTest):
        _translate = QtCore.QCoreApplication.translate
        FormCreateTest.setWindowTitle(_translate("FormCreateTest", "Form"))
        self.label_title.setText(_translate(
"FormCreateTest", "Создание теста"))
        self.label_name_test.setText(_translate(
"FormCreateTest", "Название теста"))
        self.pushButton_start.setText(_translate(
"FormCreateTest", "Сохранить"))        

class FormCreateTest(QtWidgets.QWidget, Ui_FormCreateTest):
    def __init__(self, parent=None, user=None, id_test=None):
        super().__init__()
        self.setupUi(self)
        self.db = DB()
        self.parent = parent

        if id_test is None:
            self.init_add_test(user)
        else:
            self.init_edit_test(id_test)

    def init_edit_test(self, id_test):
        self.setWindowTitle('Изменить тест')
        self.id_test = id_test
        self.pushButton_start.clicked.connect(self.edit_test)
        test = self.db.get_test(self.id_test)
        self.lineEdit_name_test.setText(test[1])

    def init_add_test(self, user):
        self.setWindowTitle('Добавить тест')
        self.user = user
        self.pushButton_start.clicked.connect(
self.show_window_create_questions)

    def search_test(self):
        return self.db.search_test_by_name(self.lineEdit_name_test.text())

    def edit_test(self):
        name_test = self.lineEdit_name_test.text()
        if (not name_test):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Не заполнены поля!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        elif (self.search_test() and self.search_test() != self.id_test):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText(
"Тест с таким названием уже существует в системе!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        else:
            self.db.set_test(name_test, self.id_test)
            self.close()
        
    def closeEvent(self, event):
        self.parent.update()
        
    def show_window_create_questions(self):
        name = self.lineEdit_name_test.text()
        if (not name):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Не заполнены поля!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        elif (self.search_test()):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText(
"Тест с таким названием уже существует в системе!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        else:
            self.id_test = self.db.add_test(name, self.user.id_user, 0)
            self.w_create_test = CreateTest(self.user, self.id_test)
            self.w_create_test.show()
            self.close()        


