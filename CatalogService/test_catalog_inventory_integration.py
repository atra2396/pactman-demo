from pactman import Consumer, Provider, Pact
from CatalogService.catalog_service import AccountingFactory, order_item, OrderRequest

pact: Pact = Consumer("catalog-service").has_pact_with(Provider("inventory-service"), host_name="inventory", port=8002)

def test_create_order_when_inventory_in_stock():
    AccountingFactory.test = (True, { "price": 100 })
    request = OrderRequest(item_id=0, quantity=5)

    pact.given("item with id 0 has at least 5 units in stock") \
        .upon_receiving("Inventory update PATCH request") \
        .with_request("PATCH", "/items/0", body={ "quantity_delta": request.quantity }) \
        .will_respond_with(200)
    with pact:
        order = order_item(request)
    
    assert order.total_price == 500