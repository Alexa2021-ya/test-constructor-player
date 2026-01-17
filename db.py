from PyQt6 import QtSql

class DB:
    def __init__(self):
        self.createConnection()

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setDatabaseName('tests')
        self.db.setUserName("postgres")
        self.db.setPassword("123")
        self.db.setPort(5432)
            
    def search_for_user_by_name(self, name):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT id FROM users WHERE name = '{name}'")
        print(query.value(0))
        while query.next():
            return query.value(0)
                
    def search_test_by_name(self, name):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT id FROM test WHERE name = '{name}'")
        
        while query.next():
            return query.value(0)

    def password_check(self, id_user, password):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT password FROM users WHERE id = '{id_user}'")

        while query.next():
            if (password == query.value(0)):
                return True
            else:
                return False            

    def add_test(self, name, id_creator, count_questions):
        query = QtSql.QSqlQuery()
        query.exec(f"INSERT INTO test (name, id_creator, count_questions) VALUES ('{name}', '{id_creator}', '{count_questions}')")
        
        return query.lastInsertId() 
    
    def add_question(self, name, id_test, id_type):
        query = QtSql.QSqlQuery()
        query.exec(f"INSERT INTO questions (name, id_test, id_type) VALUES ('{name}', '{id_test}', '{id_type}')")
        
        return query.lastInsertId() 

    def add_answer(self, name, id_question, is_true):
        query = QtSql.QSqlQuery()
        query.exec(f"INSERT INTO answers (name, id_question, is_true) VALUES ('{name}', '{id_question}', '{is_true}')")
            
    def add_user(self, name, password, id_role):
        query = QtSql.QSqlQuery()
        query.exec(f"INSERT INTO users (name, password, id_role) VALUES ('{name}', '{password}', '{id_role}')")
    
    def get_role(self, id_user):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT id_role FROM users WHERE id = '{id_user}'")

        while query.next():
            return query.value(0)
    
    def get_tests(self, id_user):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT * FROM test WHERE id_creator = '{id_user}'")
        tests = []
        while query.next():
            tests.append([query.value(0), query.value(1), 
    query.value(2), query.value(3)])
        return tests
    
    def get_id_test(self, index):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT id FROM test")
        while query.next():
            return query.value(0)

    def get_test(self, id_test):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT * FROM test WHERE id = '{id_test}'")
        while query.next():
            return [query.value(0), query.value(1), 
   query.value(2), query.value(3)]

    def get_all_info_test(self, id_user):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT name, count_questions FROM test WHERE id_creator = '{id_user}'")
        while query.next():
            return [query.value(0), query.value(1)]

    def get_all_info_questions(self, id_test):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT id, name, id_type, id_test FROM questions WHERE id_test = '{id_test}' ORDER BY id")
        questions = []
        while query.next():
            questions.append([query.value(0), query.value(1), query.value(2)])
        return questions

    def get_all_info_answers(self, id_question):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT name, is_true FROM answers WHERE id_question = '{id_question}'")
        answers = []        
        while query.next():
            answers.append([query.value(0), query.value(1)])
        return answers
        

    def set_count_questions(self, id_test, count):
        query = QtSql.QSqlQuery()
        query.exec(f"UPDATE test SET count_questions = '{count}' WHERE id = '{id_test}'")
            
    def get_count_questions(self, id_test):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT count_questions FROM test WHERE id = '{id_test}'")
        while query.next():
            return query.value(0)

    def delete_question(self, id_test, id_question):
        self.delete_answers(id_question)
        query = QtSql.QSqlQuery()
        query.exec(f"DELETE FROM questions WHERE id = '{id_question}'")
        count = self.get_count_questions(id_test)
        count = count - 1
        self.set_count_questions(id_test, count)

    def set_type_question(self, id_question, type_q):
        query = QtSql.QSqlQuery()
        query.exec(f"UPDATE questions SET id_type = '{type_q}' WHERE id = '{id_question}'")

    def delete_answers(self, id_question):
        query = QtSql.QSqlQuery()
        query.exec(f"DELETE FROM answers WHERE id_question = '{id_question}'")
            
    def set_test(self, name, id_test):
        query = QtSql.QSqlQuery()
        query.exec(f"UPDATE test SET name = '{name}' WHERE id = '{id_test}'")
            
    def delete_test(self, id_test):
        questions = self.get_all_info_questions(id_test)
        for i in questions:
            self.delete_question(id_test, i[0])
        query = QtSql.QSqlQuery()
        query.exec(f"DELETE FROM results WHERE id_test = '{id_test}'")
        query = QtSql.QSqlQuery()
        query.exec(f"DELETE FROM test WHERE id = '{id_test}'")
                
    def get_all_tests(self):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT * FROM test")
        tests = []
        while query.next():
            tests.append([query.value(0), query.value(1), 
query.value(2), query.value(3)])
        return tests    

    def get_creator(self, id_creator):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT * FROM users WHERE id = '{id_creator}'")
        while query.next():
            return query.value(0)

    def add_result(self, id_taker, id_test, result, result_percentage):
        query = QtSql.QSqlQuery()
        query.exec(f"INSERT INTO results (id_taker, id_test, result, result_percentage) VALUES ('{id_taker}', '{id_test}', '{result}', '{result_percentage}')")

    def get_result(self, id_test, id_taker):
        query = QtSql.QSqlQuery()
        query.exec(f"SELECT * FROM results WHERE id_test = '{id_test}' AND id_taker = '{id_taker}'")
        while query.next():
            return [query.value(0), query.value(1),
 query.value(2), query.value(3), query.value(4)]

    def delete_result(self, id_test, id_taker):
        query = QtSql.QSqlQuery()
        query.exec(f"DELETE FROM results WHERE id_test = '{id_test}' AND id_taker = '{id_taker}'")
 
    def set_name_question(self, id_question, name):
        query = QtSql.QSqlQuery()
        query.exec(f"UPDATE questions SET name = '{name}' WHERE id = '{id_question}'")



