from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.customer import endpoints as customerEndpoints
from app.api.order import endpoints as orderEndpoints


app = FastAPI()

app.include_router(
    customerEndpoints.router, prefix="/api/v1/customer", tags=["customers"]
)
app.include_router(orderEndpoints.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}


# Add ReDoc endpoint for the documentation
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
