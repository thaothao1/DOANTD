up:
	docker-compose up -d 
down:
	docker-compose down
build:
	docker-compose build
log:
	docker logs -t doantd_app_1
rm: 
	docker rm doantd_app_1
rmi:
	docker rmi doantd_app_1
into:
	docker exec -it doantd_app_1 bash
db_seed:
	alembic revision --autogenerate -m "add column categoryId for table Labels"
db_up:
	alembic upgrade head
