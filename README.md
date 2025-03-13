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

4. Set environment variable:
    Create a .env file in root folder and edit like this.
    ```bash
    DEBUG=False
    SECRET_KEY=XXXX
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=
    POSTGRES_DB=db_telehealth
    POSTGRES_HOST=localhost:5432
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}
    REDIS_URL=redis://localhost:6379/0
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

    Navigate to src directory and set the FLASK_APP environment variable.

    ```bash
    cd src
    export FLASK_APP=main.py

    
5. Run database migrations:
    ```bash
    cd src
    flask db init
    flask db migrate
    flask db upgrade

6. Run Redis server:
    Make sure your Redis server is running.

7. Run Flask application:
    ```bash
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
    ```json
    {
        "name":"example",
        "email":"xxx@xxx.com",
        "password":""
    }

2. Login
    - method: POST 
    - endpoint: localhost:5000/login
    - Request body
    ```json
    {
        "email":"xxx@xxx.com",
        "password":"" 
    }

3. Get Current User
    - method: GET 
    - endpoint: localhost:5000/current_user
    - Headers:
    ```json
        Authorization: Bearer <_token>

4. Create Patient
    - method: POST 
    - endpoint: localhost:5000/patients
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
    - method: GET
    - endpoint: localhost:5000/patients/<id>
    - Headers:
    ```json
        Authorization: Bearer <_token>

6. Read Patients
    - method: GET
    - endpoint: localhost:5000/patients
    - Headers:
    ```json
        Authorization: Bearer <_token>

7. Update Patient
    - method: PUT
    - endpoint: localhost:5000/patients/<id>
    - Headers:
    ```json
        Authorization: Bearer <_token>
    {
        "name":"example",
        "email":"example@gmail.com",
        "phone":"12321143214321"
    }


8. Delete Patient
    - method: DELETE 
    - endpoint: localhost:5000/patients/<id>
    - Headers:
    ```json
        Authorization: Bearer <_token>
