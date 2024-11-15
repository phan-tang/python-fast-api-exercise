## Python Fast API exercise

TO-DO application has 3 tables: User, Company, Task. There are three roles: superadmin, admin, user:
- Superadmin can manage admin account (create, update, delete), create a new company and delete a company, superadmin doesn't belong to any company.
- Admin can manage tasks, users of their company.
- User can be assigned to tasks.

Notes: API get list of items can just be filtered by one value each field, if we use search and type 'a' to search user by name, list of user will not contains user who has name 'A'.


### Install and start application
```
Run command to create virtual environment (Linux):
> virtualenv --python /usr/bin/python3.10 venv
```

```
Run command to start virtual environment:
> source ./venv/bin/activate
```

```
Install necessary packages by command:
> pip install -r requirements.txt
```

```
Run postgresql via docker:
> docker compose up -d
```

```
Copy .env.example file and change its name to .env

Migrate and seed data for database by command:
> alembic upgrade head

After seed data, there is a superadmin in user table with username is superadmin and password is password.
```

```
Create JWT_SECRET by command:
> openssl rand -hex 32

After create token, copy it into .env file
```

```
Run application by command:
> uvicorn main:app --reload
```

### APIs permission

- /admins: Only superadmin can use these APIs.
- /companies:
    - All users can use API to get list of companies.
    - Only superadmin can create, delete a new company. One company can be deleted when it doesn't have employees.
    - Only admin company can update company information.
- /users: Only company admin can use these APIs to manage their company employees.
- /tasks: Only company admin can use these APIs to manage their company tasks (tasks are assigned to their employees).
- /auth/token: All users can use this API to login.