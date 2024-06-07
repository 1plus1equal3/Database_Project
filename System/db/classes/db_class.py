from ..db_connection import conn

# Get class data of a teacher
def db_get_class(teacher_id):
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