# FastAPI Oracle CRUD application

## Introduction
This is a simple Python FastAPI test application that works with an Oracle database.

## Summary
The goal of this project was to learn a bit more about FastAPI, SQLAlchemy, Oracle Database and Docker.
Once 'HelloWorld' started working, I wanted to experiment with something a bit more complex. Specifically, CRUD API which handles Foreign Keys, One-To-One and One-To-Many cascading relationships using SQLAlchemy and Oracle database behind it. Finally, I wanted to run the whole thing in a Docker.

<!-- **Note:** This is not a production code and was written for research purposes only. -->

## Database diagram
![Database Diagram](Diagram.jpg?raw=true "Database Diagram")

## Create database tables
The app will automatically create all 3 tables with sample data in the database on startup and will automatically drop them on shutdown

## Installing and running in Docker
Tested on OS X 12.2

### Asumptions

* Python 3.8 or higher is installed
* Docker is installed

After checking out the repo, in terminal, cd to the project root directory

Build Docker image using the `Dockerfile.oracle` file

You will need to provide db_username, db_password, db_host, db_port and db_database as arguments when building the Docker

```console
docker build -f ./Dockerfile.oracle -t fastapi-oracle-image . \
--build-arg DB_USERNAME="<db_username>" \
--build-arg DB_PASSWORD="<db_password>" \
--build-arg DB_HOST="<db_host>" \
--build-arg DB_PORT="<db_port>" \
--build-arg DB_DATABASE="<db_database>"
```

### Running the server instance in Docker
Run the newly created Docker image in a `fastapi-oracle-container` container
```console
docker run -d --name fastapi-oracle-container -p 80:80 fastapi-oracle-image
```

Goto http://0.0.0.0:80/docs


To stop the container
```console
docker stop fastapi-oracle-container
```

## Installing and running in VirtualEnv (for development)
Tested on OS X 12.2

### Asumptions

* Python 3.8 or higher is installed

After checking out the repo, in terminal, cd to the project root directory

Create virtual environment for the app
```console
python3 -m venv .
```

Activate the virtual environment
```console
source ./bin/activate
```

Install required packages from `properties.txt`
```console
pip install --no-cache-dir --upgrade -r ./requirements.txt
```

### Set database connection configuration

Rename the `template.env` file to `.env`

Edit the `.env` file in the project folder
```console
emacs .env
```

By filling in the following variables:

```python
DB_USERNAME=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=
DB_DATABASE=""
```

### Running the server instance in VirtualEnv
Start the app
```console
uvicorn main:app --reload
```

Goto http://127.0.0.1:8000/docs






