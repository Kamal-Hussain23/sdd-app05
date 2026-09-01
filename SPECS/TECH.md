# Tech

## Stack

- **Backend:** Python using a lightweight HTTP server. The server serves the
  pages and handles the orders.
- **Frontend:** Vanilla HTML, CSS, and JavaScript. No React, no frameworks.
- **Data:** Kept in memory in Python while the server runs (a list of orders).
  No database, no SQL, no saving to disk.

## Architecture

One Python server with two pages:

- A **customer** page to view the menu and place orders.
- A **staff** page to see orders and mark them ready.

The server keeps orders in a shared in-memory structure so both pages see the
same data while it is running.

## Directory structure

```
sdd-app05/
├── server.py          # the Python web server
├── frontend/          # HTML, CSS, and JS files
│   ├── index.html     # customer page
│   ├── staff.html     # staff page
│   └── package.json   # frontend tooling (lint/test scripts)
├── tests/             # pytest tests
├── SPECS/             # mission, tech, roadmap, and feature specs
└── pyproject.toml     # Python tooling config
```

## Engineering standards

- **Red/Green TDD.** Write a failing test first, watch it fail (red), then
  write the minimal code to make it pass (green).
- **Spec-driven development.** All work starts from a written spec
  (requirements/plan/validation) before writing code.
- **Strict typing.** Type checks are on; type-safety is not traded away for
  convenience.
- **DRY.** Don't repeat yourself — extract shared code instead of copying.
- **Simple over complex.** Prefer the simplest solution that works.
- **Pre-commit hooks.** ruff, mypy, and pytest run before every commit.

## Outside the box

- No React, no other libraries or frameworks.
- No database, SQL, or storage on disk.
