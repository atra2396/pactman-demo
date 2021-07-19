# Consumer-Driven Contract Testing Demo

This repo is a work-in-progress demo of consumer-driven contract testing in Python using [Pactman](https://github.com/reecetech/pactman). The idea was to create several independent microservices and demonstrate how [Pact](http://pact.io) could be used to enforce contract tests between them.

- Contracts can be viewed in `ExamplePacts/cart-service-catalog-service-pact.json` and `ExamplePacts/catalog-service-accounting-service-pact.json`. 
- The pytest files that created the contracts can be found at `CartService/test_cart_service.py` and `CatalogService/test_catalog_service.py` respectively. 
- The provider verification steps for those contracts can be found at `CatalogService/verify_pacts.py` and `AccountingService/verify_pacts.py` respectively. There is not much there because Pact simply sets up the provider's state, builds the requests from the contracts, and then executes them and verifies that the output matches.

## How to use

There is a `Makefile` included that demonstrates the standard workflow one would use when creating new pacts and publishing them to the broker. In order to run these examples, you must be able to run `make` and `docker-compose`.
1. Run `make up`. This will start the five services (Accounting, Cart, Catalog, Inventory, Item) in their own containers (to simulate several disparate microservices running independently of each other), as well as the pact-broker server.
2. Run `make create-pacts`. This will create the pact files in each container for their contracts against the other services that they integrate with. Note that since Docker mounts each of the `XXXService` folders to the respective service's container, you should be able to see these pact files created in your local filesystem (i.e. you will not need to inspect the docker containers to see what the output is). 
3. Run `make publish-pacts`. This will publish the consumer pacts created in the previous step to the pact broker. At this point, you should be able to visit `localhost:9292` and see that there are several new pacts that do not yet have a "Last verified" date. For both publishing and verifying pacts, you can change the consumer/provider verison by passing in `[SERVICE]_VERSION=[new version]` to the `make` command. For example, if you wanted to publish pacts with the Cart service's consumer version to be 1.1.0 and the Catalog service's consumer version to be 1.2.1, you would do `make publish-pacts CART_VERSION=1.1.0 CATALOG_VERSION=1.2.1`.
4. Run `make verify-pacts`. This will test the provider's views of the pacts in the previous step. Now in the pact broker (again at `localhost:9292`), you should see that the pacts previously published now have green "Last verified" dates. Hooray!
5. Each container runs via `uvicorn` with the `--reload` flag, so any changes you make to the APIs should be captured on the respective container in realtime. You can add new endpoints, connections, tests, etc. and see how they affect the output without having to spin everything down and back up again.
6. When you are finished, run `make down` to spin down the services and remove the containers. There are no persistent volumes at this time, so the pact broker will lose its state when you run this command.

## TODOs

- The current provider state setup is pretty bad, and not easy to understand. A better way which would more accurately reflect a _real_ application would be to give each service its own SQLite database or something along those lines.
- A more comprehensive suite of tests to demonstrate more of Pactman's API surface.
- Better comments to illustrate what's going on so a reader would not need to continuously flip from this repo to the Pactman repo's docs