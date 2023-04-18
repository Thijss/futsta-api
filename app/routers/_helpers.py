from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from app.exceptions import ValidationError
from app.repositories.base.repo import JsonRepository


def add_or_raise_http_exception(repo: JsonRepository, asset: BaseModel, validators: list):
    """Add asset to repository"""

    try:
        repo.add(asset, validators=validators)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{"msg": str(error)}]) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{"msg": str(error)}]) from error
    return asset


def remove_or_raise_http_exception(repo: JsonRepository, asset: BaseModel, validators: list):
    """Remove asset from repository"""

    try:
        repo.remove(asset, validators=validators)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{"msg": str(error)}]) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{"msg": str(error)}]) from error
    return asset
