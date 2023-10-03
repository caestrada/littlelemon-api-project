# Little Lemon API project

## Steps taken

1. Create project directory
```
mkdir LittleLemon
cd LittleLemon
```

2. Setup Django
```
pipenv install django
```

3. Start virtual environment
```
pipenv shell
```

4. Create project
```
django-admin startproject LittleLemon .
```

5. Create app for project. This will create the app with all the necessary migration and configurations.
```
python manage.py startapp LittleLemonAPI
```

6. Install DRF
```
pipenv install djangorestframework
```

## >_ Commands

Start virtual environment
```
pipenv shell
```

Create a project
```
django-admin startproject <project_name> .
```

Create app for project
```
python manage.py startapp <app_name>
```

Run server
```
python manage.py runserver

# On different port

python manage.py runserver <port_number>
```