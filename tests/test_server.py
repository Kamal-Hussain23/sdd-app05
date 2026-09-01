"""Tests for the cafe ordering backend server (walking skeleton)."""

import json
import logging
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from typing import cast

import pytest

import server

OK = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404


@pytest.fixture()
def server_url() -> Iterator[str]:
    """Start the server on a free port for the test, then stop it."""
    httpd, port = server.make_server(port=0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


@pytest.fixture()
def clean_orders() -> Iterator[None]:
    """Empty the in-memory orders before each test so ids are predictable."""
    server.ORDERS.clear()
    yield


def post_json(url: str, payload: object) -> tuple[int, dict[str, object]]:
    """POST a JSON payload and return (status_code, parsed_body)."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def test_health_returns_ok(server_url: str) -> None:
    """The health endpoint reports the server is up."""
    with urllib.request.urlopen(f"{server_url}/api/health") as response:
        assert response.status == OK
        body = json.load(response)
    assert body == {"status": "ok"}


def test_menu_endpoint_returns_menu(server_url: str) -> None:
    """GET /api/menu returns the in-memory menu with name and price."""
    with urllib.request.urlopen(f"{server_url}/api/menu") as response:
        assert response.status == OK
        body = json.load(response)
    assert "menu" in body
    assert len(body["menu"]) == len(server.MENU)
    for item in body["menu"]:
        assert "name" in item and "price" in item


def test_place_order_endpoint_success(server_url: str, clean_orders: None) -> None:
    """A valid order is stored and returns 201 with an order id."""
    status, body = post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    assert status == CREATED
    assert body["status"] == "received"
    assert body["order_id"] == 1
    assert len(server.ORDERS) == 1


def test_place_order_endpoint_ids_increment(server_url: str, clean_orders: None) -> None:
    """Two orders get increasing ids through the endpoint."""
    _, first = post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    _, second = post_json(f"{server_url}/api/orders", {"items": ["Tea"]})
    assert cast(int, second["order_id"]) == cast(int, first["order_id"]) + 1


def test_place_order_unknown_item_rejected(server_url: str, clean_orders: None) -> None:
    """An item not on the menu returns 400 and nothing is stored."""
    status, body = post_json(f"{server_url}/api/orders", {"items": ["Not On The Menu"]})
    assert status == BAD_REQUEST
    assert "error" in body
    assert len(server.ORDERS) == 0


def test_place_order_empty_rejected(server_url: str, clean_orders: None) -> None:
    """An empty items list returns 400 and nothing is stored."""
    status, body = post_json(f"{server_url}/api/orders", {"items": []})
    assert status == BAD_REQUEST
    assert "error" in body
    assert len(server.ORDERS) == 0


def test_place_order_missing_items_key_rejected(server_url: str, clean_orders: None) -> None:
    """A body without the 'items' key returns 400."""
    status, body = post_json(f"{server_url}/api/orders", {"menu": ["Latte"]})
    assert status == BAD_REQUEST
    assert "error" in body


def test_place_order_non_list_items_rejected(server_url: str, clean_orders: None) -> None:
    """A body where 'items' is not a list returns 400."""
    status, body = post_json(f"{server_url}/api/orders", {"items": "Latte"})
    assert status == BAD_REQUEST
    assert "error" in body


def test_get_orders_endpoint_newest_first(server_url: str, clean_orders: None) -> None:
    """GET /api/orders returns stored orders, most recent first."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    post_json(f"{server_url}/api/orders", {"items": ["Tea"]})
    with urllib.request.urlopen(f"{server_url}/api/orders") as response:
        assert response.status == OK
        body = json.load(response)
    orders_ids = [cast(int, o["order_id"]) for o in body["orders"]]
    assert orders_ids == [2, 1]


def test_update_status_endpoint_success(server_url: str, clean_orders: None) -> None:
    """A valid ready update returns 200 and the new status."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    assert status == OK
    assert body == {"order_id": 1, "status": "ready"}


def test_update_status_unknown_id_returns_404(server_url: str, clean_orders: None) -> None:
    """Updating a non-existent order returns 404 and changes nothing."""
    status, body = post_json(f"{server_url}/api/orders/999/status", {"status": "ready"})
    assert status == NOT_FOUND
    assert "error" in body


def test_update_status_non_numeric_id_returns_404(server_url: str, clean_orders: None) -> None:
    """A non-numeric id in the path returns 404."""
    status, body = post_json(f"{server_url}/api/orders/abc/status", {"status": "ready"})
    assert status == NOT_FOUND
    assert "error" in body


def test_update_status_invalid_value_returns_400(server_url: str, clean_orders: None) -> None:
    """An invalid status returns 400 and the order status is unchanged."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "flying"})
    assert status == BAD_REQUEST
    assert "error" in body
    assert "unknown status" in str(body["error"])
    assert server.ORDERS[0].status == "received"


def test_update_status_to_done_success(server_url: str, clean_orders: None) -> None:
    """A valid 'done' update returns 200 and the new status."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "done"})
    assert status == OK
    assert body == {"order_id": 1, "status": "done"}


def test_full_status_lifecycle(server_url: str, clean_orders: None) -> None:
    """An order can move received -> ready -> done."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    _, first = post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    assert first["status"] == "ready"
    _, second = post_json(f"{server_url}/api/orders/1/status", {"status": "done"})
    assert second["status"] == "done"
    assert server.ORDERS[0].status == "done"


def test_update_status_backward_done_to_ready_rejected(server_url: str, clean_orders: None) -> None:
    """Moving done -> ready is rejected and status is unchanged."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    # Move to done first.
    post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    post_json(f"{server_url}/api/orders/1/status", {"status": "done"})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    assert status == BAD_REQUEST
    assert "error" in body
    assert server.ORDERS[0].status == "done"


def test_update_status_backward_ready_to_received_rejected(
    server_url: str, clean_orders: None
) -> None:
    """Moving ready -> received is rejected and status is unchanged."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    post_json(f"{server_url}/api/orders/1/status", {"status": "ready"})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "received"})
    assert status == BAD_REQUEST
    assert "error" in body
    assert server.ORDERS[0].status == "ready"


def test_update_status_in_place_rejected(server_url: str, clean_orders: None) -> None:
    """Moving received -> received is rejected and status is unchanged."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "received"})
    assert status == BAD_REQUEST
    assert "error" in body
    assert server.ORDERS[0].status == "received"


def test_update_status_skipping_step_rejected(server_url: str, clean_orders: None) -> None:
    """Moving received -> done (skipping ready) is rejected and unchanged."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    status, body = post_json(f"{server_url}/api/orders/1/status", {"status": "done"})
    assert status == BAD_REQUEST
    assert "error" in body
    assert server.ORDERS[0].status == "received"


def test_get_single_order_endpoint_success(server_url: str, clean_orders: None) -> None:
    """GET /api/orders/<id> returns the single order."""
    post_json(f"{server_url}/api/orders", {"items": ["Latte", "Tea"]})
    with urllib.request.urlopen(f"{server_url}/api/orders/1") as response:
        assert response.status == OK
        body = json.load(response)
    assert body == {"order_id": 1, "items": ["Latte", "Tea"], "status": "received"}


def test_get_single_order_unknown_id_returns_404(server_url: str, clean_orders: None) -> None:
    """GET /api/orders/<id> with an unknown id returns 404."""
    try:
        with urllib.request.urlopen(f"{server_url}/api/orders/999") as response:
            assert response.status == OK
    except urllib.error.HTTPError as error:
        assert error.code == NOT_FOUND


def test_get_single_order_non_numeric_id_returns_404(server_url: str) -> None:
    """GET /api/orders/<id> with a non-numeric id returns 404."""
    try:
        with urllib.request.urlopen(f"{server_url}/api/orders/abc") as response:
            assert response.status == OK
    except urllib.error.HTTPError as error:
        assert error.code == NOT_FOUND


def test_staff_page_served(server_url: str) -> None:
    """GET /staff returns the staff page."""
    with urllib.request.urlopen(f"{server_url}/staff") as response:
        assert response.status == OK
        html = response.read().decode("utf-8")
    assert "Staff" in html


def test_customer_page_served(server_url: str) -> None:
    """GET / returns the customer page."""
    with urllib.request.urlopen(f"{server_url}/") as response:
        assert response.status == OK
        html = response.read().decode("utf-8")
    assert "Cafe" in html


def test_requests_are_logged(server_url: str, caplog: pytest.LogCaptureFixture) -> None:
    """Each handled request is logged with its method and path."""
    with (
        caplog.at_level(logging.INFO, logger=server.LOGGER.name),
        urllib.request.urlopen(f"{server_url}/api/health") as response,
    ):
        assert response.status == OK
    messages = [r.getMessage() for r in caplog.records]
    assert any("GET /api/health" in m for m in messages)
