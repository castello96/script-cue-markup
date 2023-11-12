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
                    print("Created new page", page)
                    for cue_dict in cues:
                        print("cue_dict: ", cue_dict)
                        cue = Cue.from_dict(cue_dict)
                        print("cue: ", cue)
                        page.add_cue(cue.y_coordinate)
                        print("Added cue to page: ", page)
                    self.markup.add_page(page)
                    print("Added page to markup: ", self.markup)
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

    def get_cue_at_y_coordinate(self, page_number, y_coordinate, threshold=4):
        page = self.markup.get_page(page_number)

        for cue in page.cues:
            if abs(cue.y_coordinate - y_coordinate) <= threshold:
                return cue

        return None

    def add_cue(self, page_number, y_coordinate):
        page = self.markup.get_page(page_number)
        page.add_cue(y_coordinate)

    def delete_cue(self, page_number, cue):
        page = self.markup.get_page(page_number)
        page.remove_cue(cue)

    def get_page(self, page_number):
        return self.markup.get_page(page_number)
