# The Leonardo's Discussion Room

A full-stack secure discussion platform with a React frontend, Flask backend, MySQL database, and Nginx reverse proxy (with ModSecurity).

---

## Instructions to Run
Access the production server at https://theleonardodrhere.onthewifi.com/

For development:
1. Ensure the .env.development files in the backend, frontend and main folder are filled. Refer to .env.example to see what should be inside. Contact the developers for access to the .env.development files if required.
2. Setup Docker on your device.
3. Clone this repository. In a terminal, navigate to the main folder of the repository.
4. Use "docker-compose --env-file .env.development -f docker-compose-dev.yml up --build -d" to run the development code on Docker.
5. To stop, use "docker-compose --env-file .env.development -f docker-compose-dev.yml down"
6. Before running, use "cd .\frontend\; rm .\node_modules\; cd .." to ensure the frontend/node_modules folder is not present.

## Project Folder Structure

```
.
├── .env.development         : Environment variables for development
├── .env.example             : Sample Environment variable file.
├── .gitignore               : Specifies files/folders to ignore in git
├── docker-compose-dev.yml   : Docker Compose config for development environment
├── docker-compose-prod.yml  : Docker Compose config for production environment
├── README.md                : Main project documentation (this file)
├── .github/
│   └── workflows/
│       └── main.yml         : GitHub Actions CI/CD pipeline configuration
├── backend/                 : See Backend Folder Structure below.
├── frontend/                : See Frontend Folder Structure below.
├── nginx/
│   ├── Dockerfile           : Dockerfile for building the Nginx reverse proxy container
│   ├── nginx.conf           : Main Nginx configuration file. Sets up reverse proxying, SSL, security headers, & routing for frontend/backend.
│   └── modsecurity/         : Contains all configuration and rule files for the ModSecurity Web Application Firewall (WAF).
│       ├── crs-setup.conf   : OWASP CRS setup/configuration for ModSecurity
│       ├── modsecurity.conf : Main ModSecurity configuration file
│       ├── unicode.mapping  : Unicode mapping file for ModSecurity
│       └── rules/           : Directory containing OWASP CRS rule files and data files
├── scripts/
│   └── deploy_prod.sh       : Bash script to automate production deployment
```

## Backend Folder Structure
```
backend/
├── .dockerignore           : Files and folders to exclude from Docker builds.
├── .env.development        : Environment variable files for development environment.
├── .env.example            : Sample Environment variable file.
├── alembic.ini             : Alembic configuration for database migrations.
├── Dockerfile              : Instructions to build the backend Docker image.
├── main.py                 : Entrypoint for running the Flask app in development.
├── migrate.py              : Script to run database migrations.
├── pytest.ini              : Pytest configuration for backend tests.
├── requirements.txt        : Python dependencies for the backend.
├── run_tests.py            : Script to run all backend tests.
├── wsgi.py                 : WSGI entrypoint for production servers.
├── app/
│   ├── __init__.py         : Flask app factory and extension setup.
│   ├── db.py               : SQLAlchemy database instance.
│   ├── extensions.py       : Initialization of Flask extensions (e.g., rate limiter).
│   ├── controllers/        : Business logic for handling API requests (e.g., `post_controller.py`, `auth_controller.py`).
│   ├── interfaces/         : Abstract base classes and interfaces for services and repositories.
│   ├── models/             : SQLAlchemy ORM models for database tables (e.g., `users.py`, `posts.py`, `comments.py`, `likes.py`).
│   ├── repositories/       : Data access layer for interacting with the database. (e.g., `user_repository.py`, `post_repository.py`)
│   ├── routes/             : Flask blueprints defining API endpoints (e.g., `auth.py`, `posts.py`, `comments.py`).
│   ├── services/           : Service layer containing business logic (e.g., `post_service.py`, `profile_service.py`).
│   └── utils/              : Utility functions and helpers (e.g., validation, formatting).
├── config/
│   ├── __init__.py         : Configuration initialization logic.
│   ├── logging_config.py   : Logging configuration for the backend.
│   ├── settings.py         : Base and environment-specific settings.
│   └── environments/       : Environment-specific configuration files (e.g., `development.py`, `production.py`).
├── logs/                   : Application log files (created at runtime).
├── migrations/             : Alembic migration scripts for managing database schema changes.
└── tests/                  : Unit and integration tests for backend functionality.
```

## Frontend Folder Structure
```
frontend/
├── .babelrc                : Babel configuration for JSX/ES6 transpilation
├── .dockerignore           : Ignore rules for Docker builds
├── .env.development        : Environment variable files for development environment.
├── .env.example            : Sample Environment variable file.
├── .gitignore              : Files/folders to ignore in git
├── Dockerfile              : Dockerfile for frontend service
├── eslint.config.js        : ESLint configuration for code linting
├── index.html              : HTML entrypoint for React app
├── jest.config.js          : Jest configuration for testing
├── jest.setup.js           : Jest setup file for test environment
├── package.json            : NPM dependencies and scripts
├── vite.config.js          : Vite configuration for development/build
├── public/
│   └── leonardo.svg        : Static assets (e.g., favicon, images)
└── src/
    ├── App.css             : Global styles, imports Tailwind CSS.
    ├── App.jsx             : Main application component, sets up routing and global state.
    ├── const.js            : Centralized API route constants.
    ├── main.jsx            : Entry point, renders the app inside a router.
    ├── __tests__/          : Unit and integration tests for frontend components and pages.
    ├── components/         :Reusable React components
    │   ├── auth/           : Login, signup, and authentication-related components.
    │   ├── comments/       : Components for displaying and creating comments.
    │   ├── global/         : Shared components used across the app (e.g., NavBar, Modal).
    │   ├── home/           : Components specific to the home page (e.g., post previews).
    │   ├── posts/          : Components for creating, editing, and displaying posts (including drawing canvas).
    │   ├── profile/        : Profile modals, profile picture upload, etc.
    │   ├── totp/           : Two-factor authentication (TOTP) setup and verification.
    │   └── verify_email/   : Email verification UI components.
    ├── pages/              : Top-level React pages (routed views)
    │   ├── auth/           : Login and signup pages.
    │   ├── home/           : Home page.
    │   ├── payment_failure/: Payment failure notification page.
    │   ├── payment_success/: Payment success notification page.
    │   ├── posts/          : Post detail, create, and edit pages.
    │   └── profile/        : User profile page.
    └── utils/              : Helper functions and utilities (e.g., API helpers, rate limiting).
```