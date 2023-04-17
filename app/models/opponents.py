from pydantic import BaseModel


class Opponent(BaseModel):
    """Opponent model."""

    name: str
