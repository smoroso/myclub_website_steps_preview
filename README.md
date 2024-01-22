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
(Requirements - Best practices)[https://stackoverflow.com/questions/61536466/pips-requirements-txt-best-practice]
```shell
source venv/bin/activate
python -m pip install pip-tools
pip-compile --output-file=- > requirements.txt
pip install -r requirements.txt
```

### Best Practices: Install libraries
(Best Practices: Install libraries)[https://stackoverflow.com/questions/19135867/what-is-pips-equivalent-of-npm-install-package-save-dev]
To install a `PACKAGE`:
```shell
source venv/bin/activate
echo >> requirements.in && pip install PACKAGE && pip freeze | grep PACKAGE >> requirements.in
pip-compile --output-file=- > requirements.txt
pip install -r requirements.txt
```
Note: `echo >> requirements.in` for getting to new line in file
example: `echo >> requirements.in && pip install reportlab && pip freeze | grep reportlab >> requirements.in`

## 3- Run machine
```shell
python manage.py runserver
```

# Content
## Django Formtools for Preview Form
/add_star

## Django Formtools for Steps Form
/add_contact
/edit_contact
/add_booking
/update_booking
  Use cases:
    - Create someone with a business then update the night counts => WORKS
    - Create someone with a business then update to remove the business => Flaky
      Note: Does not really work becauyse on next update business is preselected and value still exists
    - Create somene without a business the update the night counts => WORKS
    - Create somene without a business the update the night counts then add a business => NOPE
      Note: Adding a business says: 'NoneType' object has no attribute '_meta'

## Both Steps and Preview