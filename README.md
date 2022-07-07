# Warehouse

Warehouse is the backend api for venera.

## Before doing anything

Before starting in development or production mode, please remember to fill your information in a `.env` via `.env.example`.
If you have a security bundle for cassandra, you can put it in `/private/cass-bundle.zip`.

Once done with those steps, please run migrations and table creations by running `warehouse/db/database.py`.

## Development

All you need to do to start the server is run either `./scripts/dev.bat` (for windows) or `./scripts/dev.sh` (for macOS or linux.)

Once done, you can access that server via ``https://cloud.veneralab.com:5000``.

## Production

When you want to run in production, you should run `./scripts/prod.sh`.
