.PHONY: pytest
pytest: 
	docker-compose exec accounting pytest AccountingService/
	docker-compose exec cart pytest CartService/
	docker-compose exec catalog pytest CatalogService/
	docker-compose exec inventory pytest InventoryService/
	docker-compose exec item pytest ItemService/

.PHONY: verify-pacts
verify-pacts:
	docker-compose exec accounting pactman-verifier

.PHONY: up
up:
	docker-compose up --build