from ..db_connection import conn
from flask import jsonify

def hash(password):
    hashed_password = ""
    for char in password:
        temp = int((17 * ord(char) / 11) + 2003)
        hashed_password += chr(temp % 87 + 40)
    return hashed_password

def db_register(user):
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
    return cursor.fetchone()

#!TODO: Implement login function
def db_login(user):
    pass

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