# Expense Tracker REST API

A backend REST API built using **FastAPI, Python, SQLAlchemy, and PostgreSQL** to manage personal expenses. The application provides JWT-based authentication, expense and category management, filtering, pagination, and expense reports.

## Features

- **User Authentication**
  - User registration and login
  - JWT-based authentication
  - Argon2 password hashing
  - Protected API endpoints

- **Expense Management**
  - Create, retrieve, update, and delete expenses
  - User-specific expense access
  - Category association
  - Expense descriptions and notes

- **Category Management**
  - Create, retrieve, update, and delete categories
  - Prevent deletion of categories associated with expenses
  - Shared categories across users

- **Filtering and Pagination**
  - Pagination with configurable page size
  - Filter by category
  - Filter by date range
  - Filter by minimum and maximum amount
  - Search expenses by title

- **Expense Reports**
  - Monthly expense summary
  - Category-wise expense breakdown
  - Yearly monthly expense reports

- **Database Management**
  - SQLAlchemy ORM
  - PostgreSQL database
  - Alembic database migrations

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- PyJWT
- Argon2
- Alembic
- Uvicorn

## Project Structure

```text
expense_tracker/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── dependencies.py
├── auth.py
│
├── routers/
│   ├── auth_routes.py
│   ├── expense_routes.py
│   ├── category_routes.py
│   └── report_routes.py
│
├── alembic/
│   └── versions/
│
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd expense_tracker
```

### 2. Create a virtual environment

```bash
python -m venv env
```

Activate it on Windows:

```bash
env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

Create a database named:

```sql
CREATE DATABASE expense_tracker_db;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/expense_tracker_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the database credentials and secret key with your own values.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login and generate JWT |
| GET | `/auth/me` | Get authenticated user |

### Expenses

| Method | Endpoint | Description |
|---|---|---|
| POST | `/expenses/` | Create an expense |
| GET | `/expenses/` | List expenses with filters and pagination |
| GET | `/expenses/{expense_id}` | Retrieve an expense |
| PUT | `/expenses/{expense_id}` | Update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories/` | Create a category |
| GET | `/categories/` | List categories |
| GET | `/categories/{category_id}` | Retrieve a category |
| PUT | `/categories/{category_id}` | Update a category |
| DELETE | `/categories/{category_id}` | Delete a category |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports/summary` | Monthly expense summary |
| GET | `/reports/category-wise` | Category-wise expense report |
| GET | `/reports/yearly` | Yearly monthly expense report |

## Authentication

Protected endpoints require a valid JWT access token.

After logging in, copy the generated access token and include it in the request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Database Relationships

- One user can have multiple expenses.
- One category can be associated with multiple expenses.
- Each expense belongs to one user and one category.

## Database Migrations

Alembic is used to manage database schema changes.

Apply migrations:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

## Future Improvements

- Automated unit and integration testing
- Docker support
- Deployment and CI/CD pipeline
