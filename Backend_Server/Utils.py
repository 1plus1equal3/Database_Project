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
    insert_query = f"""
    INSERT INTO Test (title, date_created, admin_id)
    VALUES (?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(insert_query, title, date.today(), 0)
    conn.commit()
    # Get max id
    check_query = """
    SELECT MAX(test_id) FROM Test
    """
    cursor = conn.cursor()
    cursor.execute(check_query)
    fetch = cursor.fetchone()
    max_id = fetch[0]
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
    #Get user input
    while True:
        title = input('Enter title: ')
        question_number = int(input('Enter number of questions: '))
        generate_random_Exam(title, question_number = question_number)
        # Continue?
        print('Do you want to continue? (y/n)')
        choice = input()
        if choice == 'n':
            break
