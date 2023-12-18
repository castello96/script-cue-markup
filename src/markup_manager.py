import json
from markup import Markup
from page import Page
from cue import Cue
from annotation import Annotation
from cue_types import CueType


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
                for page_number, page_data in raw_data.items():
                    page = Page(page_number)
                    print("[load_data] page_data: ", page_data)
                    cues = page_data["cues"]
                    print("[load_data] cues: ", cues)
                    print(
                        "[load_data] cues[CueType.MICROPHONE.value]: ",
                        cues[CueType.MICROPHONE.value],
                    )
                    print(
                        "[load_data] cues[CueType.QLAB.value]: ",
                        cues[CueType.QLAB.value],
                    )
                    # Microphone Cues
                    for microphone_cue_dict in cues[CueType.MICROPHONE.value]:
                        cue = Cue.from_dict(
                            microphone_cue_dict, CueType.MICROPHONE.value
                        )
                        page.add_existing_cue(cue)  # TODO: Add cue_type
                    # QLab Cues
                    for q_lab_cue_dict in cues[CueType.QLAB.value]:
                        cue = Cue.from_dict(q_lab_cue_dict, CueType.QLAB.value)
                        page.add_existing_cue(cue)  # TODO: Add cue_type
                    # Annotations
                    for annotation_dict in page_data["annotations"]:
                        annotation = Annotation.from_dict(annotation_dict)
                        page.add_annotation(annotation)
                    self.markup.add_page(page)
                print("data successfully loaded: ", self.markup)
        except FileNotFoundError:
            print("File not found, starting with empty markup")

    def save_data(self, filepath):
        with open(filepath, "w") as file:
            json_data = {
                str(page.number): {
                    "cues": {
                        "microphone": [
                            cue.to_dict() for cue in page.get_microphone_cues()
                        ],
                        "qLab": [cue.to_dict() for cue in page.get_q_lab_cues()],
                    },
                    "annotations": [
                        annotation.to_dict() for annotation in page.get_annotations()
                    ],
                }
                for page in self.markup.pages.values()
            }
            json.dump(json_data, file, indent=4)

    def get_cue_at_y_coordinate(self, page_number, y_coordinate, threshold=8):
        page = self.markup.get_page(page_number)

        all_page_cues = [
            *page.get_microphone_cues(),
            *page.get_q_lab_cues(),
        ]

        for cue in all_page_cues:
            if abs(cue.y_coordinate - y_coordinate) <= threshold:
                return cue

        return None

    def add_cue(self, page_number, y_coordinate):
        page = self.markup.get_page(page_number)
        page.create_new_cue_at_y_coordinate(y_coordinate)

    def delete_cue(self, page_number, cue):
        page = self.markup.get_page(page_number)
        page.remove_cue(cue)

    def get_page(self, page_number):
        return self.markup.get_page(page_number)

    def get_all_pages(self):
        return self.markup.get_pages()
