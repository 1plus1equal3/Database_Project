import pandas as pd
import pyodbc as pdb
from flask import Flask, request, jsonify
from flask_cors import CORS

### Connect to SQL Server database ###
# Connect to SQL Server database info
SERVER = 'DUYNGUYEN\SQLEXPRESS'
DATABASE = 'Project'
USERNAME = 'sa'
PASSWORD = '123456'

# Connection string
connectionString = f'''
DRIVER={{ODBC Driver 18 for SQL Server}};
SERVER={SERVER};DATABASE={DATABASE};
UID={USERNAME};
PWD={PASSWORD};
Encrypt=no;
'''

# Connect to SQL Server
conn = pdb.connect(connectionString)


### Utility functions ###
# Username, password & email validation must be done in frontend!
def register_user(user):
    username = user.get('username')
    password = user.get('password')
    email = user.get('email')

    # User_id validation
    select_query = f"""
    DECLARE @result INT;
    EXEC @result = func_register '{username}', '{password}', '{email}';
    SELECT @result;
    """
    cursor = conn.cursor()
    cursor.execute(select_query)
    records = cursor.fetchone()
    if records[0] == 1:
        msg = jsonify({'success': True})
    elif records[0] == 0:
        msg = jsonify({'success': False, 'error': 'Username already exists'})
    return msg

def login_user(user):
    username = user.get('username')
    password = user.get('password')
    query = 'SELECT dbo.func_login(?, ?)'
    cursor = conn.cursor()
    cursor.execute(query, username, password)
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        return jsonify({'success': True, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'error': 'Invalid username or password'})

def get_user_info(id):
    query = 'SELECT * FROM User_info WHERE user_id = ?'
    cursor = conn.cursor() 
    cursor.execute(query, id)
    user = cursor.fetchone()
    return jsonify(user)

def requestExam():
    query = 'SELECT * FROM dbo.request_exam();'
    cursor = conn.cursor()
    cursor.execute(query)
    fetch_result = cursor.fetchall()
    examList = []
    base_url = 'http://localhost:5000/exam?test_id='
    for i in fetch_result:
        test_dict = {
            'test_url': base_url + str(i[0]),
            'title': i[1],
            'date_created': i[2],
        }
        examList.append(test_dict)
    return jsonify(examList)


### Server communication ###
app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    msg = register_user(data)
    return msg

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    msg = login_user(data)
    return msg

@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    data = request.get_json()
    info = get_user_info(data)
    return info

@app.route('/request_exam', methods=['GET'])
def request_exam():
    examList = requestExam()
    print(examList)
    return examList

# Start server
if __name__ == '__main__':
    app.run(debug=True)

