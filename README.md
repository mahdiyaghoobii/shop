# Django E-Shop Project

This repository contains a web application built using Python and the Django framework. It includes features for user authentication, product management, order processing, and a contact module.

## Project Structure

- `shop/`: Main Django project configuration (settings, main URLs).
- `account/`: Handles user registration, login, logout, and profile management.
- `contact_module/`: Manages contact form submissions.
- `home/`: Contains product listings, details, categories, search/filtering, basket functionality, and sliders.
- `main/`: Core application logic and main views (e.g., homepage).
- `templates/`: HTML templates for the frontend.
- `static/`: Static files (CSS, JavaScript, Images).
- `media/`: User-uploaded files (e.g., product images).

## Setup and Configuration

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/docs/getting-started/installation/) (for caching)

### PostgreSQL Configuration

1.  **Install PostgreSQL**
    Follow the instructions from the official [PostgreSQL documentation](https://www.postgresql.org/docs/).

2.  **Create a User and Database**
    Open your PostgreSQL shell and execute:

   ```sql
   CREATE USER your_username WITH PASSWORD 'your_password';
   CREATE DATABASE your_database_name OWNER your_username;
   ```

   Replace `your_username`, `your_password`, and `your_database_name` with your actual PostgreSQL username, password, and database name.

3.  **Verify Django Settings**
    Ensure the `DATABASES` setting in `shop/settings.py` matches your PostgreSQL setup:

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

1.  **Clone the repository** (if you haven't already):
    ```bash
    # git clone <repository_url>
    cd django-pr/shop
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    # source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser** (for accessing the Django admin):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## Key Features & Modules

- **User Authentication**: Login, registration, logout using Django's built-in system and Simple JWT for API tokens.
- **Product Catalog**: View products, product details, categories, filtering, and search.
- **Shopping Basket**: Add products to a basket (session-based or user-linked).
- **Contact Form**: Allows users to send messages.
- **Admin Interface**: Django admin for managing users, products, orders, etc.
- **API**: RESTful API built with Django REST Framework (DRF) and GraphQL (using Graphene-Django).
- **Caching**: Redis is used for caching data to improve performance.

## API Endpoints (Examples)

*Note: This is based on the analyzed `urls.py` files. Refer to the Swagger/Redoc documentation (`/api/schema/swagger-ui/` or `/api/schema/redoc/`) for a complete and interactive API specification.* 

- **Authentication (Simple JWT)**:
    - `POST /api/token/`: Obtain JWT access and refresh tokens.
    - `POST /api/token/refresh/`: Refresh JWT access token.
- **Account Management (Views)**:
    - `POST /signup/`: Register a new user.
    - `POST /signin/`: Log in a user.
    - `GET /signout/`: Log out a user.
- **Product Endpoints (`/product/`)**:
    - `GET /product/list-product/`: List products.
    - `GET /product/most-sells-products/`: List most sold products.
    - `GET /product/popular-products/`: List popular products.
    - `POST /product/setrate/`: Rate a product.
    - `GET /product/filter/`: Filter products.
    - `GET /product/slider/`: Get slider images/data.
    - `GET /product/categories/`: List product categories.
    - `GET /product/<slug>/`: View product details.
    - `GET /product/add-to-basket/<slug>/`: Add product to basket.
    - `GET /product/clear_basket/`: Clear the shopping basket.
- **Contact (`/contact-us/`)**:
    - `GET/POST /contact-us/`: Display and handle contact form submissions.
- **Main (`/`)**:
    - `GET /`: Homepage.
- **GraphQL**: 
    - `POST /graphql/`: GraphQL endpoint for queries and mutations.
- **API Schema**: 
    - `GET /api/schema/`: OpenAPI schema.
    - `GET /api/schema/swagger-ui/`: Swagger UI for API documentation.
    - `GET /api/schema/redoc/`: ReDoc UI for API documentation.

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature-branch`).
6.  Open a pull request.

## License

This project is likely under the MIT License if a `LICENSE` file exists, but please verify.

## Contact

For any inquiries or issues, please update this section with appropriate contact information.
