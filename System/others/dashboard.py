from flask import Flask, request, jsonify
import pyodbc

conn_str = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=MSI\SQLEXPRESS;DATABASE=Prj;UID=sa;PWD=123456'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def show_dash_board():
    query = """
            SELECT Name, Images
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
            WHERE Name = ?
            """
    cursor.execute(query, test)
    exam = cursor.fetchall()
    return jsonify({'Name': exam[0][1], 'Date': exam[0][2], 'AdminID': exam[0][3]})

app = Flask(__name__)

@app.route('/dashboard', methods = ['GET'])
def dash_board():
    msg = show_dash_board()
    return msg

@app.route('/dashboard/<test>', methods = ['GET'])
def show(test):
    msg = show_detail(test)
    return msg

if __name__ == '__main__':
    app.run(debug=True)