"""Application configuration."""

import os
import secrets
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent


def _load_dotenv() -> None:
	"""Load key=value pairs from .env into process environment.

	Existing environment variables take precedence over .env values.
	"""
	env_path = BASE_DIR / ".env"
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#"):
			continue

		if line.startswith("export "):
			line = line[len("export "):].strip()

		if "=" not in line:
			continue

		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip()
		if not key:
			continue

		if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
			value = value[1:-1]

		os.environ.setdefault(key, value)


_load_dotenv()

DATABASE: Path = BASE_DIR / "finance.db"

# SECRET_KEY must be set via environment variable in production.
# A random key is generated per-process for development (sessions won't survive restarts).
SECRET_KEY: str = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# Configurable person names (defaults for a couple finance app)
PERSON1_NAME: str = os.environ.get("PERSON1_NAME", "Person 1")
PERSON2_NAME: str = os.environ.get("PERSON2_NAME", "Person 2")
