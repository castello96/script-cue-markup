from markup_manager import MarkupManager
from cursor_mode import CursorMode
import PySimpleGUI as sg


class Gui:
    def __init__(self, markup_manager):
        self.markup_manager = markup_manager
        self.selected_cue = None
        self.cursor_mode = CursorMode.SELECT

        self.pdf_files = [
            "Page -2 (0 cues) 1",
            "Page -1 (0 cues) 2",
            "Page 0 (2 cues) 3",
            "Page 1 (2 cues) 4",
            "Page 2 (1 cues) 5",
            "Page 3 (1 cues) 6",
            "Page 4 (3 cues) 7",
        ]

        self.file_io_buttons = [
            [
                sg.Button("Load", key="-LOAD-"),
                sg.Button("Save As", key="-SAVE_AS-"),
                sg.Button("Save", key="-SAVE-"),
            ]
        ]

        self.cursor_mode_buttons = [
            [
                sg.Button("Select", key="-SELECT-"),
                sg.Button("Add Cue", key="-ADD_CUE-"),
                sg.Button("Annotate", key="-ANNOTATE-"),
                sg.Button("Offset", key="-OFFSET-"),
            ],
            [sg.Text("Cursor Mode", key="-CURSOR_MODE-")],
        ]

        self.action_buttons = [
            [
                sg.Button("Delete", key="-DELETE-"),
            ]
        ]

        self.menu = [
            # TODO: Add tooltips for all buttons
            [
                sg.Col(self.file_io_buttons),
                sg.Col(self.cursor_mode_buttons),
                sg.Col(self.action_buttons),
            ]
        ]

        self.col_pages_list = [
            [sg.Text("Rock of Ages.pdf", size=(80, 3), key="-FILENAME-")],
            [
                sg.Listbox(
                    values=self.pdf_files,
                    size=(60, 30),
                    key="-LISTBOX-",
                    enable_events=True,
                )
            ],
            [
                sg.Text(
                    "Select a page. Use scrollwheel or arrow keys on keyboard to scroll through files one by one."
                )
            ],
        ]

        self.col_page_view = [
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
            [
                sg.Button("Next", size=(8, 2)),
                sg.Button("Prev", size=(8, 2)),
                sg.Text(
                    f"Page 1 of {len(self.pdf_files)}",
                    size=(15, 1),
                    key="-FILE_NUM-",
                ),
            ],
        ]

        self.layout = [
            [self.menu],
            [sg.Col(self.col_pages_list), sg.Col(self.col_page_view)],
        ]

        self.window = sg.Window(
            "PDF Markup Tool",
            self.layout,
            return_keyboard_events=True,
            enable_close_attempted_event=True,
        )

    def launch_gui(self):
        while True:
            event, values = self.window.read()
            print(event)
            if (
                event in (sg.WIN_CLOSE_ATTEMPTED_EVENT, "Exit")
                and sg.popup_yes_no("Do you really want to exit?") == "Yes"
            ):
                break
            elif event == "-LOAD-":
                self.handle_load_file()
            elif event == "-SAVE_AS-":
                self.handle_save_file_as()
            elif event == "-SAVE-":
                self.handle_save_file()
            elif event in ("-SELECT-", "s"):
                self.handle_update_cursor_mode(CursorMode.SELECT)
            elif event in ("-ADD_CUE-", "c"):
                self.handle_update_cursor_mode(CursorMode.CUE)
            elif event in ("-ANNOTATE-", "a"):
                self.handle_update_cursor_mode(CursorMode.ANNOTATE)
            elif event in ("-OFFSET-", "o"):
                self.handle_update_cursor_mode(CursorMode.OFFSET)
            elif event == "-DELETE-":
                self.handle_delete_key_press()
            elif event == "-PREV_PAGE-":
                self.handle_previous_page_click
            elif event == "-NEXT_PAGE-":
                self.handle_next_page_click()
            # TODO: Handle -WINDOW_CLOSED- event

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
        file_path = sg.popup_get_file(
            "Select a destination to save your markup to",
            "Save file",
            save_as=True,
            no_window=True,
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

    def handle_update_cursor_mode(self, cursor_mode):
        # TODO: Update this to outline the currently selected button
        self.cursor_mode = cursor_mode
        self.window["-CURSOR_MODE-"].update(f"Cursor Mode: {self.cursor_mode.name}")

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
