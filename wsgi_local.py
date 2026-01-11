import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("FLASK_ENV", "development")
os.environ.setdefault("SECRET_KEY", "dev-key")

INSTANCE_PATH = os.path.join(PROJECT_ROOT, "instance")
os.makedirs(INSTANCE_PATH, exist_ok=True)

from app import create_app

application = create_app(instance_path=INSTANCE_PATH)
