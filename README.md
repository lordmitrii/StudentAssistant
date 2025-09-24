# Student Assistant 

## Project Description
The Student Assistant is a web application designed to help students track academic deadlines 
and manage their grades efficiently. 
Users are able to add, edit, and delete courses, as well as add deadlines for specific courses to 
keep track of assignments, quizzes, and projects. They can also input grades for deadlines or add 
them without linking to a specific assignment. Deadlines can be sorted by date, allowing 
students to plan their schedules effectively.

## Instructions to run the project

Create virtual environment and install the dependencies:

```bash
# Create venv 
python -m venv venv
```

If you are using `mac` or `linux`, run:
```bash
# Activate venv
src venv/bin/activate
```

For `windows`:
```bash
# Activate venv
venv\Scripts\activate
```

Then, use:
```bash
# Install the requirements
pip install -r requirements.txt
```

Now, you are ready to run the project. Use:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Branch flow rules
`main`:
- This is a **base** of the project.
- **Do not commit to this branch**, first commit to a separate branch and make a pull request if everything works fine.
- After making a pull request, wait untill someone approves it.
- After the approval, we can merge changes to `main`.

`other`:
- To work on the project, create a separate branch and push **only** to it.
- If you are done with the feature/bugfix/other, you can make a pull request to `main` branch.
- Before you push the changes, please update the requirements.txt if installed any new packages
- When you work on the project, ensure that your branch is up-to-date with the main branch

## Sources used
- Bootstrap v5.3.3: https://getbootstrap.com/
- Google Oauth v2.0: https://developers.google.com/identity
- Django-Allauth v65.5.0 https://django-allauth.readthedocs.io
- PyJWT v2.6.0 https://pypi.org/project/PyJWT/
- Requests https://pypi.org/project/requests/
- Typing Extension https://pypi.org/project/typing_extensions/
