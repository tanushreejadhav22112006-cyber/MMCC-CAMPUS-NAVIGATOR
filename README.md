# 🚀 Campus Navigator Backend

Flask REST API backend for Campus Navigator with PostgreSQL database.

---

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+

---

## 🛠️ Setup Instructions

### 1. Create PostgreSQL Database

Open PostgreSQL command line and run:
```sql
CREATE DATABASE navigator;
```

### 2. Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment

The `.env` file is already configured with:
- Database: `navigator`
- Password: `kapil123`

### 4. Initialize Database

```bash
python init_db.py
```

This creates:
- All database tables
- Default admin user (`admin@campus.edu` / `admin123`)
- 15 sample campus locations

### 5. Run the Server

```bash
python app.py
```

API available at: **http://localhost:5000**

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/admin-login` | Admin login |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password |
| GET | `/api/auth/verify-token` | Verify JWT token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/profile` | Get user profile |
| PUT | `/api/users/profile` | Update profile |
| POST | `/api/users/change-password` | Change password |
| GET | `/api/users/admin/overview` | Admin statistics |
| GET | `/api/users/admin/users` | Get all users |
| PUT | `/api/users/admin/users/<id>` | Update user |
| DELETE | `/api/users/admin/users/<id>` | Delete user |

### Locations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/locations` | Get all locations |
| GET | `/api/locations/<id>` | Get location by ID |
| POST | `/api/locations` | Create location (admin) |
| PUT | `/api/locations/<id>` | Update location (admin) |
| DELETE | `/api/locations/<id>` | Delete location (admin) |
| GET | `/api/locations/search?q=query` | Search locations |
| GET | `/api/locations/nearby?lat=x&lng=y` | Get nearby locations |
| GET | `/api/locations/types` | Get location types |
| POST | `/api/locations/<id>/save` | Save to favorites |
| GET | `/api/locations/saved` | Get saved locations |
| DELETE | `/api/locations/saved/<id>` | Remove saved location |

---

## 🔐 Default Admin Credentials

- **Email:** `admin@campus.edu`
- **Password:** `admin123`

⚠️ Change password after first login!

---

## 🧪 Test API

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"password\":\"password123\"}"
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"john@example.com\",\"password\":\"password123\"}"
```

**Get Locations:**
```bash
curl http://localhost:5000/api/locations
```

---

## 🗄️ Database Models

- **User** - User accounts with authentication
- **Location** - Campus buildings, labs, classrooms
- **LoginHistory** - User login tracking
- **SavedLocation** - User's favorite locations
- **PasswordResetToken** - Password recovery tokens

---

## 📁 Project Structure

```
backend/
├── app.py              # Flask application entry
├── config.py           # Configuration settings
├── models.py           # SQLAlchemy models
├── init_db.py          # Database initialization
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── routes/
    ├── auth.py         # Authentication routes
    ├── users.py        # User management routes
    └── locations.py    # Location CRUD routes
```

---

## 🔧 Troubleshooting

**PostgreSQL not running:**
```bash
# Windows: Start PostgreSQL service from Services
# macOS:
brew services start postgresql
# Linux:
sudo systemctl start postgresql
```

**Module not found:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Port 5000 in use:**
Change port in `app.py` or kill the process using port 5000.

---

## 📞 Support

For issues, check logs or contact the development team.

---

**Version:** 1.0.0 | **Made with ❤️ for Campus Navigator**

admin login credentials-
email-admin@gmail.com
pass-admin123
