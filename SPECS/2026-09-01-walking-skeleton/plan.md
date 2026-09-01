# Walking Skeleton — Plan

This is a Red/Green TDD repo: write the tests first, watch them fail (red),
then write the code to make them pass (green).

## Task group 1 — Project scaffolding

1. Create a `.gitignore` so cache folders (`__pycache__`, `.pytest_cache`,
   `.mypy_cache`, `.ruff_cache`) and `frontend/node_modules` are not committed.
2. Create the `tests/` folder for pytest (the `pyproject.toml` already points
   `testpaths` at `tests`).

## Task group 2 — Backend contracts (tests first)

3. Write `tests/test_server.py` — tests for the data model, the ordering logic,
   and the HTTP endpoints (menu, place order, list orders, update status, and
   the customer/staff pages). This is the **Red** step — the module does not
   exist yet, so the tests fail.
4. Create `server.py` implementing:
   - Dataclass contracts: `Item` and `Order`.
   - In-memory `MENU` and `ORDERS`.
   - Business functions: `place_order`, `get_orders`, `update_order_status`.
   - A logging decorator so request handling stays separate from logging.
   - The HTTP handler with the routes from `requirements.md`.
   - A `make_server(port=0)` helper so tests can start the server on a free
     port (also lets us bind to `0.0.0.0` for the public URL).
5. Run the tests until **Green**. Run `ruff` and `mypy` and fix issues.

## Task group 3 — Frontend pages

6. Create `frontend/index.html` — the customer page: shows the menu (loaded
   from `/api/menu` via JS) and a form to place an order.
7. Create `frontend/staff.html` — the staff page: shows orders (from
   `/api/orders`) and a button to mark each one ready.
8. Create `frontend/package.json` with `scripts.lint` and `scripts.test` so the
   pre-commit hooks (`npm run lint --prefix frontend` and
   `npm test --prefix frontend`) have something to run.
9. Add a little JS/CSS so the pages are usable and simple (vanilla, inline or
   small, per project conventions).

## Task group 4 — Verification

10. Run the full suite: `pytest`, `ruff check`, `ruff format --check`,
    `mypy`, and the frontend lint/test scripts.
11. Serve the site, verify it responds on the local port and the public Codio
    URL, then confirm every item in `validation.md`.
