from typing import Type, TypeVar, Any, Dict

T = TypeVar("T")


def dict_to_dataclass(cls: Type[T], data: Dict[str, Any]) -> T:
    fieldtypes = {f.name: f.type for f in cls.__dataclass_fields__.values()}
    return cls(
        **{
            f: dict_to_dataclass(fieldtypes[f], data[f])
            if isinstance(data[f], dict)
            else data[f]
            for f in data
        }
    )
