# Database Migrations

This folder is reserved for database migration files.

The project is expected to use Alembic for version-controlled database migrations.

Typical workflow:

1. Initialize Alembic
2. Generate a migration
3. Apply the migration

Commands:

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head
