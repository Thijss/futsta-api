"""Test the base repository class."""
import os
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from app.exceptions import NotFoundError
from app.repositories.base.repo import JsonRepository


class _MyAsset(BaseModel):
    name: str


class _MyJsonRepo(JsonRepository):
    """Dummy class for testing the base repository class"""

    assets: list[_MyAsset] = []

    class Config:
        """Pydantic config"""

        json_file_name = "test.json"


def test_save_and_load_with_asset(tmp_path):
    """Test loading a json file."""
    repo = _MyJsonRepo()
    repo.assets = [_MyAsset(name="test")]

    with patch.dict(os.environ, {"LOCAL_ACCESS": "true", "local_assets_dir": str(tmp_path)}):
        repo.save()
        repo = _MyJsonRepo.load()
    assert repo.assets == [_MyAsset(name="test")]


def test_add_and_remove_asset():
    """Test loading a json file."""
    repo = _MyJsonRepo()
    my_asset = _MyAsset(name="test")

    repo.add(my_asset)
    assert repo.assets == [my_asset]
    repo.remove(my_asset)
    assert not repo.assets


def test_remove_non_existing_asset():
    """Test loading a json file."""
    repo = _MyJsonRepo()
    my_asset = _MyAsset(name="test")

    with pytest.raises(NotFoundError):
        repo.remove(my_asset)
