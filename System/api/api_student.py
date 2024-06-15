from flask import jsonify
import matplotlib.pyplot as plt
import numpy as np
from db.exam import *
from db.classes import *

### Student APIS ###
def requestExam():
    exam_list = db_exam.db_get_exam()
    return jsonify(exam_list)

def show_test(exam_id):
    question_list = db_exam.db_test_question(exam_id)
    return jsonify(question_list)

def evaluate_exam(answer):
    # print(answer.get('selectedOptions')[0])
    # print(answer.get('user_id'))
    user_id = answer.get('user_id')
    test_id = answer.get('test_id')
    question_num = answer.get('num_of_questions')
    selectedOptions = answer.get('selectedOptions')
    # Get number of correct answers
    point = 0
    for ans in selectedOptions:
        correct_answer = db_exam.db_question_answer(ans.get('question_id'))
        if ans.get('answer') == ord(correct_answer) - ord('a'):
            point += 1
    # Calculate score
    point = round(point / question_num * 10, 2)

    # Insert score into database
    status = db_history.db_new_history(user_id, test_id, point)
    if status:
        return jsonify({'success': status,'submit_state': 'success', 'score': point})
    else:
        return jsonify({'success': status,'submit_state': 'fail'})
    
def evaluate_class_exam(test_id, class_id, answer):
    # print(answer.get('selectedOptions')[0])
    # print(answer.get('user_id'))
    user_id = answer.get('user_id')
    test_id = answer.get('test_id')
    question_num = answer.get('num_of_questions')
    selectedOptions = answer.get('selectedOptions')
    # Get number of correct answers
    point = 0
    for ans in selectedOptions:
        correct_answer = db_exam.db_question_answer(ans.get('question_id'))
        if ans.get('answer') == ord(correct_answer) - ord('a'):
            point += 1
    # Calculate score
    point = round(point / question_num * 10, 2)

    # Insert score into database
    status = db_history.db_new_history(user_id, test_id, point)
    status = db_history.db_new_class_history(user_id, test_id, class_id, point)
    if status:
        return jsonify({'success': status,'submit_state': 'success', 'score': point})
    else:
        return jsonify({'success': status,'submit_state': 'fail'})

def show_history(user_id):
    history = db_history.db_get_history(user_id)
    return jsonify(history)

def search_test(search_request):
    print(search_request)
    type = search_request['option']
    if type == 1: #search by id
        list_test = db_exam.db_search_exam_id(int(search_request['search']))
        return jsonify(list_test)
    else:
        list_test = db_exam.db_search_exam_title(search_request['search'])
        return jsonify(list_test)

def statistic(user_id):
    # Get statistic data
    data = db_statistic.db_get_statistic(user_id)
    statistic_data = {'Number_of_test' : data[0][0], 'Average_score': data[0][1], 'Max_score': data[0][2], 'Min_score': data[0][3]}
    # Get all scores
    list_score = db_statistic.db_get_scores(user_id)
    # Calculate average, max, and min
    average_value = round(statistic_data['Average_score'], 2)
    max_value = statistic_data['Max_score']
    min_value = statistic_data['Min_score']
    # Plot the list_score as a bar chart
    plt.clf()
    plt.ticklabel_format(style='plain',axis='x',useOffset=False)
    plt.bar(range(len(list_score)), list_score, label='list_score', color='#03A9F4')
    # Add bars for average, max, and min values
    plt.axhline(average_value, color='r', linestyle='--', label='Average score')
    plt.axhline(max_value, color='g', linestyle='--', label='Max score')
    plt.axhline(min_value, color='b', linestyle='--', label='Min score')
    # Add labels and title
    plt.xlabel('Test')
    plt.ylabel('Score')
    plt.title('Evaluate study process')
    # Add legend
    plt.legend()
    # Save the plot
    plt.savefig('System/static/statistic_images/statistic_barchart.png')
    # Clean up the current plot
    plt.clf()
    # Create a pie chart
    bins = [0, 4, 8, 10]
    # Use numpy's histogram function to count values in each bin
    hist, _ = np.histogram(list_score, bins=bins)
    # Calculate the percentage of values in each bin
    total_values = len(list_score)
    percentages = hist / total_values * 100
    # Labels for different ranges
    labels = ['Below average', 'Average', 'Good']
    # Plot the pie chart
    plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    # Add title
    plt.title('Percentage of score')
    # Show the plot
    plt.savefig('System/static/statistic_images/statistic_piechart.png')
    msg = {'success': True, 
           'average': average_value,
           'max': max_value,
           'min': min_value}
    return jsonify(msg)


def getStudentClass(id):
    class_list = db_class.db_get_student_classes(id)
    return jsonify(class_list)