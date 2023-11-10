import json


class CueManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CueManager, cls).__new__(cls)
            cls._instance.data = {}
        return cls._instance

    def load_data(self, filepath):
        try:
            with open(filepath, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self, filepath):
        with open(filepath, "w") as file:
            json.dump(self.data, file, indent=4)

    def infer_click_intent(self, page_number, y_click, threshold=10):
        """
        Determine the intent of the click based on the y-coordinate.

        Args:
        page_number: int - The number of the current page.
        y_click: float - The y-coordinate of the click.
        threshold: int - The maximum distance from a cue to be considered a selection.

        Returns:
        dict: A dictionary with the inferred action ('select' or 'add') and the relevant cue data.
        """
        # Ensure the current page is in the data structure
        self.data.setdefault(str(page_number), [])

        # Sort cues by their y-coordinate
        current_sorted_page_cues = self.get_page_cues_sorted_by_y_coordinate(
            page_number
        )

        for cue in current_sorted_page_cues:
            if abs(cue["y-coordinate"] - y_click) <= threshold:
                # The click is close enough to an existing cue to be considered a selection
                return {"action": "select", "cue": cue}

        # The click is not close enough to any cue, so we treat it as an add
        return {"action": "add", "y-coordinate": y_click}

    def add_cue(self, page_number, y_click):
        # Ensure page_number is a string since it's used as a key in the dictionary
        page_number = str(page_number)
        current_sorted_page_cues = self.get_page_cues_sorted_by_y_coordinate(
            page_number
        )
        new_cue_number = 1  # Start with 1 and increment if needed

        # Find the correct position to insert the new cue based on y_click
        for index, cue in enumerate(current_sorted_page_cues):
            if y_click < cue["y-coordinate"]:
                # Found the position where the new cue should be inserted
                break
            new_cue_number += 1
        else:
            # If the new cue's y-coordinate is larger than all existing ones, it gets added to the end
            index = len(current_sorted_page_cues)

        # Insert the new cue at the found position
        current_sorted_page_cues.insert(
            index,
            {"y-coordinate": y_click, "cueNumber": f"{page_number}.{new_cue_number}"},
        )

        # Update cue numbers for all cues that come after the new cue
        for subsequent_cue in current_sorted_page_cues[index + 1 :]:
            # Increment the cue number suffix by 1
            subsequent_cue_number = int(subsequent_cue["cueNumber"].split(".")[1]) + 1
            subsequent_cue["cueNumber"] = f"{page_number}.{subsequent_cue_number}"

        # Update the data structure with the new sorted cues
        self.data[page_number] = current_sorted_page_cues

    def get_page_cues_sorted_by_y_coordinate(self, page_number):
        # Fetch the cues for the page and sort them by y-coordinate
        page_cues = self.data.get(str(page_number), [])
        return sorted(page_cues, key=lambda x: x["y-coordinate"])

    def delete_cue(self, page_number, cue_to_delete):
        # Logic to delete a cue
        pass

    # Additional methods as needed
