1. Cài lib: pip install -r requirements.txt
2. Cài môi trường ảo: python3 -m venv .venv
3. Chạy môi trường ảo: .venv/Scripts/activate
4. Chạy server: python manage.py runserver
5. Migration: python3 manage.py makemigrations [app-name]
6. Migrate to db: python3 manage.py migrate

Note: các model nằm trong models.py, api nằm trong views.py, valid dữ liệu trong serializers.py, url nằm trong urls.py, mỗi lần tạo model mới thì gõ python manage.py makemigrations để tạo migration cho models, rồi gõ python manage.py migrate để migrate.

Quy định port:
- Auth: 8000
- User: 8001
- Question: 8002
- Answer: 8003
- Review: 8004
...

username = doadmin
password = AVNS_K5SzVPk_FNY2EGlYeOZ hide
host = db-mysql-19httt6-do-user-14203209-0.b.db.ondigitalocean.com
port = 25060
database = defaultdb
sslmode = REQUIRED