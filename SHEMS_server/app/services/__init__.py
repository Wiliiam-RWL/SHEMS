from .auth_service import check_user_credentials, register_user
from .customer_service import get_user_info, get_customer_id
from .location_service import (
    get_customer_location,
    add_location,
    modify_location,
    delete_location,
)
from .device_service import (
    get_customer_device,
    get_all_device_model,
    add_device,
    delete_device,
    update_device,
    get_event_by_device_id,
)
from .energy_service import (
    get_energy_by_customer_per_day,
    get_energy_by_customer_per_month,
    get_energy_by_device_type,
    get_energy_by_location_id,
    get_customer_energy_per_locatoin,
    get_energy_of_all_devices,
    get_energy_of_all_device_per_day,
    get_energy_by_location_device_type,
)
from .price_service import get_price_of_locations, get_price_of_each_device_type
