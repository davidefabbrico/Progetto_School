# Documentation

For all the following things you have to change directory in the mysite folder of the project.

## Requirements

For the project the installed pakages are:
* Pandas
* Numpy
* Django
* Pymysql
* Django-Verify-Email

So when you have already install the pip extention you can run the following line in the terminal:
  ```
  pip install pandas
  pip install numpy (pandas have already the numpy package)
  pip install django
  pip install pymysql
  pip install Django-Verify-Email
  ```

For running the project in local you need a mysql database and modify the settings.py in the mysite folder.
For example if you create a database with name progettoschool the custom code is the follow:

  ```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database name',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'your password',
      }
  }
  ```

You should create a super user for enter in the django administration (`http://127.0.0.1:8000/admin/` for example) with this line of code: 
  `python3 manage.py createsuperuser`

## Run it

When you have install, configurate the local server and create a database you can run the project with the following line of code (terminal):
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver
  ```
  
For the query in the existing table you can run the shell with: `python3 manage.py shell`
