from inspect import getmembers, isfunction, signature
from typing import Dict, Any, Callable, List

import hermes.backend.redis

cache_hermes = hermes.Hermes(hermes.backend.redis.Backend, host='localhost', db=1)


def remove_none_from_dict(dictionary: dict, remove_empty_string=False):
    for key, value in list(dictionary.items()):
        if value is None:
            del dictionary[key]
        if remove_empty_string and isinstance(value, str) and value == "":
            del dictionary[key]
        elif isinstance(value, dict):
            remove_none_from_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    remove_none_from_dict(item)

    return dictionary


def collect_handlers_functions(module) -> Dict[Any, Callable | List[Callable]]:
    functions = {}  # type: Dict[Any, Callable| List[Callable]]
    for p, c in getmembers(module, isfunction):
        for name, model_type in signature(c).parameters.items():
            if name == "command":
                functions.update({model_type.annotation: c})
                break

            if name == "message":
                functions.setdefault(model_type.annotation, []).append(c)
                break

    return functions


def parse_query_params(query_params):
    limit = 10
    page = 0
    category_id = None

    query_params_dict = {}
    for param in query_params:
        key = param[0]
        value = param[1]
        if key == 'limit' and (isinstance(value, str) and value.isdigit()) or (isinstance(value, int)):
            limit = int(value)
        elif key == 'page' and (isinstance(value, str) and value.isdigit()) or (isinstance(value, int)):
            page = int(value) * limit
        elif key == 'category':

            category_id = value
        query_params_dict[key] = value
    return query_params_dict, category_id, limit, page


def cache(ttl=None):
    def decorator(func):
        return cache_hermes(func, ttl=ttl)

    return decorator
