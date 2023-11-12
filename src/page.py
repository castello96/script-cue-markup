# TODO: Fix this import and script running stuff
try:
    from .cue import Cue  # When imported as a package
except ImportError:
    from cue import Cue  # When run as a standalone script


class Page:
    def __init__(self, number: int, cues=[]):
        self.number = number
        self.cues = cues

    def add_cue(self, cue_to_add_y_coordinate):
        # Find the index where the new cue should be inserted
        insert_index = None
        for index, current_cue in enumerate(self.cues):
            if cue_to_add_y_coordinate < current_cue.y_coordinate:
                insert_index = index
                break

        # Insert the new cue at the found position, or append if not found
        if insert_index is not None:
            self.cues.insert(
                insert_index, Cue(cue_to_add_y_coordinate, insert_index + 1)
            )
            # Update cue numbers for subsequent cues
            for i in range(insert_index + 1, len(self.cues)):
                self.cues[i].number = i + 1
        else:
            new_cue_number = len(self.cues) + 1
            self.cues.append(Cue(cue_to_add_y_coordinate, new_cue_number))

    def remove_cue(self, cue_to_remove):
        # TODO: Could start the index at self.cues[cue_to_remove.number - 1] instead of the beginning
        removed = False
        for index, current_cue in enumerate(self.cues):
            if current_cue == cue_to_remove and not removed:
                self.cues.remove(current_cue)
                removed = True
            if removed and index != len(self.cues):
                self.cues[index].number -= 1

    def __eq__(self, other) -> bool:
        if not isinstance(other, Page):
            # don't attempt to compare against unrelated types
            return False

        return self.number == other.number and self.cues == other.cues

    def __repr__(self) -> str:
        return f"Page {self.number}, Cues: {self.cues}"
