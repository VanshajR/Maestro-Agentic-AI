from pydantic import BaseModel, ValidationError


def validate_model(data: dict, model: type[BaseModel]):
    try:
        return model(**data)
    except ValidationError as e:
        raise e
