# django-vendor-management-system

### Follow below steps to run the assignment in local
#### Basic Setup
- Clone the repository to your local.
  ```bash
  https://github.com/rajveerbeerda/django-vendor-management-system.git
  ```
- Move inside sumtracker_assignment directory
  ```bash
  cd django-vendor-management-system
  ```
- Install Python Virtual Environment
  ```bash
  python3 -m venv venv # On MacOS
  ```
- Activate Virtual Environment
  ```bash
  source venv/bin/activate
  ```
- Upgrade pip version
  ```bash
  pip install --upgrade pip
  ```
- Install Requirements from requirements.txt
  ```bash
  pip install -r requirements.txt
  ```

Run below scripts to make model migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Create Superuser for Admin Controls
```bash
python manage.py createsuperuser
```

#### Start Application Server
- `python manage.py runserver 0.0.0.0:8000` - Start the server at 8000 port

#### Access Swagger and ReDoc
- http://localhost:8000/swagger/
- http://localhost:8000/redoc/

