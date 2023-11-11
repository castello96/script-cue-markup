import json
from markup import Markup
from page import Page
from cue import Cue


class MarkupManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarkupManager, cls).__new__(cls)
            cls._instance.markup = Markup()
        return cls._instance

    def load_data(self, filepath):
        try:
            with open(filepath, "r") as file:
                raw_data = json.load(file)
                for page_number, cues in raw_data.items():
                    page = Page(page_number)
                    for cue_dict in cues:
                        cue = Cue.from_dict(cue_dict)
                        page.add_cue(cue)
                    self.markup.add_page(page)
                print("data successfully loaded: ", self.markup)
        except FileNotFoundError:
            print("File not found, starting with empty markup")

    def save_data(self, filepath):
        with open(filepath, "w") as file:
            json_data = {
                page.number: [cue.to_dict() for cue in page.cues]
                for page in self.markup.pages.values()
            }
            json.dump(json_data, file, indent=4)

    def infer_click_intent(self, page_number, y_click, threshold=2):
        """
        Determine the intent of the click based on the y-coordinate.

        Args:
        page_number: int - The number of the current page.
        y_click: float - The y-coordinate of the click.
        threshold: int - The maximum distance from a cue to be considered a selection.

        Returns:
        dict: A dictionary with the inferred action ('select' or 'add') and the relevant cue data.
        """
        page = self.markup.get_page(page_number)

        for cue in page.cues:
            if abs(cue.y_coordinate - y_click) <= threshold:
                return {"action": "select", "cue": cue}

        return {"action": "add", "y-coordinate": y_click}

    def add_cue(self, page_number, y_click):
        page = self.markup.get_page(page_number)

        print("[markup_manager.add_cue] page", page)

        new_cue = Cue(
            y_coordinate=y_click, number=None
        )  # Number to be set inside add_cue
        page.add_cue(new_cue)

    def delete_cue(self, page_number, cue):
        page = self.markup.get_page(page_number)
        page.remove_cue(cue)
