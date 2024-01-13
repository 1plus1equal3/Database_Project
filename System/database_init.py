import pyodbc as pdb
import json
import random

### Connect to SQL Server database ###
# Connect to SQL Server database info
SERVER = 'DUYNGUYEN\SQLEXPRESS'
DATABASE = 'Project'
USERNAME = 'sa'
PASSWORD = '123456'

# Connection string
connectionString = f'''
DRIVER={{ODBC Driver 18 for SQL Server}};
SERVER={SERVER};DATABASE={DATABASE};
UID={USERNAME};
PWD={PASSWORD};
Encrypt=no;
'''

# Connect to SQL Server
conn = pdb.connect(connectionString)

### Database initialization functions ###
# Create Question table
def create_question_table():
    question = open('database_init\\question.json')
    json_question = json.load(question)
    for q in json_question:
        question = q['question']
        id = q['id']
        subject_name = q['subject_name']
        topic_name = q['topic_name']
        level = random.randint(1, 3)
        query = """
        INSERT INTO Question VALUES (?, ?, ?, ?, ?)
        """
        params = (id, question, level, subject_name, topic_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    return 'Question table created!'

# Create Answer table
def create_answer_table():
    answer = open('database_init\\question.json')
    json_answer = json.load(answer)
    for a in json_answer:
        id = a['id']
        opa = a['opa']
        opb = a['opb']
        opc = a['opc']
        opd = a['opd']
        op = [opa, opb, opc, opd]
        opstr = ['a', 'b', 'c', 'd']
        is_correct = a['cop']
        for i in range(4):
            cr = 0
            if i == (is_correct-1): cr = 1
            query = """
            INSERT INTO Answer VALUES (?, ?, ?, ?)
            """
            params = (id, opstr[i], op[i], cr)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
    return 'Answer table created!'

# Create Explaination table
def create_explaination_table():
    explaination = open('database_init\\question.json')
    json_explaination = json.load(explaination)
    for e in json_explaination:
        id = e['id']
        exp = e['exp']
        query = """
        INSERT INTO Explaination VALUES (?, ?)
        """
        params = (id, exp)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    return 'Explaination table created!'


### Main ###
if __name__ == '__main__':
    #print(create_question_table())
    #print(create_answer_table())
    print(create_explaination_table())
    conn.close()

