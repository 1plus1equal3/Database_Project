import pandas as pd
import pyodbc as pdb
from flask import Flask, request, jsonify
from flask_cors import CORS

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


### Utility functions ###
# Username, password & email validation must be done in frontend!
def register_user(user):
    username = user.get('username')
    password = user.get('password')
    email = user.get('email')

    # User_id validation
    select_query = f"""
    DECLARE @result INT;
    EXEC @result = func_register '{username}', '{password}', '{email}';
    SELECT @result;
    """
    cursor = conn.cursor()
    cursor.execute(select_query)
    conn.commit()
    records = cursor.fetchone()
    if records[0] == 1:
        msg = jsonify({'success': True})
    elif records[0] == 0:
        msg = jsonify({'success': False, 'error': 'Username already exists'})
    return msg

def login_user(user):
    username = user.get('username')
    password = user.get('password')
    cursor = conn.cursor()
    query = 'SELECT dbo.func_login(?, ?)'
    cursor.execute(query, username, password)
    user = cursor.fetchone()
    user_id = user[0]
    if user_id != -1:
        return jsonify({'success': True, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'error': 'Invalid username or password'})

def get_user_info(id):
    query = 'SELECT * FROM User_info WHERE user_id = ?'
    cursor = conn.cursor() 
    cursor.execute(query, id)
    user = cursor.fetchone()
    return jsonify(user)

def requestExam():
    cursor = conn.cursor()
    query = 'SELECT * FROM dbo.request_exam();'
    cursor.execute(query)
    fetch_result = cursor.fetchall()
    examList = []
    # base_url = 'http://localhost:5000/exam?exam_id='
    for i in fetch_result:
        test_dict = {
            'exam_id': i[0],
            'title': i[1],
            'date_created': i[2],
        }
        examList.append(test_dict)
    return jsonify(examList)

def show_test(exam_id):
    cursor = conn.cursor()
    query = "EXEC GetTestQuestions @TestID = ?"
    cursor.execute(query, exam_id)
    questions = cursor.fetchall()
    #return questions
    list_ques = []
    for i in range(len(questions)):
        # print(questions[i][0])
        cursor = conn.cursor()
        query_opt = f"EXEC GetAnswerText @question_ID = '{questions[i][0]}';"
        cursor.execute(query_opt)
        options = cursor.fetchall()
        list_ques.append({'question': questions[i][1], 'opt_a': options[0][0], 'opt_b': options[1][0], 'opt_c': options[2][0], 'opt_d': options[3][0], 'question_id': questions[i][0]})
    return jsonify(list_ques)

def evaluate_exam(answer):
    # print(answer.get('selectedOptions')[0])
    # print(answer.get('user_id'))
    user_id = answer.get('user_id')
    test_id = answer.get('test_id')
    question_num = answer.get('num_of_questions')
    selectedOptions = answer.get('selectedOptions')
    # Get number of correct answers
    point = 0
    for ans in selectedOptions:
        query = f"SELECT dbo.getCorrectAns('{ans.get('question_id')}');"
        cursor = conn.cursor()
        cursor.execute(query)
        correct_answer = cursor.fetchone()
        # print(correct_answer[0])
        # print(ord(correct_answer[0]) - ord('a'))
        if ans.get('answer') == ord(correct_answer[0]) - ord('a'):
            point += 1
    # Calculate score
    point = round(point / question_num * 10, 2)

    # Insert score into database
    cursor = conn.cursor()
    query = f"EXEC insertHistory @user_id = {user_id}, @test_id = {test_id}, @score = {point};"
    cursor.execute(query)
    conn.commit()
    return jsonify({'success': True,'submit_state': 'success', 'score': point})

def show_history(user_id):
    cursor = conn.cursor()
    query = f"SELECT * FROM dbo.request_user_history({user_id});"
    cursor.execute(query)
    history = cursor.fetchall()
    list_history = []
    for i in range(len(history)):
        list_history.append({'test_id': history[i][1], 'title': history[i][4], 'score': history[i][2], 'date': history[i][3]})
    return jsonify(list_history)

### Server communication ###
app = Flask(__name__)
CORS(app)

# @app.route('/')
# def home():
#     return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    msg = register_user(data)
    return msg

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    msg = login_user(data)
    return msg

@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    data = request.get_json()
    info = get_user_info(data)
    return info

@app.route('/request_exam', methods=['GET'])
def request_exam():
    examList = requestExam()
    print(examList)
    return examList

@app.route('/exam', methods=['GET'])
def exam():
    exam_id = request.args.get('exam_id')
    questionList = show_test(exam_id)
    return questionList

@app.route('/test_interface', methods = ['POST'])
def test_interface():
    answer = request.get_json()
    result = evaluate_exam(answer)
    return result

@app.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id')
    history = show_history(user_id)
    return history

# Start server
if __name__ == '__main__':
    app.run(debug=True)

