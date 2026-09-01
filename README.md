# Cafe Ordering System

A simple web app for a cafe. Customers open the site, view the menu, and place
an order. Staff open another page and see new orders, then mark them ready.

Built with **vanilla HTML, CSS, and JavaScript** on the front, and a **Python**
server in the background. Orders stay **in memory** while the server runs — no
database.

## Getting started

Run the server, then open the site in your browser.

```
python server.py
```

The site will be served at a public URL (in Codio, look for the
`https://<hostname>-<port>.codio.io/` link the server prints).

> Currently in development — the app itself is not built yet.

## Project layout

- `SPECS/MISSION.md` — what the project is for and the non-negotiables.
- `SPECS/TECH.md` — the technology stack and engineering standards.
- `SPECS/ROADMAP.md` — the plan for building the app step by step.
- `frontend/` — the customer and staff web pages.
- `server.py` — the Python web server.
- `tests/` — automated tests.

## Conventions

- Tests are written first (Red/Green TDD) and follow a written spec.
- No frameworks, no databases — keep it simple.
