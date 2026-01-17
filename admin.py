from PyQt6 import QtCore, QtGui, QtWidgets, QtSql
from db import *

class Ui_AdminPanel(object):
    def setupUi(self, AdminPanel):
        AdminPanel.setObjectName("AdminPanel")
        AdminPanel.resize(588, 395)
        self.gridLayout = QtWidgets.QGridLayout(AdminPanel)
        self.gridLayout.setObjectName("gridLayout")
        
        self.pushButton_add_user = QtWidgets.QPushButton(parent=AdminPanel)
        self.pushButton_add_user.setObjectName("pushButton_add_user")
        self.pushButton_add_user.clicked.connect(self.add_user)
        self.gridLayout.addWidget(self.pushButton_add_user, 0, 0, 1, 1)

        self.pushButton_delete = QtWidgets.QPushButton(parent=AdminPanel)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.pushButton_delete.clicked.connect(self.delete)

        self.gridLayout.addWidget(self.pushButton_delete, 0, 1, 1, 1)
        self.pushButton_update = QtWidgets.QPushButton(parent=AdminPanel)
        self.pushButton_update.setObjectName("pushButton_update")
        self.pushButton_update.clicked.connect(self.update)
        self.gridLayout.addWidget(self.pushButton_update, 0, 2, 1, 1)      
        self.table_users = QtWidgets.QTableView(parent=AdminPanel)
        self.table_users.setObjectName("table_users")
        self.gridLayout.addWidget(self.table_users, 1, 0, 1, 3)
        self.retranslateUi(AdminPanel)
        QtCore.QMetaObject.connectSlotsByName(AdminPanel)

    def retranslateUi(self, AdminPanel):
        _translate = QtCore.QCoreApplication.translate
        AdminPanel.setWindowTitle(_translate("AdminPanel", "Form"))
        self.pushButton_add_user.setText(_translate(
"AdminPanel", "Добавить пользователя"))
        self.pushButton_update.setText(_translate("AdminPanel", "Обновить"))
        self.pushButton_delete.setText(_translate("AdminPanel", "Удалить"))
        self.setWindowTitle('Администрирование')

class AdminPanel(QtWidgets.QWidget, Ui_AdminPanel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = DB()
        self.setModel()

    def add_user(self):
        from register_form import AddUser
        self.w = AddUser(self)
        self.w.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.w.show()
        
    def update(self):
        self.model_users.select()

    def delete(self):
        row = self.table_users.currentIndex().row()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Удаление записи")
        if row == -1:
            msg.setText('Выберите запись для удаления.')
            return          
        msg.setText("Удалить запись?")
        msg.addButton("Да", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.RejectRole)
        returnValue = msg.exec()
        if returnValue == 0:
            self.model_users.removeRow(self.table_users.currentIndex().row())
            self.update()
            msg.setText('Запись удалена.')
        else:
            msg.setText('Диалог сброшен.')
            return

    def setModel(self):   
        self.model_users = QtSql.QSqlRelationalTableModel()
        self.model_users.setEditStrategy(
QtSql.QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.model_users.setTable('users')
        self.model_users.setHeaderData(1, 
QtCore.Qt.Orientation.Horizontal, 'Имя')
        self.model_users.setHeaderData(2, 
QtCore.Qt.Orientation.Horizontal, 'Пароль')
        self.model_users.setHeaderData(3, 
QtCore.Qt.Orientation.Horizontal, 'Роль')
        self.model_users.setRelation(3, 
QtSql.QSqlRelation("role", "id", "name"))
        self.model_users.setJoinMode(
QtSql.QSqlRelationalTableModel.JoinMode.LeftJoin)
        self.model_users.select()
        self.table_users.setModel(self.model_users)
        self.table_users.setColumnHidden(0, True)
        self.table_users.setSortingEnabled(True)
        self.table_users.setItemDelegate(
QtSql.QSqlRelationalDelegate(self.table_users))  
        self.table_users.horizontalHeader().setSectionResizeMode(
QtWidgets.QHeaderView.ResizeMode.Stretch)


