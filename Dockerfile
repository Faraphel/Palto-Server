# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=Palto.settings

# Set the working directory in the container
WORKDIR /App

# Copy the current directory contents into the container
COPY . /App

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port on which your Django application will run
EXPOSE 80

# Start the Django application
ENTRYPOINT ["python", "manage.py", "runserver_plus", "0.0.0.0:80"]
