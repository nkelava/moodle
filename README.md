# Moodle (SkillUp)

A small course and enrollment management system built with Django for a university class. Students sign up, browse courses and track their enrollments semester by semester. Staff (professors) can edit courses and manage student enrollments. Administrators manage everything, including user accounts.

The app's UI is branded **SkillUp**. It is a class project rather than a production system. Settings are development defaults, and validation is kept minimal on purpose.

## Features

- **Email-based accounts.** A custom user model (`users.CustomUsers`) logs in with email instead of a username, and email matching is case-insensitive.
- **Roles and study status.** Each user has a role (`student` or `professor`) and a status (`none`, `full time` or `part time`).
- **Course catalogue.** Each course has a name, a unique course code, a curriculum, ECTS credits, a semester for full-time and for part-time study, and an optional/mandatory flag.
- **Enrollments.** Courses can be enrolled, marked as passed or removed for each student. Enrollments are grouped by semester: 6 semesters for full-time students and 8 for part-time.
- **Permission-aware UI.** What each user sees depends on their account flags:

| Action | Student | Staff (`is_staff`) | Admin (`is_admin`) |
| --- | :---: | :---: | :---: |
| View courses and own profile | ✓ | ✓ | ✓ |
| Enroll in courses and update own enrollments | ✓ | | |
| Edit courses | | ✓ | ✓ |
| Create and delete courses | | | ✓ |
| View students and manage any student's enrollments | | ✓ | ✓ |
| Register new students or professors | | | ✓ |

## Tech stack

- Python 3 and Django 2.2.8
- SQLite (`src/db.sqlite3`, created on the first migration)
- Django templates styled with Bootstrap 4 and jQuery, both loaded from CDNs

## Prerequisites

- **Python 3.8 or 3.9.** Django 2.2 does not support newer Python versions.
- `pip` and `venv`

## Getting started

```bash
git clone https://github.com/nkelava/moodle.git
cd moodle

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install Django==2.2.8
```

> `requirements.txt` pins the full environment the project was developed in. That environment includes several MySQL packages (`mysql`, `mysqlclient`, `mysql-connector-python`) and scraping libraries that the app never imports. On a fresh machine, `pip install -r requirements.txt` usually fails while building `mysql`/`mysqlclient`. Django is the only dependency the app needs to run.

Create the database, an admin account, and start the development server:

```bash
cd src
python manage.py migrate
python manage.py createsuperuser   # prompts for email and password
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with your new account. The Django admin is at http://127.0.0.1:8000/admin/.

### Fix the static files path

`src/moodle/settings.py` points `STATICFILES_DIRS` to an absolute Windows path from the original author's machine:

```python
STATICFILES_DIRS = [ "D:\ProjDev\Python\Moodle\Moodle\src\static",
]
```

The app still runs without changing this, but the CSS and images will not load. Point the setting at the project's own `static` folder:

```python
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## Usage

1. **Admin.** Sign in with the superuser account. From **Users** you can add students and professors. From **Courses** you can add, edit and delete courses.
2. **Students.** Anyone can create a student account from the **Register** button on the login page. Under **Enrollments**, students can enroll in available courses and see their enrolled and passed courses grouped by semester.
3. **Staff.** Give a professor staff access by ticking *staff status* on their user in `/admin/`. Staff get a **Students** page where they can open a student's enrollments, enroll them in courses, mark courses as passed and remove enrollments. They can also edit courses.

### Main routes

| Path | Purpose |
| --- | --- |
| `/`, `/login/` | Log in |
| `/register/` | Create an account |
| `/index/` | Home page after login |
| `/courses/` | Course list |
| `/create_course/`, `/edit_course/<id>`, `/delete_course/<id>` | Course management |
| `/users/` | Student and professor list |
| `/user_profile/` | Current user's profile |
| `/student_enrollments/<student_id>` | A student's enrollments by semester |
| `/enroll/…`, `/course_passed/…`, `/remove_enrollment/…` | Enrollment actions (`<course_id>/<student_id>`) |
| `/admin/` | Django admin |

## Project structure

```text
moodle/
├── requirements.txt        # Pinned packages from the original dev environment
└── src/
    ├── manage.py           # Django management entry point
    ├── db.sqbpro           # DB Browser for SQLite project file (optional tooling)
    ├── moodle/             # Project package: settings, root URLconf, WSGI
    ├── main/               # Login, logout, registration, home page, base layout and navbar
    ├── users/              # Custom email-based user model, roles/status enums, auth backend, user pages
    ├── courses/            # Course model, form and CRUD views
    ├── enrollments/        # Enrollment model and enroll / pass / remove views
    └── static/             # CSS and images
```

Each app follows the standard Django layout: `models.py`, `views.py`, `urls.py`, `forms.py` and `admin.py`, plus a `templates/` and a `migrations/` folder.

## Configuration

The project does not read any environment variables or `.env` file. All configuration lives in `src/moodle/settings.py`:

| Setting | Value | Note |
| --- | --- | --- |
| `DEBUG` | `True` | Development only |
| `SECRET_KEY` | Hard-coded | Replace it before deploying anywhere |
| `ALLOWED_HOSTS` | `[]` | Add your host if you are not running on localhost |
| `DATABASES` | SQLite at `src/db.sqlite3` | |
| `AUTH_USER_MODEL` | `users.CustomUsers` | |
| `AUTHENTICATION_BACKENDS` | `AllowAllUsersModelBackend`, `users.backends.CaseInsensitiveModelBackend` | Case-insensitive email login |
| `STATICFILES_DIRS` | Absolute Windows path | See [Fix the static files path](#fix-the-static-files-path) |

## Status

This is a finished class assignment that is no longer actively developed. Some edge cases, such as error handling on invalid course forms, are not fully implemented.
