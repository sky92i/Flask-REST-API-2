# Python Flask REST API with MongoDB, Prometheus and Grafana

Assignment of COMP3122

### Steps to launch the application
#### Open the shell in myapp folder and execute the following command 
```
docker-compose up
```

### To stop and remove the running containers and created volumes, execute the following command in this folder:
```
docker-compose down -v
```

### To access the python flask app
```
curl localhost:15000/students
curl localhost:15000/takes
curl localhost:15000/students/<student_id>
curl localhost:15000/takes/<student_id>
curl -X POST localhost:15000/addstudent/ -H 'Content-Type: application/json' -d '{"dept_name": "Comp. Sci.","gpa": 4.0,"name": "Sky","student_id": "12345"}'
curl -X DELETE localhost:15000/delstudent/ -H 'Content-Type: application/json' -d '{"student_id": "12345","name": "Sky"}'
curl -X POST localhost:15000/addstucourse/ -H 'Content-Type: application/json' -d '{"student_id": "12345","course_id": "COMP5555","credits": 3}'
curl -X DELETE localhost:15000/delstucourse/ -H 'Content-Type: application/json' -d '{"student_id": "12345","course_id": "COMP5555"}'
```

### To access the metric exporter in the python flask app
#### Visit http://localhost:15000/metrics

### To access Prometheus
#### Visit http://localhost:9090

### To access Grafana
#### Visit http://localhost:3000, username is comp3122, pwd is 12345678D

### To run unit tests against your python flask app (running in the student_service container), execute the following command in tests folder
```
pytest tests/unit.py -v
```
