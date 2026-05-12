from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine
from app.models.employee import Employee
from app.routers.employees import router as employee_router

# Create all database tables on startup
Employee.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee CRUD API",
    description=(
        "A RESTful API for managing employee records. "
        "Supports full CRUD operations with filtering, pagination, and search."
    ),
    version="1.0.0",
    contact={
        "name": "Employee API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Employee CRUD API is running.", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
