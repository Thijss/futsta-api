"""Validators for repositories."""
from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.exceptions import AlreadyExistsError, NotFoundError

if TYPE_CHECKING:
    from app.repositories.base.repo import JsonRepository


def assert_in(asset: BaseModel, repo: "JsonRepository"):
    """Assert that an asset is in the repository."""
    if asset not in repo.assets:
        raise NotFoundError(f"{asset} does not exist")


def assert_not_in(asset: BaseModel, repo: "JsonRepository"):
    """Assert that an asset is not in the repository."""
    if asset in repo.assets:
        raise AlreadyExistsError(f"{asset} already exists")
