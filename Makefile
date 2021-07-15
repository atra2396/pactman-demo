.PHONY: create-pacts
create-pacts: 
	docker-compose exec -w /src/CartService cart pytest
	docker-compose exec -w /src/CatalogService catalog pytest

.PHONY: publish-pacts
publish-pacts:
	docker-compose exec -w /src/CartService cart pact-broker publish "*.json" --consumer-app-version=1.0.0
	docker-compose exec -w /src/CatalogService catalog pact-broker publish "*.json" --consumer-app-version=1.0.0

.PHONY: verify-pacts
verify-pacts:
	docker-compose exec -w /src/AccountingService accounting pytest \
		--pact-publish-results \
		--pact-provider-name=accounting-service \
		--pact-provider-version=1.0.0 \
		verify_pacts.py 
	docker-compose exec -w /src/CatalogService catalog pytest \
		--pact-publish-results \
		--pact-provider-name=catalog-service \
		--pact-provider-version=1.0.0 \
		verify_pacts.py 

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down