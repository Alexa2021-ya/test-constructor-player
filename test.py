from PyQt6 import QtCore, QtGui, QtWidgets
from db import *
from create_test_questions import *

class Ui_Test(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(683, 100)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_main = QtWidgets.QGridLayout()
        self.gridLayout_main.setObjectName("gridLayout_main")
        self.gridLayout_3.addLayout(self.gridLayout_main, 0, 1, 1, 1)

        self.gridLayout_info = QtWidgets.QGridLayout()
        self.gridLayout_info.setObjectName("gridLayout_info")
        self.gridLayout_3.addLayout(self.gridLayout_info, 0, 0, 1, 1)
        
        self.groupBox_questions = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_questions.setObjectName("groupBox_questions")
        self.gridLayout_info.addWidget(self.groupBox_questions, 1, 0, 1, 2)
        
        self.groupBox_question = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_question.setObjectName("groupBox_question")
        self.gridLayout_main.addWidget(self.groupBox_question, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class Test(QtWidgets.QWidget, Ui_Test):
    def __init__(self, user, id_test):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.id_test = id_test
        self.db = DB()
        self.test = None
        self.questions_list = None

        self.layout_questions = QtWidgets.QGridLayout()
        self.groupBox_questions.setLayout(self.layout_questions)

        self.layout_question = QtWidgets.QGridLayout()
        self.groupBox_question.setLayout(self.layout_question)
         
        self.index = 0
        self.get_data()
        
        if (len(self.questions_list)):
            self.fill_grid()
        
        self.groupBox_questions.setLayout(self.layout_questions)
        self.groupBox_questions.setTitle(self.test[1])

        self.setWindowTitle(self.test[1])

    def button_group(self, object):
        id_button = self.group.id(object)
        self.index = id_button - 1
        self.clear_grid(self.layout_question)
        self.get_content_question()
        
    def fill_grid(self):
        number_questions = self.test[3]
        n = 0
        m = 0    
        k = number_questions // 5

        self.group = QtWidgets.QButtonGroup(self.layout_questions)
        for i in range(number_questions):
            self.pushButton_question = QtWidgets.QPushButton(str(i + 1))
            self.layout_questions.addWidget(
self.pushButton_question, m, n, 1, 1)
            self.group.addButton(self.pushButton_question, i + 1)
            if n == k:
                n = 0
                m += 1
            else:
                n += 1

        self.group.buttonClicked.connect(self.button_group)
            
    def get_data(self):
        self.test = self.db.get_test(self.id_test)
        self.questions_list = self.db.get_all_info_questions(self.id_test)
        self.answers_list = []
        for i in self.questions_list:
            self.answers_list.append(self.db.get_all_info_answers(i[0]))
                
    def clear_grid(self, grid):
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None) 

class CreateTest(Test):
    def __init__(self, user, id_test):
        super().__init__(user, id_test)
        self.get_interface()
        if (len(self.questions_list)):
            self.get_content_question()
        
    def get_interface(self):
        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setText("Удалить вопрос")
        self.delete_button.clicked.connect(self.delete_question)
        self.gridLayout_main.addWidget(self.delete_button, 0, 0, 1, 1)

        self.edit_button = QtWidgets.QPushButton()
        self.edit_button.setText("Редактировать вопрос")
        self.edit_button.clicked.connect(self.edit_question)
        self.gridLayout_main.addWidget(self.edit_button, 0, 1, 1, 1)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setText("Добавить вопрос")
        self.add_button.clicked.connect(self.add_question)
        self.gridLayout_info.addWidget(self.add_button, 0, 0, 1, 1)

        self.update_button = QtWidgets.QPushButton()
        self.update_button.setText("Обновить")
        self.update_button.clicked.connect(self.update)
        self.gridLayout_info.addWidget(self.update_button, 0, 1, 1, 1)

    def add_question(self):
        self.w = AddQuestion(self, self.id_test)
        self.w.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.w.show()
    
    def update(self):
        self.clear_grid(self.layout_questions)
        self.clear_grid(self.layout_question)
        self.get_data()
        if (len(self.questions_list)):
            self.fill_grid()
            
        if (len(self.questions_list)):
            self.get_content_question()
        else:
            self.groupBox_question.setTitle("")
                    
    def delete_question(self):
        if (len(self.questions_list)):
            self.db.delete_question(
self.id_test, self.questions_list[self.index][0])
            self.index = self.index - 1
        self.update()
            
    def edit_question(self):
        if (len(self.questions_list)- 1 >= self.index):
            self.w = EditQuestion(self, self.questions_list[self.index])
            self.w.setWindowModality(
QtCore.Qt.WindowModality.ApplicationModal)
            self.w.show()

    def get_content_question(self):
        n = 0
        j = 0 
        for i in self.answers_list[self.index]:
            if (self.questions_list[self.index][2] == 1):
                self.radio_answer = QtWidgets.QRadioButton()
                self.radio_answer.setChecked(
 self.answers_list[self.index][j][1])
                self.radio_answer.setDisabled(True)
                self.layout_question.addWidget(self.radio_answer, n, 0, 1, 1)
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.lineedit_answer.setText(
 self.answers_list[self.index][j][0])
                self.lineedit_answer.setDisabled(True)        
                self.layout_question.addWidget(
 self.lineedit_answer, n, 1, 1, 1)
            elif (self.questions_list[self.index][2] == 2):
                self.check_answer = QtWidgets.QCheckBox()
                self.check_answer.setChecked(
  	self.answers_list[self.index][j][1])
                self.check_answer.setDisabled(True)
                self.layout_question.addWidget(self.check_answer, n, 0, 1, 1)   
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.lineedit_answer.setText(
self.answers_list[self.index][j][0])
                self.lineedit_answer.setDisabled(True)
                self.layout_question.addWidget(
self.lineedit_answer, n, 1, 1, 1)
            elif (self.questions_list[self.index][2] == 3):
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.layout_question.addWidget(self.lineedit_answer, n, 0, 1, 1)
                self.lineedit_answer.setText(self.answers_list[self.index][j][0])
                self.lineedit_answer.setDisabled(True)
             
            n += 1
            j += 1
        self.groupBox_question.setTitle(self.questions_list[self.index][1])

class TakeTest(Test):
    def __init__(self, user, id_test):
        super().__init__(user, id_test)
        self.get_interface()
        self.f_index = 0
        self.answers = []
        for i in range(self.test[3]):
            self.answers.append([])
        if (len(self.questions_list)):
            self.get_content_question()
        self.b = False
        self.id_button = 1

    def get_interface(self):
        self.exit_button = QtWidgets.QPushButton()
        self.exit_button.setText("Завершить тестирование")
        self.exit_button.clicked.connect(self.calculate_result)
        self.gridLayout_main.addWidget(self.exit_button, 2, 0, 1, 2)

    def save(self, result, result_percentage):
        self.db.add_result(
self.user.id_user, self.id_test, result, result_percentage)

    def set(self, object):
        self.id_button = self.group.id(object)
        self.index = self.id_button - 1
        self.clear_grid(self.layout_question)
        self.get_content_question()
                
    def get_answer(self):
        answer = []
        for i in range(self.layout_question.count()):
            widget = self.layout_question.itemAt(i).widget()
            if type(widget) == QtWidgets.QLineEdit:
                answer.append(widget.text())
                if answer[0]:
                    self.b = True
            elif type(widget) == QtWidgets.QRadioButton or type(widget) == QtWidgets.QCheckBox:
                if widget.isChecked():
                    self.b = True

    def set_color_button(self):
        self.get_answer()    
        if self.b:
            self.group.button(self.id_button).setStyleSheet(
'background: rgb(144,238,144);')
        else:
            self.group.button(self.id_button).setStyleSheet(None)
        self.b = False
        
    def get_content_question(self):
        n = 0 
        j = 0 
        for i in self.answers_list[self.index]:
            if (self.questions_list[self.index][2] == 1):
                self.radio_answer = QtWidgets.QRadioButton(
self.answers_list[self.index][j][0])
                self.radio_answer.clicked.connect(self.set_color_button)
                if self.answers[self.index]:
                    self.radio_answer.setChecked(self.answers[self.index][j])
                self.layout_question.addWidget(self.radio_answer, n, 0, 1, 1)
            elif (self.questions_list[self.index][2] == 2):
                self.check_answer = QtWidgets.QCheckBox(
self.answers_list[self.index][j][0])
                self.check_answer.clicked.connect(self.set_color_button)
                self.layout_question.addWidget(self.check_answer, n, 0, 1, 1)
                if self.answers[self.index]:
                    self.check_answer.setChecked(self.answers[self.index][j])
            elif (self.questions_list[self.index][2] == 3):
                self.lineedit_answer = QtWidgets.QLineEdit()
                self.lineedit_answer.textChanged.connect(
self.set_color_button)
                self.layout_question.addWidget(
self.lineedit_answer, n, 0, 1, 1)   
                if self.answers[self.index]:
                   self.lineedit_answer.setText(
str(self.answers[self.index][j]))   
            n += 1
            j += 1
        self.groupBox_question.setTitle(self.questions_list[self.index][1])        

    def calculate_result(self):
        result = 0
        for i in range(len(self.answers_list)):
            a = True
            for j in range(len(self.answers_list[i])):
                if self.answers[i]:
                    if (isinstance(self.answers[i][j], str)):
                        if self.answers_list[i][j][0]!= self.answers[i][j]:
                            a = False
                    else:
                        if self.answers_list[i][j][1]!= self.answers[i][j]:
                            a = False
                else:
                    a = False
            if a:
                result += 1

        number_questions = self.test[3]
        result_percentage = (result * 100) / number_questions

        self.save(result, result_percentage)
        self.view_result(result_percentage)

    def msgClick(self):
        self.close()
        
    def view_result(self, result_percentagle):
        msg = QtWidgets.QMessageBox()
        msg.setText(
f"Тестирование завершено.\nВаш результат: {result_percentagle}%")
        msg.setWindowTitle("Результат")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.buttonClicked.connect(self.msgClick)
        msg.exec()    


    




