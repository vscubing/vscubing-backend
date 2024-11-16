import ulid
from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(
    *,
    fields: dict,
    data: dict | None = None,
    **kwargs,
):
    serializer_class = create_serializer_class(
        name=('S' + str(ulid.new())),
        fields=fields,
    )

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
