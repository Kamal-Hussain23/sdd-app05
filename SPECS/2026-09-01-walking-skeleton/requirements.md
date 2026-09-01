# Walking Skeleton — Requirements

## Feature name

Walking Skeleton (Milestone 1 of the ROADMAP).

## Goal

Build the thinnest end-to-end slice of the cafe ordering system so the whole
loop works: a customer opens a page, sees the menu, places an order, and staff
see that order appear. This is the foundation we grow later features on.

## Scope — in

- A menu that lives in the Python server and is served to the customer page.
- A customer page (`index.html`) showing the menu and letting the customer
  place an order.
- A staff page (`staff.html`) showing new orders as they arrive.
- A Python HTTP server (built with the standard library only) that serves the
  pages and keeps orders in memory.
- Staff can mark an order as **ready** (the simplest status flow).
- Automated tests written first (Red/Green TDD).

## Scope — out (later milestones)

- Marking orders **done/completed** and multi-step status history (Milestone 2).
- Nicer styling, quantities, order history, confirmations (Milestone 3).
- Logins, accounts, payments, persistence. Always out of scope.

## Non-negotiable constraints

- **No database.** Orders live in memory and reset on server restart.
- **No frameworks.** Vanilla HTML/CSS/JS + Python standard library only.
- **Simple over clever.** Use the most obvious solution.
- Use contracts/schemas (dataclasses, typed models) over regexes/ad-hoc parsing.

## Data model

An **Order** has:
- `order_id` (int) — unique, assigned by the server, starting at 1.
- `items` (list of str) — item names from the menu.
- `status` (str) — starts as `"received"`; staff can change it to `"ready"`.

## API

| Method | Path                | What it does                                  |
|--------|---------------------|-----------------------------------------------|
| GET    | `/api/health`       | Health check, returns `{"status": "ok"}`      |
| GET    | `/api/menu`         | Returns the menu as JSON                      |
| POST   | `/api/orders`       | Places an order; returns the new order        |
| GET    | `/api/orders`       | Returns all orders to the staff page          |
| POST   | `/api/orders/<id>/status` | Staff marks an order ready            |
| GET    | `/` , `/index.html` | Serves the customer page                      |
| GET    | `/staff`            | Serves the staff page                         |

## Error handling

- Unknown item in an order → `400` with an error message; nothing stored.
- Empty or malformed order → `400`; nothing stored.
- Unknown order id on a status update → `404`.
- Invalid status value → `400`.
