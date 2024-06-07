from flask import jsonify
from db.authentication import authen

### Authentication APIS ###
def register_user(user):
    records = authen.register_user(user)
    msg = ''
    if records[0] == -1:
        msg = jsonify({'success': False, 'error': 'Username already exists'})
        return msg
    msg = jsonify({'success': True})
    return msg

    
#!TODO: Change the query
def login_user(user):
    pass
    # username = user.get('username')
    # password = hash(user.get('password'))
    # cursor = conn.cursor()
    # query = 'SELECT dbo.func_login(?, ?)'
    # cursor.execute(query, username, password)
    # user = cursor.fetchone()
    # user_id = user[0]
    # if user_id == -1:
    #     return jsonify({'success': False, 'error': 'Invalid username or password'})
    # query = 'SELECT dbo.checkUserRole(?)'
    # cursor.execute(query, user_id)
    # user_type = cursor.fetchone()[0]
    # return jsonify({'success': True, 'user_id': user_id, 'username': username, 'user_type': user_type})