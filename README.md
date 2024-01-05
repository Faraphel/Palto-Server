# Palto-Server

(This is a project realised for our University, it will not be maintained after and it should not be used outside of testing)

Palto is a project to check students attendances at their school classes. 
It allows teachers to create sessions containing students that should be present. 
They can then scan their student card with the NFC technology and they will be automatically marked as present to 
this session.

# Installation

1. Install `python >= 3.11`
2. Create a virtual environment with `python -m venv ./.venv/`. The next steps will be inside it.
3. Install the dependencies with `python -m pip install -r ./requirements.txt`.
4. Modify the `Palto/settings.py` file to setup your database and other settings.
5. Make the migrations with `python ./manage.py makemigrations`.
6. Apply the migrations to the database with `python ./manage.py migrate`.
7. Run the program by with `python ./manage.py runserver`.
