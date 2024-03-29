# Intro
Based on multiple tutorials and personal investigation:
  - [Django Wednesday by Codemy](https://www.youtube.com/playlist?list=PLCC34OHNcOtqW9BJmgQPPzUpJ8hl49AGy)
  - [Django Form-Previews by BugBytes](https://www.youtube.com/watch?v=d5YlrHe0uzw)
  - [Django - Building Form Wizards by BugBytes](https://www.youtube.com/watch?v=8xb9s3jnRF8)
  - [Django Formtools documentation](https://django-formtools.readthedocs.io/en/latest/index.html)

# Setup
## 1- Virtual machine
```shell
python3 -m venv venv
source venv/bin/activate
```

## 2- Install dependencies
```shell
pip install -r requirements.txt
```

### Best Practices: Requirements
[Requirements - Best practices](https://stackoverflow.com/questions/61536466/pips-requirements-txt-best-practice)
After creating requirements.in: `echo "django==5.0.1" > requirements.in`
```shell
source venv/bin/activate
python -m pip install pip-tools
pip-compile --output-file=- > requirements.txt
pip install -r requirements.txt
```

### Best Practices: Install libraries
[Best Practices: Install libraries](https://stackoverflow.com/questions/19135867/what-is-pips-equivalent-of-npm-install-package-save-dev)
To install a `PACKAGE`:
```shell
source venv/bin/activate
echo >> requirements.in && pip install PACKAGE && pip freeze | grep PACKAGE >> requirements.in
pip-compile --output-file=- > requirements.txt
pip install -r requirements.txt
```
Note: `echo >> requirements.in` for getting to new line in file

Example: `echo >> requirements.in && pip install reportlab && pip freeze | grep reportlab >> requirements.in`

## 3- Run machine
```shell
python manage.py runserver
```

You would need initially to run migrations:
```shell
python manage.py makemigrations
python manage.py migrate
```

# Content
## Django Preview Form Vanilla
/add_wish - [basic preview after save](https://stackoverflow.com/questions/61998149/form-preview-in-django)

## Django Formtools for [Preview Form](https://django-formtools.readthedocs.io/en/latest/preview.html)
/add_star - using Django Formtools Preview functionality

## Django Formtools for [Steps Form](https://django-formtools.readthedocs.io/en/latest/wizard.html)
/add_contact - Basic 2 steps form

/add_booking - 2 or 3 steps form + save

/update_booking - Use cases:
  - Create someone with a business then update the night counts => WORKS
  - Create someone with a business then update to remove the business => WORKS
  - Create someone without a business then update the night counts => WORKS
  - Create someone without a business then add a business => WORKS

## Both Steps and Preview
/add_tour - 3 steps form + 4th step as a preview