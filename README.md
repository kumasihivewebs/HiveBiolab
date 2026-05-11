# HiveBiolab Backend

This Django service implements the API surface that `hive-bio` reaches out to when it needs persistence or notifications. Incoming submissions are stored in Django models backed by a conventional SQL database: local SQLite for development, or a managed PostgreSQL instance on hosts like Railway, Render, or similar platforms. There is no Firebase dependency in the active backend code path.

## Getting started

1. Create a Python virtual environment (Python 3.10+) and install the pinned dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` (*keep it out of source control*) and update it with host/CORS settings plus real secrets such as `SECRET_KEY`. The file is automatically loaded by `python-decouple`.
3. Run Django migrations so the `contact`, `newsletter`, and `training` tables exist.

   ```bash
   python manage.py migrate
   ```

4. Start the dev server:

   ```bash
   python manage.py runserver
   ```

## Configuration

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django secret key (must be kept secret in production). | `django-insecure-local-only` for local dev only |
| `DEBUG` | Disable for production (`false`); `true` enables Django’s error pages locally. | `false` |
| `ALLOWED_HOSTS` | Space-separated hosts allowed to serve the API. | `127.0.0.1 localhost .onrender.com .up.railway.app api.biolab.kumasihive.com` |
| `FRONTEND_ORIGINS` | Space-separated origins that can make CORS requests. | `http://localhost:8080 http://127.0.0.1:8080 https://biolab.kumasihive.com` |
| `CSRF_TRUSTED_ORIGINS` | Origins allowed to bypass the CSRF origin check (defaults to `FRONTEND_ORIGINS`). | (see above) |
| `DATABASE_URL` | Database connection string. Use PostgreSQL in production, SQLite locally. | `sqlite:///.../db.sqlite3` |
| `DATABASE_SSL_REQUIRE` | Require SSL/TLS for the database connection. | `true` for Postgres URLs, `false` for local SQLite |
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

Use the JSON payloads below when the Vite app submits data. All endpoints accept `POST` only, return JSON, and respond with `detail` plus the created record `id`.

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

- Install from `requirements.txt`; it now includes `dj-database-url` and `psycopg` so the app can bind directly to a managed PostgreSQL instance.
- Run `python manage.py collectstatic --noinput` during build and `python manage.py migrate --noinput` before the service starts serving traffic.
- Set `DATABASE_URL` to your managed Postgres connection string. On Railway you can reference `${{Postgres.DATABASE_URL}}`; on Render use the managed Postgres connection string injected into the web service.
- Set `ALLOWED_HOSTS`, `FRONTEND_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` for your real frontend/backend domains, and keep `DEBUG=False`.
- Use `/health/` as the platform health check path.
