from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, Manager


def get_object_or_none(manager: Manager, *args, **kwargs) -> Optional[Model]:
    """
    Similar to the Manager.get method, but return None instead of raising an error.
    """

    try:
        return manager.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return None
