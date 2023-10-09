# Little Lemon API project

## Review criteria

- [x] The admin can assign users to the manager group

- [x] You can access the manager group with an admin token

- [x] The admin can add menu items 

- [x] The admin can add categories

- [x] Managers can log in 

- [x] Managers can update the item of the day

- [x] Managers can assign users to the delivery crew

- [x] Managers can assign orders to the delivery crew

- [ ] The delivery crew can access orders assigned to them

- [x] The delivery crew can update an order as delivered

- [x] Customers can register

- [x] Customers can log in using their username and password and get access tokens

- [x] Customers can browse all categories 

- [x] Customers can browse all the menu items at once

- [x] Customers can browse menu items by category

- [ ] Customers can paginate menu items

- [x] Customers can sort menu items by price

- [x] Customers can add menu items to the cart

- [ ] Customers can access previously added items in the cart

- [x] Customers can place orders

- [x] Customers can browse their own orders



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