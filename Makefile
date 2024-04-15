superuser:
	docker-compose down -v
	docker-compose up -d
	sleep 4
	python manage.py migrate
	python manage.py createsuperuser

run: superuser
	python manage.py import_data data_all/import.csv --admin_id 1
	python manage.py runserver
