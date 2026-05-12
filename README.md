# 🧑‍💼 Employee CRUD API

A production-ready RESTful API built with **FastAPI** and **SQLite** for managing employee records. Supports full CRUD operations with filtering, pagination, and search.

---

## 🚀 Features

- **Full CRUD** — Create, Read, Update, Delete employees
- **Pagination** — Page-based navigation for large datasets
- **Filtering** — Filter by department, active status
- **Search** — Search employees by name or email
- **Validation** — Pydantic-powered input validation
- **Auto Docs** — Interactive Swagger UI at `/docs`
- **Tests** — Pytest test suite with 100% endpoint coverage

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM |
| [SQLite](https://www.sqlite.org/) | Database |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Pytest](https://pytest.org/) | Testing |

---

## 📁 Project Structure

```
employee-crud-api/
├── app/
│   ├── main.py              
│   ├── database/
│   │   └── session.py        # DB engine & session
│   ├── models/
│   │   └── employee.py       # SQLAlchemy model
│   ├── schemas/
│   │   └── employee.py       # Pydantic schemas
│   └── routers/
│       └── employees.py      # CRUD route handlers
├── tests/
│   └── test_employees.py     # Pytest test suite
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/employee-crud-api.git
cd employee-crud-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be live at **http://localhost:8000**

---

## 📖 API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### Base URL: `/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/employees/` | List all employees (paginated) |
| `POST` | `/employees/` | Create a new employee |
| `GET` | `/employees/{id}` | Get employee by ID |
| `PUT` | `/employees/{id}` | Update employee (partial ok) |
| `DELETE` | `/employees/{id}` | Delete an employee |

### Query Parameters for `GET /employees/`

| Parameter | Type | Description |
|---|---|---|
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 10, max: 100) |
| `department` | string | Filter by department name |
| `is_active` | bool | Filter by active status |
| `search` | string | Search by name or email |

---

## 📦 Employee Schema

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@company.com",
  "phone": "+1-555-0100",
  "department": "Engineering",
  "job_title": "Software Engineer",
  "salary": 75000.00,
  "is_active": true,
  "hire_date": "2024-01-15"
}
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_employees.py::test_root PASSED
tests/test_employees.py::test_health_check PASSED
tests/test_employees.py::test_create_employee PASSED
tests/test_employees.py::test_create_duplicate_employee PASSED
tests/test_employees.py::test_list_employees PASSED
tests/test_employees.py::test_get_employee PASSED
tests/test_employees.py::test_get_nonexistent_employee PASSED
tests/test_employees.py::test_update_employee PASSED
tests/test_employees.py::test_delete_employee PASSED
tests/test_employees.py::test_search_employees PASSED
tests/test_employees.py::test_filter_by_department PASSED
```

---

## 📝 Example Requests

### Create an employee

```bash
curl -X POST http://localhost:8000/api/v1/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@company.com",
    "department": "Engineering",
    "job_title": "Backend Developer",
    "salary": 90000
  }'
```

### List employees with search

```bash
curl "http://localhost:8000/api/v1/employees/?search=jane&department=Engineering"
```

### Update an employee

```bash
curl -X PUT http://localhost:8000/api/v1/employees/1 \
  -H "Content-Type: application/json" \
  -d '{"job_title": "Senior Backend Developer", "salary": 110000}'
```

### Delete an employee

```bash
curl -X DELETE http://localhost:8000/api/v1/employees/1
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
