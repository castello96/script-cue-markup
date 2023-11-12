class Cue:
    def __init__(self, y_coordinate, number):
        self.y_coordinate = y_coordinate
        self.number = number

    def to_dict(self):
        return {"y_coordinate": self.y_coordinate, "number": self.number}

    @staticmethod
    def from_dict(data):
        return Cue(data["y_coordinate"], data["number"])

    def update(self, y_coordinate, number):
        self.y_coordinate = y_coordinate
        self.number = number

    def __eq__(self, other):
        if not isinstance(other, Cue):
            # don't attempt to compare against unrelated types
            return False

        return self.y_coordinate == other.y_coordinate and self.number == other.number

    def __repr__(self) -> str:
        return f"y_coordinate: {self.y_coordinate} number: {self.number}"
