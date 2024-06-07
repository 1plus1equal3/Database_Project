from ..db_connection import conn

# Get user info from database
def db_user_info(user_id):
    query = 'EXEC getUserInfo @user_id = ?;'
    cursor = conn.cursor() 
    cursor.execute(query, user_id)
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
    return user

# Get user list from database
def db_user_list():
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
    return userList

# def get_user_info(id):
#     query = 'EXEC getUserInfo @user_id = ?;'
#     cursor = conn.cursor() 
#     cursor.execute(query, id)
#     user = cursor.fetchone()
#     user_id = user[0]
#     username = user[1]
#     email = user[3]
#     user_type = user[4]
#     user = {
#         'user_id': user_id,
#         'username': username,
#         'email': email,
#         'user_type': user_type
#     }
#     return jsonify(user)

# def getUserList():
#     cursor = conn.cursor()
#     query = 'SELECT * FROM dbo.userList();'
#     cursor.execute(query)
#     fetch_result = cursor.fetchall()
#     userList = []
#     for i in fetch_result:
#         user_dict = {
#             'user_id': i[0],
#             'username': i[1],
#             'email': i[2],
#         }
#         userList.append(user_dict)
#     return jsonify(userList)

