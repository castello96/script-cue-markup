from cue import Cue


class Page:
    def __init__(self, number):
        self.number = number
        self.cues = []

    def add_cue(self, cue_to_add):
        print("[page.add_cue] self.cues before: ", self.cues)

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

        print("[page.add_cue] self.cues after: ", self.cues)

    def remove_cue(self, cue_number):
        # Logic to remove a cue
        pass

    def __repr__(self) -> str:
        return f"Page {self.number}\nCues: {self.cues}"
