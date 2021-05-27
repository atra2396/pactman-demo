FROM python:3.9.4 AS build
WORKDIR /src
COPY requirements.txt ./requirements.txt
COPY __init__.py ./__init__.py
RUN pip install -r requirements.txt

FROM build AS accounting
COPY AccountingService/ AccountingService/
CMD uvicorn --host=0.0.0.0 AccountingService.accounting_service:app

FROM build AS cart
COPY CartService/ CartService/
CMD uvicorn --host=0.0.0.0 CartService.cart_service:app

FROM build AS catalog
COPY CatalogService/ CatalogService/
CMD uvicorn --host=0.0.0.0 CatalogService.catalog_service:app

FROM build as inventory
COPY InventoryService/ InventoryService/
CMD uvicorn --host=0.0.0.0 InventoryService.inventory_service:app

FROM build as item
COPY ItemService/ ItemService/
CMD uvicorn --host=0.0.0.0 ItemService.item_service:app