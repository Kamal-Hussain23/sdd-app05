# Roadmap

## Current state

The project is brand new. The file structure, tooling config, and this
constitution exist, but there is no application code yet.

## Milestone 1 — Walking skeleton

Build the thinnest end-to-end slice first so the whole loop works:

- A **customer page** shows a menu and lets the customer place an order.
- The Python server keeps orders in memory.
- A **staff page** shows new orders as they arrive.

Nothing fancy — just the shortest path from "customer orders" to "staff sees
it."

## Milestone 2 — Order management

Grow the skeleton:

- Staff can **mark an order as ready** (and maybe as completed/done).
- Status changes show up so both sides can see where an order stands.
- Maybe a small confirmation or order summary for the customer.

## Milestone 3 — Polish

Make it nicer:

- Better styling and layout.
- Quantities or multiple items per order.
- A simple order history / ticket view.

## Long-term vision

Beyond the milestones above, the project could add things like a real menu
editor or nicer ordering flow — but only if the core loop is solid first. Keep
it simple and grow one step at a time.
