.PHONY: help build up down logs db-shell

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build and start the stack
	docker-compose up -d --build

up: ## Start containers
	docker-compose up -d

down: ## Stop containers
	docker-compose down

logs: ## Follow logs
	docker-compose logs -f nats-logic

db-shell: ## Access TimescaleDB
	docker exec -it timescaledb psql -U postgres

clean: ## Wipe containers and volumes
	docker-compose down -v