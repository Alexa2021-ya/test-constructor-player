from PyQt6 import QtCore, QtGui, QtWidgets
from db import *

class Ui_FormCreateQuestion(object):
    def setupUi(self, FormCreateQuestion):
        FormCreateQuestion.setObjectName("FormCreateQuestion")
        FormCreateQuestion.resize(672, 200)
        self.gridLayout_2 = QtWidgets.QGridLayout(FormCreateQuestion)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_question = QtWidgets.QLabel(parent=FormCreateQuestion)
        self.label_question.setObjectName("label_question")
        self.gridLayout_2.addWidget(self.label_question, 1, 0, 1, 1)
        self.button_save = QtWidgets.QPushButton()
        self.button_save.setText("Сохранить")         
        self.label_title = QtWidgets.QLabel(parent=FormCreateQuestion)
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 2)
        self.textEdit_question = QtWidgets.QTextEdit(
parent=FormCreateQuestion)
        self.textEdit_question.setObjectName("textEdit_question")
        self.gridLayout_2.addWidget(self.textEdit_question, 2, 0, 1, 2)
        self.comboBox = QtWidgets.QComboBox(parent=FormCreateQuestion)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(
["Один из списка", "Несколько из списка", "Текст(строка)"])
        self.comboBox.activated.connect(self.activated)
        self.gridLayout_2.addWidget(self.comboBox, 6, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=FormCreateQuestion)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 5, 0, 1, 2)

        self.retranslateUi(FormCreateQuestion)
        QtCore.QMetaObject.connectSlotsByName(FormCreateQuestion)

    def retranslateUi(self, FormCreateQuestion):
        _translate = QtCore.QCoreApplication.translate
        FormCreateQuestion.setWindowTitle(
_translate("FormCreateQuestion", "Form"))
        self.label_question.setText(_translate("FormCreateQuestion", "Вопрос"))
        self.label.setText(_translate("FormCreateQuestion", "Добавить поле"))

class FormCreateQuestion(QtWidgets.QWidget, Ui_FormCreateQuestion):
    def __init__(self, parent=None):
        super().__init__()        
        self.setupUi(self)
        self.parent = parent
        self.db = DB()
        self.type = 0
        self.n = 0
        self.a = -1
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_2.addLayout(self.gridLayout_3, 9, 0, 1, 2)
    
    def clear_grid(self, grid):
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)
        
    def closeEvent(self, event):
        self.parent.update()

    def activated(self, index):
        if (index == 0):
            if (self.a != index):
                self.a = index
                self.n = 0
                self.clear_grid(self.gridLayout_3)
            self.lineeditradio = QtWidgets.QLineEdit()
            self.gridLayout_3.addWidget(self.lineeditradio, self.n, 1, 1, 1)
            self.radio = QtWidgets.QRadioButton()
            self.gridLayout_3.addWidget(self.radio, self.n, 0, 1, 1)

            self.type = 1            
            self.n += 1
        elif (index == 1):
            if (self.a != index):
                self.a = index
                self.n = 0
                self.clear_grid(self.gridLayout_3)
            self.type = 2
            self.lineeditcheck = QtWidgets.QLineEdit()
            self.gridLayout_3.addWidget(self.lineeditcheck, self.n, 1, 1, 1)
            self.checkbox = QtWidgets.QCheckBox()
            self.gridLayout_3.addWidget(self.checkbox, self.n, 0, 1, 1)
            self.n += 1
        elif (index == 2):
            if (self.a != index):
                self.a = index
                self.clear_grid(self.gridLayout_3)
                self.n = -1
                self.lineedit = QtWidgets.QLineEdit()
            self.gridLayout_3.addWidget(self.lineedit, 0, 0, 1, 2)
            self.type = 3

class AddQuestion(FormCreateQuestion):
    def __init__(self, parent=None, id_test=None):
        super().__init__(parent)
        self.get_interface()
        self.id_test = id_test
        
    def get_interface(self):
        self.button_save.clicked.connect(self.add_question)
        self.gridLayout_2.addWidget(self.button_save, 10, 1, 1, 1)
        self.setWindowTitle('Добавить вопрос')

    def add_question(self):
        name = []
        isTrue = []
        name_question = self.textEdit_question.toPlainText()
        
        for i in range(self.gridLayout_3.count()):
            widget = self.gridLayout_3.itemAt(i).widget() 
            if type(widget) == QtWidgets.QLineEdit:
                if widget.text():
                    name.append(widget.text())
                else:
                    break
            elif type(widget) == QtWidgets.QRadioButton or type(widget) == QtWidgets.QCheckBox:
                    isTrue.append(widget.isChecked())
                
        if (not len(isTrue)):
            isTrue.append(True)

        if len(name) and len(isTrue) and name_question:
            id_question = self.db.add_question(name_question,
 self.id_test, self.type)
            for i in range(len(name)):
                self.db.add_answer(name[i], id_question, isTrue[i])
            count = int(self.db.get_count_questions(self.id_test)) + 1
            self.db.set_count_questions(self.id_test, count)
            self.close()
        else:
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText("Не заполнены поля!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()
        
    def closeEvent(self, event):
        self.parent.update()

class EditQuestion(FormCreateQuestion):
    def __init__(self, parent=None, question=None):
        super().__init__(parent)
        self.question = question
        self.answers = self.db.get_all_info_answers(self.question[0])
        self.get_interface()
        
    def get_interface(self):
        self.button_save.clicked.connect(self.edit_question)
        self.gridLayout_2.addWidget(self.button_save, 10, 1, 1, 1)

        self.textEdit_question.setText(self.question[1])
        self.get_content_question()

        self.setWindowTitle('Редактировать вопрос')

    def edit_question(self):
        name = []
        isTrue = []
        name_question = self.textEdit_question.toPlainText()
        for i in range(self.gridLayout_3.count()):
            widget = self.gridLayout_3.itemAt(i).widget()
            if type(widget) == QtWidgets.QLineEdit:
                if widget.text():
                    name.append(widget.text())
                else:
                    break
            elif type(widget) == QtWidgets.QRadioButton or type(widget) == QtWidgets.QCheckBox:
                    isTrue.append(widget.isChecked())
                    
        if (not len(isTrue)):
            isTrue.append(True)
   
        if len(name) and len(isTrue) and name_question:
            id_question = self.question[0]
            self.db.delete_answers(id_question)
        
            for i in range(len(name)):
                self.db.add_answer(name[i], id_question, isTrue[i])

            self.db.set_name_question(id_question, name_question)
            self.db.set_type_question(id_question, self.type)
            
            self.close()
        else:
            msg_error = QtWidgets.QMessageBox()
            msg_error.setText(
"Пользователя с такими данными не найдено. Проверьте введённые логин и пароль!")
            msg_error.setWindowTitle("Ошибка")
            msg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_error.exec()

    def get_content_question(self):
        j = 0 
        for i in self.answers:
            if (self.question[2] == 1):
                self.radio_answer = QtWidgets.QRadioButton()
                self.radio_answer.setChecked(self.answers[j][1])
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.lineedit_answer.setText(self.answers[j][0])
                self.gridLayout_3.addWidget(
self.lineedit_answer, self.n, 1, 1, 1)
                self.gridLayout_3.addWidget(
self.radio_answer, self.n, 0, 1, 1)

                self.a = 0
                self.type = 1        
            elif (self.question[2] == 2):
                self.check_answer = QtWidgets.QCheckBox()
                self.check_answer.setChecked(self.answers[j][1])
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.lineedit_answer.setText(self.answers[j][0])
                self.gridLayout_3.addWidget(
self.lineedit_answer, self.n, 1, 1, 1)
                self.gridLayout_3.addWidget(
self.check_answer, self.n, 0, 1, 1)

                self.a = 1
                self.type = 2            
            elif (self.question[2] == 3):
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.gridLayout_3.addWidget(
self.lineedit_answer, self.n, 0, 1, 1)
                self.lineedit_answer.setText(self.answers[j][0])

                self.a = 2
                self.type = 3
                
            self.n += 1
            j+= 1




