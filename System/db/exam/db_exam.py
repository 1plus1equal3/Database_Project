from ..db_connection import conn
from datetime import date

# Query random exam for students to practice
def db_get_exam():
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
    return examList

# Query exam created by admin
def db_admin_exam(user_id):
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
    return examList

# Query test questions
def db_test_question(exam_id):
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
    return list_ques

# Evaluate question answer
def db_question_answer(question_id):
    query = f"SELECT dbo.getCorrectAns('{question_id}');"
    cursor = conn.cursor()
    cursor.execute(query)
    correct_answer = cursor.fetchone()
    return correct_answer[0]

# Search exam by id
def db_search_exam_id(id):
    cursor = conn.cursor()
    query_id = "EXEC SearchTestID @TestID = ?"
    cursor.execute(query_id, id)
    info = cursor.fetchall()
    list_test = []
    list_test.append({'exam_id': info[0][0], 'Title': info[0][1], 'Admin': info[0][3], 'Date': info[0][2]})
    return list_test

# Search exam by title
def db_search_exam_title(title):
    cursor = conn.cursor()
    query_title = "EXEC SearchTestTitle @title = ?"
    cursor.execute(query_title, title)
    info = cursor.fetchall()
    list_test = []
    for i in range(len(info)):
        list_test.append({'exam_id': info[i][0], 'Title': info[i][1], 'Admin': info[i][3], 'Date': info[i][2]})
    return list_test

# Search question by content, subject, level
def db_search_question(content, subject, difficulty):
    query = "EXEC searchQuestion @content = ?, @subject = ?, @level = ?"
    level = 1
    if difficulty == 'Medium':
        level = 2
    elif difficulty == 'Hard':
        level = 3
    question_info = []
    cursor = conn.cursor()
    cursor.execute(query, content, subject, level)
    info = cursor.fetchall()
    for i in range(len(info)):
        query = "EXEC getAnswerText @question_ID = ?"
        cursor.execute(query, info[i][0])
        answer = cursor.fetchall()
        question_info.append({'question_id': info[i][0], 'content': info[i][1], 'level': info[i][2], 'subject': info[i][3], 'opt_a': answer[0][0], 'opt_b': answer[1][0], 'opt_c': answer[2][0], 'opt_d': answer[3][0]})
    return question_info

# Create test
def db_create_test(test_info):
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

# def requestExam():
#     cursor = conn.cursor()
#     query = 'SELECT * FROM dbo.request_exam();'
#     cursor.execute(query)
#     fetch_result = cursor.fetchall()
#     examList = []
#     # base_url = 'http://localhost:5000/exam?exam_id='
#     for i in fetch_result:
#         test_dict = {
#             'exam_id': i[0],
#             'title': i[1],
#             'date_created': i[2],
#         }
#         examList.append(test_dict)
#     return jsonify(examList)

# def getAdminExam(user_id):
#     cursor = conn.cursor()
#     query = 'SELECT * FROM dbo.request_admin_exam(?);'
#     cursor.execute(query, user_id)
#     fetch_result = cursor.fetchall()
#     examList = []
#     for i in fetch_result:
#         test_dict = {
#             'exam_id': i[0],
#             'title': i[1],
#             'date_created': i[2],
#             'subject': i[4],
#             'difficulty': i[5]
#         }
#         examList.append(test_dict)
#     return jsonify(examList)

# def show_test(exam_id):
#     cursor = conn.cursor()
#     query = "EXEC GetTestQuestions @TestID = ?"
#     cursor.execute(query, exam_id)
#     questions = cursor.fetchall()
#     #return questions
#     list_ques = []
#     for i in range(len(questions)):
#         # print(questions[i][0])
#         cursor = conn.cursor()
#         query_opt = f"EXEC GetAnswerText @question_ID = '{questions[i][0]}';"
#         cursor.execute(query_opt)
#         options = cursor.fetchall()
#         list_ques.append({'question': questions[i][1], 'opt_a': options[0][0], 'opt_b': options[1][0], 'opt_c': options[2][0], 'opt_d': options[3][0], 'question_id': questions[i][0]})
#     return jsonify(list_ques)

# def evaluate_exam(answer):
#     # print(answer.get('selectedOptions')[0])
#     # print(answer.get('user_id'))
#     user_id = answer.get('user_id')
#     test_id = answer.get('test_id')
#     question_num = answer.get('num_of_questions')
#     selectedOptions = answer.get('selectedOptions')
#     # Get number of correct answers
#     point = 0
#     for ans in selectedOptions:
#         query = f"SELECT dbo.getCorrectAns('{ans.get('question_id')}');"
#         cursor = conn.cursor()
#         cursor.execute(query)
#         correct_answer = cursor.fetchone()
#         # print(correct_answer[0])
#         # print(ord(correct_answer[0]) - ord('a'))
#         if ans.get('answer') == ord(correct_answer[0]) - ord('a'):
#             point += 1
#     # Calculate score
#     point = round(point / question_num * 10, 2)

#     # Insert score into database
#     cursor = conn.cursor()
#     query = f"EXEC insertHistory @user_id = {user_id}, @test_id = {test_id}, @score = {point};"
#     cursor.execute(query)
#     conn.commit()
#     return jsonify({'success': True,'submit_state': 'success', 'score': point})

# def search_test(search_request):
#     print(search_request)
#     type = search_request['option']
#     cursor = conn.cursor()
#     query_id = "EXEC SearchTestID @TestID = ?"
#     query_title = "EXEC SearchTestTitle @title = ?"
#     if type == 1: #search by id
#         cursor.execute(query_id, int(search_request['search']))
#         info = cursor.fetchall()
#         list_test = []
#         list_test.append({'exam_id': info[0][0], 'Title': info[0][1], 'Admin': info[0][3], 'Date': info[0][2]})
#         return jsonify(list_test)
#     else:
#         cursor.execute(query_title, search_request['search'])
#         info = cursor.fetchall()
#         list_test = []
#         for i in range(len(info)):
#             list_test.append({'exam_id': info[i][0], 'Title': info[i][1], 'Admin': info[i][3], 'Date': info[i][2]})
#         return jsonify(list_test)
    
# def search_question(search_request):
#     query = "EXEC searchQuestion @content = ?, @subject = ?, @level = ?"
#     level = 1
#     if search_request['difficulty'] == 'Medium':
#         level = 2
#     elif search_request['difficulty'] == 'Hard':
#         level = 3
#     question_info = []
#     cursor = conn.cursor()
#     cursor.execute(query, search_request['search'], search_request['subject'], level)
#     info = cursor.fetchall()
#     for i in range(len(info)):
#         query = "EXEC getAnswerText @question_ID = ?"
#         cursor.execute(query, info[i][0])
#         answer = cursor.fetchall()
#         question_info.append({'question_id': info[i][0], 'content': info[i][1], 'level': info[i][2], 'subject': info[i][3], 'opt_a': answer[0][0], 'opt_b': answer[1][0], 'opt_c': answer[2][0], 'opt_d': answer[3][0]})
#     return jsonify(question_info)
    
# def create_test(test_info):
#     title = test_info.get('title')
#     question_number = test_info.get('numQuestions')
#     subject = test_info.get('subject')
#     difficulty = test_info.get('difficulty')
#     if difficulty == 'Easy':
#         difficulty = 1
#     elif difficulty == 'Medium':
#         difficulty = 2
#     else:
#         difficulty = 3
#     admin_id = test_info.get('admin_id')
#     query_question = """
#     SET NOCOUNT ON;
#     EXEC createTest ?, ?, ?, ?, ?, ?;
#     """
#     cursor = conn.cursor()
#     cursor.execute(query_question, question_number, title, date.today(), admin_id, subject, difficulty)
#     records = cursor.fetchone()
#     conn.commit()
#     if records[0] == 0:
#         return {'success': False , 'message': 'Test already exists! or Invalid title!'}
#     return {'success': True, 'test_id': records[0], 'message': 'Test created successfully!'}