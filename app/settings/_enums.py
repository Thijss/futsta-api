"""Generic enums for settings."""
from enum import Enum


class SettingsProfile(Enum):
    """File access"""

    DEV_ON_AWS = "dev"
    PRD_ON_AWS = "prd"
    LOCAL = "local"
