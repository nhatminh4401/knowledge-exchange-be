1. Cài lib: pip install -r requirements.txt
2. Cài môi trường ảo: python3 -m venv .venv
2. Chạy môi trường ảo: .venv/Scripts/activate
3. Chạy server: python manage.py runserver

Note: các model nằm trong models.py, api nằm trong views.py, valid dữ liệu trong serializers.py, url nằm trong urls.py, mỗi lần tạo model mới thì gõ python manage.py makemigrations để tạo migration cho models, rồi gõ python manage.py migrate để migrate.