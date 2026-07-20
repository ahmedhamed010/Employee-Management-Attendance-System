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
| POST | `/accounts/auth/register/` | Register new user | Public |
| POST | `/accounts/auth/login/` | Login | Public |
| POST | `/accounts/auth/logout/` | Logout | Auth |
| POST | `/accounts/auth/refresh/` | Refresh token | Public |
| GET | `/accounts/auth/profile/` | Get profile | Auth |
| PATCH | `/accounts/auth/profile/` | Update profile | Auth |
| DELETE | `/accounts/auth/profile/` | Deactivate account | Auth |
| POST | `/accounts/auth/change-password/` | Change password | Auth |

### Role Management
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/accounts/admin/users/` | List all users | Admin, HR |
| PATCH | `/accounts/admin/users/<id>/role/` | Assign role | Admin |

### Employees
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/employees/employees/` | List employees | Admin, HR |
| POST | `/employees/employees/` | Create employee | Admin, HR |
| GET | `/employees/employees/search/` | Search employees | Admin, HR |
| GET | `/employees/employees/<id>/` | Get employee | Admin, HR |
| PATCH | `/employees/employees/<id>/` | Update employee | Admin, HR |
| DELETE | `/employees/employees/<id>/` | Delete employee | Admin, HR |

### Departments
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/departments/departments/` | List departments | Admin, HR |
| POST | `/departments/departments/` | Create department | Admin, HR |
| GET | `/departments/departments/<id>/` | Get department | Admin, HR |
| PATCH | `/departments/departments/<id>/` | Update department | Admin, HR |
| DELETE | `/departments/departments/<id>/` | Delete department | Admin, HR |

### Attendance
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/attendance/attendance/` | List records | Admin, HR |
| POST | `/attendance/attendance/` | Create record | Admin, HR |
| GET | `/attendance/attendance/me/` | My attendance | Auth |
| POST | `/attendance/attendance/check-in/` | Check in | Auth |
| POST | `/attendance/attendance/check-out/` | Check out | Auth |
| GET | `/attendance/attendance/<id>/` | Get record | Admin, HR |
| PATCH | `/attendance/attendance/<id>/` | Update record | Admin, HR |
| DELETE | `/attendance/attendance/<id>/` | Delete record | Admin, HR |

### Leave Management
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/leaves/leaves/` | List leave requests | Admin, HR = All / Others = Own |
| POST | `/leaves/leaves/` | Create leave request | Auth |
| GET | `/leaves/leaves/<id>/` | Get leave request | Auth |
| PATCH | `/leaves/leaves/<id>/` | Update leave request | Owner (pending only) |
| DELETE | `/leaves/leaves/<id>/` | Delete leave request | Owner (pending only) |
| PATCH | `/leaves/leaves/<id>/manager-approval/` | Manager approve/reject | Manager |
| PATCH | `/leaves/leaves/<id>/hr-approval/` | HR approve/reject | Admin, HR |
| PATCH | `/leaves/leaves/<id>/cancel/` | Cancel request | Owner |

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
