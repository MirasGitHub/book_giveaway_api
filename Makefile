IMAGE_NAME ?= book_giveaway_api
CONTAINER_NAME ?= book_giveaway_api_container
PORT ?= 8000


build:
	docker build -t $(IMAGE_NAME)

run:
	docker run -p 127.0.0.1:$(PORT):$(PORT) $(IMAGE_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) django-admin shell

migrations:
	docker exec -it $(CONTAINER_NAME) python manage.py makemigrations

migrate:
	docker exec -it $(CONTAINER_NAME) python manage.py migrate

createsuperuser:
	docker exec -it $(CONTAINER_NAME) python manage.py createsuperuser

populate_db:
	docker exec -it $(CONTAINER_NAME) python manage.py runscript populate_database

stop:
	docker stop $(CONTAINER_NAME)

clean:
	docker rm $(CONTAINER_NAME)
