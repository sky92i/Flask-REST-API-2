# Python Flask REST API with MongoDB

### Steps to run the image
#### 1. To startup the Mongo DB with sample data, git clone the Github repository by executing:
```
git clone https://github.com/cswclui/mongodb-docker
```

#### 2. Launch the mongoDB container by executing:
```
cd mongodb-docker
docker-compose up
```
Exit the mongo shell with Ctrl+D.

#### 3. Build the docker image by executing:
```
docker build . -t 12345678d/student_svc
```

#### 4. Run my docker image by executing:
```
docker run --rm --network asm2 -e MONGO_USERNAME=comp3122 -e MONGO_PASSWORD=12345 -e MONGO_SERVER_HOST='mongo' -e MONGO_SERVER_PORT='27017' -p 15000:15000 12345678d/student_svc
```
### To stop and remove the running containers and created volumes, execute:
```
docker-compose down -v
```
