# Order Management — Validation

This feature is **done and can be merged** when every check below passes.

## Automated checks

- [ ] `python -m pytest tests/` passes (all tests green).
- [ ] `python -m ruff check .` passes with no errors.
- [ ] `python -m ruff format --check .` passes.
- [ ] `python -m mypy .` passes in strict mode.
- [ ] `npm run lint --prefix frontend` passes.
- [ ] `npm test --prefix frontend` passes.

## Functional checks — status lifecycle

- [ ] A new order starts at `received`.
- [ ] `POST /api/orders/<id>/status` with `{"status": "ready"}` returns `200`
      and the order becomes `ready`.
- [ ] `POST /api/orders/<id>/status` with `{"status": "done"}` returns `200`
      and the order becomes `done`.
- [ ] A backward move (`done → ready` or `ready → received`) returns `400` and
      the status is unchanged.
- [ ] An in-place move (`received → received`) returns `400` and the status is
      unchanged.
- [ ] An unknown status value (e.g. `flying`) returns `400` and the status is
      unchanged.
- [ ] Updating with an unknown or non-numeric id returns `404`.

## Functional checks — order lookup

- [ ] `GET /api/orders/<id>` returns `200` with `order_id`, `items`, and
      `status` for a valid order.
- [ ] `GET /api/orders/<id>` returns `404` for an unknown id.
- [ ] `GET /api/orders/<id>` returns `404` for a non-numeric id.

## Functional checks — regression (walking skeleton still works)

- [ ] `GET /api/health`, `GET /api/menu`, `POST /api/orders`,
      `GET /api/orders` (list), `GET /`, `GET /staff` all still behave as
      defined in the walking skeleton spec.

## End-to-end walkthrough

- [ ] A customer opens `/`, places an order, and can look it up in the
      "Track order" box, seeing status `received`.
- [ ] Staff opens `/staff`, marks the order `ready`, then `done`.
- [ ] The customer re-tracks the order and sees the updated status; the staff
      page shows `done`.

## Note

Any difference between what was implemented and these specs (or the
constitution in SPECS/) must be surfaced, discussed, and — with approval —
reflected back into the specs before merge.
