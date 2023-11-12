from markup_manager import MarkupManager
from cursor_mode import CursorMode
import PySimpleGUI as sg


class Gui:
    def __init__(self, markup_manager):
        self.markup_manager = markup_manager
        self.selected_cue = None
        self.cursor_mode = CursorMode.SELECT

        self.layout = [
            [
                sg.Button("Load", key="-LOAD-"),
                sg.Button("Save As", key="-SAVE_AS-"),
                sg.Button("Save", key="-SAVE-"),
                sg.Button("Select", key="-SELECT-"),
                sg.Button("Add Cue", key="-ADD_CUE-"),
                sg.Button("Annotate", key="-ANNOTATE-"),
                sg.Button("Calibrate", key="CALIBRATE"),
                sg.Button("Delete", key="-DELETE-"),
            ],
            [sg.Text("Cursor Mode:"), sg.Text("SELECT", key="-CURSOR-MODE-")],
            [sg.Image(key="-IMAGE-")],  # Placeholder for PDF page image
            [
                sg.Button("Prev Page", key="-PREV_PAGE-"),
                sg.Button("Next Page", key="-NEXT_PAGE-"),
            ],
        ]
        self.window = sg.Window("PDF Markup Tool", self.layout)

    def launch_gui(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            elif event == "-LOAD-":
                self.handle_load_file()
            elif event == "-SAVE_AS-":
                self.handle_save_file_as()
            elif event == "-SAVE-":
                self.handle_save_file()
            elif event == "-SELECT-":
                self.cursor_mode = CursorMode.SELECT
            elif event == "-ADD_CUE-":
                self.cursor_mode = CursorMode.CUE
            elif event == "-ANNOTATE-":
                self.cursor_mode = CursorMode.ANNOTATE
            elif event == "-CALIBRATE-":
                self.cursor_mode = CursorMode.CALIBRATE
            elif event == "-DELETE-":
                self.handle_delete_key_press()
            elif event == "-PREV_PAGE-":
                self.handle_previous_page_click
            elif event == "-NEXT_PAGE-":
                self.handle_next_page_click()

            self.window["-CURSOR-MODE-"].update(self.cursor_mode.name)

        self.window.close()

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
        # TODO: file_types is not filtering to JSON
        file_path = sg.popup_get_file(
            "Select a file to open",
            title="Load file",
            file_types=(("JSON Files", "*.json"),),
            no_window=True,
        )

        if file_path:  # Check if a file was selected
            print("loading file ", file_path)
            self.markup_manager.load_data(file_path)
        else:
            print("File loading cancelled.")

    def handle_save_file(self):
        # TODO: Use this if file has already been saved with a name
        pass

    def handle_save_file_as(self):
        # Will need a file save dialogue here
        file_path = sg.popup_get_file(
            "Select a destination to save your markup to",
            "Save file",
            save_as=True,
            default_extension=".json",
        )
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
