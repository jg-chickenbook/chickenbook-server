# Django REST API Application
This document provides instructions for setting up and running the Django REST API application. This API serves as the backend for Chickenbook application.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

* Python 3.10 or higher
* pip (Python package manager, Python include pip) verify installation with command: pip --version

## Installation
Follow these steps to set up the Django REST API application on your local development machine.

1. Clone the Repository
Clone the repository to your local machine using Git:

```sh
git clone https://github.com/jg-chickenbook/chickenbook-server.git
```
```sh
cd chickenbook-server
```

2. Create and Activate a Virtual Environment
For Unix/macOS:

```sh
python3 -m venv env
```
```sh
source env/bin/activate
```

For Windows:

```sh
python -m venv env
```
```sh
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


## 🤝 Collaboration guide

`ISSUE` ➡️ `BRANCH` ➡️ `COMMITS` & `PUSHES` ➡️ `PULL REQUEST` ➡️ `CODE REVIEW` ➡️ `MERGE into DEV`

### 🔥 Issue
- Always use corresponding labels for an issue `feature`, `bug`, `documentation`,  `refactoring`, `help wanted`
- You can use an issue template for a feature or bug but feel free to use a blank issue as well. The issue description should describe a given feature/problem/bug/task.

| Branch Category (label)      | Meaning       |
| -----------: | ------------- |
| `main`          | for deployment        |
| `dev`           | for putting the code together before deployment |
| `feature`       | for adding a feature  |
| `bug`           | for defining and fixing a bug  |
| `hotfix`        | for quickly fixing critical issues, usually with a temporary solution  |
| `refactoring`   | for restructuring and improving project/code |
| `test`          | for experimenting something which is not an issue |
| `docs`          | for documntation updates |

The name of the branch should has the following format:

`<branch-category>/<name-initials>-<issue-number>-<issue-name>`
```
EXAMPLE: feature/jt-30-profile-screen
jt = initials of name
feature = branch category
30 = number of issue 
the rest = the branch title
```

### ➕ Commits
- Commit small changes separately. More commits are better than few. 
- Each commit should be one logical unit. For example, you shouldn't add a small icon component and update documentation in one single commit.
- Always write commit in the following format: `<ver-in-infinitive> <something>`, for example: `Create function for fetching user data`

### 🙏 Pull requests

Pull requests should target the `dev` branch (set `base: dev` and `compare: <your-branch>`). Any change that is going to be merged should be checked by at least one other developer. Therefore **add others as reviewers in your pull request** so they get a notification that you need them to check it out. **Branch shouldn't be merged without a code review and/or some feedback written in the pull request**. Comments or at least reactions are required in PRs and **all the PR related communication should happen within the given PR** or be at least noticed/mentioned including its outcome.

Each pull requests should contain at least basic information about the changes. You can use this simple template:

```
- A reference to a related issue in your repository.
- A description of the changes proposed in the pull request.
  - What's new?
  - What has been modified?
  - What has been deleted?
```

### 💬 Communication
- **An answer to a comment is always required.** An emoji reactions can be used in some cases, such as 👍 or 👎 in the case of yes or no questions.
- **Any code that is part of the task should be well-committed and appropriately documented.**

### 🧱 Folder Structure
In process

### ⚙️ Recommended VS Code Extensions
In process