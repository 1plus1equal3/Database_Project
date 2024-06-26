import pandas as pd
import pyodbc as pdb
from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib.pyplot as plt
import numpy as np

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

def hash(password):
    hashed_password = ""
    for char in password:
        temp = int((17 * ord(char) / 11) + 2003)
        hashed_password += chr(temp % 87 + 40)
    return hashed_password

def register_user(user):
    username = user.get('username')
    password = hash(user.get('password'))
    email = user.get('email')

    # User validation
    select_query = f"""select dbo.checkUser('{username}');"""
    cursor = conn.cursor()
    cursor.execute(select_query)
    records = cursor.fetchone()
    msg = ''
    if records[0] == -1:
        msg = jsonify({'success': False, 'error': 'Username already exists'})
        return msg
    msg = jsonify({'success': True})
    select_query = f"""EXEC func_register '{username}', '{password}', '{email}';"""
    cursor = conn.cursor()
    cursor.execute(select_query)
    return msg
    

def login_user(user):
    username = user.get('username')
    password = hash(user.get('password'))
    cursor = conn.cursor()
    query = 'SELECT dbo.func_login(?, ?)'
    cursor.execute(query, username, password)
    user = cursor.fetchone()
    user_id = user[0]
    if user_id == -1:
        return jsonify({'success': False, 'error': 'Invalid username or password'})
    query = 'SELECT dbo.checkUserRole(?)'
    cursor.execute(query, user_id)
    user_type = cursor.fetchone()[0]
    return jsonify({'success': True, 'user_id': user_id, 'username': username, 'user_type': user_type})
        

def get_user_info(id):
    query = 'EXEC getUserInfo @user_id = ?;'
    cursor = conn.cursor() 
    cursor.execute(query, id)
    user = cursor.fetchone()
    user_id = user[0]
    username = user[1]
    email = user[3]
    user_type = user[4]
    user = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'user_type': user_type
    }
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

def search_test(search_request):
    print(search_request)
    type = search_request['option']
    cursor = conn.cursor()
    query_id = "EXEC SearchTestID @TestID = ?"
    query_title = "EXEC SearchTestTitle @title = ?"
    if type == 1: #search by id
        cursor.execute(query_id, int(search_request['search']))
        info = cursor.fetchall()
        test = {'exam_id': info[0][0], 'Title': info[0][1], 'Admin': info[0][3], 'Date': info[0][2]}
        return jsonify(test)
    else:
        cursor.execute(query_title, search_request['search'])
        info = cursor.fetchall()
        list_test = []
        for i in range(len(info)):
            list_test.append({'exam_id': info[i][0], 'Title': info[i][1], 'Admin': info[i][3], 'Date': info[i][2]})
        return jsonify(list_test)

'''
CREATE FUNCTION [dbo].Statist
(
@used_id INT
)
RETURNS TABLE
AS
RETURN(
SELECT COUNT (*) AS num_of_test, AVG(score) AS average_score, MAX(score) as max_score, MIN(score) as min_score
FROM History WHERE user_id = @used_id
);
'''

def statistic(user_id):
    query = "SELECT * from dbo.statistic(?)"
    cursor = conn.cursor()
    cursor.execute(query, user_id)
    data = cursor.fetchall()
    statistic_data = {'Number_of_test' : data[0][0], 'Average_score': data[0][1], 'Max_score': data[0][2], 'Min_score': data[0][3]}
    list_score = []
    query_score = "SELECT score FROM History WHERE user_id = ?"
    cursor.execute(query_score, user_id)
    score = cursor.fetchall()
    for i in range(len(score)):
        list_score.append(score[i][0])
    
    # Calculate average, max, and min
    average_value = statistic_data['Average_score']
    max_value = statistic_data['Max_score']
    min_value = statistic_data['Min_score']

# Plot the list_score as a bar chart
    plt.bar(range(len(list_score)), list_score, label='list_score', color='#03A9F4')

# Add bars for average, max, and min values
    plt.axhline(average_value, color='r', linestyle='--', label='Average score')
    plt.axhline(max_value, color='g', linestyle='--', label='Max score')
    plt.axhline(min_value, color='b', linestyle='--', label='Min score')

# Add labels and title
    plt.xlabel('Test')
    plt.ylabel('Score')
    plt.title('Evaluate study process')

# Add legend
    plt.legend()

# Show the plot
    plt.savefig('static_images/statistic_barchart.png')

    bins = [0, 4, 7, 9 ,float('inf')]
 
# Use numpy's histogram function to count values in each bin
    hist, _ = np.histogram(list_score, bins=bins)
    
    # Calculate the percentage of values in each bin
    total_values = len(list_score)
    percentages = hist / total_values * 100
    
    # Labels for different ranges
    labels = ['Below average', 'Average', 'Good', 'Excellent']
    
    # Plot the pie chart
    plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    
    # Add title
    plt.title('Percentage of score')
    
    # Show the plot
    plt.savefig('static_images/statistic_piechart.png')

    

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
    user_id = request.args.get('user_id')
    info = get_user_info(user_id)
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

@app.route('/search', methods=['POST'])
def search():
    search_request = request.get_json()
    result = search_test(search_request)
    return result

@app.route('/create_test', methods=['POST'])
def create_test():
    data = request.get_json()
    print(data)
    return jsonify({'success': True})

# Start server
if __name__ == '__main__':
    app.run(debug=True)

