# Instructions
Clone this repository
```
git clone git@github.com:Reyozaki/simple-webapp.git
```

## Requirements
- Python 3.12
- uv package manager: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- make (for Makefile)

## Installation
Install uv package manager:
```
# install using pip
pip install uv
```

Check if make is installed, in terminal:
```
make --version
```

If not installed:
- For Windows, install from [GNUWin32](https://gnuwin32.sourceforge.net/packages/make.htm)
- For Linux or WSL,
```
# others
sudo apt-get install make

# arch
sudo pacman -S base-devel
```

## Regular Setup
Using make, `make help` for available commands. Configure `.env` first, instructions [below](https://github.com/Reyozaki/simple-webapp?tab=readme-ov-file#configure-environment-variables).
```
# build webapp image
make docker-build

# first time running backend server
make setup

# running server afterwards
make server

# incase of error and docker containers persist
make docker-down

# clean containers and volumes(database wipe)
make docker-clean
```

## Use the Webapp
Server will run on localhost port 8000. 
- SwaggerDocs [localhost:8000/docs](http://localhost:8000/docs)
- Login Page [localhost:8000/static/html/login.html](http://localhost:8000/static/html/login.html)

### Features
- login:
  - username: admin
  - password: password

- Create:
  - Users page: Input details and save user.

- Read: 
  - Profile page: User(self) data.
  - Users page: (admin role required) User(all) List.

- Update:
  - Users page: Update button on Users List.
                User data is retrieved(excluding password), change values and save user.
- Delete:
  - Users page: Delete button on Users List to delete user.

- PDF generation:
  - Users page: Download users list in pdf.
  - Profile page: Download user details in pdf. **(Not working)**

- Data Filtering: Filter by address.

- Pagination: 
  - Backend 10 rows of data.
  - Frontend 5 rows of data.


## Dev Setup (might not be updated)
Packages/dependencies handled by uv. Creates a virtual environment `.venv` and install all dependencies.
```
# sync dependencies from pyproject.toml
uv sync

# dev group packages (pre-commit, ruff)
uv sync --dev
```

Activate your virtual environment.
```bash
source .venv/bin/activate
```
or use `uv run` before every command that uses python packages.

## Configure environment variables.
```
cp .env.example .env
```
Duplicate `.env.example` and rename it as `.env`, open `.env` file and change:
- username-> postgres
- password-> postgres
- database-> webapp
- host-> postgres_db (docker cointainer with postgres)

### Database
Use PostgreSQL through docker container.

```
docker compose -f docker/compose.dev.yaml -d
```

Migrate latest version of the database model.
```
python scripts/migration.py
```

Add an admin user for login and actions.
```
python scripts/add_admin.py
```

### Run backend server
```
uvicorn app.main:app --reload
```
it will run on localhost port 8000. SwaggerDocs [here](localhost:8000/docs)


Disclaimer: Gen AI/LLMs used for some frontend content, mainly styling and layout.

# Tools
- Backend: FastApi, SQLAlchmey, Alembic, Docker
- Authentication: passlib\[brcypt](password hashing), OAuth2, python-jose\[cryptography](JWT)
- PDF generation: Weasyprint, Jinja2
- Frontend: HTML, CSS, Javascript
- Backend-Frontend connection: StaticFiles from FastApi

# Structure
```
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 17ff0663bc3f_add_user_data.py
│       ├── 47dc6e9da235_users_table.py
│       ├── 64c4665bb6da_update.py
│       ├── 7973250a27f5_remove_password_char_limit_2.py
│       └── e56751fa3090_remove_password_char_limit.py
├── alembic.ini
├── app
│   ├── admin
│   │   ├── __init__.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── auth
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── config
│   │   ├── database.py
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── main.py
│   ├── shared
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── base.py
│   │   │   ├── __init__.py
│   │   │   └── mixin.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   └── responses.py
│   │   └── services
│   │       ├── __init__.py
│   │       └── pdf_generation.py
│   └── user
│       ├── __init__.py
│       ├── routers.py
│       ├── schemas.py
│       └── services.py
├── docker
│   ├── compose.dev.yaml
│   └── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── scripts
│   ├── add_admin.py
│   ├── migration.py
│   └── setup.py
├── static
│   ├── css
│   │   └── style.css
│   ├── html
│   │   ├── dashboard.html
│   │   └── login.html
│   └── js
│       ├── admin.js
│       ├── api.js
│       ├── auth.js
│       ├── dashboard.js
│       ├── pdf.js
│       └── profile.js
├── templates
│   ├── profile.html
│   └── users.html
└── uv.lock

20 directories, 60 files
```

