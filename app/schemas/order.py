from pydantic import BaseModel


class Order(BaseModel):
    description: str

    class Config:
        from_attributes = True
