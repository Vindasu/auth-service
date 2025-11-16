# Auth Service

A Django REST API microservice for user authentication and management. This service handles user registration, login, and JWT token management for the coolest 361 group and their desktop applications.

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
- Python 3.8 or higher
- Git (optional)

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

### Example API Usage

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

## Integration Examples - Flutter/Flask/JS

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

## Database

This project uses **SQLite** by default:
- **No setup required** - Database file (`db.sqlite3`) is created automatically
- **Perfect for development** and small to medium applications
- **Easy to backup** - Just copy the `db.sqlite3` file
- **Can upgrade later** - Easy migration to PostgreSQL or MySQL when needed

## Development

### Running Tests
```bash
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

## Production Deployment

For production deployment:

1. **Change the SECRET_KEY** in `settings.py`
2. **Set DEBUG = False**
3. **Update ALLOWED_HOSTS** with your domain
4. **Configure a production database** (PostgreSQL recommended but I'll probably shop around later and configure it for all of us)
5. **Set up proper CORS origins** (remove CORS_ALLOW_ALL_ORIGINS depending on framework this might look different)
6. **Use environment variables** for sensitive settings/api keys/etc
7. **Set up HTTPS** for secure token transmission

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