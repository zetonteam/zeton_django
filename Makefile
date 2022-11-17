up:
	docker-compose up

drop:
	docker-compose down -v

load_data:
	docker-compose exec web bash -c "python manage.py loaddata fixtures/*.json"

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

dbshell:
	docker-compose exec web python manage.py dbshell
