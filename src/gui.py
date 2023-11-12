from markup_manager import MarkupManager
from cursor_mode import CursorMode


class Gui:
    def __init__(self):
        self.markup_manager = MarkupManager()
        self.selected_cue = None
        self.cursor_mode = CursorMode.SELECT

    def launch_gui(self):
        self.markup_manager.load_data("test/session_data.json")
        while True:
            print("\nMenu:")
            print("c) Click")
            print("d) Delete")
            print("l) Load file")
            print("s) Save file")
            print("q) Quit")
            choice = input("Enter your choice: ").lower()

            if choice == "c":
                page_number = int(input("Enter a page number: "))
                y_click = int(input('Enter a y_coordinate to simulate a "click": '))
                self.handle_page_click(page_number, y_click)
            elif choice == "d":
                self.handle_delete_key_press()
            elif choice == "l":
                self.handle_load_file()
            elif choice == "s":
                self.handle_save_file()
            elif choice == "q":
                print("Exiting program.")
                break
            else:
                print("Invalid choice, please try again.")

    def handle_page_click(self, page_number, y_click):
        print("Page before: ", self.markup_manager.get_page(page_number))
        if self.cursor_mode == CursorMode.SELECT:
            self.select_cue(page_number, y_click)
        elif self.cursor_mode == CursorMode.CUE:
            self.markup_manager.add_cue(page_number, y_click)
        elif self.cursor_mode == CursorMode.ANNOTATE:
            pass

        print("Page after: ", self.markup_manager.get_page(page_number))

        # Rerender the page
        self.render_pdf_page(page_number)

    def handle_load_file(self):
        # Will need a file load dialogue here
        file_path = input("Enter a file path to load: ")
        print("loading file ", file_path)
        self.markup_manager.load_data(file_path)

    def handle_save_file(self):
        # Will need a file save dialogue here
        file_path = input("Enter a file path to save: ")
        self.markup_manager.save_data(file_path)
        print("file saved! ")

    def handle_delete_key_press(self):
        # Check if there is a selected cue and if so, delete it
        if self.selected_cue:
            self.markup_manager.delete_cue(
                self.selected_cue["page_number"], self.selected_cue["cue"]
            )
            return
        print("Cannot delete! No cue selected")

    def select_cue(self, page_number, y_click):
        cue = self.markup_manager.get_cue_at_y_coordinate(page_number, y_click)
        if cue:
            self.selected_cue = {"page_number": page_number, "cue": cue}
            print(f"Cue selected: {self.selected_cue}")

    def handle_next_page_click(self):
        pass

    def handle_previous_page_click(self):
        pass

    def render_pdf_page(self, page_number):
        pass

    def draw_line(self, reader, page_number, y_coordinate, cue_number):
        # Since we cannot directly draw on the PDF using PyPDF2, we need to define
        # what we mean by drawing a line. We can prepare the data for drawing
        # which will be used by the front end.
        pass
