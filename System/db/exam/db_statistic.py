from ..db_connection import conn

# Get statistic data of a user
def db_get_statistic(user_id):
    query = "SELECT * from dbo.Statist(?)"
    cursor = conn.cursor()
    cursor.execute(query, user_id)
    data = cursor.fetchall()
    return data

# Get score data of a user
def db_get_scores(user_id):
    cursor = conn.cursor()
    list_score = []
    query_score = "SELECT score FROM History WHERE user_id = ?"
    cursor.execute(query_score, user_id)
    score = cursor.fetchall()
    for i in range(len(score)):
        list_score.append(score[i][0])
    return list_score

# def statistic(user_id):
#     query = "SELECT * from dbo.Statist(?)"
#     cursor = conn.cursor()
#     cursor.execute(query, user_id)
#     data = cursor.fetchall()
#     statistic_data = {'Number_of_test' : data[0][0], 'Average_score': data[0][1], 'Max_score': data[0][2], 'Min_score': data[0][3]}
#     list_score = []
#     query_score = "SELECT score FROM History WHERE user_id = ?"
#     cursor.execute(query_score, user_id)
#     score = cursor.fetchall()
#     for i in range(len(score)):
#         list_score.append(score[i][0])
#     # Calculate average, max, and min
#     average_value = round(statistic_data['Average_score'], 2)
#     max_value = statistic_data['Max_score']
#     min_value = statistic_data['Min_score']
#     # Plot the list_score as a bar chart
#     plt.clf()
#     plt.ticklabel_format(style='plain',axis='x',useOffset=False)
#     plt.bar(range(len(list_score)), list_score, label='list_score', color='#03A9F4')
#     # Add bars for average, max, and min values
#     plt.axhline(average_value, color='r', linestyle='--', label='Average score')
#     plt.axhline(max_value, color='g', linestyle='--', label='Max score')
#     plt.axhline(min_value, color='b', linestyle='--', label='Min score')
#     # Add labels and title
#     plt.xlabel('Test')
#     plt.ylabel('Score')
#     plt.title('Evaluate study process')
#     # Add legend
#     plt.legend()
#     # Save the plot
#     plt.savefig('System/static/statistic_images/statistic_barchart.png')
#     # Clean up the current plot
#     plt.clf()
#     # Create a pie chart
#     bins = [0, 4, 8, 10]
#     # Use numpy's histogram function to count values in each bin
#     hist, _ = np.histogram(list_score, bins=bins)
#     # Calculate the percentage of values in each bin
#     total_values = len(list_score)
#     percentages = hist / total_values * 100
#     # Labels for different ranges
#     labels = ['Below average', 'Average', 'Good']
#     # Plot the pie chart
#     plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
#     # Add title
#     plt.title('Percentage of score')
#     # Show the plot
#     plt.savefig('System/static/statistic_images/statistic_piechart.png')
#     msg = {'success': True, 
#            'average': average_value,
#            'max': max_value,
#            'min': min_value}
#     return jsonify(msg)
