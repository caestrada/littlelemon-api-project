# Little Lemon API project

## Review criteria

- [x] The admin can assign users to the manager group

- [ ] You can access the manager group with an admin token

- [ ] The admin can add menu items 

- [ ] The admin can add categories

- [ ] Managers can log in 

- [ ] Managers can update the item of the day

- [ ] Managers can assign users to the delivery crew

- [ ] Managers can assign orders to the delivery crew

- [ ] The delivery crew can access orders assigned to them

- [ ] The delivery crew can update an order as delivered

- [ ] Customers can register

- [ ] Customers can log in using their username and password and get access tokens

- [ ] Customers can browse all categories 

- [ ] Customers can browse all the menu items at once

- [ ] Customers can browse menu items by category

- [ ] Customers can paginate menu items

- [ ] Customers can sort menu items by price

- [ ] Customers can add menu items to the cart

- [ ] Customers can access previously added items in the cart

- [ ] Customers can place orders

- [ ] Customers can browse their own orders



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