setup:
	python scripts/setup.py

server:
	python scripts/setup.py --server-only

docker-build:
	docker build -t webapp -f docker/Dockerfile . --rm
	@echo "Building image for container: webapp"

docker-down:
	docker compose -f docker/compose.dev.yaml down
	@echo "Cointaners cleaned"

docker-clean:
	docker compose -f docker/compose.dev.yaml down -v
	@echo "Containers stopped and volumes cleaned"

help:
	@echo "Commands:"
	@echo "make setup         — initial first setup of docker containers, migration, admin user and server run"
	@echo "make server        — repeat use of fastapi server running on localhost:8000"
	@echo "make docker-build  — build image from Dockerfile"
	@echo "make docker-down   — stop and clean docker containers"
	@echo "make docker-clean  — stop and clean docker cointainers and volumes (wipes database)"
