# Book Giveaway Service API

Book Giveaway Service is an api built with Django and Django REST framework where registered users can offer books for free and also can implement CRUD operations.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Docker Setup](#docker-setup)


## Requirements

- Python 3.x
- Docker

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/MirasGitHub/book_giveaway_api
    cd book_giveaway_api
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv virtualenv
    source virtualenv/bin/activate
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

2. populate database with fixture data

   ```python
   make populate_database
   ```
3. create a super user
   ```python
   make createsuperuser
   ```
after running a project you should be able to perform CRUD operations on the following endpoint:

**localhost:8000/api/books**

## API Endpoints

- **Authors**: `/api/authors/`
- **Genres**: `/api/genres/`
- **Conditions**: `/api/conditions/`
- **Books**: `/api/books/`
- **User Books**: `/api/user-books/`
- **User Registration**: `/api/users/register/`
- **User Login**: `/api/users/login/`
- **Swagger Docs**: `/swagger/`


## Docker Setup

Docker is required to run a project.


1. Build the Docker image:

  ```bash
make build
```

2. Run the Docker container:

run a project.
```bash
make run
```

3. Access the API at `http://localhost:8000`.


### Author 
   - **Miranda Kobalia**
