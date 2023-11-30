import pyodbc as pdb
from datetime import date 
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

def insert_new_exam(title, question_exam):
    check_query = """
    SELECT MAX(test_id) FROM Test
    """
    cursor = conn.cursor()
    cursor.execute(check_query)
    fetch = cursor.fetchone()
    max_id = fetch[0] + 1
    print(max_id)
    insert_query = f"""
    INSERT INTO Test 
    VALUES (?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(insert_query, max_id, title, date.today(), 0)
    conn.commit()
    for q in question_exam:
        query = """
        INSERT INTO Test_question
        VALUES (?, ?)
        """
        cursor = conn.cursor()
        cursor.execute(query, q, max_id)
        conn.commit()
    return 'Question table inserted successfully!'

def generate_random_Exam(title, subject = '%', question_number = 10):
    query_question = f"""
    SELECT TOP {question_number} * FROM Question
    WHERE subject LIKE '{subject}'
    ORDER BY NEWID()
    """
    cursor = conn.cursor()
    cursor.execute(query_question)
    records = cursor.fetchall()
    question_exam = []
    for i in records:
        question_exam.append(i[0])
    print(question_exam)
    insert_new_exam(title, question_exam)

# Test
if __name__ == '__main__':
    generate_random_Exam(title='Sample_01',subject='Medicine')
    generate_random_Exam(title='Sample_02')
    generate_random_Exam(title='Sample_03',question_number=20)
