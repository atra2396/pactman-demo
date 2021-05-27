# Consumer-Driven Contract Testing Demo

This repo is a work-in-progress demo of consumer-driven contract testing in Python using [Pactman](https://github.com/reecetech/pactman). The idea was to create several independent microservices and demonstrate how [Pact](http://pact.io) could be used to enforce contract tests between them.

Contracts can be viewed in `cart-service-catalog-service-pact.json` and `catalog-service-accounting-service-pact.json`. The pytest files that created the contracts can be found at `CartService/test_cart_service.py` and `CatalogService/test_catalog_service.py` respectively. The provider verification steps for those contracts can be found at `CatalogService/verify_pacts.py` and `AccountingService/verify_pacts.py` respectively. There is not much there because Pact simply sets up the provider's state, builds the requests from the contracts, and then executes them and verifies that the output matches.

## How to use
I don't really recommend trying to run this yet because there are still a _ton_ of kinks to iron out, and the Makefile is not even close to being finished. However, if you are truly determined to see this running right now, continue on.

I do not recommend using the docker-compose file for this yet. Here is how I've been running it:

1. Open the repo in VSCode using the included devcontainer configuration.
2. Install the python packages, and install Ruby and the pact broker CLI [as per the instructions in this repo](https://github.com/pact-foundation/pact_broker-client)
3. Export the environment variables to your terminal, you may have to do this multiple times if you switch windows often: `export $(cat .env | xargs)`
4. The contracts are already created, as mentioend above. But if you want to see how they get created, you can delete the `.json` files from the root directory and run `python -m pytest CartService/test_cart_service.py` and `python -m pytest CatalogService/test_catalog_service.py` (Yes you must include the `python -m`, I still don't understand how modules work in Python and just running `pytest` wasn't working). The json contracts should have reappeared in the root of the repository. You could also just run `python -m pytest` to generate them all at once.
5. If you started the devcontainer in step 1, the pact broker should already be running. To publish these contracts, run `pact-broker publish <contract name here>.json --consumer-app-version=1.0.0`. There are many more options you can publish with, which can be viewed in the pact broker client GitHub repo. You should see a message like this:
    ```
    Publishing cart-service/catalog-service pact to pact broker at http://pact-broker:9292
    The latest version of this pact can be accessed at the following URL:
    http://pact-broker:9292/pacts/provider/catalog-service/consumer/cart-service/latest
    ```
    If you navigate to `localhost:9292` in a web browser, you should see the new contract.
6. Verifying the contracts is a bit trickier. Here is how you would verify the Cart-Catalog contract. The instructions are the same for the Catalog-Accounting contract:
    1. Run the _provider_ service (in this case, the catalog service) in a new shell within VSCode. Note that you will probably have to export the env variables again before running it. You can start the app by running `uvicorn CatalogService.catalog_service:app`.
    2. In the first terminal window, execute the `verify_pacts.py` file _in the provider folder_ with pytest, but with a few additional arguments: `python -m pytest --pact-publish-results --pact-provider-name=catalog-service  --pact-provider-version=1.0.0 CatalogService/verify_pacts.py`. This causes pytest to pull the contract for the given `pact-provider-name` from the pact-broker (whose URL is in an environment variable), execute the `verify_pacts` tests, and publish those results back up to the broker. If you look at the pact broker in a web browser again, you should see that the contract you previously published now has a "last verified" date.