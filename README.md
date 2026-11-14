# Gestion'aire API

A small-business operations API built with **FastAPI**, **SQLAlchemy 2**, and **Pydantic**.

Gestion'aire aims to give independent professionals and small teams one place to manage clients, projects, and day-to-day work.

## Features

- User registration and JWT authentication
- Password hashing with Argon2
- Client management (create, list, delete)
- Project management (create, list)
- Tasks attached to projects, with status and priority
- Per-user data isolation for clients and projects
- Automatic OpenAPI documentation
- Health-check endpoint
- Docker image and automated smoke test

## Tech stack

Python 3.12 · FastAPI · SQLAlchemy 2 · Pydantic 2 · SQLite · JWT · Pytest · Docker

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Quick start

1. Register at `POST /api/v1/auth/register`.
2. Log in at `POST /api/v1/auth/login` using the email as `username` and your password.
3. Click **Authorize** in Swagger UI and enter the returned bearer token.
4. Create a client with `POST /api/v1/clients`.
5. Create a project with `POST /api/v1/projects`.
6. Add tasks with `POST /api/v1/projects/{project_id}/tasks`.

## Run tests

```bash
pytest
```

## Run with Docker

```bash
docker compose up --build
```

## API overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/v1/auth/register` | Create account |
| POST | `/api/v1/auth/login` | Get access token |
| GET | `/api/v1/auth/me` | Current user |
| GET / POST | `/api/v1/clients` | List / create clients |
| DELETE | `/api/v1/clients/{id}` | Delete a client |
| GET / POST | `/api/v1/projects` | List / create projects |
| GET / POST | `/api/v1/projects/{id}/tasks` | List / create project tasks |

## Project status

Early-stage MVP. The API is a foundation for a broader business-management product. It is not yet intended for production use with sensitive business data.

## Roadmap

- [ ] Alembic database migrations
- [ ] Update endpoints and pagination
- [ ] Team invitations and role-based permissions
- [ ] Frontend dashboard
- [ ] PostgreSQL deployment profile
- [ ] CI workflow for linting and tests

## Contributing

Issues and pull requests are welcome. For substantial changes, please open an issue first to discuss the proposal.

## License

MIT. See [LICENSE](LICENSE).
