from pydantic import BaseModel


class Player(BaseModel):
    """A player."""
    name: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name.lower() == other.name.lower()
        return NotImplemented

    def __str__(self):
        return f"A player named {self.name}"
