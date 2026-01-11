## How to run locally

Instructions below:

```
pip install pipenv
git clone <repository-url>
cd <project-folder>
pipenv install
export FLASK_APP=wsgi_local.py
pipenv run flask db upgrade
pipenv run python run.py
```

### How to deploy on PythonAnywhere (PA)

#### Step 1: Upload your files to PythonAnywhere
- Log in to PA
- Go to Files tab.
- pload entire project folder, keeping structure: app/, instance/, requirements.txt, wsgi.py, etc.

#### Step 2: Set up your virtualenv on PA
- Go to Consoles → start a Bash console.
- Create and activate virtualenv:

```bash
python3.10 -m venv ~/postplaton/venv
source ~/postplaton/venv/bin/activate
pip install -r ~/postplaton/requirements.txt
```
#### Step 3: Configure your Web App on PA
- Go to Web tab → Add a new web app.
- Choose: Manual configuration Python 3.10
- Source code: `/home/yourusername/postplaton/`
- Working directory: `/home/yourusername/postplaton/`
- Virtualenv: `/home/yourusername/postplaton/venv/'
- Static files: `/home/yourusername/postplaton/app/static`

#### Step 4: Configure WSGI file
- Edit `/var/www/postplaton_pythonanywhere_com_wsgi.py`

#### Step 6: Updating your app later
Whenever you want to update your app:
- Upload new/modified files to `/home/yourusername/postplaton/`.
- Install any new packages in virtualenv:
```bash
source ~/postplaton/venv/bin/activate
pip install -r ~/postplaton/requirements.txt
```
- Reload the web app from Web tab.

Database notes:

- SQLite DB (instance/events.db) is live. Do not overwrite it unless you want to reset it.
- For migrations, you can either Use flask db upgrade via Bash console (e.g.`reset_password.py`) Or manually update the database file locally and upload:

```bash
flask db migrate -m "Add EventResources table"
flask db upgrade
```

#### Step 7: Optionally: environmental variables
If you want to avoid hardcoding secrets, open your WSGI file and set: `os.environ['SECRET_KEY'] = 'super_secret_here'`

Or use a .env file and python-dotenv, but remember to pip install python-dotenv in your virtualenv.

### How to dmigrate the database
After updating the database file events.db there are a ferw steps to migrate the database:
```
pipenv run flask db migrate -m "Update..."
pipenv run flask db upgrade
sqlite3 instance/events.db "select count(*) from event;"
```
