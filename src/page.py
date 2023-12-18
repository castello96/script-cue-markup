# TODO: Fix this import and script running stuff
try:
    from .cue import Cue  # When imported as a package
except ImportError:
    from cue import Cue  # When run as a standalone script
    from cue_types import CueType


class Page:
    def __init__(self, number: int, cues=None, annotations=None):
        self.number = number
        self._cues = (
            cues
            if cues is not None
            else {CueType.MICROPHONE.value: [], CueType.QLAB.value: []}
        )
        self._annotations = annotations if annotations is not None else []

    def create_new_cue_at_y_coordinate(self, cue_to_add_y_coordinate, cue_type):
        # TODO: Add logic to prevent adding a cue on top of a preexisting one
        cue_list = self._cues[cue_type]
        # Find the index where the new cue should be inserted
        insert_index = None
        for index, current_cue in enumerate(cue_list):
            if cue_to_add_y_coordinate < current_cue.y_coordinate:
                insert_index = index
                break

        # Insert the new cue at the found position, or append if not found
        if insert_index is not None:
            cue_list.insert(
                insert_index, Cue(cue_type, cue_to_add_y_coordinate, insert_index + 1)
            )
            # Update cue numbers for subsequent cues
            for i in range(insert_index + 1, len(cue_list)):
                cue_list[i].number = i + 1
        else:
            new_cue_number = len(cue_list) + 1
            cue_list.append(Cue(cue_type, cue_to_add_y_coordinate, new_cue_number))

    def add_existing_cue(self, cue_to_add):
        cue_list = self._cues[cue_to_add.type]
        insert_index = None
        for index, current_cue in enumerate(cue_list):
            if cue_to_add.number <= current_cue.number:
                insert_index = index
                break

        if insert_index is not None:
            cue_list.insert(insert_index, cue_to_add)
            # Update cue numbers for subsequent cues
            for i in range(insert_index + 1, len(cue_list)):
                cue_list[i].number = i + 1
        else:
            cue_list.append(cue_to_add)

    def remove_cue(self, cue_to_remove):
        # TODO: Could start the index at self.cues[cue_to_remove.number - 1] instead of the beginning
        cue_list = self._cues[cue_to_remove.type]
        removed = False
        for index, current_cue in enumerate(cue_list):
            if current_cue == cue_to_remove and not removed:
                cue_list.remove(current_cue)
                removed = True
            if removed and index != len(cue_list):
                cue_list[index].number -= 1

    def add_annotations(self, annotations_to_add):
        self._annotations.append(annotations_to_add)

    def get_microphone_cues(self):
        return self._cues[CueType.MICROPHONE.value]

    def get_q_lab_cues(self):
        return self._cues[CueType.QLAB.value]

    def get_annotations(self):
        print("[get_annotations] annotations: ", self._annotations)
        return self._annotations

    def __eq__(self, other) -> bool:
        if not isinstance(other, Page):
            # don't attempt to compare against unrelated types
            return False

        # TODO: can you do == on cue dictionary or do we have to index it by cue type
        return (
            self.number == other.number
            and self._cues == other._cues
            and self._annotations == self._annotations
        )

    def __repr__(self):
        # TODO: Do we need to create a new list explicitly calling repr() on each cue?
        microphone_cues_repr = ", ".join(
            repr(cue) for cue in self._cues[CueType.MICROPHONE.value]
        )
        q_lab_cues_repr = ", ".join(repr(cue) for cue in self._cues[CueType.QLAB.value])
        return f"Page(number={self.number}, Microphone cues=[{microphone_cues_repr}], Qlab cues=[{q_lab_cues_repr}], Annotations=[{self._annotations}])"
