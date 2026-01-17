import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from db import *
from menu_test_teach import *

class User:
    def __init__(self, id_user, role):
        self.id_user = id_user
        self.role = role    
class Ui_FormRegister(object):
    def setupUi(self, FormRegister):
        FormRegister.setObjectName("FormRegister")
        FormRegister.resize(412, 197)
        self.gridLayout = QtWidgets.QGridLayout(FormRegister)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_enter = QtWidgets.QPushButton(parent=FormRegister)
        self.pushButton_enter.setObjectName("pushButton_enter")        
        self.gridLayout.addWidget(self.pushButton_enter, 7, 0, 1, 2)
        
        self.lineEdit_login = QtWidgets.QLineEdit(parent=FormRegister)
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.gridLayout.addWidget(self.lineEdit_login, 2, 0, 1, 2)
        self.label_login = QtWidgets.QLabel(parent=FormRegister)
        self.label_login.setObjectName("label_login")
        self.gridLayout.addWidget(self.label_login, 1, 0, 1, 2)
        self.label_password = QtWidgets.QLabel(parent=FormRegister)
        self.label_password.setObjectName("label_password")
        self.gridLayout.addWidget(self.label_password, 3, 0, 1, 2)
        self.lineEdit_password = QtWidgets.QLineEdit(parent=FormRegister)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 4, 0, 1, 2)
        
        self.retranslateUi(FormRegister)
        QtCore.QMetaObject.connectSlotsByName(FormRegister)

    def retranslateUi(self, FormRegister):
        _translate = QtCore.QCoreApplication.translate
        FormRegister.setWindowTitle(_translate("FormRegister", "Form"))
        self.label_login.setText(_translate("FormRegister", "Логин"))
        self.label_password.setText(_translate("FormRegister", "Пароль"))
class UserForm(QtWidgets.QWidget, Ui_FormRegister):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.setupUi(self)
        self.get_interface()

    def get_role(self, id_user):
        role = self.db.get_role(id_user)
        return role

class FormRegister(UserForm):
    def __init__(self):
        super().__init__()
        
    def get_interface(self):
        self.pushButton_enter.clicked.connect(self.show_main_window)
        self.pushButton_enter.setText("Войти")

        self.label_welcome = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_welcome, 0, 0, 1, 2)
        self.label_welcome.setText("Добро пожаловать! Авторизируйтесь в системе.")

        self.setWindowTitle('Авторизация')
        
    def get_account_access(self):
        name = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        id_user = self.db.search_for_user_by_name(name)
        if (id_user):
            self.user = User(id_user, self.get_role(id_user))
            return self.db.password_check(id_user, password)
        else:
            return False
                
    def show_main_window(self):
        if (self.get_account_access()):
            id_user = self.db.search_for_user_by_name(
self.lineEdit_login.text())
            self.user = User(id_user, self.get_role(id_user))

            if self.user.role == 1:
                self.w_main = Creator(self.user)
            elif self.user.role == 2:
                self.w_main = Taker(self.user)
            else:
                self.w_main = Admin(self.user)
            self.w_main.show()
            self.close()
        else:
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Пользователя с такими данными не найдено. Проверьте введённые логин и пароль!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()

class AddUser(UserForm):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def add_user(self):
        name = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        role = self.comboBox_role.currentIndex() + 1

        if (self.db.search_for_user_by_name(name)):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Пользователь с таким именем уже существует!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        elif (not name or not password):
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Не заполнены поля!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        else:
            self.db.add_user(name, password, role)
            self.close()

    def get_interface(self):
        self.pushButton_enter.clicked.connect(self.add_user)
        self.pushButton_enter.setText("Зарегистрировать")

        self.label_role = QtWidgets.QLabel()
        self.label_role.setText("Зачем вы сюда пришли?")
        self.gridLayout.addWidget(self.label_role, 5, 0, 1, 2)

        self.comboBox_role = QtWidgets.QComboBox()
        self.comboBox_role.setObjectName("comboBox_role")
        self.comboBox_role.addItem("Я буду проходить тесты")
        self.comboBox_role.addItem("Я буду создавать тесты")
        self.comboBox_role.addItem("Я администратор")
        self.gridLayout.addWidget(self.comboBox_role, 6, 0, 1, 2)

        self.setWindowTitle('Добавить пользователя')

    def closeEvent(self, event):
        self.parent.update()
        
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    w_reg = FormRegister()
    w_reg.show()


