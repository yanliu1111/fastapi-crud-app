# FastAPI with CRUD operations

### Project purpose

Start by setting up a FastAPI project and running a simple web server. Then, progress to more advanced topics, including building REST APIs, handling path and query parameters, and working with databases using SQLModel. Additionally, explore managing settings with Pydantic, organizing your API with routers, and implementing asynchronous SQLModel connections.

### Tech stack

- FastAPI
- Postgresql by [NEON](https://neon.tech/docs/guides/python) COULD BD (Set your Postgresql db in cloud)
- ORM managed by SQLAlchemy
- Data validating managed by Pydantic
- CRUD With SQLModel
- Alembic for migrations, offers good template for using async DB
- passlib for password hashing
- pydantic for data validation and settings management
- pyjwt for JWT token management
  
### Project setup
1. Clone the project repository:
```bash
git clone https://github.com/yanliu1111/fastapi-crud-app.git
```

2. Navigate to the project directory:
```bash
cd fastapi-crud-app/
```

3. Create a virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file in the root directory and add Neon database URL:
```bash
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
JWT_SECRET=#reference 8👉
JWT_ALGORITHM=HS256
```
6. Run database migrations to initialize the database schema:
```bash
alembic upgrade head
```
7. Run the FastAPI application:
```bash
fastapi dev src/
```

8. 👉JWT token generation:
```bash
python
import secrets
secrets.token_hex(16)
```