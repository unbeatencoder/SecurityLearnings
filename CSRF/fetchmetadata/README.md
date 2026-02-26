# Fetch Metadata CSRF Defense Demo

This folder demonstrates CSRF protection using Fetch Metadata request headers.

## 1) Start the victim server

From this folder (`CSRF/fetchmetadata`), run:

```bash
python3 simple_server.py
```

Victim app runs at `http://localhost:8000`.

## 2) Open the victim page

Visit:

- `http://localhost:8000/index.html`

This page sets a demo session cookie and submits transfer requests to `POST /transfer`.

## 3) Start attacker host on a different origin

In another terminal (from this same folder), run:

```bash
python3 -m http.server 9000
```

Then open:

- `http://127.0.0.1:9000/localhost.html`

Using `127.0.0.1` against victim `localhost` helps simulate cross-site/cross-origin request context.

## 4) What you should observe in server logs

For each transfer attempt, server prints Fetch Metadata headers first:

- `Sec-Fetch-Site`
- `Sec-Fetch-Mode`
- `Sec-Fetch-Dest`
- `Sec-Fetch-User`

Example log pattern:

```text
🔎 Fetch Metadata headers:
   Sec-Fetch-Site: cross-site
   Sec-Fetch-Mode: navigate
   Sec-Fetch-Dest: document
   Sec-Fetch-User: ?1
🛡️ Blocked request by Fetch Metadata policy: Cross-site state-changing requests are blocked
```

When allowed, you should instead see:

```text
💸 Transfer processed: to=..., amount=..., remaining_balance=...
```

## 5) How the defense works

`POST /transfer` now validates Fetch Metadata before processing business logic:

- Blocks if `Sec-Fetch-Site` is missing on unsafe methods.
- Blocks if `Sec-Fetch-Site` is `cross-site`.
- Blocks if `Sec-Fetch-Site` is `none` and mode is not `navigate`.
- Allows request only when Fetch Metadata policy passes, then checks session cookie and transfer input.

So even if browser sends session cookies automatically, suspicious cross-site state-changing requests are rejected with HTTP `403`.
