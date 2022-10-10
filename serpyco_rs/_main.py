from typing import Any, TypeVar, Generic

import orjson

from ._describe import describe_type
from ._impl import make_encoder
from ._json_schema import ValicoValidator, to_json_schema

T = TypeVar("T", bound=Any)


class Serializer(Generic[T]):

    def __init__(self, t: type[T]) -> None:
        type_info = describe_type(t)
        self._encoder = make_encoder(type_info)
        self._validator = ValicoValidator(to_json_schema(type_info).dump())

    def dump(self, value: T) -> Any:
        return self._encoder.dump(value)

    def load(self, data: Any, validate: bool = True) -> T:
        if validate:
            self._validator.validate(data)
        return self._encoder.load(data)

    def load_json(self, data: str, validate: bool = True) -> T:
        if validate:
            self._validator.validate_json(data)
        return self._encoder.load(orjson.loads(data))
