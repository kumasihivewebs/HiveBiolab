# HiveBiolab Backend

This Django service implements the API surface that `hive-bio` reaches out to when it needs persistence or notifications. Incoming submissions are stored in Django models backed by PostgreSQL. The local and server Docker setup runs Postgres as the `db` service; managed hosts can still use a `DATABASE_URL`. There is no Firebase dependency in the active backend code path.

## Getting started

1. Create a Python virtual environment (Python 3.10+) and install the pinned dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` (*keep it out of source control*) and update it with host/CORS settings plus real secrets such as `SECRET_KEY`. The file is automatically loaded by `python-decouple`.
3. Run Postgres and the API with Docker Compose:

   ```bash
   docker compose up -d --build
   ```

   The Postgres container creates the database named by `DB_NAME` the first time its volume is initialized. The API container waits for Postgres, runs migrations, then starts Gunicorn on port `8001`.

4. For non-Docker development, start a local Postgres instance using the same `DB_*` variables, then run Django migrations so the `contact`, `newsletter`, and `training` tables exist.

   ```bash
   python manage.py migrate
   ```

5. Start the dev server:

   ```bash
   python manage.py runserver
   ```

## Configuration

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django secret key (must be kept secret in production). | `django-insecure-local-only` for local dev only |
| `DEBUG` | Disable for production (`false`); `true` enables Django’s error pages locally. | `false` |
| `ALLOWED_HOSTS` | Space-separated hosts allowed to serve the API. | `127.0.0.1 localhost biolab-api.kumasihive.com` |
| `FRONTEND_ORIGINS` | Space-separated origins that can make CORS requests. | `http://localhost:8080 http://127.0.0.1:8080 https://biolab.kumasihive.com` |
| `CSRF_TRUSTED_ORIGINS` | Origins allowed to bypass the CSRF origin check (defaults to `FRONTEND_ORIGINS`). | (see above) |
| `DB_NAME` | PostgreSQL database name used by Docker Compose. | `biolab` |
| `DB_USER` | PostgreSQL username used by Docker Compose. | `africaosh` |
| `DB_PASSWORD` | PostgreSQL password used by Docker Compose. Required in `.env`. | unset |
| `DB_HOST` | PostgreSQL host. Use `db` inside Docker Compose. | `db` |
| `DB_PORT` | PostgreSQL port. | `5432` |
| `DATABASE_URL` | Optional managed/external PostgreSQL connection string. When set, it overrides the `DB_*` values. | unset |
| `DATABASE_SSL_REQUIRE` | Require SSL/TLS for `DATABASE_URL` connections. | `false` |
| `DATABASE_CONN_MAX_AGE` | Persistent connection lifetime in seconds. | `600` |
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS in production. | `true` |
| `USE_X_FORWARDED_HOST` | Trust forwarded host headers from the platform proxy. | `true` |

`python-decouple` automatically loads the `.env` file when Django boots, so any env var you place there is visible to the settings module.

## Environment file

- Copy `.env.example` to `.env` and populate it with sensible host, CORS, and database values plus secrets such as `SECRET_KEY`. Keep that file out of version control.
- Each `manage.py` invocation and deployed container reads the same environment variables through `python-decouple`.

## Stored data

- `ContactMessage` stores incoming contact forms (name, email, subject, message, optional organization) plus metadata.
- `NewsletterSubscriber` stores subscription requests (email, name, source) and metadata.
- `TrainingRegistration` captures training interest (name, email, phone, program, optional background/goals) and metadata.
- Metadata includes headers such as `ip_address`, `user_agent`, `referrer`, and `accept_language`, and every record has `created_at`.

## API endpoints

Use the JSON payloads below when the Vite app reads page content or submits data. All endpoints return JSON. Form endpoints respond with `detail` plus the created record `id`.

### `GET /health/`

Response:

```json
{
  "status": "ok",
  "database": "ok"
}
```

### `POST /api/newsletter/subscribe/`

Payload:

```json
{
  "email": "researcher@hive.com",
  "name": "Kwaku Mensah",
  "source": "homepage"
}
```

Response:

```json
{
  "detail": "Subscription received. We'll keep you posted!",
  "subscription_id": 1
}
```

### `POST /api/contact/`

Payload:

```json
{
  "name": "Amina Adom",
  "email": "amina@example.com",
  "subject": "Training inquiry",
  "message": "Interested in the molecular biology workshop."
}
```

Response:

```json
{
  "detail": "Thanks for reaching out! We will respond as soon as possible.",
  "message_id": 1
}
```

### `GET /api/contact/`

Response:

```json
{
  "page": {
    "title": "Contact",
    "contact": {
      "email": "biolab@kumasihive.com",
      "location": "Kumasi Hive, Kumasi, Ghana"
    },
    "inquiryTypes": ["Training inquiry", "Research collaboration"]
  }
}
```

### `GET /api/projects/`

Response:

```json
{
  "page": {
    "title": "Projects"
  },
  "projects": [
    {
      "id": "ecb4osh",
      "slug": "ecb4osh-project",
      "title": "ECB4OSH Project"
    }
  ]
}
```

### `GET /api/projects/<slug>/`

Response:

```json
{
  "project": {
    "id": "ecb4osh",
    "slug": "ecb4osh-project",
    "title": "ECB4OSH Project"
  }
}
```

### `GET /api/training/`

Response:

```json
{
  "page": {
    "title": "Training"
  },
  "programs": [
    {
      "id": "training-microbiology",
      "slug": "microbiology",
      "title": "Microbiology Training"
    }
  ]
}
```

### `GET /api/training/programs/`

Response:

```json
{
  "programs": [
    {
      "id": "training-microbiology",
      "slug": "microbiology",
      "title": "Microbiology Training"
    }
  ]
}
```

### `GET /api/training/programs/<slug>/`

Response:

```json
{
  "program": {
    "id": "training-molecular-biology",
    "slug": "molecular-biology",
    "title": "Molecular Biology & Genetic Engineering"
  }
}
```

### `POST /api/training/register/`

Payload:

```json
{
  "full_name": "Fred Boateng",
  "email": "fred@hive.org",
  "program": "Bioinformatics & Data Analysis",
  "phone": "+233501234567",
  "experience": "Python scripting, basic genomics",
  "goals": "Build pipelines for AMR tracking"
}
```

Response:

```json
{
  "detail": "Registration received. Our team will reach out with next steps.",
  "registration_id": 1
}
```

## Testing

```
python manage.py test
```

## Deployment notes

- Install from `requirements.txt`; it includes `dj-database-url` and `psycopg` so the app can bind to Docker Postgres or a managed PostgreSQL instance.
- Run `python manage.py collectstatic --noinput` during build and `python manage.py migrate --noinput` before the service starts serving traffic.
- For Docker on your own server, set the `DB_*` values in `.env` and run `docker compose up -d --build`. For a managed database, set `DATABASE_URL` instead.
- Set `ALLOWED_HOSTS`, `FRONTEND_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` for your real frontend/backend domains, and keep `DEBUG=False`.
- Use `/health/` as the platform health check path.
