# Employee Management & Attendance System

A Django REST Framework API for managing employees, departments, attendance, and leave requests.

---

## Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **Database:** PostgreSQL / SQLite
- **Other:** django-filter, Pillow

---

## Project Structure

```
project/
│
├── config/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                # User management & authentication
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
│
├── employees/               # Employee profiles
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   └── urls.py
│
├── departments/             # Department management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── attendance/              # Attendance tracking
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
└── leaves/                  # Leave management
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/employee-management.git
cd employee-management

# 2. Create virtual environment
python -m venv env
source env/bin/activate        # Linux/Mac
env\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
TIME_ZONE=Africa/Cairo
```

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/register/` | Register new user | Public |
| POST | `/api/auth/login/` | Login | Public |
| POST | `/api/auth/logout/` | Logout | Auth |
| POST | `/api/auth/refresh/` | Refresh token | Public |
| GET | `/api/auth/profile/` | Get profile | Auth |
| PATCH | `/api/auth/profile/` | Update profile | Auth |
| DELETE | `/api/auth/profile/` | Deactivate account | Auth |
| POST | `/api/auth/change-password/` | Change password | Auth |

### Role Management
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/admin/users/` | List all users | Admin, HR |
| PATCH | `/api/admin/users/<id>/role/` | Assign role | Admin |

### Employees
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/employees/` | List employees | Admin, HR |
| POST | `/api/employees/` | Create employee | Admin, HR |
| GET | `/api/employees/search/` | Search employees | Admin, HR |
| GET | `/api/employees/<id>/` | Get employee | Admin, HR |
| PATCH | `/api/employees/<id>/` | Update employee | Admin, HR |
| DELETE | `/api/employees/<id>/` | Delete employee | Admin, HR |

### Departments
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/departments/` | List departments | Admin, HR |
| POST | `/api/departments/` | Create department | Admin, HR |
| GET | `/api/departments/<id>/` | Get department | Admin, HR |
| PATCH | `/api/departments/<id>/` | Update department | Admin, HR |
| DELETE | `/api/departments/<id>/` | Delete department | Admin, HR |

### Attendance
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/attendance/` | List records | Admin, HR |
| POST | `/api/attendance/` | Create record | Admin, HR |
| GET | `/api/attendance/me/` | My attendance | Auth |
| POST | `/api/attendance/check-in/` | Check in | Auth |
| POST | `/api/attendance/check-out/` | Check out | Auth |
| GET | `/api/attendance/<id>/` | Get record | Admin, HR |
| PATCH | `/api/attendance/<id>/` | Update record | Admin, HR |
| DELETE | `/api/attendance/<id>/` | Delete record | Admin, HR |

### Leave Management
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/leaves/` | List leave requests | Admin, HR = All / Others = Own |
| POST | `/api/leaves/` | Create leave request | Auth |
| GET | `/api/leaves/<id>/` | Get leave request | Auth |
| PATCH | `/api/leaves/<id>/` | Update leave request | Owner (pending only) |
| DELETE | `/api/leaves/<id>/` | Delete leave request | Owner (pending only) |
| PATCH | `/api/leaves/<id>/manager-approval/` | Manager approve/reject | Manager |
| PATCH | `/api/leaves/<id>/hr-approval/` | HR approve/reject | Admin, HR |
| PATCH | `/api/leaves/<id>/cancel/` | Cancel request | Owner |

---

## Roles & Permissions

| Role | Description |
|------|-------------|
| `admin` | Full access to everything |
| `hr` | Manage employees, attendance, and leaves |
| `manager` | Approve/reject leave requests |
| `employee` | View own data, check-in/out, request leaves |

---

## Leave Approval Workflow

```
Employee submits request  →  status: Pending
        ↓
Manager approves          →  status: Manager Approved
        ↓
HR approves               →  status: Approved
```

Any step can be rejected → status: `Rejected`
Employee can cancel → status: `Cancelled` (if pending or manager_approved)

---

## Attendance Logic

- **Check-in before 9:15 AM** → status: `Present`
- **Check-in after 9:15 AM** → status: `Late`
- One record per employee per day
- Check-out calculates working hours automatically

---

## Employee Search

```bash
# Search by name
GET /api/employees/search/?search=ahmed

# Filter by department
GET /api/employees/search/?department=engineering

# Filter by status
GET /api/employees/search/?status=active

# Filter by salary range
GET /api/employees/search/?salary_min=5000&salary_max=10000

# Ordering
GET /api/employees/search/?ordering=-salary

# Pagination
GET /api/employees/search/?page=1&page_size=10
```

---

## Authentication

All protected endpoints require a Bearer token in the header:

```
Authorization: Bearer <access_token>
```

Tokens are obtained from `/api/auth/login/` and can be refreshed via `/api/auth/refresh/`.

---

## Requirements

```
Django>=5.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-filter>=24.0
Pillow>=10.0
python-dotenv>=1.0
```
