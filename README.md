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

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/eshop.git
    cd eshop
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```



## Configuration

- **Database**: Configure your database settings in `shop/settings.py`.
- **Static Files**: Ensure your static files are correctly set up in `shop/settings.py`.
- **Media Files**: Configure media file settings in `shop/settings.py`.

## API Endpoints

- **User Authentication**:
    - `POST /api/auth/login/`: User login
    - `POST /api/auth/register/`: User registration
    - `POST /api/auth/logout/`: User logout

- **Product Management**:
    - `GET /api/products/`: List all products
    - `GET /api/products/<id>/`: Retrieve a specific product
    - `POST /api/products/`: Create a new product
    - `PUT /api/products/<id>/`: Update a product
    - `DELETE /api/products/<id>/`: Delete a product

- **Order Processing**:
    - `GET /api/orders/`: List all orders
    - `POST /api/orders/`: Create a new order

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact [yourname@example.com](mailto:yourname@example.com).
