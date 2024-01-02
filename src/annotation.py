class Annotation:
    def __init__(self, x_coordinate, y_coordinate, note) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.note = note

    def to_dict(self):
        return {
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "note": self.note,
        }

    @staticmethod
    def from_dict(data):
        return Annotation(data["y_coordinate"], data["x_coordinate"], data["note"])

    def update(self, x_coordinate, y_coordinate, note):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.note = note

    def __eq__(self, other):
        if not isinstance(other, Annotation):
            # don't attempt to compare against unrelated types
            return False

        return (
            self.x_coordinate == other.x_coordinate
            and self.y_coordinate == other.y_coordinate
            and self.note == other.note
        )

    def __repr__(self):
        return f"Annotation(x_coordinate={self.x_coordinate}, y_coordinate={self.y_coordinate}, note={self.note})"
