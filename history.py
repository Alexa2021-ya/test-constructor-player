from PyQt6 import QtCore, QtGui, QtWidgets, QtSql
from db import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(478, 369)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.table_history = QtWidgets.QTableView(parent=Form)
        self.table_history.setObjectName("table_history")
        self.gridLayout.addWidget(self.table_history, 0, 0, 1, 1)
    
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = DB()
        self.db.createConnection()
        self.setModel()
        
    def setModel(self):
        self.model_history = QtSql.QSqlRelationalTableModel() 
        self.model_history.setTable('results')
        
        self.model_history.setHeaderData(1, 
QtCore.Qt.Orientation.Horizontal, 'Пользователь')
        self.model_history.setHeaderData(2, 
QtCore.Qt.Orientation.Horizontal, 'Тест')
        self.model_history.setHeaderData(4, 
QtCore.Qt.Orientation.Horizontal, 'Результат(в процентах)')
        self.model_history.setRelation(1, 
QtSql.QSqlRelation("users", "id", "name"))
        self.model_history.setRelation(2, 
QtSql.QSqlRelation("test", "id", "name"))
        self.model_history.setJoinMode(
QtSql.QSqlRelationalTableModel.JoinMode.LeftJoin)
        self.model_history.select()
        self.table_history.setModel(self.model_history)
        self.table_history.setColumnHidden(0, True)
        self.table_history.setColumnHidden(3, True)
        self.table_history.setEditTriggers(
QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)              
        self.table_history.setSortingEnabled(True)        
        self.table_history.horizontalHeader().setSectionResizeMode(
QtWidgets.QHeaderView.ResizeMode.Stretch)        


