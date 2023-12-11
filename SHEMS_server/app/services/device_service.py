from ..db.database import Database
from sqlalchemy import text
from ..services.customer_service import get_customer_id

def get_customer_device(email):
    customer_id = get_customer_id(email)
    res = []
    return res