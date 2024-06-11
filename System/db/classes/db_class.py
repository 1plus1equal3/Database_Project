from ..db_connection import conn

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
    if response[0] == 0:
        return {'success': False, 'message': 'Class already exists!'}
    else:
        return {'success': True, 'message': 'Class created successfully!'}

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

def get_class_info(teacherID, classID):
    cursor = conn.cursor()
    # Execute the stored procedure
    query = 'EXEC dbo.GetClassInfo @teacherId = ?, @classId = ?'
    cursor.execute(query, teacherID, classID)
    
    # Fetch the first result set (summary)
    summary = cursor.fetchone()
    if summary is None:
        return "This class does not exist or does not belong to the specified teacher"
    
    number_of_students = summary[0]
    number_of_tests = summary[1]
    
    # Move to the next result set and fetch the student information
    cursor.nextset()
    students = cursor.fetchall()
    
    # Format the results
    student_list = []
    for student in students:
        student_info = {
            'user_id': student.user_id,
            'username': student.username,
            'avg_score': student.avg_score
        }
        student_list.append(student_info)
    
    return {
        'number_of_students': number_of_students,
        'number_of_tests': number_of_tests,
        'students': student_list
    }
    
def view_test_results(studentID, testID, classID):
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

def add_student_to_class(studentID, classID):
    # Prepare the query with the output parameter
    query = '''
    EXEC addStudentToClass @classId = ?, @studentId = ?
    '''
    # Fetch the result
    #vcursor.execute(query, classID, studentID)
    cursor = conn.cursor()
    cursor.execute(query, classID, studentID)
    result = cursor.fetchone()
    conn.commit()
    # print(result[0])
    
    # Print the result
    if result[0] == -1:
        print("Operation failed: This student does not exist, or the class does not exist, or the student is already in the class.")
    elif result[0] == 1:
        print("Student added successfully")

def delete_student_from_class(studentID, classID):
    # Prepare the query with the output parameter
    query = '''
    EXEC deleteStudentFromClass @classId = ?, @studentId = ?
    '''
    # Fetch the result
    cursor = conn.cursor()
    cursor.execute(query, classID, studentID)
    result = cursor.fetchone()
    conn.commit()
    #Print the result
    if result[0] == -1:
        print("Operation failed: This student does not exist, or the class does not exist, or the student is not in the class.")
    elif result[0] == 1:
        print("Student deleted from class successfully")

def add_student_to_class(studentID, classID):
    # Prepare the query with the output parameter
    query = '''
    EXEC addStudentToClass @classId = ?, @studentId = ?
    '''
    # Fetch the result
    #vcursor.execute(query, classID, studentID)
    cursor = conn.cursor()
    cursor.execute(query, classID, studentID)
    result = cursor.fetchone()
    conn.commit()
    # print(result[0])
    
    # Print the result
    if result[0] == -1:
        print("Operation failed: This student does not exist, or the class does not exist, or the student is already in the class.")
    elif result[0] == 1:
        print("Student added successfully")