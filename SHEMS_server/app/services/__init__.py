from .auth_service import check_user_credentials, register_user
from .customer_service import get_user_info, get_customer_id
from .location_service import (
    get_customer_location,
    add_location,
    modify_location,
    delete_location,
)
from .device_service import get_customer_device, get_all_device_model, add_device, delete_device, update_device
