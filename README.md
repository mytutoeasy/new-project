# Student Django Project

A modern Django starter project for students featuring:

- **PostgreSQL** (with SQLite fallback)
- **Django REST Framework** + **JWT Authentication**
- **Docker** + docker-compose
- Full sample app: Students, Courses, Enrollments, Assignments, Submissions
- Advanced admin interface
- Environment-based configuration

## Features

### Models
| Model | Description |
|-------|-------------|
| **Student** | Profile linked to Django User (student ID, contact, photo) |
| **Course** | Courses with level, credits, instructor, capacity |
| **Enrollment** | Student ↔ Course with status & grade |
| **Assignment** | Course assignments with due dates |
| **Submission** | Student submissions with score & feedback |

### API Endpoints
```
POST   /api/auth/token/          → Obtain JWT (username + password)
POST   /api/auth/token/refresh/  → Refresh JWT

GET/POST     /api/students/
GET/PUT/PATCH/DELETE /api/students/{id}/

GET/POST     /api/courses/
GET/PUT/...  /api/courses/{id}/
GET          /api/courses/{id}/enrollments/

GET/POST     /api/enrollments/
GET/POST     /api/assignments/
GET/POST     /api/submissions/
```

Browsable API available at `/api/` when authenticated.

---

## Quick Start (Docker – Recommended)

```bash
# 1. Clone
git clone https://github.com/mytutoeasy/new-project.git
cd new-project

# 2. Start everything
docker compose up --build

# 3. Create superuser (in another terminal)
docker compose exec web python manage.py createsuperuser
```

App runs at: **http://localhost:8000**  
Admin: **http://localhost:8000/admin/**  
API: **http://localhost:8000/api/**

---

## Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Use SQLite
cp .env.example .env
# Edit .env and set: DATABASE_URL=sqlite:///db.sqlite3

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## PostgreSQL (local without Docker)

1. Install PostgreSQL and create a database
2. Copy `.env.example` → `.env`
3. Set `DATABASE_URL=postgres://user:password@localhost:5432/student_db`
4. Run migrations

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `True` | Debug mode |
| `SECRET_KEY` | insecure | Django secret key |
| `ALLOWED_HOSTS` | localhost,127.0.0.1 | Allowed hosts |
| `DATABASE_URL` | sqlite | Full database URL |

---

## Project Structure

```
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── .env.example
├── student_project/
│   ├── settings.py          # Advanced settings (environ + DRF + JWT)
│   ├── urls.py
│   └── ...
└── students/
    ├── models.py            # Student, Course, Enrollment, Assignment, Submission
    ├── admin.py
    └── api/
        ├── serializers.py
        ├── views.py
        └── urls.py
```

---

## Next Steps for Students

1. Explore the models in `/admin/`
2. Test the API with the browsable interface or Postman/Insomnia
3. Add custom permissions (e.g. students can only see their own enrollments)
4. Add Celery for background tasks (email notifications)
5. Add HTMX or a React frontend
6. Deploy to Render / Railway / Fly.io

Happy coding! 🚀
