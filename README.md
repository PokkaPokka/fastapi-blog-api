# FastAPI Blog API

This project is a blog API built using FastAPI, SQLAlchemy, and PostgreSQL. It includes features for user authentication, post creation, comments, and voting. The project also includes testing with Pytest and database migrations with Alembic.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)

## Features

- User authentication (registration, login)
- CRUD operations for posts
- Commenting on posts
- Voting on posts
- JWT-based authentication
- Database migrations with Alembic
- Testing with Pytest

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up the environment variables by creating a `.env` file in the `app` directory with the following content:

   ```env
   DB_HOST=<your-database-host>
   DB_NAME=<your-database-name>
   DB_USER=<your-database-user>
   DB_PASSWORD=<your-database-password>
   OAUTH_SECRET_KEY=<your-oauth-secret-key>
   ALGORITHM=<your-algorithm>
   TOKEN_EXPIRE_MINUTES=<your-token-expire-minutes>
   ```

5. Run the database migrations:
   ```sh
   alembic upgrade head
   ```

## Usage

1. Start the FastAPI server:

   ```sh
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`.

3. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Testing

1. To run the tests, use the following command:
   ```sh
   pytest
   ```

## Deployment

1. Build the Docker image:

   ```sh
   docker build -t fastapi-blog-api .
   ```

2. Run the Docker container:
   ```sh
   docker-compose up
   ```

## Environment Variables

- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `OAUTH_SECRET_KEY`: Secret key for JWT
- `ALGORITHM`: Algorithm for JWT
- `TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Project Structure

```plaintext
.
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── comment.py
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── vote.py
│   ├── schemas.py
│   ├── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_posts.py
│   ├── test_users.py
├── Dockerfile
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── requirements.txt
├── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Skills

Programming Languages: Python, SQL

Frameworks & Tools: FastAPI (API development), PostgreSQL (database manipulation), Pytest (testing), Pydantic (data validation), Postman (API testing), SQLAlchemy (Python SQL toolkit and Object Relational Mapper), Alembic (database migration), Heroku (deployment)

Skills: API design (routes, serialization/deserialization, schema validation, user authentication),
ORM (Object Relational Mapper), JWT (JSON Web Token), CI/CD pipeline, Database migration, CORS (Cross-Origin Resources Sharing)
