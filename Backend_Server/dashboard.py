from flask import Flask, request, jsonify
import pyodbc

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

conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def show_dash_board():
    print('Show dashboard')
    query = """
            SELECT title, Image
            FROM Test
            """
    cursor.execute(query)
    names = cursor.fetchall()
    numbers = 0
    if len(names) > 20:
        numbers = 20
    else:
        numbers = len(names)

    list_exams = []
    for i in range(numbers):
        list_exams.append({'name': names[i][0], 'image': names[i][1]})
    
    return jsonify(list_exams)

def show_detail(test):
    query = """
            SELECT *
            FROM Test
            WHERE title = ?
            """
    cursor.execute(query, test)
    exam = cursor.fetchall()
    return jsonify({'Name': exam[0][1], 'Date': exam[0][2], 'AdminID': exam[0][3]})

app = Flask(__name__)

@app.route('/dashboard/Item', methods = ['GET'])
def show():
    id = request.args.get('id')
    print(f'Test name: {id}')
    msg = show_detail(id)
    return msg

@app.route('/dashboard', methods = ['GET'])
def dash_board():
    msg = show_dash_board()
    return msg



if __name__ == '__main__':
    app.run(debug=True)