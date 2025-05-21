from .crud_task import get, get_multi, get_multi_by_family, create, update, delete
from .crud_shopping import shopping_list, shopping_item

task = type('Task', (), {
    'get': get,
    'get_multi': get_multi,
    'get_multi_by_family': get_multi_by_family,
    'create': create,
    'update': update,
    'delete': delete
})

__all__ = ["task", "shopping_list", "shopping_item"] 