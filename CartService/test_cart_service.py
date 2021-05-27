from fastapi.exceptions import HTTPException
from CartService.cart_service import get_cart, create_cart, add_item_to_cart, AddItemRequest
from pactman import Consumer, Provider, Pact, Like

pact: Pact = Consumer('cart-service').has_pact_with(Provider('catalog-service'), host_name="catalog", port=8000) 

def test_update_cart_adds_items():
    cart_id = create_cart()
    request = AddItemRequest(item_id=0, quantity=2, cart_id=cart_id)
    pact.given("item with id 0 exists") \
        .upon_receiving("order item request") \
        .with_request("POST", "/order", body={ "item_id": request.item_id, "quantity": request.quantity}) \
        .will_respond_with(200, body={
            "total_price": Like(10)
        })
    with pact:
        add_item_to_cart(request)
    
    cart = get_cart(cart_id)
    assert 1 == len(cart.items)

    item = cart.items[0]
    assert 2 == item.item_quantity
    assert 10 == item.total_cost

def test_update_cart_when_catalog_out_of_stock():
    cart_id = create_cart()
    request = AddItemRequest(item_id=0, quantity=10, cart_id=cart_id)
    pact.given("item with if 0 exists with 0 stock") \
        .upon_receiving("order item request") \
        .with_request("POST", "/order", body={"item_id": request.item_id, "quantity": request.quantity}) \
        .will_respond_with(400)
    with pact:
        try:
            add_item_to_cart(request)
        except HTTPException as e:
            print(e)
            assert e.status_code == 400
            return
    
    assert False, "Status code 400 expected"
    
