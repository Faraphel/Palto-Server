# Palto-Server

(This is a project realised for our University, it will not be maintained after and it should not be used outside of testing)

Palto is a project to check students attendances at their school classes. 
It allows teachers to create sessions containing students that should be present. 
They can then scan their student card with the NFC technology and they will be automatically marked as present to 
this session.

# Installation

## Classic

1. Install `python >= 3.11`
2. Create a virtual environment with `python -m venv ./.venv/`. The next steps will be inside it.
3. Install the dependencies with `python -m pip install -r ./requirements.txt`.
4. Modify the `Palto/settings.py` file to setup your database and other settings.
5. Make the migrations with `python ./manage.py makemigrations`.
6. Apply the migrations to the database with `python ./manage.py migrate`.
7. Run the program by with `python ./manage.py runserver`.

## Docker

1. Start a terminal in the directory of the project.
2. Run `docker build`.
3. Change the environment variables to match your configuration.

# Advanced Settings

## Debug Mode

By default, the server is launch in production mode. 
This disables the automatic static files serving since they are considered as being already served by nginx or apache.
You can start with the environment variable `DEBUG=true` to start it in development mode. 

## Secret Key

You should set a django secret key manually in the `DJANGO_SECRET_KEY` environment variable. You can get one by
opening a python interpreter with django and calling the function `django.core.management.utils.get_random_secret_key()`.

## Database

The database used by default is `sqlite`. This is not recommended to keep it since it won't be saved by docker after
a restart if no volume are set, and it is considered a slow database engine. Using a `postgres` database is recommended.
You can find more details about the database in the configuration `settings.py`.