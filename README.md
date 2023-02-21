# ShoppingStore

Backend for abstract shopping store.

[![Tests](https://github.com/TheDim0n/ShoppingStore/actions/workflows/tests.yml/badge.svg)](https://github.com/TheDim0n/ShoppingStore/actions/workflows/tests.yml)

### Configuration

Available environment variables:

```
DATABASE_URL                   # string, required. URL to PostgreSQL database
DEBUG                          # boolean, default is false. If true, enable
                                 server reloading
ACCESS_TOKEN_EXPIRES_MINUTES   # int, required. Access token lifetime in minutes
REFRESH_TOKEN_EXPIRES_DAYS     # int, required. Refresh token lifetime in days
SECRET_KEY                     # string, required. Secret key for passwords.
INITIAL_USER_USERNAME          # string, required. Username of initial user.
INITIAL_USER_PASSWORD          # string, required. Password of initial user.
LOAD_MOCK                      # boolean, default is false. If true, load mock
                                 data
CORS_ORIGINS                   # string, default is empty string. List of origins
                                 for CORS policy.
ROOT_PATH                      # string, default is empty string. Path setting
                                 for proxy.
```

### Run

With `Docker`:

```
docker compose up --build
```

or with `python`:

- create and activate python virtual environment
- install dependencies:
  ```
  python -m pip install -U pip
  pip install -r requirements.txt
  ```
- create `.env` file to configurate application (see `Configuration` section)
- Apply database migrations:
  ```
  python migrate.py
  ```
- Run application:
  ```
  python run.py
  ```

> API documentation awailable at http://localhost:8000/docs
