# Instructions
Clone this repository
```
# HTTPS
git clone https://github.com/Reyozaki/simple-webapp.git

# SSH
git clone git@github.com:Reyozaki/simple-webapp.git
```

Open simple-webapp directory
```
cd simple-webapp
```

## Requirements
- Python 3.12
- uv package manager: [Github](https://github.com/astral-sh/uv)
- Docker: [Docker-desktop](https://www.docker.com/products/docker-desktop/)
- make (for Makefile)

## Installation
Install uv package manager:
```
# install using pip
pip install uv

# Mac, with homebrew
brew install uv
```

Check if make is installed, in terminal:
```
make --version
```

If not installed:
- For Windows, install from [GNUWin32](https://gnuwin32.sourceforge.net/packages/make.htm)
```
# Linux
sudo apt-get install make

# Arch
sudo pacman -S base-devel

# Mac
brew install make
```

## Regular Setup
Using make, `make help` for available commands. Configure `.env` first, instructions [below](https://github.com/Reyozaki/simple-webapp?tab=readme-ov-file#configure-environment-variables).<br> **Open Docker-desktop if available(background)**
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
- Health check — [localhost:8000/](http://localhost:8000/)
- SwaggerDocs — [localhost:8000/docs](http://localhost:8000/docs)
- Login Page — [localhost:8000/static/html/login.html](http://localhost:8000/static/html/login.html)

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
  - Profile page: Download user details in pdf.

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
# linux using bash
source .venv/bin/activate

# windows using powershell
.\\venv\\Scripts\activate.bat

# windows using bash/WSL
source venv/Scripts/activate
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
- host-> postgres (docker compose service containing postgres image)

### Database
Use PostgreSQL through docker container.

```
docker compose -f docker/compose.dev.yaml -d
```

Database Migrations
```
# migrate existing versions
python scripts/migration.py

or

(uv run) alembic upgrade head

# create a new migration file for database if schema is modified change
(uv run) alembic revision --autogenerate -m <change_title>
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
Modular monolith approach for the backend, which runs the frontend through static file mounting.
```
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── app
│   ├── admin
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── auth
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── config
│   │   ├── database.py
│   │   └── settings.py
│   ├── core
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── main.py
│   ├── shared
│   │   ├── models
│   │   │   ├── base.py
│   │   │   └── mixin.py
│   │   ├── schemas
│   │   │   └── responses.py
│   │   └── services
│   │       └── pdf_generation.py
│   └── user
│       ├── routers.py
│       ├── schemas.py
│       └── services.py
├── docker
│   ├── compose.dev.yaml
│   └── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── sample/
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

21 directories, 58 files
```
