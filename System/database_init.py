import pyodbc as pdb
import json
import random
from datetime import date 

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

def create_test(test_info):
    title = test_info.get('title')
    question_number = test_info.get('numQuestions')
    subject = test_info.get('subject')
    difficulty = test_info.get('difficulty')
    if difficulty == 'Easy':
        difficulty = 1
    elif difficulty == 'Medium':
        difficulty = 2
    else:
        difficulty = 3
    admin_id = test_info.get('admin_id')
    query_question = """
    SET NOCOUNT ON;
    EXEC createTest ?, ?, ?, ?, ?, ?;
    """
    cursor = conn.cursor()
    cursor.execute(query_question, question_number, title, date.today(), admin_id, subject, difficulty)
    records = cursor.fetchone()
    conn.commit()
    if records[0] == 0:
        return {'success': False , 'message': 'Test already exists! or Invalid title!'}
    return {'success': True, 'test_id': records[0], 'message': 'Test created successfully!'}


### Main ###
if __name__ == '__main__':
    Subject = ["Unknown", "Biochemistry", "Surgery", "Ophthalmology",
                "Physiology", "Gynaecology & Obstetrics", "Anaesthesia", "Psychiatry",
                "Microbiology", "Medicine", "Pharmacology", "Dental", "ENT",
                "Forensic Medicine", "Pediatrics", "Orthopaedics", "Radiology",
                "Pathology", "Skin", "Anatomy", "Social & Preventive Medicine"]
    difficulty = ['Easy', 'Medium', 'Hard']
    # Generate 100 sample tests
    for i in range (99, 121):
        # Get random subject
        subject = random.choice(Subject)
        # Get random difficulty
        level = random.choice(difficulty)
        # Get random number of questions
        numQuestions = random.randint(1, 5) * 10
        test_info = {
            'title': f'sample_test_{i}',
            'numQuestions': numQuestions,
            'subject': subject,
            'difficulty': level,
            'admin_id': 1
        }
        msg = create_test(test_info)
        print(msg)
    conn.close()

