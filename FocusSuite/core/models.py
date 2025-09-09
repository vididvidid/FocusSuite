# defines the core data structures for the application

from dataclasses import dataclass

@dataclass
class DistractionArea:
    """Data class for distraction area with metadata."""
    x: int
    y: int
    width: int
    height: int
    confidence: float
    text: str = ""
    timestamp: float = 0

    def contains_point(self, px:int, py:int) -> bool :
        return self.x <= px <= self.x + self.width and self.y <=py <= self.y + self.height
