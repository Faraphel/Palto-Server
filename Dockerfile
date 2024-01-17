# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=Palto.settings
ENV DJANGO_SECRET_KEY=""
ENV DATABASE_ENGINE="sqlite"
ENV DEBUG=false

# Set the working directory in the container
WORKDIR /App

# Copy the current directory contents into the container
COPY . /App

# Install requirements
RUN python -m pip install -r requirements.txt

# Prepare the server
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

# Expose the port on which your Django application will run
EXPOSE 80

# Start the Django application
ENTRYPOINT ["python", "manage.py", "runserver_plus", "0.0.0.0:80"]
