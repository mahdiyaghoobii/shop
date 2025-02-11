# Shop

This repository contains a web application built using HTML and Python (Django framework).

## Setup and Configuration

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

### PostgreSQL Configuration

1. **Install PostgreSQL**
   Follow the instructions to install PostgreSQL from the official [PostgreSQL documentation](https://www.postgresql.org/docs/).

2. **Create a User and Database**
   Open your PostgreSQL shell and execute the following commands:

   ```sql
   CREATE USER your_username WITH PASSWORD 'your_password';
   CREATE DATABASE your_database_name OWNER your_username;
   ```

   Replace `your_username`, `your_password`, and `your_database_name` with your actual PostgreSQL username, password, and database name.

3. **Update Django Settings**
   Update the `DATABASES` setting in your `settings.py` file:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Django Setup

1. **Install Requirements**

   Navigate to the project directory and install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

2. **Apply Migrations**

   Apply the database migrations:

   ```sh
   python manage.py migrate
   ```

3. **Run the Server**

   Start the Django development server:

   ```sh
   python manage.py runserver
   ```

   Your application should now be running at `http://127.0.0.1:8000/`.
