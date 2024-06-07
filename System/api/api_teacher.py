from flask import jsonify
from db.exam import *
from db.classes import *

### Teacher APIS ###
#! Exam APIs
def getAdminExam(user_id):
    exam_list = db_exam.db_admin_exam(user_id)
    return jsonify(exam_list)

def show_test(exam_id):
    question_list = db_exam.db_test_question(exam_id)
    return jsonify(question_list)

def search_test(search_request):
    print(search_request)
    type = search_request['option']
    if type == 1: #search by id
        list_test = db_exam.db_search_exam_id(int(search_request['search']))
        return jsonify(list_test)
    else:
        list_test = db_exam.db_search_exam_title(search_request['search'])
        return jsonify(list_test)
    
def search_question(search_request):
    question_info = db_exam.db_search_question(search_request['search'], search_request['subject'], search_request['difficulty'])
    return jsonify(question_info)
    
def create_test(test_info):
    return db_exam.db_create_test(test_info)


#! Class APIs
def getClassFromDB(teacher_id):
    class_list = db_class.db_get_class(teacher_id)
    return jsonify(class_list)

def createNewClass(info):
    return db_class.db_create_class(info)
    