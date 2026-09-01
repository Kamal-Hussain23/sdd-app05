# Order Management — Plan

This is a Red/Green TDD repo: write the tests first, watch them fail (red),
then write the code to make them pass (green). Run `python -m pytest tests/`
after each step.

## Task group 1 — Backend: status transitions (test-first)

1. Add tests to `tests/test_server.py` (Red):
   - A valid full lifecycle: `received → ready` (200) then `ready → done`
     (200), final status `done`.
   - Backward move (`done → ready`) returns `400` and leaves status `done`.
   - Backward move (`ready → received`) returns `400` and leaves status `ready`.
   - In-place move (`received → received`, or `ready → ready`) returns `400`
     and leaves the status unchanged.
   - Unknown status (`flying`) still returns `400`.
2. Update `server.py`:
   - Add `done` to `VALID_STATUSES`.
   - Replace the current "any allowed status may be set" logic with a
     **forward-only transitions contract** (e.g. an ordered `NEXT_STATUS` map
     or allowed-transitions dict) so an order can only move to the next step.
   - Use the existing `log_request` decorator (no new logging logic mixed into
     the business rule).
3. Run `python -m pytest tests/` until Green, then `ruff` and `mypy`.

## Task group 2 — Backend: single-order lookup (test-first)

4. Add tests to `tests/test_server.py` (Red):
   - `GET /api/orders/1` returns `200` with that order's `order_id`, `items`,
     and `status`.
   - `GET /api/orders/999` (unknown) returns `404`.
   - `GET /api/orders/abc` (non-numeric) returns `404`.
5. Update `server.py`:
   - Add a `get_order(order_id)` helper (reuse the existing order contract and
     `ORDERS` — DRY with `get_orders`).
   - Add the `GET /api/orders/<id>` route to `do_GET`, reusing the same id
     parsing approach as the status path.
6. Run `python -m pytest tests/` until Green, then `ruff` and `mypy`.

## Task group 3 — Frontend: customer tracking + staff done

7. Update `frontend/index.html`:
   - Add a "Track order" section: an input for the order number and a button.
   - On submit, `fetch("/api/orders/<id>")` and show the status
     (received / ready / done), or a clear message if the order is not found.
   - Keep using vanilla JS (no libraries).
8. Update `frontend/staff.html`:
   - Show the new `done` status.
   - After `ready`, offer a "Mark done" button that posts `{"status": "done"}`.
   - Keep the existing "Mark ready" behaviour for `received` orders.
9. Update `frontend/scripts/lint.js` / `test.js` only if the new content
   changes what those scripts check, so `npm run lint` and `npm test` pass.

## Task group 4 — Verification

10. Run the full suite: `pytest`, `ruff check`, `ruff format --check`,
    `mypy`, `npm run lint --prefix frontend`, `npm test --prefix frontend`.
11. Restart the server (bound to `0.0.0.0`), verify the local and public Codio
    URLs respond, and complete every item in `validation.md`.
12. Run the verifier agent for an independent per-item audit.
