import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db

# Use an in-memory SQLite DB for tests
TEST_DATABASE_URL = "sqlite:///./test_employees.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

SAMPLE_EMPLOYEE = {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@company.com",
    "phone": "+1-555-0101",
    "department": "Engineering",
    "job_title": "Backend Developer",
    "salary": 90000.00,
    "is_active": True,
    "hire_date": "2023-06-01",
}


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_employee():
    response = client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == SAMPLE_EMPLOYEE["email"]
    assert data["id"] is not None


def test_create_duplicate_employee():
    client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    response = client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    assert response.status_code == 400


def test_list_employees():
    client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    response = client.get("/api/v1/employees/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["employees"]) == 1


def test_get_employee():
    created = client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE).json()
    response = client.get(f"/api/v1/employees/{created['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == SAMPLE_EMPLOYEE["email"]


def test_get_nonexistent_employee():
    response = client.get("/api/v1/employees/9999")
    assert response.status_code == 404


def test_update_employee():
    created = client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE).json()
    response = client.put(
        f"/api/v1/employees/{created['id']}",
        json={"job_title": "Senior Backend Developer", "salary": 110000.00},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Senior Backend Developer"
    assert data["salary"] == 110000.00


def test_delete_employee():
    created = client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE).json()
    response = client.delete(f"/api/v1/employees/{created['id']}")
    assert response.status_code == 204
    # Verify deleted
    get_response = client.get(f"/api/v1/employees/{created['id']}")
    assert get_response.status_code == 404


def test_search_employees():
    client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    response = client.get("/api/v1/employees/?search=jane")
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_filter_by_department():
    client.post("/api/v1/employees/", json=SAMPLE_EMPLOYEE)
    response = client.get("/api/v1/employees/?department=Engineering")
    assert response.status_code == 200
    assert response.json()["total"] == 1
