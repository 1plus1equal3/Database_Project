from ..db_connection import conn

# Insert score into database
def db_new_history(user_id, test_id, score):
    cursor = conn.cursor()
    query = f"EXEC insertHistory @user_id = {user_id}, @test_id = {test_id}, @score = {score};"
    cursor.execute(query)
    conn.commit()
    return True

# Get history from database
def db_get_history(user_id):
    cursor = conn.cursor()
    query = f"SELECT * FROM dbo.request_user_history({user_id});"
    cursor.execute(query)
    history = cursor.fetchall()
    list_history = []
    for i in range(len(history)):
        list_history.append({'test_id': history[i][1], 'title': history[i][4], 'score': history[i][2], 'date': history[i][3]})
    return list_history

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

# def show_history(user_id):
#     cursor = conn.cursor()
#     query = f"SELECT * FROM dbo.request_user_history({user_id});"
#     cursor.execute(query)
#     history = cursor.fetchall()
#     list_history = []
#     for i in range(len(history)):
#         list_history.append({'test_id': history[i][1], 'title': history[i][4], 'score': history[i][2], 'date': history[i][3]})
#     return jsonify(list_history)