.PHONY: create-pacts
create-pacts: 
	docker-compose exec -w /src/CartService cart pytest
	docker-compose exec -w /src/CatalogService catalog pytest

CART_VERSION=1.0.0
CATALOG_VERSION=1.0.0
ACCOUNTING_VERSION=1.0.0

.PHONY: publish-pacts
publish-pacts:
	docker-compose exec -w /src/CartService cart pact-broker publish "*.json" --consumer-app-version=$(CART_VERSION)
	docker-compose exec -w /src/CatalogService catalog pact-broker publish "*.json" --consumer-app-version=$(CATALOG_VERSION)


.PHONY: verify-pacts
verify-pacts:
	docker-compose exec -w /src/AccountingService accounting pytest \
		--pact-publish-results \
		--pact-provider-name=accounting-service \
		--pact-provider-version=$(ACCOUNTING_VERSION) \
		verify_pacts.py 
	docker-compose exec -w /src/CatalogService catalog pytest \
		--pact-publish-results \
		--pact-provider-name=catalog-service \
		--pact-provider-version=$(CATALOG_VERSION) \
		verify_pacts.py 

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down