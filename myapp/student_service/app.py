import os, sys
from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

try:
    # connect mongodb with the environment variables
    client = MongoClient(f'mongodb://{os.environ.get("MONGO_USERNAME")}:{os.environ.get("MONGO_PASSWORD")}@{os.environ.get("MONGO_SERVER_HOST")}:27017/{os.environ.get("MONGO_DATABASE")}?authSource=admin')
    client.server_info() # check database connection
except Exception as e: # print error and exit
    print ("[x] Database connection error")
    if e.code == 18: print ("[x] Database authentication failed.")
    print ("Error details: ", e.details)
    sys.exit(1)

db = client['university'] # use university database

# add a specified student
@app.route("/addstudent", methods=['POST'])
@app.route("/addstudent/", methods=['POST'])
def add_student():
    data = request.json
    try:
        if data is None or data == {} or data['student_id'] == '' or data['name'] == '' or data['dept_name'] == '' or data['gpa'] == '':
            abort(400, description="Please provide student id, name, dept name and gpa")
    except KeyError:
        abort(400, description="Please provide student id, name, dept name and gpa")
    new_document = data
    response = db.student.insert_one(new_document)
    return {"Status": "Student data successfully added", "Document_ID": str(response.inserted_id)}, 201

# remove a specified student
@app.route("/delstudent", methods=['DELETE'])
@app.route('/delstudent/', methods=['DELETE'])
def del_student():
    data = request.json
    try:
        if data is None or data == {} or data['student_id'] == '' or data['name'] == '':
            abort(400, description="Please provide student id and name")
    except KeyError:
        abort(400, description="Please provide student id and name")
    stu_filter = data
    response = db.student.delete_one(stu_filter)
    return {"Status": "Student data successfully deleted" if response.deleted_count > 0 else "Student not found."}, 200

# add a course taken by a specified student
@app.route('/addstucourse', methods=['POST'])
@app.route('/addstucourse/', methods=['POST'])
def add_stu_course():
    data = request.json
    try:
        if data is None or data == {} or data['student_id'] == '' or data['course_id'] == '' or data['credits'] == '':
            abort(400, description="Please provide student id, course id and credits")
    except KeyError:
        abort(400, description="Please provide student id, course id and credits")
    new_document = data
    response = db.takes.insert_one(new_document)
    return {"Status": "Successfully added a course taken by a specified student", "Document_ID": str(response.inserted_id)}, 201

# remove a specified course taken by a specified student
@app.route("/delstucourse", methods=['DELETE'])
@app.route('/delstucourse/', methods=['DELETE'])
def del_stu_course():
    data = request.json
    try:
        if data is None or data == {} or data['student_id'] == '' or data['course_id'] == '':
            abort(400, description="Please provide student id and course id")
    except KeyError:
        abort(400, description="Please provide student id and course id")
    stu_filter = data
    response = db.takes.delete_one(stu_filter)
    return {"Status": "Student data successfully deleted" if response.deleted_count > 0 else "Record not found."}, 200

# defines the /students, /students/<student_id> GET route of the API
@app.route("/students", defaults={'student_id': None})
@app.route("/students/", defaults={'student_id': None})
@app.route("/students/<student_id>", methods=['GET'])
def return_students_data(student_id):
    key = None if student_id == None else {"student_id": student_id}
    student_data = [{item: data[item] for item in data if item != '_id'} for data in db.student.find(key).sort("student_id")]
    if student_data == []:
        abort(404, description="not found")
    return jsonify(student_data)

# defines the /takes, /takes/<student_id> GET route of the API
@app.route("/takes", defaults={'student_id': None})
@app.route("/takes/", defaults={'student_id': None})
@app.route("/takes/<student_id>", methods=['GET'])
def return_takes_data(student_id):
    key = None if student_id == None else {"student_id": student_id}
    student_data = [{"dept_name": stu["dept_name"], "gpa": stu["gpa"], "name": stu["name"], "student_id": stu["student_id"], 
    "student_takes": [{"course_id": take["course_id"], "credits": take["credits"]} 
    for take in db.takes.find({"student_id": stu["student_id"]}).sort("course_id")]} 
    for stu in db.student.find(key).sort("student_id")]
    if student_data == []:
        abort(404, description="not found")
    return jsonify(student_data)

# 404 error handler
@app.errorhandler(404)
def resource_not_found(e):
    return {"error": "not found"}, 404

# 400 error handler
@app.errorhandler(400)
def resource_not_found(e):
    return {"error": "bad request"}, 400

# 405 error handler
@app.errorhandler(405)
def resource_not_found(e):
    return {"error": "method not allowed"}, 405

# 500 error handler
@app.errorhandler(500)
def resource_not_found(e):
    return {"error": "internal server error"}, 500

# my information
@app.route('/me')
@app.route('/me/')
def my_info():
    return jsonify({"name": "Chan Tai Man", "student_id": "12345678D"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15000) # listen 0.0.0.0:15000
