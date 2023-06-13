# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /.

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Set the environment variables
ENV DJANGO_SETTINGS_MODULE=PlatePalDjango.settings
ENV PYTHONUNBUFFERED=1

# Expose the port on which the Django application will run
EXPOSE 8080

# Run the Django application
RUN python manage.py runserver 0.0.0.0:8080