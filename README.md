# FastAPI Oracle CRUD application

## Introduction
This is a simple Python FastAPI test application that works with an Oracle database.

## Summary
The goal of this project was to learn a bit more about FastAPI, SQLAlchemy, Oracle Database and Docker.
Once 'HelloWorld' started working, I wanted to experiment with something a bit more complex. Specifically, CRUD API which handles Foreign Keys, One-To-One and One-To-Many cascading relationships using SQLAlchemy and Oracle database behind it. Finally, I wanted to run the whole thing from Docker.

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

### Set database connection configuration

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

Build Docker image using the `Dockerfile.oracle` file
```console
docker build -f ./Dockerfile.oracle -t FastAPI-Oracle-Image . 
```

### Running the server instance in Docker
Run the newly created Docker image in a `FastAPI-Oracle-Container` container
```console
docker run -d --name FastAPI-Oracle-Container -p 80:80 FastAPI-Oracle-Image
```

Goto http://0.0.0.0:80/docs


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






