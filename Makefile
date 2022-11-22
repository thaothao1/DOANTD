up:
	docker-compose up -d 
down:
	docker-compose down
log:
	docker logs -t web_doan_app_1
rm: 
	docker rm web_doan_app_1
rmi:
	docker rmi web_doan_app
into:
	docker exec -it web_doan_app_1 bash
db_seed:
	alembic revision --autogenerate -m "name 1"
db_up:
	alembic upgrade head