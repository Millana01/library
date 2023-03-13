from typing import Any, Union


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Union[dict, Any]:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
