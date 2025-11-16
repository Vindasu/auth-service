# Auth Service

A Django REST API microservice for user authentication and management. This service handles user registration, login, and JWT token management for the coolest 361 group and their desktop applications.

## Communication Contract 

### How to REQUEST Data from This Microservice

**Base URL:** `http://127.0.0.1:8000`

```python
# Example: Register new user
import requests
response = requests.post(
    'http://127.0.0.1:8000/auth/register/',
    json={
        'username': 'your_username',
        'email': 'user@example.com', 
        'password': 'secure_password',
        'password_confirm': 'secure_password'
    },
    headers={'Content-Type': 'application/json'}
)

# Example: Login with username OR email
response = requests.post(
    'http://127.0.0.1:8000/auth/login/',
    json={
        'login': 'username_or_email@example.com',  # Can be either username or email currently, will probably switch to username only later.
        'password': 'secure_password'
    },
    headers={'Content-Type': 'application/json'}
)

# Example: Get user profile (requires JWT token)
response = requests.get(
    'http://127.0.0.1:8000/auth/user/',
    headers={
        'Authorization': 'Bearer YOUR_JWT_ACCESS_TOKEN',
        'Content-Type': 'application/json'
    }
)
```

### How to RECEIVE Data from This Microservice

```python
# Registration Response
if response.status_code == 201:
    data = response.json()
    access_token = data['access']      # JWT access token (1 hour)
    refresh_token = data['refresh']    # JWT refresh token (7 days) 
    user_info = data['user']          # User profile data
    print(f"User created: {user_info['username']}")
else:
    errors = response.json()  # Validation errors

# Login Response 
if response.status_code == 200:
    data = response.json()
    access_token = data['access']      # Use for authenticated requests
    refresh_token = data['refresh']    # Use to get new access tokens
    user_data = data['user']
    print(f"Login successful for: {user_data['username']}")
else:
    print("Login failed:", response.json())
```

## Features

- **Dual Login Support**: Users can login with either username OR email
- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **User Registration**: Create new user accounts with validation
- **Profile Management**: Update user information
- **Password Management**: Secure password change functionality
- **SQLite Database**: Built-in database (no setup required - but might move to something better later)
- **CORS Enabled**: Ready for Flutter/Flask/etc desktop app integration
- **Admin Interface**: Django admin panel for user management (coolest django feature imo)

### Prerequisites
- Python 3.14 (we're using the latest now)
- Django 5.2.8+ (required for Python 3.14 compatibility and earlier versions won't work)
- Git (optional but please use if making changes) 

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   git clone <your-repo-url>
   cd auth-service
   ```

2. **Create a Virtual Environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # On Mac/Linux  
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   ```bash
   # Create database tables (SQLite file will be created automatically if everything went well (pls))
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create an Admin User (Optional)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   
   The API will be available at: `http://127.0.0.1:8000/`

### Communication Flow

**UML sequence:**
1. **Register:** Client → POST /auth/register/ → API → Database → JWT tokens → Response
2. **Login:** Client → POST /auth/login/ → API → Authenticate → JWT tokens → Response  
3. **Get Profile:** Client → GET /auth/user/ → API → Verify token → Database → Response

## API Endpoints - IMPORTANT

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register a new user account |
| POST | `/auth/login/` | Login with username/email and password |
| POST | `/auth/token/refresh/` | Refresh JWT access token |
| GET | `/auth/user/` | Get current user information |
| PUT | `/auth/user/` | Update user profile |
| POST | `/auth/change-password/` | Change user password |

### Example API Usage (Streamlined version)

#### 1. Register a New User
```http
POST /auth/register/
Content-Type: application/json

{
    "username": "jo_doe",
    "email": "dontbanjo@pls.com",
    "password": "redemption!",
    "password_confirm": "redemption!",
    "first_name": "Jo",
    "last_name": "Sephine"
}
```

#### 2. Login (with username OR email)
```http
POST /auth/login/
Content-Type: application/json

{
    "login": "mojojojo",  // Can be username OR email
    "password": "redemption!"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", // arbitrary token keyboard spam don't reference this.
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johmojojojo",
        "email": "dontbanjo@pls.com",
        "first_name": "Jo",
        "last_name": "Sephine"
    }
}
```

#### 3. Access Protected Endpoints
Add the JWT token to your requests:
```http
GET /auth/user/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Test Program

**File:** `test_auth_service.py` - Complete test program for Sprint 2.6

```bash
python test_auth_service.py
```

**What it tests:**
- Service connectivity check
- User registration via API
- Login with username
- Login with email (dual login capability)
- Authenticated profile retrieval  
- JWT token refresh

**Sample Output:**
```
AUTH SERVICE MICROSERVICE TEST PROGRAM
CS 361 - Sprint 2.6 Implementation

REQUEST: POST /auth/register/
RESPONSE: 201 {"access": "jwt_token", "user": {...}}
User registration successful!

REQUEST: POST /auth/login/  
RESPONSE: 200 {"access": "jwt_token", "user": {...}}
Login with username successful!
```

Above shows how other microservices can communicate with the auth service!

## Integration Examples - Flutter/Flask/JS/Logan I'll add yours later!

### Flutter Integration
```dart
// Login API call (Flutter)
final response = await http.post(Uri.parse('http://127.0.0.1:8000/auth/login/'),
  headers: {'Content-Type': 'application/json'},
  body: json.encode({'login': 'username_or_email', 'password': 'password'}));
```

### Flask Integration  
```python
# Login API call (Flask/Python)
import requests
response = requests.post('http://127.0.0.1:8000/auth/login/', 
  json={'login': 'username_or_email', 'password': 'password'})
```

### JavaScript Integration
```javascript
// Login API call (JavaScript/Web)
const response = await fetch('http://127.0.0.1:8000/auth/login/', {
  method: 'POST', headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({login: 'username_or_email', password: 'password'})
});
```

**All return JWT tokens:** `{access: "token...", refresh: "token...", user: {...}}`

## Security Features

- **Password Validation**: Minimum 8 characters with complexity requirements
- **JWT Tokens**: Secure, stateless authentication
- **Token Rotation**: Refresh tokens are rotated for enhanced security
- **CORS Protection**: Configured for your specific Flutter app domains
- **Input Validation**: All API inputs are validated and sanitized
- **SQL Injection Protection**: Django ORM provides automatic protection

## Database (will update later)

This project uses **SQLite** by default because it's built in to Django and works fine for testing:
- **No setup required** - Database file (`db.sqlite3`) is created automatically
- **Works 'good enough' for development** and small to medium applications but again I'll probably upgrade soon.
- **Easy to backup** - Just copy the `db.sqlite3` file
- **Will upgrade later** - Easy migration to PostgreSQL or MySQL when needed

## Development

### Running Tests
```bash
# CS 361 Assignment Test Program
python test_auth_service.py

# Django Unit Tests (will add more later)
python manage.py test
```

### Accessing Admin Panel 
1. Make sure you created a superuser account: `python manage.py createsuperuser`
2. Start the server: `python manage.py runserver`
3. Visit: `http://127.0.0.1:8000/admin/`

### Making Database Changes
When you modify models:
```bash
python manage.py makemigrations
python manage.py migrate
```


## Dependencies

- **Django 4.2+**: Web framework
- **Django REST Framework**: API framework
- **SimpleJWT**: JWT authentication - might upgrade later. 
- **django-cors-headers**: CORS support
- **python-dotenv**: Environment variable management

## If anything breaks or isn't working:

1. **Ask Alex** I may have missed something
2. **Check the server logs** in your terminal
2. **Verify your virtual environment** is activated
3. **Make sure all dependencies** are installed: `pip install -r requirements.txt` 
(I always forget this ^ and it's helpful to have a script that does it for you if you can't remember)
4. **Check database migrations** are up to date: `python manage.py migrate`
5. **Verify the server is running** on `http://127.0.0.1:8000/`

## Next Steps (maybe next sprint if we have time?)

After getting the basic auth service running:

1. **Test with your app** - Update the auth page to call the api.
2. **Add password reset** functionality (email-based) - might do this on next sprint if we need it.
3. **Implement email verification** for new users - stretch goal
4. **Add user roles/permissions** for now we are all admins and role heirarchy can be implemented later.
5. **Set up proper logging** I haven't figured out if this should go to a text file but usually I manage this in a VRM but we're using
a SQL equivalent so I'll have to look into this.
6. **Configure production database** when ready to deploy let me know your preferred deployment location. 

## Future Production/Deployment considerations:

1. **Change the SECRET_KEY** in `settings.py`
2. **Set DEBUG = False**
3. **Update ALLOWED_HOSTS** with your domain
4. **Configure a production database** (PostgreSQL recommended but I'll probably shop around later and configure it for all of us)
5. **Set up proper CORS origins** (remove CORS_ALLOW_ALL_ORIGINS depending on framework this might look different)
6. **Use environment variables** for sensitive settings/api keys/etc
7. **Set up HTTPS** for secure token transmission