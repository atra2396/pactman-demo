FROM python:3.9.6-buster AS build
WORKDIR /src
COPY requirements.txt ./requirements.txt
RUN apt-get update && \
    apt-get install ruby --no-install-recommends -y && \
    gem install pact_broker-client
RUN pip install -r requirements.txt

FROM build AS accounting
CMD uvicorn --host=0.0.0.0 AccountingService.accounting_service:app

FROM build AS cart
CMD uvicorn --host=0.0.0.0 CartService.cart_service:app

FROM build AS catalog
CMD uvicorn --host=0.0.0.0 CatalogService.catalog_service:app

FROM build as inventory
CMD uvicorn --host=0.0.0.0 InventoryService.inventory_service:app

FROM build as item
CMD uvicorn --host=0.0.0.0 ItemService.item_service:app