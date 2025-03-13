## Overview
This is a flask application that demonstrates how to integrate PostgreSQL as the database and Celery for asynchronous task processing.

## Features
- User authentication
- Asynchronous task processing with Celery
- PostgreSQL database integration

## Prerequisites
Before you begin, ensure you hae the following installed:

- python 3,10 or higher
- PostgreSQL
- Redis( for Celery )

## Installation
1. Create a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Setup PostgreSQL:
    - Create a new PostgreSQL database and user.
    - Update the database connection settings in .env file.
    - Create a DB named 'db_telehealth'

4. Navigate to the src directory and set the FLASK_APP environment variable:
    cd src
    export FLASK_APP=main.py

5. Run database migrations:
    cd src
    flask db init
    flask db migrate
    flask db upgrade

6. Run Redis server
    Make sure your Redis server is running.

7. Run Flask application
    cd src
    flask run

8. Start the Celery worker:
    ```bash
    cd src
    celery -A core.celery worker -l INFO

## Usage

## API Endpoints

1. User Registration
    - method: POST 
    - endpoint: localhost:5000/register
    - Request body
    json:
    {
        "name":"example",
        "email":"xxx@xxx.com",
        "password":"" #Should be at least 8 characters with upper and lower case letters, numbers and special characters
    }

2. Login
    - method: POST 
    - endpoint: localhost:5000/login
    - Request body
    json:
    {
        "email":"xxx@xxx.com",
        "password":"" #Should be at least 8 characters with upper and lower case letters, numbers and special characters
    }

3. Get Current User
    - method: GET 
    - endpoint: localhost:5000/current_user
    - Headers:
        Authorization: Bearer <_token>

4. Create Patient
    - ** POST ** localhost:5000/patients
    - Headers:
        Authorization: Bearer <_token>
    - Request body:
    ```json
    {
        "name":"example",
        "email":"example@gmail.com",
        "phone":"12321143214321"
    }

5. Read Patient
    - ** GET ** localhost:5000/patients/<id>
    - Headers:
        Authorization: Bearer <_token>

6. Read Patients
    - ** GET ** localhost:5000/patients
    - Headers:
        Authorization: Bearer <_token>

7. Update Patient
    - ** PUT ** localhost:5000/patients/<id>
    - Headers:
        Authorization: Bearer <_token>
    {
        "name":"example",
        "email":"example@gmail.com",
        "phone":"12321143214321"
    }


8. Delete Patient
    - ** DELETE ** localhost:5000/patients/<id>
    - Headers:
        Authorization: Bearer <_token>
