# Authentication Demo

This folder contains a simple authentication demo with:

- A frontend page (`index.html`) for creating users and logging in
- A Python server (`simple_server.py`) with auth API endpoints

## Requirements

- Python 3.6+
- No external packages required

## How to Run

From the repository root (`SecurityLearnings`):

```bash
python3 "Authentication/simple_server.py"
```

You should see output like:

- `Server started at http://localhost:8000`
- `Endpoints: POST /api/register, POST /api/login`

Then open this in your browser:

- [http://localhost:8000](http://localhost:8000)

## How to Interact (UI)

On the page, there are two forms:

1. **Create User**
   - Enter a username (minimum 3 characters)
   - Enter a password (minimum 6 characters)
   - Click **Create User**

2. **Login**
   - Enter the same username/password
   - Click **Login**
   - On success, a demo session token is shown

Status messages appear at the bottom of the page for success/error responses.

## API Endpoints

### `POST /api/register`

Creates a new user in memory.

Request body (JSON):

```json
{
  "username": "alice",
  "password": "supersecret"
}
```

Success response:

```json
{
  "status": "ok",
  "message": "User 'alice' created"
}
```

### `POST /api/login`

Logs in an existing user.

Request body (JSON):

```json
{
  "username": "alice",
  "password": "supersecret"
}
```

Success response:

```json
{
  "status": "ok",
  "message": "Welcome, alice",
  "token": "..."
}
```

## Test with cURL (Optional)

Create user:

```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"supersecret"}'
```

Login:

```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"supersecret"}'
```

## Notes

- User data is stored in memory (`USERS` dictionary), so it resets when the server stops.
- This is a learning/demo app, not production-ready authentication.
