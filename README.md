# Bmat technical assignment

The test consists of two logical parts:
1. CSV processing module.
2. API and task execution system which uses this module to process the uploaded files.



# Solution

## Description

1. To start I create a project from a cookiecutter based on **Docker**
2. The project consists of 6 services:
    - `Django`: Server with API
    - `Postgres`: Database engine
    - `Celery Worker`: For asynchronous task queue
    - `Celery Beat`: for schedule tasks if it were necessary
    - `Flower`: for task traking dashboard
    - `Redis`: in this case for horizontal scaling if it were necessary

    This could have been made much simpler but my intention was that you could see apply SOLID principles and The 12 Factor setting.

3. I start developing a Restful API. Write some test.
4. A model is created to save info about these `reports`.
    ```
    pid:         Celery ID task
    input_file:  CSV input file
    outout_file: CSV output file
    status:      Could be Processing or Done
    created:     Timestamp
    updated:     Timestamp, both could be used to calculate the report's duration
    ```

5. Also, a serializer class and the view are created to handle the two endpoints requested.

    ```
    bmat\api\models\reports.py
    bmat\api\serializers\reports.py
    bmat\api\views\reports.py
    bmat\api\tests\test_reports.py
    ```


6. Then create an app to handle celery and create a task to process these input files sent.

    ```
    bmat\taskapp\tasks.py
    ```
7. Use [Dask](https://docs.dask.org/) for the main process. 

    **Why Dask?**
    - Utilizes multiple CPU cores by internally chunking dataframe and process in parallel.
    - Can handle large datasets on a single CPU exploiting its multiple cores or cluster of machines refers to distributed computing.
    - Dask instead of computing first, create a graph of tasks which says about how to perform that task.

## Endpoint

### 1. Schedule file to processing

```
POST: /api/reports/

Parm: 
- input_file: file

Return:
- pid: string
```

### 2. Download the result

```
GET: /api/reports/<pid>

Parm: 
- pid: string

Return:
- pid: string
- status: int
- output_file: string (file url)
```

## Features
This project has the following features:
* **Python** 3.6
* **Django** 2.0.10
* **Django REST Framework** 3.9.1
* [**12 Factor**](https://12factor.net/) based settings
* Folow **SOLID** principles
* **PostgreSQL** as database engine
* **Docker** as container engine
* Optimized development and production settings
* Run tests with unittest or pytest
* **Flake8** for Style Guide Enforcement

Notes:
- I start this project with my personal [cookiecutter](https://github.com/gianfrancolombardo/cookiecutter-django-api) for a matter of time. I know I have to update some package versions but it works for this assignment.



## Development

```bash
$ docker-compose -f local.yml up --build
```

## Test
```bash
$ docker-compose -f local.yml run django ./manage.py test
```

## Flower
```bash
url:  http://localhost:5555
user: user
pass: flower
```

