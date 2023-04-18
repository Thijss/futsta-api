"""Generic enums for settings."""
from enum import Enum


class SettingsProfile(Enum):
    """File access"""

    AWS_LAMBDA_DEV = "aws_lambda_dev"
    AWS_LAMBDA_PRD = "aws_lambda_prd"
    LOCAL = "local_dev"
