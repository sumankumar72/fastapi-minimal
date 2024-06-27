from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_orders():
    return [{"order_id": 1}, {"order_id": 2}]
