## (Havin' fun) Extending  the sprint 01 assignment using apache airflow and Docker

### Description

* FastAPI was used to retrieve the pytest result from test_extract and test_transform files in order to check its correct execution on Apache Airflow

* Apache Airflow was used to retrieve the pytest results in order to check if the EDA noteboook can run as expected

* There are two main containers on the docker ecosystem: Apache Airflow and a Python server (wich runs both a Jupyter and FastAPI services)

### Pre-requisites
1. Don't have any services running on ports 8888,8000 and 8080

2. Having docker and docker-compose (fig) installed

### Notes

1. The new added files won't conflict with your project as docker-compose mounts your code in volumes to the containers. In case  your source code uses a dependency not described on requirements-for-docker-c.txt you should install it manually on the python container using 

```
pip install <package==version>
``` 

### Set up
1. From your sprint 1 assignment folder, pull the master branch using

git init (If the repo does not exist previously)
git remote add origin https://github.com/diegorg4/aia_sp01_airflow_docker_plus.git
git pull origin master

2. You should see that new files and folders have been added to your folder structure
|
|-airflow
    |- dags
        |- validate_tests_dag.py
|-fastapi
    |-validate-tests.py
|-docker-compose.yaml
|-Dockerfile
|-requirements-for-docker-c.txt


3. From the command line, being in the docker-compose.yaml path, download the project image using:

```
docker pull diegorg4/anyoneai_sprint01_assigment:diegoroman_sprint01_assigment
``` 

This may take a minutes to download the containers image

4. Set up and ready the environment:

```
docker-compose up
``` 

5. Check on a new terminal the containers are running properly

```
docker ps
``` 
```
Example output:
CONTAINER ID   IMAGE                  COMMAND                  CREATED             STATUS                    PORTS                                            NAMES
fdcc5c5c75b6   apache/airflow:2.3.3   "/usr/bin/dumb-init …"   About an hour ago   Up 29 minutes (healthy)   0.0.0.0:8080->8080/tcp                           assignment-airflow-webserver-1
47af1aa29e5b   apache/airflow:2.3.3   "/usr/bin/dumb-init …"   About an hour ago   Up 29 minutes (healthy)   8080/tcp                                         assignment-airflow-worker-1
7abffee9138f   apache/airflow:2.3.3   "/usr/bin/dumb-init …"   About an hour ago   Up 29 minutes (healthy)   8080/tcp                                         assignment-airflow-scheduler-1
875474da36cb   apache/airflow:2.3.3   "/usr/bin/dumb-init …"   About an hour ago   Up 29 minutes (healthy)   8080/tcp                                         assignment-airflow-triggerer-1
0d7bdff56537   assignment-python      "/usr/bin/supervisor…"   About an hour ago   Up 29 minutes             0.0.0.0:8000->8000/tcp, 0.0.0.0:8888->8888/tcp   assignment-python-1
8cd73b4be540   postgres:13            "docker-entrypoint.s…"   About an hour ago   Up 29 minutes (healthy)   5432/tcp                                         assignment-postgres-1
e414dac2f043   redis:latest           "docker-entrypoint.s…"   About an hour ago   Up 29 minutes (healthy)   6379/tcp                                         assignment-redis-1
```

6. You can now start using the services using your browser, postman, etc

```
0.0.0.0:8000/api/v1/test-extract        -> describes pytest execution to test_extract.py 
0.0.0.0:8000/api/v1/test-transform      -> describes pytest execution to test_transform.py 
0.0.0.0:8000/api/v1/get_jupyter_token   -> gives you the access token for jupyter
```
if you are a mac user try using your machine hostname instead of 0.0.0.0

7. You can access airflow using:

```
0.0.0.0:8080
user/pass: airflow

```
if you are a mac user try using your machine hostname instead of 0.0.0.0

8. To run your EDA notebook enter on your browser:

```
0.0.0.0:8888/login -> remember to use the token from 0.0.0.0:8000/api/v1/get_jupyter_token
```

9. Explore the new code, change yours and see what happens to the APIs, Airflow DAG and the EDA Notebook. :smile: Any change you make on your local machine will be reflected inmediatly on the containers

## Stop environment

Just Ctrl/Cmd + Z on the command line where you tap docker-compose up

