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
    class_list = db_class.db_get_classes(teacher_id)
    return jsonify(class_list)

def createNewClass(info):
    return db_class.db_create_class(info)

def deleteClass(class_id):
    return db_class.db_delete_class(class_id)

#! Class specific APIs
def getClassInfo(classId):
    return db_class.db_get_class_info(classId)

def addStudentToClass(class_id, student_id):
    return db_class.db_add_student_to_class(student_id, class_id)

def deleteStudentFromClass(class_id, student_id):
    return db_class.db_delete_student_from_class(student_id, class_id)

def getClassTest(class_id):
    return db_class.db_get_class_test(class_id)

def addTestToClass(class_id, test_id, duration):
    return db_class.db_add_test_to_class(test_id, class_id, duration)
    
def deleteTestFromClass(class_id, test_id):
    return db_class.db_delete_test_from_class(test_id, class_id)