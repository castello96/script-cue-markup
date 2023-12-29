from enum import Enum
from cue_types import CueType


class Cue:
    def __init__(
        self,
        type: CueType,
        y_coordinate,
        number,
        note="",
    ):
        self.type = type
        self.y_coordinate = y_coordinate
        self.number = number
        self.note = note

    def to_dict(self):
        return {
            "y_coordinate": self.y_coordinate,
            "number": self.number,
            "note": self.note,
        }

    @staticmethod
    def from_dict(data, type):
        return Cue(type, data["y_coordinate"], data["number"], data["note"])

    def __eq__(self, other):
        if not isinstance(other, Cue):
            # don't attempt to compare against unrelated types
            return False

        if self.type != other.type:
            return False

        return (
            self.y_coordinate == other.y_coordinate
            and self.number == other.number
            and self.note == other.note
        )

    def update_y_coordinate(self, direction, amount):
        self.y_coordinate += amount * direction

    def __repr__(self):
        return f"Cue(type={self.type}, y_coordinate={self.y_coordinate}, number={self.number}, note={self.note})"
