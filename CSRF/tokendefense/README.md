# CSRF Demo Walkthrough

This folder contains a deliberately vulnerable CSRF demo.

## 1) Start the victim server

From the `CSRF` directory, run:

```bash
python3 simple_server.py
```

This starts the victim app at `http://localhost:8000`.

## 2) Open the vulnerable page

Visit:

- `http://localhost:8000/index.html`

This page issues a demo session cookie and has a transfer form that posts to `POST /transfer`.

## 3) Start a second server for the attacker page

In a separate terminal, from the same `CSRF` directory, run:

```bash
python3 -m http.server 9000
```

This hosts files at `http://0.0.0.0:9000` (reachable locally via `127.0.0.1`).

## 4) Open attacker page using 127.0.0.1

Visit:

- `http://127.0.0.1:9000/localhost.html`

Using `127.0.0.1` (instead of `localhost`) makes the host visibly different from the victim host in the URL, which is useful when demonstrating cross-origin behavior.

## 5) Trigger the CSRF action

Click the link/button on `localhost.html` to submit the forged request to:

- `http://localhost:8000/transfer`

Then check the victim server terminal logs for the transfer result.

## 6) Expected observations with synchronizer token protection

When you trigger the forged request from `localhost.html`, you should observe:

- The request still reaches `POST /transfer` (the browser can submit cross-origin forms).
- The demo session cookie may still be sent, so the request can look authenticated.
- The attacker form does **not** include `csrf_token`, so the server rejects it.
- Response should be `403` with JSON:
  - `{"status":"error","message":"Forbidden: invalid or missing CSRF token"}`
- No transfer is processed, so account balance/transfer history should remain unchanged.

For comparison, submitting the form from `index.html` should include the expected token and succeed with `200`, which demonstrates why synchronizer tokens prevent blind cross-site form submissions from changing state.
