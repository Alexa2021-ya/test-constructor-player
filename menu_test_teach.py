from PyQt6 import QtCore, QtGui, QtWidgets
from create_test_base import *
from test import *
from history import *
from admin import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_update = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_update.setObjectName("pushButton_update")
        self.pushButton_update.clicked.connect(self.update)
        
        self.label_sort = QtWidgets.QLabel()
        
        self.combobox_sort = QtWidgets.QComboBox(parent=self.centralwidget)
        self.combobox_sort.setObjectName("combobox_sort")
        self.combobox_sort.activated.connect(self.sort)
        
        self.combobox_sort.addItem("Сортировать в алфавитном порядке")
        self.combobox_sort.addItem("Сортировать в обратном порядке")

        self.label_search = QtWidgets.QLabel()
        self.lineedit_search = QtWidgets.QLineEdit()
        self.lineedit_search.textChanged.connect(self.search)

        self.label_title = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 2)
        self.listWidget_tests = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_tests.setObjectName("listWidget_tests")
        self.listWidget_tests.itemDoubleClicked.connect(self.double_click)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_update.setText(_translate("MainWindow", "Обновить"))
        self.label_title.setText(_translate("MainWindow", "Мои тесты"))
        self.label_sort.setText(_translate("MainWindow", "Сортировка"))
        self.label_search.setText(_translate("MainWindow", "Поиск"))
        self.setWindowTitle('Система проверки знаний')

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.db = DB()
        self.id_test = None

    def search(self):
        text = self.lineedit_search.text()
        search_answers = self.listWidget_tests.findItems(text, QtCore.Qt.MatchFlag.MatchRegularExpression)

        if len(search_answers) and text:
            for i in range(self.listWidget_tests.count()):
                if not self.listWidget_tests.item(i) in search_answers:
                    self.listWidget_tests.item(i).setHidden(True)
        else:
            for i in range(self.listWidget_tests.count()):
                self.listWidget_tests.item(i).setHidden(False)
             
    def sort(self):
        selected_sort = self.combobox_sort.currentIndex()
        if selected_sort == 0:
            self.listWidget_tests.sortItems()
            self.list_tests.sort(key=lambda x: x[1])
        else:
            self.listWidget_tests.sortItems(
QtCore.Qt.SortOrder.DescendingOrder)
            self.list_tests.sort(key=lambda x: x[1], reverse=True)    
                
    def update(self):
        self.listWidget_tests.clear()
        self.f()

class Creator(MainWindow):
    def __init__(self, user):
        super().__init__(user)
        self.get_data()
        self.get_interface()

    def get_data(self):
        self.list_tests = self.db.get_tests(self.user.id_user)
        for i in range(len(self.list_tests)):
            self.listWidget_tests.addItem(self.list_tests[i][1])
            self.listWidget_tests.item(i).setData(
QtCore.Qt.ItemDataRole.UserRole, self.list_tests[i][0])
            result = self.db.get_result(self.list_tests[i][0], self.user.id_user)
            if result:
                self.listWidget_tests.item(i).setForeground(
QtGui.QBrush(QtGui.QColor("#00008B")));
        self.sort()

    def get_interface(self):
        self.pushButton_add = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_add.clicked.connect(self.show_window_create_test)
        self.gridLayout.addWidget(self.pushButton_add, 5, 0, 1, 6)

        self.pushButton_delete = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.pushButton_delete.clicked.connect(self.delete_test)
        self.gridLayout.addWidget(self.pushButton_delete, 1, 0, 1, 1)
        self.pushButton_edit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_edit.setObjectName("pushButton_edit")

        self.pushButton_edit.clicked.connect(self.edit_name_test)
        self.gridLayout.addWidget(self.pushButton_edit, 1, 2, 1, 1)
        
        self.pushButton_history = QtWidgets.QPushButton(
parent=self.centralwidget)
        self.pushButton_history.setObjectName("pushButton_history")
        self.pushButton_history.clicked.connect(self.get_history)
        self.gridLayout.addWidget(self.pushButton_history, 1, 3, 1, 1)
        
        self.pushButton_add.setText("Добавить тест")
        self.pushButton_delete.setText("Удалить тест")
        self.pushButton_edit.setText("Изменить")
        self.pushButton_history.setText("История")

        self.gridLayout.addWidget(self.pushButton_update, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.label_sort, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.label_search, 2, 3, 1, 3)
        self.gridLayout.addWidget(self.combobox_sort, 3, 0, 1, 3)
        self.gridLayout.addWidget(self.lineedit_search, 3, 3, 1, 3)

        self.gridLayout.addWidget(self.listWidget_tests, 4, 0, 1, 6)
        self.listWidget_tests.itemClicked.connect(self.click_one)

    def double_click(self):
        self.id_test = self.listWidget_tests.item(
self.listWidget_tests.currentRow()).data(
QtCore.Qt.ItemDataRole.UserRole)
        self.w_test = CreateTest(self.user.id_user, self.id_test)
        self.id_test = None
        self.listWidget_tests.setCurrentItem(None)
        self.w_test.setWindowModality(
QtCore.Qt.WindowModality.ApplicationModal)
        self.w_test.show()

    def get_history(self):
        self.w = Form()
        self.w.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.w.show()
        
    def click_one(self):
        self.id_test = self.listWidget_tests.item(
self.listWidget_tests.currentRow()).data(
QtCore.Qt.ItemDataRole.UserRole)

    def edit_name_test(self):
        if self.id_test != None:
            self.w_edit_test = FormCreateTest(self ,id_test=self.id_test)
            self.w_edit_test.setWindowModality(
QtCore.Qt.WindowModality.ApplicationModal)
            self.w_edit_test.show()

    def delete_test(self):
        if self.id_test != None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setWindowTitle("Удаление записи")
            msg.setText("Удалить запись?")
            msg.addButton("Да", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
            msg.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.RejectRole)

            returnValue = msg.exec()
            if returnValue == 0:
                self.db.delete_test(self.id_test)
                self.update()
                msg.setText('Запись удалена.')
            else:
                msg.setText('Диалог сброшен.')
                return
        else:
            msg.setText('Выберите запись для удаления.')
            return
            
    def show_window_create_test(self):
        self.w_create_test = FormCreateTest(self, self.user)             
        self.w_create_test.setWindowModality(
    QtCore.Qt.WindowModality.ApplicationModal)
        self.w_create_test.show()

class Admin(Creator):
    def __init__(self, user):
        super().__init__(user)
        self.get_data()
        self.get_interface()

        self.pushButton_admin = QtWidgets.QPushButton(
parent=self.centralwidget)
        self.pushButton_admin.clicked.connect(self.create_admin_panel)
        self.gridLayout.addWidget(self.pushButton_admin, 1, 4, 1, 1)
        self.pushButton_admin.setText("Администрирование")

    def create_admin_panel(self):
        self.w = AdminPanel()
        self.w.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.w.show()

class Taker(MainWindow):
    def __init__(self, user):
        super().__init__(user)
        self.get_data()
        self.get_interface()
        
    def double_click(self):
        self.id_test = self.listWidget_tests.item(
self.listWidget_tests.currentRow()).data(
QtCore.Qt.ItemDataRole.UserRole)
        result = self.db.get_result(self.id_test, self.user.id_user)
        if result:        
            msg = QtWidgets.QMessageBox()
            msg.setText(f"Тестирование завершено.\nВаш результат: {result[4]}%\nХотите пройти тестирование заново? Ваши результаты будут перезаписаны.")
            msg.setWindowTitle("Тест")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Question)
        msg.addButton("Да", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Нет", QtWidgets.QMessageBox.ButtonRole.RejectRole)

        returnValue = msg.exec()
                
        if returnValue == 0:
            self.w_test = TakeTest(self.user, self.id_test)
            self.listWidget_tests.setCurrentItem(None)
            self.w_test.setWindowModality(	QtCore.Qt.WindowModality.ApplicationModal)
            self.w_test.show()
            self.db.delete_result(self.id_test, self.user.id_user)
        else:
            self.w_test = TakeTest(self.user, self.id_test)
            self.listWidget_tests.setCurrentItem(None)
            self.w_test.setWindowModality(	QtCore.Qt.WindowModality.ApplicationModal)
            self.w_test.show()
    
    def get_interface(self):
        self.gridLayout.addWidget(self.pushButton_update, 1, 0, 1, 4)
        self.gridLayout.addWidget(self.combobox_sort, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.label_sort, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.label_search, 2, 2, 1, 2)
        self.gridLayout.addWidget(self.lineedit_search, 3, 2, 1, 2)
        self.gridLayout.addWidget(self.listWidget_tests, 4, 0, 1, 4)

    def get_data(self):
        self.list_tests = self.db.get_all_tests()
        for i in range(len(self.list_tests)):
            self.listWidget_tests.addItem(self.list_tests[i][1])
            self.listWidget_tests.item(i).setData(
QtCore.Qt.ItemDataRole.UserRole, self.list_tests[i][0])      
            result = self.db.get_result(self.list_tests[i][0], self.user.id_user)
            if result:
                self.listWidget_tests.item(i).setForeground(QtGui.QBrush(
QtGui.QColor("#00008B")));
        self.sort()





