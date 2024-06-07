from flask import jsonify
from db.authentication import user_info

### User Information APIS ###
def get_user_info(id):
    user = user_info.db_user_info(id)
    return jsonify(user)

def getUserList():
    userList = user_info.db_user_list()
    return jsonify(userList)