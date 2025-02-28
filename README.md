# Student Assistnat 

## Project Description
This is a student assistant application build with django. 

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