from fastapi import FastAPI

# from fastapi_redoc import Redoc
from fastapi.openapi.utils import get_openapi
from app.api.endpoints import user, customer, order
from app.db.init_db import init_db

# Initialize the database
init_db()
app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(customer.router, prefix="/customer", tags=["customers"])
app.include_router(order.router, prefix="/orders", tags=["orders"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}


# Add ReDoc endpoint
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Minimal App",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
