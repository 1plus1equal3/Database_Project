from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from db import db_connection
from api import *

### Server communication ###
app = Flask(__name__)
CORS(app)

# API endpoints
#! User pages

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login.html')
def login_html():
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

@app.route('/student_class.html')
def student_class_html():
    return render_template('student_class.html')

@app.route('/student_class_interface.html')
def student_class_interface_html():
    return render_template('student_class_interface.html')

#! Admin pages

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

@app.route('/user_class.html')
def user_class_html():
    return render_template('user_class.html')

@app.route('/class.html')
def class_html():
    return render_template('class.html')

@app.route('/delete_class.html')
def delete_class_html():
    return render_template('delete_class_selection.html')

@app.route('/class_interface.html')
def class_interface_html():
    return render_template('class_interface.html')

@app.route('/add_student_to_class.html')
def add_student_to_class_html():
    return render_template('add_student_to_class.html')

@app.route('/delete_student_from_class.html')
def delete_student_from_class_html():
    return render_template('delete_student_from_class.html')

@app.route('/class_test.html')
def class_test_html():
    return render_template('class_test.html')

@app.route('/class_result.html')
def class_results_html():
    return render_template('class_result.html')

# API endpoints
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    msg = api_authen.register_user(data)
    return msg

#!TODO: Change the query
def hash(password):
    hashed_password = ""
    for char in password:
        temp = int((17 * ord(char) / 11) + 2003)
        hashed_password += chr(temp % 87 + 40)
    return hashed_password

def login_user(user):
    username = user.get('username')
    password = hash(user.get('password'))
    from db.db_connection import conn
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    msg = login_user(data)
    return msg

@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    user_id = request.args.get('user_id')
    info = api_user.get_user_info(user_id)
    return info

@app.route('/request_exam', methods=['GET'])
def request_exam():
    examList = api_student.requestExam()
    print(examList)
    return examList

@app.route('/request_admin_exam', methods=['GET'])
def request_admin_exam():
    user_id = request.args.get('id')
    list = api_teacher.getAdminExam(user_id)
    return list

@app.route('/exam', methods=['GET'])
def exam():
    exam_id = request.args.get('exam_id')
    questionList = api_student.show_test(exam_id)
    return questionList

@app.route('/submit_test', methods = ['POST'])
def test_interface():
    answer = request.get_json()
    result = api_student.evaluate_exam(answer)
    return result

@app.route('/submit_class_test', methods = ['POST'])
def submit_class_test():
    test_id = request.args.get('test_id')
    class_id = request.args.get('class_id')
    answer = request.get_json()
    result = api_student.evaluate_class_exam(test_id, class_id, answer)
    return result

@app.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id')
    history = api_student.show_history(user_id)
    return history

@app.route('/search', methods=['POST'])
def search():
    search_request = request.get_json()
    result = api_teacher.search_test(search_request)
    return result

@app.route('/create_test', methods=['POST'])
def create_random_test():
    data = request.get_json()
    msg = api_teacher.create_test(data)
    return jsonify(msg)

@app.route('/view_test', methods=['GET'])
def view_test():
    exam_id = request.args.get('exam_id')
    questionList = api_teacher.show_test(exam_id)
    return questionList

@app.route('/search_question', methods=['POST'])
def search_question_api():
    search_request = request.get_json()
    result = api_teacher.search_question(search_request)
    return result

@app.route('/list_user', methods=['GET'])
def getUserListAPI():
    userList = api_user.getUserList()
    return userList

@app.route('/statistic', methods=['GET'])
def statistic_html():
    user_id = request.args.get('user_id')
    msg = api_student.statistic(user_id)
    return msg

@app.route('/student_class', methods=['GET'])
def get_student_class():
    student_id = request.args.get('id')
    classes = api_student.getStudentClass(student_id)
    return classes

@app.route('/request_class', methods=['GET'])
def request_class():
    teacher_id = request.args.get('id')
    classes = api_teacher.getClassFromDB(teacher_id)
    return classes

@app.route('/create_class', methods=['POST'])
def create_new_class():
    class_info = request.get_json()
    response = api_teacher.createNewClass(class_info)
    print(response)
    return response

@app.route('/delete_class', methods=['POST'])
def delete_class():
    class_ids = request.get_json()['class_ids']
    for class_id in class_ids:
        # print(class_id)
        result = api_teacher.deleteClass(class_id)
    return {'success': True, 'message': 'Class deleted successfully!'}

@app.route('/get_class_info', methods=['GET'])
def class_info():
    class_id = request.args.get('c_id')
    class_info = api_teacher.getClassInfo(class_id)
    return class_info

@app.route('/add_student_to_class', methods=['POST'])
def add_student_to_class():
    class_id = request.get_json()['class_id']
    student_ids = request.get_json()['student_ids']
    error = []
    for student_id in student_ids:
        response = api_teacher.addStudentToClass(class_id, student_id)
        if response['success'] == False:
            print(f'Error adding student {student_id} to class')
            error.append(student_id)
        print(response['message'])
    if len(error) > 0:
        return {'success': False, 'message': 'Error adding students to class', 'error': error}
    return {'success': True, 'message': 'Class deleted successfully!'}

@app.route('/delete_student_from_class', methods=['POST'])
def delete_student_from_class():
    class_id = request.get_json()['class_id']
    student_ids = request.get_json()['student_ids']
    error = []
    for student_id in student_ids:
        response = api_teacher.deleteStudentFromClass(class_id, student_id)
        if response['success'] == False:
            print(f'Error deleting student {student_id} from class')
            error.append(student_id)
        print(response['message'])
    if len(error) > 0:
        return {'success': False, 'message': 'Error deleting students from class', 'error': error}
    return {'success': True, 'message': 'Class deleted successfully!'}

@app.route('/get_class_test', methods=['GET'])
def get_class_test():
    class_id = request.args.get('id')
    test_list = api_teacher.getClassTest(class_id)
    return test_list

@app.route('/add_test_to_class', methods=['POST'])
def add_test_to_class():
    class_id = request.get_json()['class_id']
    test_id = request.get_json()['test_id']
    duration = request.get_json()['duration']
    response = api_teacher.addTestToClass(class_id, test_id, duration)
    return response

@app.route('/delete_test_from_class', methods=['POST'])
def delete_test_from_class():
    class_id = request.get_json()['class_id']
    test_id = request.get_json()['test_id']
    response = api_teacher.deleteTestFromClass(class_id, test_id)
    return response

@app.route('/get_test_result', methods=['POST'])
def get_test_result():
    class_id = request.get_json()['class_id']
    user_id = request.get_json()['user_id']
    test_id = request.get_json()['test_id']
    result = api_teacher.getTestResult(user_id, test_id, class_id)
    return result

# Start server
if __name__ == '__main__':
    app.run(debug=True)
