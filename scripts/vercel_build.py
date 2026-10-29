"""Run safe, repeatable database preparation during a Vercel build."""

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

database_url = os.getenv("DATABASE_URL_UNPOOLED") or os.getenv("DATABASE_URL")
if not database_url:
    raise SystemExit(
        "Vercel build stopped: connect a PostgreSQL integration so DATABASE_URL is available."
    )

# Direct connections are safer for schema migrations than a transaction pooler.
os.environ["DATABASE_URL"] = database_url
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsavo_hub.settings")
os.environ.setdefault("DJANGO_DEBUG", "False")

import django  # noqa: E402
from django.core.management import call_command  # noqa: E402


django.setup()
call_command("migrate", interactive=False, verbosity=1)
call_command("seed_initial_data", verbosity=1)
