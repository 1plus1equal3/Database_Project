from ..db_connection import conn
import numpy as np

# Get student classes
def db_get_student_classes(student_id):
    query = 'EXEC dbo.getStudentClass @Id = ?'
    cursor = conn.cursor()
    cursor.execute(query, student_id)
    data = cursor.fetchall()
    #Structure data
    classList = []
    for i in data:
        class_data = {
            'id': i[0],
            'title': i[2],
            'std_num': i[3],
            'create_date': i[4],
            'teacher': i[5]
        }
        classList.append(class_data)
    return classList

# Get classes created by a teacher
def db_get_classes(teacher_id):
    query = 'EXEC dbo.viewTeacherClasses @teacherId = ?'
    cursor = conn.cursor()
    cursor.execute(query, teacher_id)
    data = cursor.fetchall()
    #Structure data
    classList = []
    for i in data:
        class_data = {
            'id': i[0], # 'class_id' is the key to be used in the frontend, 'i[0]' is the value from the database
            'title': i[2],
            'std_num': i[3],
            'date': i[4]
        }
        classList.append(class_data)
    return classList

# Create a new class
#!TODO: BUG need to fix?!
def db_create_class(info):
    class_name = info.get('class_name')
    teacher_id = info.get('user_id')
    query = 'EXEC dbo.createClass @teacherId = ?, @className = ?'
    cursor = conn.cursor()
    cursor.execute(query, teacher_id, class_name)
    response = cursor.fetchone()
    conn.commit()
    if int(response[0]) == 0:
        return {'success': False, 'message': 'Class already exists!'}
    else:
        return {'success': True, 'message': 'Class created successfully!'}
    
def db_delete_class(class_id):
    query = 'EXEC dbo.deleteClass @class_id = ?'
    cursor = conn.cursor()
    cursor.execute(query, class_id)
    response = cursor.fetchone()
    conn.commit()
    if int(response[0]) == 0:
        return {'success': False, 'message': 'Class' + str(class_id) + 'does not exist!'}
    else:
        return {'success': True, 'message': 'Class' + str(class_id) + ' deleted successfully!'}

# def getClassFromDB(teacher_id):
#     # Query database for data
#     query = 'EXEC dbo.viewTeacherClasses @teacherId = ?'
#     cursor = conn.cursor()
#     cursor.execute(query, teacher_id)
#     data = cursor.fetchall()
#     # Structure data
#     classList = []
#     for i in data:
#         class_data = {
#             'title': i[2],
#             'std_num': i[3],
#             'date': i[4]
#         }
#         classList.append(class_data)
#     cursor.commit()
#     # Return json data
#     return jsonify(classList)

# def createNewClass(info):
#     class_name = info.get('class_name')
#     teacher_id = info.get('user_id')
#     query = 'EXEC dbo.createClass @teacherId = ?, @className = ?'
#     cursor = conn.cursor()
#     cursor.execute(query, teacher_id, class_name)
#     response = cursor.fetchone()
#     conn.commit()
#     if response[0] == 0:
#         return {'success': False, 'message': 'Class already exists!'}
#     else:
#         return {'success': True, 'message': 'Class created successfully!'}

def db_get_class_info(classID):
    cursor = conn.cursor()
    # Get student_number and test_number
    query = 'EXEC dbo.classInfo @class_id = ?'
    cursor.execute(query, classID)
    summary = cursor.fetchone()
    number_of_students = summary[0]
    number_of_tests = summary[1]
    
    # Get student list
    query = 'EXEC dbo.studentInfoClass @class_id = ?'
    cursor.execute(query, classID)
    students = cursor.fetchall()
    # Format the results
    student_list = []
    for student in students:
        student_info = {
            'user_id': student.user_id,
            'username': student.username,
            'max_score': student.max_score,
            'avg_score': student.avg_score,
            'test_num': student.test_per_std,
        }
        student_list.append(student_info)
    
    return {
        'number_of_students': number_of_students,
        'number_of_tests': number_of_tests,
        'students': student_list
    }
    
def db_view_test_results(studentID, testID, classID):
    cursor = conn.cursor()
    # Execute the stored procedure
    query = 'EXEC dbo.GetTestResults @userID = ?, @testID = ?, @classID = ?'
        
    # Execute the stored procedure with the provided parameters
    cursor.execute(query, studentID, testID, classID)
    
    # Fetch and print the results
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
        
    # Process the results into a list of dictionaries
    result_list = [dict(zip(columns, row)) for row in results]
        
    return result_list

def db_add_student_to_class(studentID, classID):
    # Prepare the query with the output parameter
    query = f'''
    EXEC dbo.addStudentToClass @classId = {classID}, @studentId = {studentID}
    '''
    # Fetch the result
    #vcursor.execute(query, classID, studentID)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.commit()
    
    if result[0] == -1:
        return {'success': False, 'message': 'The student is already in the class.'}
    elif result[0] == 0:
        return {'success': False, 'message': 'This student does not exist'}
    else:
        return {'success': True, 'message': 'Student added to class successfully'}

def db_delete_student_from_class(studentID, classID):
    # Prepare the query with the output parameter
    query = '''
    EXEC dbo.deleteStudentFromClass @classId = ?, @studentId = ?
    '''
    # Fetch the result
    cursor = conn.cursor()
    cursor.execute(query, classID, studentID)
    result = cursor.fetchone()
    conn.commit()
    #Print the result
    if result[0] == -1:
        return {'success': False, 'message': 'The student is not in the class.'}
    elif result[0] == 1:
        return {'success': True, 'message': 'Student removed from class successfully'}
    
def db_get_class_test(classID):
        cursor = conn.cursor()
        # Get student_number and test_number
        query = 'EXEC dbo.getClassTest @class_id = ?'
        cursor.execute(query, classID)
        tests = cursor.fetchall()
        # Format the results
        test_list = []
        for test in tests:
            test_info = {
                'test_id': test.test_id,
                'title': test.title,
                'subject': test.subject,
                'level': test.difficulty_level,
                'duration': test.duration
            }
            test_list.append(test_info)
        return test_list

def db_add_test_to_class(testID, classID, duration):
    # Prepare the query with the output parameter
    query = f'''
    EXEC dbo.addTestToClass @classId = {classID}, @testId = {testID}, @duration = {duration}
    '''
    # Fetch the result
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.commit()
    
    if result[0] == -1:
        return {'success': False, 'message': 'The test is already in the class.'}
    elif result[0] == 0:
        return {'success': False, 'message': 'This test does not exist'}
    else:
        return {'success': True, 'message': 'Test added to class successfully'}
    
def db_delete_test_from_class(testID, classID):
    # Prepare the query with the output parameter
    query = '''
    EXEC dbo.deleteTestFromClass @classId = ?, @testId = ?
    '''
    # Fetch the result
    cursor = conn.cursor()
    cursor.execute(query, classID, testID)
    result = cursor.fetchone()
    conn.commit()
    #Print the result
    if result[0] == -1:
        return {'success': False, 'message': 'The test is not in the class.'}
    elif result[0] == 1:
        return {'success': True, 'message': 'Test removed from class successfully'}
    
def db_get_test_result(studentID, testID, classID):
    cursor = conn.cursor()
    # Get student_number and test_number
    query = 'EXEC dbo.getTestResults @userID = ?, @testID = ?, @classID = ?'
    cursor.execute(query, studentID, testID, classID)
    results = cursor.fetchall()
    # Format the results
    result_list = []
    for result in results:
        result_info = {
            'username': result.username,
            'user_id': result.user_id,
            'test_id': result.test_id,
            'score': result.score,
        }
        result_list.append(result_info)
    return result_list
