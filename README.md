# Django REST API Backend

## Overview
This is a Django REST Framework (DRF) template designed to integrate with the React frontend. It includes preset configurations for a scalable API.

It has a prebuilt authentication system with a custom user model (Account). All you need is a frontend application.

## Features
- **Django REST Framework** for API development
- **Modular Apps** under `core/apps`
- **Media & Static File Handling**
- **Environment Configuration** using `.env`
- **Database Configuration** in `db.py-tpl`


## Folder Structure
```
drf_api/
│── core/
│   ├── apps/      # Modular Django apps
│   	├── account/		# Custom authentication app
│   	├── misc/			# Mmiscellaneous project features
│   ├── cdn/       # Static & media storage
│   ├── media/     # Media files
│── project_name/
│   ├── __init__.py-tpl
│   ├── settings.py-tpl  # Django settings template
│   ├── urls.py-tpl      # URL routing template
│   ├── wsgi.py-tpl      # WSGI application setup
│   ├── asgi.py-tpl      # ASGI application setup
│   ├── db.py-tpl        # Database connection setup
│── .env                 # Environment variables
│── manage.py-tpl        # Django management script
```

## Installation & Setup
```sh
# Install dependencies
pip install -r requirements.txt

# Create a project
cd ..
django-admin startproject <project_name> --template drf_api 

# Set Postgresql database details in .env file
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

# Make migrations (neccesary for the account module)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

