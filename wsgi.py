import sys
import os

# ----------------------------
# 1. Add project folder to sys.path
# ----------------------------
project_home = "/home/postPlaton/postpaton"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ----------------------------
# 2. Set environment variables
# ----------------------------
# Optional: set Flask environment variables
os.environ.setdefault("FLASK_ENV", "production")
# Secret key (can be configured on PA in Web tab -> Environment Variables)
os.environ.setdefault("SECRET_KEY", "dev-key")

# ----------------------------
# 3. Ensure instance folder exists
# ----------------------------
instance_path = os.path.join(project_home, "instance")
os.makedirs(instance_path, exist_ok=True)

# ----------------------------
# 4. Import Flask app factory
# ----------------------------
from app import create_app

# ----------------------------
# 5. Create the app
# ----------------------------
application = create_app()
