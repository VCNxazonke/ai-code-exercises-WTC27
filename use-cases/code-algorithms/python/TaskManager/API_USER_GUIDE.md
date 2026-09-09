# Developer Usage Guide: User Registration API

## Endpoint Overview
- **HTTP Method**: `POST`
- **Path**: `/api/users/register`
- **Content-Type**: `application/json`
- **Authentication**: None required (Public registration endpoint)

---

## Request Format

### Headers
```http
POST /api/users/register HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

### JSON Body Fields
| Field Name | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `username` | String | Yes | Must be unique | Account username |
| `email` | String | Yes | Valid email syntax (`user@domain.tld`) | Account email address (lowercased automatically) |
| `password` | String | Yes | Minimum 8 characters | Account password |

---

## Code Examples

### 1. cURL
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123!"
  }'
```

### 2. Python (`requests`)
```python
import requests

url = "http://localhost:5000/api/users/register"
payload = {
    "username": "johndoe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123!"
}

response = requests.post(url, json=payload)

if response.status_code == 201:
    data = response.json()
    print("User registered:", data["user"])
else:
    print(f"Error {response.status_code}:", response.json()["message"])
```

### 3. JavaScript (`fetch`)
```javascript
async function registerUser(username, email, password) {
  try {
    const response = await fetch('http://localhost:5000/api/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('Registered successfully:', data.user);
      return data;
    } else {
      console.error(`Error (${response.status}):`, data.message);
    }
  } catch (error) {
    console.error('Network failure:', error);
  }
}
```

---

## Response Status Codes & Examples

### 201 Created (Success)
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 101,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "created_at": "2026-09-09T11:15:00.000000",
    "role": "user"
  }
}
```

### 400 Bad Request
- **Missing Required Field**:
  ```json
  {
    "error": "Missing required field",
    "message": "email is required"
  }
  ```
- **Invalid Email Format**:
  ```json
  {
    "error": "Invalid email",
    "message": "Please provide a valid email address"
  }
  ```
- **Weak Password**:
  ```json
  {
    "error": "Weak password",
    "message": "Password must be at least 8 characters long"
  }
  ```

### 409 Conflict
- **Username Taken**:
  ```json
  {
    "error": "Username taken",
    "message": "Username is already in use"
  }
  ```
- **Email Exists**:
  ```json
  {
    "error": "Email exists",
    "message": "An account with this email already exists"
  }
  ```

### 500 Internal Server Error
```json
{
  "error": "Server error",
  "message": "Failed to register user"
}
```

---

## Technical Considerations & Edge Cases
1. **Email Normalization**: The email address is converted to lowercase prior to persistence.
2. **Password Security**: Passwords are hashed using Werkzeug (`generate_password_hash`) and never stored in plaintext or returned in API responses.
3. **Email Dispatch Non-Blocking Error**: If the confirmation email fails to send, the system logs the error but still returns status `201` as the database transaction succeeds.
4. **Database Rollbacks**: Any database session error triggers an immediate `db.session.rollback()` and returns HTTP `500`.
