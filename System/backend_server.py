import pyodbc as pdb
from datetime import date 
from flask import Flask, request, jsonify, render_template, send_from_directory
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

### Authentication functions ###

def register_user(user):
    username = user.get('username')
    password = hash(user.get('password'))
    email = user.get('email')

    # User validation
    select_query = f"""
    SET NOCOUNT ON;
    EXEC func_register '{username}', '{password}', '{email}';
    """
    cursor = conn.cursor()
    cursor.execute(select_query)
    records = cursor.fetchone()
    msg = ''
    if records[0] == -1:
        msg = jsonify({'success': False, 'error': 'Username already exists'})
        return msg
    msg = jsonify({'success': True})
    return msg
    
#!TODO: Change the query
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
        
### User information functions ###
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

def getAdminExam(user_id):
    cursor = conn.cursor()
    query = 'SELECT * FROM dbo.request_admin_exam(?);'
    cursor.execute(query, user_id)
    fetch_result = cursor.fetchall()
    examList = []
    for i in fetch_result:
        test_dict = {
            'exam_id': i[0],
            'title': i[1],
            'date_created': i[2],
            'subject': i[4],
            'difficulty': i[5]
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
        list_test = []
        list_test.append({'exam_id': info[0][0], 'Title': info[0][1], 'Admin': info[0][3], 'Date': info[0][2]})
        return jsonify(list_test)
    else:
        cursor.execute(query_title, search_request['search'])
        info = cursor.fetchall()
        list_test = []
        for i in range(len(info)):
            list_test.append({'exam_id': info[i][0], 'Title': info[i][1], 'Admin': info[i][3], 'Date': info[i][2]})
        return jsonify(list_test)
    
def search_question(search_request):
    query = "EXEC searchQuestion @content = ?, @subject = ?, @level = ?"
    level = 1
    if search_request['difficulty'] == 'Medium':
        level = 2
    elif search_request['difficulty'] == 'Hard':
        level = 3
    question_info = []
    cursor = conn.cursor()
    cursor.execute(query, search_request['search'], search_request['subject'], level)
    info = cursor.fetchall()
    for i in range(len(info)):
        query = "EXEC getAnswerText @question_ID = ?"
        cursor.execute(query, info[i][0])
        answer = cursor.fetchall()
        question_info.append({'question_id': info[i][0], 'content': info[i][1], 'level': info[i][2], 'subject': info[i][3], 'opt_a': answer[0][0], 'opt_b': answer[1][0], 'opt_c': answer[2][0], 'opt_d': answer[3][0]})
    return jsonify(question_info)
    
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

def getUserList():
    cursor = conn.cursor()
    query = 'SELECT * FROM dbo.userList();'
    cursor.execute(query)
    fetch_result = cursor.fetchall()
    userList = []
    for i in fetch_result:
        user_dict = {
            'user_id': i[0],
            'username': i[1],
            'email': i[2],
        }
        userList.append(user_dict)
    return jsonify(userList)

def statistic(user_id):
    query = "SELECT * from dbo.Statist(?)"
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
    average_value = round(statistic_data['Average_score'], 2)
    max_value = statistic_data['Max_score']
    min_value = statistic_data['Min_score']
    # Plot the list_score as a bar chart
    plt.clf()
    plt.ticklabel_format(style='plain',axis='x',useOffset=False)
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
    # Save the plot
    plt.savefig('System/static/statistic_images/statistic_barchart.png')
    # Clean up the current plot
    plt.clf()
    # Create a pie chart
    bins = [0, 4, 8, 10]
    # Use numpy's histogram function to count values in each bin
    hist, _ = np.histogram(list_score, bins=bins)
    # Calculate the percentage of values in each bin
    total_values = len(list_score)
    percentages = hist / total_values * 100
    # Labels for different ranges
    labels = ['Below average', 'Average', 'Good']
    # Plot the pie chart
    plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    # Add title
    plt.title('Percentage of score')
    # Show the plot
    plt.savefig('System/static/statistic_images/statistic_piechart.png')
    msg = {'success': True, 
           'average': average_value,
           'max': max_value,
           'min': min_value}
    return jsonify(msg)

def getClassFromDB(teacher_id):
    # Query database for data
    query = 'EXEC dbo.viewTeacherClasses @teacherId = ?'
    cursor = conn.cursor()
    cursor.execute(query, teacher_id)
    data = cursor.fetchall()
    # Structure data
    classList = []
    for i in data:
        class_data = {
            'title': i[2],
            'std_num': i[3],
            'date': i[4]
        }
        classList.append(class_data)
    cursor.commit()
    # Return json data
    return jsonify(classList)

def createNewClass(info):
    class_name = info.get('class_name')
    teacher_id = info.get('user_id')
    query = 'EXEC dbo.createClass @teacherId = ?, @className = ?'
    cursor = conn.cursor()
    cursor.execute(query, teacher_id, class_name)
    response = cursor.fetchone()
    conn.commit()
    if response[0] == 0:
        return {'success': False, 'message': 'Class already exists!'}
    else:
        return {'success': True, 'message': 'Class created successfully!'}
    

### Server communication ###
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register.html')
def testregister():
    return render_template('testregister.html')

@app.route('/dashboard_user.html')
def dashboard_user():
    return render_template('dashboard_user.html')

@app.route('/dashboard_admin.html')
def dashboard_admin():
    return render_template('dashboard_admin.html')

@app.route('/test_interface.html')
def test_interface_html():
    exam_id = request.args.get('exam_id')
    return render_template('test_interface.html', exam_id=exam_id)

@app.route('/history.html')
def history_html():
    return render_template('history.html')

@app.route('/dashboard_user_search.html')
def search_html():
    return render_template('dashboard_user_search.html')

@app.route('/profile.html')
def profile_html():
    return render_template('profile.html')

@app.route('/test_view.html')
def test_view_html():
    exam_id = request.args.get('exam_id')
    return render_template('test_view.html', exam_id=exam_id)

@app.route('/profile_admin.html')
def profile_admin_html():
    return render_template('profile_admin.html')

@app.route('/createtests_admin.html')
def create_test_html():
    return render_template('createtests_admin.html')

@app.route('/admin_search_question.html')
def search_question_html():
    return render_template('admin_search_question.html')

@app.route('/dashboard_admin_search.html')
def search_admin_html():
    return render_template('dashboard_admin_search.html')

@app.route('/admin_stats.html')
def admin_stats_html():
    return render_template('admin_stats.html')

@app.route('/user_stats.html')
def user_stats_html():
    return render_template('user_stats.html')

@app.route('/statistic_piechart.png')
def statistic_piechart():
    return send_from_directory('static', 'statistic_images/statistic_piechart.png')

@app.route('/statistic_barchart.png')
def statistic_barchart():
    return send_from_directory('static', 'statistic_images/statistic_barchart.png')

@app.route('/class.html')
def class_html():
    return render_template('class.html')

@app.route('/delete_class.html')
def delete_class_html():
    return render_template('delete_class.html')

@app.route('/class_interface.html')
def class_interface_html():
    return render_template('class_interface.html')

@app.route('/add_student_to_class.html')
def add_student_to_class_html():
    return render_template('add_student_to_class.html')

@app.route('/delete_student_from_class.html')
def delete_student_from_class_html():
    return render_template('delete_student_from_class.html')

# API endpoints
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

@app.route('/request_admin_exam', methods=['GET'])
def request_admin_exam():
    user_id = request.args.get('id')
    list = getAdminExam(user_id)
    return list

@app.route('/exam', methods=['GET'])
def exam():
    exam_id = request.args.get('exam_id')
    questionList = show_test(exam_id)
    return questionList

@app.route('/submit_test', methods = ['POST'])
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
def create_random_test():
    data = request.get_json()
    msg = create_test(data)
    return jsonify(msg)

@app.route('/view_test', methods=['GET'])
def view_test():
    exam_id = request.args.get('exam_id')
    questionList = show_test(exam_id)
    return questionList

@app.route('/search_question', methods=['POST'])
def search_question_api():
    search_request = request.get_json()
    result = search_question(search_request)
    return result

@app.route('/list_user', methods=['GET'])
def getUserListAPI():
    userList = getUserList()
    return userList

@app.route('/statistic', methods=['GET'])
def statistic_html():
    user_id = request.args.get('user_id')
    msg = statistic(user_id)
    return msg

@app.route('/request_class', methods=['GET'])
def request_class():
    teacher_id = request.args.get('id')
    classes = getClassFromDB(teacher_id)
    return classes

@app.route('/create_class', methods=['POST'])
def create_new_class():
    class_info = request.get_json()
    response = createNewClass(class_info)
    return response


# Start server
if __name__ == '__main__':
    app.run(debug=True)

