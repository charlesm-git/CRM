import re
from sqlalchemy import inspect


def object_formatter(obj):
    mapper = inspect(obj.__class__)
    columns = [
        col.key for col in mapper.attrs if col.key not in mapper.relationships
    ]
    relationships = [rel.key for rel in mapper.relationships]

    data = []

    for column in columns:
        value = getattr(obj, column, "")
        data.append([column, value])

    for relationship in relationships:
        value = getattr(obj, relationship, None)
        # If the relationship is a list
        if isinstance(value, list) and value:
            data.append([relationship, [str(line) for line in value]])
            continue
        data.append([relationship, str(value)])
    return data
