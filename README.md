## Python Fast API exercise

TO-DO application has 3 tables: User, Company, Task. There are three roles: superadmin, admin, user:
- Superadmin can manage admin account (create, update, delete), create a new company and delete a company, superadmin doesn't belong to any company.
- Admin can manage tasks, users of their company.
- User can be assigned to tasks.

Notes: API get list of items can just be filtered by one value each field, if we use search and type 'a' to search user by name, list of user will not contains user which has name 'A'.
