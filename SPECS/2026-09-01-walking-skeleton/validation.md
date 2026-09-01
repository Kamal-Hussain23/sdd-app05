# Walking Skeleton — Validation

This feature is **done and can be merged** when every check below passes.

## Automated checks

- [ ] `pytest` passes (all tests in `tests/` are green).
- [ ] `ruff check` passes with no errors.
- [ ] `ruff format --check` passes (code is formatted).
- [ ] `mypy` passes in strict mode.
- [ ] `npm run lint --prefix frontend` passes.
- [ ] `npm test --prefix frontend` passes.

## Functional checks

- [ ] GET `/api/health` returns `{"status": "ok"}`.
- [ ] GET `/api/menu` returns the menu with `name` and `price` for each item.
- [ ] POST `/api/orders` with a valid `items` list returns `201` and an
      `order_id`, and stores the order with status `"received"`.
- [ ] POST `/api/orders` with an unknown item, empty list, or malformed body
      returns `400` and stores nothing.
- [ ] GET `/api/orders` returns the stored orders (most recent first).
- [ ] POST `/api/orders/<id>/status` with `{"status": "ready"}` updates the
      order to `"ready"` and returns `200`.
- [ ] POST `/api/orders/<id>/status` with an unknown id returns `404`.
- [ ] POST `/api/orders/<id>/status` with an invalid status returns `400`.
- [ ] GET `/` serves the customer page.
- [ ] GET `/staff` serves the staff page.

## End-to-end walkthrough

- [ ] A customer can open `/`, see the menu, and place an order.
- [ ] A staff member can open `/staff`, see that order appear, and mark it ready.

## Note

Any difference between what was implemented and these specs must be surfaced,
discussed, and (with approval) reflected back into the specs before merge.
