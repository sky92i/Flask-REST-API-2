import pytest, requests

#1
def test_get_students():
    response = requests.get("http://localhost:15000/students/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History'
    assert response_body[0]["gpa"] == 2.1
    assert response_body[0]["name"] == 'Carol'
    assert response_body[0]["student_id"] == '11111'
    assert response_body[1]["dept_name"] == 'History.'
    assert response_body[1]["gpa"] == 2.0
    assert response_body[1]["name"] == 'Bob'
    assert response_body[1]["student_id"] == '22222'
    assert response_body[2]["dept_name"] == 'Comp. Sci.'
    assert response_body[2]["gpa"] == 3.1
    assert response_body[2]["name"] == 'Alice'
    assert response_body[2]["student_id"] == '33333'

#2
def test_get_specific_students():
    response = requests.get("http://localhost:15000/students/11111")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History'
    assert response_body[0]["gpa"] == 2.1
    assert response_body[0]["name"] == 'Carol'
    assert response_body[0]["student_id"] == '11111'

    response = requests.get("http://localhost:15000/students/22222")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History.'
    assert response_body[0]["gpa"] == 2.0
    assert response_body[0]["name"] == 'Bob'
    assert response_body[0]["student_id"] == '22222'

    response = requests.get("http://localhost:15000/students/33333")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'Comp. Sci.'
    assert response_body[0]["gpa"] == 3.1
    assert response_body[0]["name"] == 'Alice'
    assert response_body[0]["student_id"] == '33333'

#3
def test_get_takes():
    response = requests.get("http://localhost:15000/takes/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    for n in range(2):
        assert 'dept_name' in response_body[n]
        assert 'gpa' in response_body[n]
        assert 'name' in response_body[n]
        assert 'student_id' in response_body[n]
        assert 'student_takes' in response_body[n]
    assert response_body[1]["student_takes"][0]["course_id"] == 'COMP1234'
    assert response_body[1]["student_takes"][1]["course_id"] == 'COMP2345'
    assert response_body[2]["student_takes"][0]["course_id"] == 'COMP1234'

#4
def test_get_404():
    response = requests.get("http://localhost:15000/abc/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 404

#5
def test_post_specific_student():
    response = requests.post("http://localhost:15000/addstudent", json={
        "dept_name": "Comp. Sci.",
        "gpa": 4.0,
        "name": "Sky",
        "student_id": "12345"
    })
    response = requests.post("http://localhost:15000/addstudent", json={
        "dept_name": "Comp. Sci.",
        "gpa": 4.3,
        "name": "Tin",
        "student_id": "54321"
    })
    response = requests.post("http://localhost:15000/addstudent", json={
        "dept_name": "Comp. Sci.",
        "gpa": 4.3,
        "name": "Ben",
        "student_id": "88888",
        "phone": "1234 5678"
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 201

#6
def test_post_specific_student_error():
    response = requests.post("http://localhost:15000/addstudent", json={
        "dept_name": "Comp. Sci.",
        "gpa": 4.0,
        "name": "Anson",
        "student_id": ""
    })
    
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.post("http://localhost:15000/addstudent", json={})
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.get("http://localhost:15000/addstudent/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

    response = requests.delete("http://localhost:15000/addstudent/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

#7
def test_del_specific_student():
    response = requests.delete("http://localhost:15000/delstudent", json={
        "student_id": "12345",
        "name": "Sky"
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

#8
def test_del_specific_student_error():
    response = requests.delete("http://localhost:15000/delstudent", json={
        "student_id": "1234",
        "name": "Sky"
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

    response = requests.delete("http://localhost:15000/delstudent", json={
        "student_id": "",
        "name": ""
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.delete("http://localhost:15000/delstudent", json={})
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.get("http://localhost:15000/delstudent/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

    response = requests.post("http://localhost:15000/delstudent/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

#9
def test_post_student_course():
    response = requests.post("http://localhost:15000/addstucourse", json={
        "student_id": "54321",
        "course_id": "COMP5555",
        "credits": 3
    })
    response = requests.post("http://localhost:15000/addstucourse", json={
        "student_id": "54321",
        "course_id": "COMP8888",
        "credits": 3
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 201

#10
def test_post_student_course_error():
    response = requests.post("http://localhost:15000/addstucourse", json={
        "student_id": "54321",
        "course_id": "",
        "credits": 3
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.post("http://localhost:15000/addstucourse", json={})
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.get("http://localhost:15000/addstucourse/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

    response = requests.delete("http://localhost:15000/addstucourse/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

#11
def test_del_specific_student_course():
    response = requests.delete("http://localhost:15000/delstucourse", json={
        "student_id": "54321",
        "course_id": "COMP5555"
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

#12
def test_del_specific_student_course_error():
    response = requests.delete("http://localhost:15000/delstucourse", json={
        "student_id": "",
        "course_id": "COMP5555"
    })
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.delete("http://localhost:15000/delstucourse", json={})
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 400

    response = requests.get("http://localhost:15000/delstucourse/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

    response = requests.post("http://localhost:15000/delstucourse/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405

#13
def test_me():
    response = requests.get("http://localhost:15000/me")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["name"] == 'Chan Tai Man'
    assert response_body["student_id"] == '12345678D'

#14
def test_get_students_again_with_new_student():
    response = requests.get("http://localhost:15000/students/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History'
    assert response_body[0]["gpa"] == 2.1
    assert response_body[0]["name"] == 'Carol'
    assert response_body[0]["student_id"] == '11111'
    assert response_body[1]["dept_name"] == 'History.'
    assert response_body[1]["gpa"] == 2.0
    assert response_body[1]["name"] == 'Bob'
    assert response_body[1]["student_id"] == '22222'
    assert response_body[2]["dept_name"] == 'Comp. Sci.'
    assert response_body[2]["gpa"] == 3.1
    assert response_body[2]["name"] == 'Alice'
    assert response_body[2]["student_id"] == '33333'
    assert response_body[3]["dept_name"] == 'Comp. Sci.'
    assert response_body[3]["gpa"] == 4.3
    assert response_body[3]["name"] == 'Tin'
    assert response_body[3]["student_id"] == '54321'
    assert response_body[4]["dept_name"] == 'Comp. Sci.'
    assert response_body[4]["gpa"] == 4.3
    assert response_body[4]["name"] == 'Ben'
    assert response_body[4]["student_id"] == '88888'
    assert response_body[4]["phone"] == '1234 5678'

#15
def test_get_specific_students_again_with_new_student():
    response = requests.get("http://localhost:15000/students/11111")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History'
    assert response_body[0]["gpa"] == 2.1
    assert response_body[0]["name"] == 'Carol'
    assert response_body[0]["student_id"] == '11111'

    response = requests.get("http://localhost:15000/students/22222")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'History.'
    assert response_body[0]["gpa"] == 2.0
    assert response_body[0]["name"] == 'Bob'
    assert response_body[0]["student_id"] == '22222'

    response = requests.get("http://localhost:15000/students/33333")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'Comp. Sci.'
    assert response_body[0]["gpa"] == 3.1
    assert response_body[0]["name"] == 'Alice'
    assert response_body[0]["student_id"] == '33333'

    response = requests.get("http://localhost:15000/students/54321")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'Comp. Sci.'
    assert response_body[0]["gpa"] == 4.3
    assert response_body[0]["name"] == 'Tin'
    assert response_body[0]["student_id"] == '54321'

    response = requests.get("http://localhost:15000/students/88888")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["dept_name"] == 'Comp. Sci.'
    assert response_body[0]["gpa"] == 4.3
    assert response_body[0]["name"] == 'Ben'
    assert response_body[0]["student_id"] == '88888'
    assert response_body[0]["phone"] == '1234 5678'

#16
def test_get_takes_again_with_new_student_course():
    response = requests.get("http://localhost:15000/takes/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    for n in range(2):
        assert 'dept_name' in response_body[n]
        assert 'gpa' in response_body[n]
        assert 'name' in response_body[n]
        assert 'student_id' in response_body[n]
        assert 'student_takes' in response_body[n]
    assert response_body[1]["student_takes"][0]["course_id"] == 'COMP1234'
    assert response_body[1]["student_takes"][1]["course_id"] == 'COMP2345'
    assert response_body[2]["student_takes"][0]["course_id"] == 'COMP1234'
    assert response_body[3]["student_takes"][0]["course_id"] == 'COMP8888'