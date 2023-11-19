from markup_manager import MarkupManager
from cursor_mode import CursorMode
import PySimpleGUI as sg


IMAGE_SIZE = (900, 700)


class Gui:
    def __init__(self, pdf_manager, markup_manager):
        self.markup_manager = markup_manager
        self.pdf_manager = pdf_manager
        self.current_page = 0
        self.cursor_mode = CursorMode.SELECT
        self.selected_cue = None

        self.pdf_files = [
            "Page -2 (0 cues) 1",
            "Page -1 (0 cues) 2",
            "Page 0 (2 cues) 3",
            "Page 1 (2 cues) 4",
            "Page 2 (1 cues) 5",
            "Page 3 (1 cues) 6",
            "Page 4 (3 cues) 7",
        ]

        button_padding = (1, 1)
        self.file_io_buttons = [
            [
                sg.Button("Load PDF", key="-LOAD_PDF-", pad=button_padding),
                sg.Button("Load Markup", key="-LOAD_MARKUP-", pad=button_padding),
                sg.Button("Save As", key="-SAVE_AS-", pad=button_padding),
                sg.Button("Save", key="-SAVE-", pad=button_padding),
                sg.Button("Export", key="-EXPORT-", pad=button_padding),
            ],
        ]

        self.cursor_mode_buttons = [
            [
                sg.Button("Select", key="-SELECT-", pad=button_padding),
                sg.Button("Add Cue", key="-ADD_CUE-", pad=button_padding),
                sg.Button("Annotate", key="-ANNOTATE-", pad=button_padding),
                sg.Button("Offset", key="-OFFSET-", pad=button_padding),
            ],
            [sg.Text("Cursor Mode", key="-CURSOR_MODE-")],
        ]

        self.action_buttons = [
            [sg.Button("Delete", key="-DELETE-", pad=button_padding)],
        ]

        # TODO: Move all these to an actual menu instead of buttons
        self.menu = [
            # TODO: Add tooltips for all buttons
            [
                sg.Col(self.file_io_buttons, expand_x=True),
                sg.Col(self.cursor_mode_buttons, expand_x=True),
                sg.Col(self.action_buttons, expand_x=True),
            ],
        ]

        self.col_pages_list = [
            [sg.Text(size=(80, 3), key="-FILENAME-")],
            [
                sg.Listbox(
                    values=self.pdf_files,
                    size=(30, 90),
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
            [
                sg.Image(
                    key="-IMAGE-",
                    size=IMAGE_SIZE,
                    enable_events=True,
                )
            ],
            [
                sg.Button("Prev", key="-PREV_PAGE-", size=(8, 2)),
                sg.Button("Next", key="-NEXT_PAGE-", size=(8, 2)),
                sg.Text(
                    f"Page {self.current_page} of {len(self.pdf_files)}",
                    size=(15, 1),
                    key="-FILE_NUM-",
                ),
            ],
        ]

        self.layout = [
            [self.menu],
            [
                sg.Col(
                    self.col_pages_list, size=(333, None), expand_x=True, expand_y=True
                ),
                sg.Col(
                    self.col_page_view, size=(667, None), expand_x=True, expand_y=True
                ),
            ],
        ]

        self.window = sg.Window(
            "PDF Markup Tool",
            self.layout,
            return_keyboard_events=True,
            enable_close_attempted_event=True,
            size=(1000, 900),
            finalize=True,
        )

        self.window.bind("<Motion>", "Motion")

    def launch_gui(self):
        while True:
            event, values = self.window.read()
            if event == "Motion":
                continue
            print(event)
            if (
                event in (sg.WIN_CLOSE_ATTEMPTED_EVENT, "Exit")
                and sg.popup_yes_no("Do you really want to exit?") == "Yes"
            ):
                break
            elif event == "-LOAD_PDF-":
                self.handle_load_pdf_file()
            elif event == "-LOAD_MARKUP-":
                self.handle_load_file()
            elif event == "-SAVE_AS-":
                self.handle_save_file_as()
            elif event == "-SAVE-":
                self.handle_save_file()
            elif event == "-EXPORT-":
                self.handle_export_pdf_with_markup()
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
                self.handle_previous_page_click()
            elif event == "-NEXT_PAGE-":
                self.handle_next_page_click()
            elif event.startswith("-IMAGE-"):
                e = self.window.user_bind_event
                print("e: ", e)

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

    def handle_load_markup_file(self):
        # TODO: file_types is not filtering to JSON
        markup_file_path = sg.popup_get_file(
            "Select a file to open",
            title="Load markup file",
            file_types=(("JSON Files", "*.json"),),
            no_window=True,
        )

        if markup_file_path:  # Check if a file was selected
            print("loading file ", markup_file_path)
            self.markup_manager.load_data(markup_file_path)
        else:
            print("File loading cancelled.")

    def handle_load_pdf_file(self):
        # TODO: file_types is not filtering to pdf
        pdf_file_path = sg.popup_get_file(
            "Select a file to open",
            title="Load pdf file",
            file_types=(("PDF Files", "*.pdf"),),
            no_window=True,
        )

        if pdf_file_path:  # Check if a file was selected
            print("loading file ", pdf_file_path)
            self.window["-FILENAME-"].update(pdf_file_path)
            self.pdf_manager.open_pdf(pdf_file_path)
            image_data = self.pdf_manager.get_page_as_png_image_data(
                self.current_page, IMAGE_SIZE
            )
            self.window["-IMAGE-"].update(data=image_data)
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

    def handle_export_pdf_with_markup(self):
        # TODO: Export the pdf with markups
        pass

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
        image_data = self.pdf_manager.get_page_as_png_image_data(
            self.current_page + 1, IMAGE_SIZE
        )
        if image_data:
            self.current_page += 1
            self.window["-IMAGE-"].update(data=image_data)

    def handle_previous_page_click(self):
        image_data = self.pdf_manager.get_page_as_png_image_data(
            self.current_page - 1, IMAGE_SIZE
        )
        if image_data:
            self.current_page -= 1
            self.window["-IMAGE-"].update(data=image_data)

    # TODO: Abstract logic into this function
    def render_pdf_page(self, page_number):
        pass

    def handle_image_click(self, event):
        if event.startswith("-IMAGE"):
            print("[handle_image_click] event: ", event)
            _, x, y = event.split(";")
            print(_, x, y)
            self.draw_line_on_image(int(y))

    def draw_line(self, reader, page_number, y_coordinate, cue_number):
        pass
