from CatalogService.catalog_service import OrderRequest, order_item 
from pactman import Consumer, Provider, Pact
from CatalogService.catalog import InventoryFactory

pact: Pact = Consumer("catalog-service").has_pact_with(Provider("accounting-service"), host_name="accounting", port=8001)

def test_order_total_cost():
    InventoryFactory.test = (True, True)
    request = OrderRequest(item_id=0, quantity=3)

    pact.given("item with id 0 has price 10") \
        .upon_receiving("Accounting GET request") \
        .with_request("GET", "/items/0") \
        .will_respond_with(200, body={ "price": 10})
    with pact:
        response = order_item(request)
    
    assert 30 == response.total_price