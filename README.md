# Course Registration Portal 🎓

A simple Django-based web application for course registration, supporting both students and faculty. This system allows:
- Students to register for courses (max 2).
- Faculty to offer courses and view student registrations.
- Role-based access control.

---

## 🚀 Features

- 🧑‍🎓 Student & 🧑‍🏫 Faculty login system
- 🔐 Passwords securely stored using Django's password hashing
- 📚 Course offering & registration
- 🔄 Role detection based on email domain:
  - `@ds.study.iitm.ac.in` → Student
  - `@pod.iitm.ac.in` → Faculty
- 📊 Dashboards for students & faculty
- ⚠️ Login required

---

## 🗂️ Project Structure

course_registration/
├── core/ # App with views, models, templates
├── course_reg/ # Django project config
├── db.sqlite3 # SQLite database
├── manage.py # Django project runner
├── requirements.txt # Python dependencies
└── README.md # This file

## 🚦 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/course_registration.git
```

2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate 
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run Migrations
```bash
python manage.py migrate
```

5. Run the Development Server
```bash
python manage.py runserver
```

6. db export
```bash
pg_dump -U postgres -d coursedb -f "D:\course_reg_assignment\course_reg\coursedb.sql
```

7. create exported db
```bash
createdb -U postgres coursedb
```

8. Restore db
```bash
psql -U postgres -d coursedb -f coursedb.sql
```





   
