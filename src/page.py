from cue import Cue


class Page:
    def __init__(self, number):
        self.number = number
        self.cues = []

    def add_cue(self, cue_to_add):
        # Find the index where the new cue should be inserted
        insert_index = None
        for index, current_cue in enumerate(self.cues):
            if cue_to_add.y_coordinate < current_cue.y_coordinate:
                insert_index = index
                break

        # Insert the new cue at the found position, or append if not found
        if insert_index is not None:
            self.cues.insert(
                insert_index, Cue(cue_to_add.y_coordinate, insert_index + 1)
            )
            # Update cue numbers for subsequent cues
            for i in range(insert_index + 1, len(self.cues)):
                self.cues[i].number = i + 1
        else:
            new_cue_number = len(self.cues) + 1
            self.cues.append(Cue(cue_to_add.y_coordinate, new_cue_number))

    def remove_cue(self, cue_to_remove):
        # TODO: Could start the index at self.cues[cue_to_remove.number - 1] instead of the beginning
        removed = False
        for index, current_cue in enumerate(self.cues):
            if current_cue == cue_to_remove and not removed:
                self.cues.remove(current_cue)
                removed = True
            if removed:
                self.cues[index].number -= 1

    def __repr__(self) -> str:
        return f"Page {self.number}\nCues: {self.cues}"
