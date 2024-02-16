# Django REST API Application
This document provides instructions for setting up and running the Django REST API application. This API serves as the backend for Chickenbook application.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

* Python 3.8 or higher
* pip (Python package manager)
* Virtualenv (optional, but recommended for creating isolated Python environments)

## Installation
Follow these steps to set up the Django REST API application on your local development machine.

1. Clone the Repository
Clone the repository to your local machine using Git:

```sh
git clone https://example.com/your-repository.git
cd your-repository
```

2. Create and Activate a Virtual Environment
For Unix/macOS:

```sh
python3 -m venv env
source env/bin/activate
```

For Windows:

```sh
python -m venv env
.\env\Scripts\activate
```

3. Install Required Packages
Install all required packages using pip:

```sh
pip install -r requirements.txt
```

4. Apply Migrations
Apply database migrations to set up your database schema:

```sh
python manage.py migrate
```

5. Create an Admin User
Create an admin user to access the Django admin interface:

```sh
python manage.py createsuperuser
```

Follow the prompts to set up your username, email, and password.

6. Run the Development Server

Start the Django development server:

```sh
python manage.py runserver
```

The API will be available at http://localhost:8000. If you need run server on different port just specify port at the end of the command

Testing the API
To test the API endpoints, you can use tools like Postman or curl. Here is an example curl command to test the API:

```sh
curl -X GET http://localhost:8000/api/accounts/test_token
```

Replace /api/endpoints with the actual endpoint you wish to test.

## Feedback
If you have any feedback, please file an issue in the GitHub repository or contact us on github.

