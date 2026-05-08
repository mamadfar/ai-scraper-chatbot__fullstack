
.PHONY: backend client up down build help
.DEFAULT_GOAL := help

backend: 	## Start backend dev server
	$(MAKE) -C backend dev 		## -C means change to the backend directory and run the dev target

client: 	## Start client dev server
	$(MAKE) -C client dev

up: 	## Start all Docker services
	docker compose up -d

down: 	## Stop all Docker services
	docker compose down

build: 	## Build all Docker images
	docker compose build

logs: 	## Tail logs from all Docker services
	docker compose logs -f

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'