# Order Management — Requirements

## Feature name

Order Management (Milestone 2 of the ROADMAP).

## Goal

Grow the walking skeleton so both customers and staff can see where an order
stands. Two things make this happen:

1. Orders can move through a full lifecycle: **received → ready → done**,
   moving only forward (staff cannot undo a step).
2. A customer can look up their own order by its number and see its current
   status — so status changes show up on both sides, not just the staff page.

## Scope — in

- Extend the status lifecycle to `received → ready → done` (keeping the
  existing `received` and `ready`, adding `done`).
- Enforce **forward-only** transitions via a contract (map of allowed moves).
- A new endpoint to look up a single order: `GET /api/orders/<id>`.
- A **"Track order"** box on the customer page where a customer enters an
  order number and sees its status.
- The staff page shows the `done` step so staff can finish an order.
- Automated tests written first (Red/Green TDD).

## Scope — out (later milestones)

- Richer order summary / ticket view, quantities (Milestone 3).
- Order history / real menu editor (long-term).
- Logins, accounts, payments, persistence. Always out of scope.

## Non-negotiable constraints

- **No database.** Orders live in memory and reset on server restart.
- **No frameworks.** Vanilla HTML/CSS/JS + Python standard library only.
- **Simple over clever.** Prefer the obvious solution.
- Use contracts/schemas (dataclasses, an explicit transitions map) over
  ad-hoc logic or regexes.
- **Backward compatible (confirmed):** keep and extend the existing
  `received` / `ready` behavior and existing tests. Don't rework old code
  unless required.

## Status lifecycle (contract)

An order starts at **received**. Staff may move it forward one step at a time:

| From      | To     |
|-----------|--------|
| received  | ready  |
| ready     | done   |

- Moving **backward** (e.g. `done → ready`, `ready → received`) is rejected
  with `400`.
- Moving **in place** (e.g. `received → received`) is rejected with `400`.
- Setting an **unknown** status (e.g. `flying`) is rejected with `400`.
- In all rejected cases the order's status is left unchanged.

## API

| Method | Path                  | What it does                                      |
|--------|-----------------------|---------------------------------------------------|
| GET    | `/api/orders/<id>`    | Returns one order (order_id, items, status)       |
| POST   | `/api/orders/<id>/status` | Moves an order forward one status step        |

- `GET /api/orders/<id>` with a valid id returns `200` and
  `{"order_id": ..., "items": [...], "status": "..."}`.
- `GET /api/orders/<id>` with an unknown or non-numeric id returns `404`.
- Existing endpoints (`/api/orders` list, `/api/menu`, `/api/health`,
  placing orders, serving pages) keep working unchanged.

## Data model

An **Order** keeps its fields from the walking skeleton:

- `order_id` (int) — unique, starts at 1.
- `items` (list of str) — item names from the menu.
- `status` (str) — one of `received`, `ready`, `done`.

## Error handling

- Backward or in-place status move → `400` with a clear error; status unchanged.
- Unknown status value → `400`.
- Unknown or non-numeric order id (lookup or status update) → `404`.
