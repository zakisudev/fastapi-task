# FastAPI MVC Application

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Configure the database in `app/config/database.py`
3. Run the application: `uvicorn app.main:app --reload`

## Features
- MVC architecture
- SQLAlchemy ORM with MySQL
- Pydantic validation
- Token-based authentication
- Response caching
- Payload size validation

## Endpoints

### User Endpoints
- **POST /signup**: User signup
- **POST /login**: User login

### Post Endpoints (Authenticated)
- **POST /posts**: Add a new post
- **GET /posts**: Get all posts for the authenticated user
- **DELETE /posts**: Delete a post by ID

## Project Structure
.fastAPI/ ├── .gitignore ├── README.md ├── requirements.txt └── app/ ├── __init__.py ├── main.py ├── config/ │ ├── __init__.py │ └── database.py ├── controllers/ │ ├── __init__.py │ └── user_controller.py ├── dependencies/ │ ├── __init__.py │ └── auth.py ├── models/ │ ├── __init__.py │ └── database_models.py ├── schemas/ │ ├── __init__.py │ └── request_schemas.py └── services/ ├── __init__.py └── user_service.py


License
This project is licensed under the MIT License.
