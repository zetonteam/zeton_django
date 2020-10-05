up:
	docker-compose up

drop:
	docker-compose down -v

load_data:
	docker-compose exec web bash -c "python manage.py loaddata fixtures/*.json"

