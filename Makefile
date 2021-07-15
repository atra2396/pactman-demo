.PHONY: create-pacts
create-pacts: 
	docker-compose exec -w /src/CartService cart pytest
	docker-compose exec -w /src/CatalogService catalog pytest

.PHONY: verify-pacts
verify-pacts:
	docker-compose exec accounting pactman-verifier

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down