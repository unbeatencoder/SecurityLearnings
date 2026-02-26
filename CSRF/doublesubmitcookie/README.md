# CSRF Double Submit Cookie Demo

This folder demonstrates the **double submit cookie** CSRF defense pattern using a static token for learning.

## 1) Start the victim server

From the `CSRF/doublesubmitcookie` directory, run:

```bash
python3 simple_server.py
```

This starts the victim app at `http://localhost:8000`.

## 2) Open the victim page first

Visit:

- `http://localhost:8000/index.html`

On this page load, server sets:

- `session=victim123`
- `csrf_token=demo-fixed-csrf-token-12345`

The page JavaScript reads `csrf_token` from cookie and fills the hidden form field.

## 3) Start a second server for attacker page

In a separate terminal, from the same `CSRF/doublesubmitcookie` directory, run:

```bash
python3 -m http.server 9000
```

This hosts files at `http://127.0.0.1:9000`.

## 4) Open attacker page

Visit:

- `http://127.0.0.1:9000/localhost.html`

This origin is different from `localhost:8000`, so it simulates a cross-site request.

## 5) Trigger forged request

Submit from `localhost.html` to:

- `http://localhost:8000/transfer`

Then check the victim server logs.

## 6) Expected observations with double submit cookie

When request is sent from attacker page:

- Browser may send `session` and `csrf_token` cookies to victim server.
- Attacker form does not know and cannot reliably provide matching `csrf_token` body value.
- Server compares `csrf_token` in request body vs `csrf_token` cookie.
- If values are missing or different, response is `403`:
  - `{"status":"error","message":"Forbidden: invalid or missing double-submit CSRF token"}`
- Transfer is rejected.

When form is submitted from `index.html`:

- Hidden field is populated from cookie, so body token matches cookie token.
- Server accepts request and responds with `200`.

## Key observation

Double submit cookie does not require server-side CSRF token storage. It relies on a value in cookie being echoed back in the request body/header and validated for equality.
