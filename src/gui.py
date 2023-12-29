from enum import Enum
from cursor_mode import CursorMode
from cue_types import CueType
from arrow_keys import ArrowKey
from y_directions import YDirection
from annotation import Annotation
import PySimpleGUI as sg


class FileType(Enum):
    PNG = "PNG"
    PDF = "PDF"


window_config = {
    "x": 1300,
    "y": 825,
    "left_col_screen_percentage": 0.25,
    "right_col_screen_percentage": 0.75,
}
image_config = {
    "x": window_config["x"] * window_config["right_col_screen_percentage"],
    "y": window_config["y"] * 0.95,
}
# image_config = {
#     "x": 900,
#     "y": 700,
# }


class Gui:
    def __init__(self, pdf_manager, markup_manager):
        self.markup_manager = markup_manager
        self.pdf_manager = pdf_manager
        self.current_page = 0
        self.cursor_mode = CursorMode.SELECT
        self.selected_cue = None
        self.cue_type_to_add = CueType.MICROPHONE.value
        self.view = set([CueType.MICROPHONE.value, CueType.QLAB.value, "annotation"])
        self.current_file_path = None

        # Define the File menu
        self.menu_def = [
            ["&File", ["&Load PDF", "&Load Markup", "&Save As", "&Save", "&Export"]]
        ]

        # Define button options
        self.button_selected_color = ("white", "green")
        self.button_normal_color = ("white", "blue")
        button_padding = (1, 1)
        self.cursor_mode_buttons = [
            [
                sg.Button(
                    "Select",
                    key="-SELECT-",
                    pad=button_padding,
                    button_color=self.button_normal_color,
                ),
                sg.Button(
                    "Add Cue",
                    key="-ADD_CUE-",
                    pad=button_padding,
                    button_color=self.button_normal_color,
                ),
                sg.Button(
                    "Annotate",
                    key="-ANNOTATE-",
                    pad=button_padding,
                    button_color=self.button_normal_color,
                ),
                sg.Button(
                    "Offset",
                    key="-OFFSET-",
                    pad=button_padding,
                    button_color=self.button_normal_color,
                ),
            ],
        ]

        self.action_buttons = [
            [
                sg.Button(
                    "Delete",
                    key="-DELETE-",
                    pad=button_padding,
                    expand_x=True,
                    expand_y=True,
                    button_color=("white", "red"),
                )
            ],
        ]

        self.col_pages_list = [
            # TODO: Add tooltips for all buttons
            [
                sg.Col(self.cursor_mode_buttons, expand_x=True),
            ],
            [
                sg.Col(
                    self.action_buttons,
                )
            ],
            [sg.Text(key="-FILENAME-")],
            [
                sg.Listbox(
                    values="",
                    size=(30, 80),
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
                sg.Button("Prev", key="-PREV_PAGE-", size=(4, 2)),
                sg.Image(
                    key="-IMAGE-",
                    # size=(image_config["x"], image_config["y"]),
                    enable_events=True,
                    expand_y=True,
                    expand_x=True,
                ),
                sg.Button("Next", key="-NEXT_PAGE-", size=(4, 2)),
                sg.Column(
                    [
                        [
                            sg.Frame(
                                title="Add Cue Type",
                                layout=[
                                    [
                                        sg.Radio(
                                            "Microphone",
                                            "RADIO1",
                                            key="-RADIO_MIC-",
                                            default=True,
                                            enable_events=True,
                                        )
                                    ],
                                    [
                                        sg.Radio(
                                            "Qlab",
                                            "RADIO1",
                                            key="-RADIO_QLAB-",
                                            enable_events=True,
                                        )
                                    ],
                                ],
                                vertical_alignment="top",
                            )
                        ],
                        [
                            sg.Frame(
                                title="View",
                                layout=[
                                    [
                                        sg.Checkbox(
                                            "Microphone Cues",
                                            key="-VIEW_CHECKBOX_MIC-",
                                            default=CueType.MICROPHONE.value
                                            in self.view,
                                            enable_events=True,
                                        )
                                    ],
                                    [
                                        sg.Checkbox(
                                            "Qlab Cues",
                                            key="-VIEW_CHECKBOX_QLAB-",
                                            default=CueType.QLAB.value in self.view,
                                            enable_events=True,
                                        )
                                    ],
                                    [
                                        sg.Checkbox(
                                            "Annotations",
                                            key="-VIEW_CHECKBOX_ANNOTATION-",
                                            default="annotation" in self.view,
                                            enable_events=True,
                                        )
                                    ],
                                ],
                                vertical_alignment="top",
                            )
                        ],
                    ],
                    vertical_alignment="top",
                ),
            ],
            [
                sg.Text("", expand_x=True),  # Spacer
                sg.Text("", size=(15, 1), key="-FILE_NUM-", justification="center"),
                sg.Text("", expand_x=True),  # Spacer
            ],
        ]

        self.layout = [
            [sg.Menu(self.menu_def)],
            [
                sg.Col(
                    self.col_pages_list,
                    size=(
                        window_config["x"]
                        * window_config["left_col_screen_percentage"],
                        None,
                    ),
                    expand_y=True,
                ),
                sg.Col(
                    self.col_page_view,
                    size=(
                        window_config["x"]
                        * window_config["right_col_screen_percentage"],
                        None,
                    ),
                    expand_y=True,
                    expand_x=True,
                ),
            ],
        ]

        self.window = sg.Window(
            "PDF Markup Tool",
            self.layout,
            return_keyboard_events=True,
            enable_close_attempted_event=True,
            size=(window_config["x"], window_config["y"]),
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
            elif event == "Load PDF":
                self.handle_load_pdf_file()
            elif event == "Load Markup":
                self.handle_load_markup_file()
            elif event == "Save As":
                self.handle_save_file_as()
            elif event == "Save":
                self.handle_save_file()
            elif event == "Export":
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
            elif event == "-RADIO_MIC-":
                self.cue_type_to_add = CueType.MICROPHONE.value
            elif event == "-RADIO_QLAB-":
                self.cue_type_to_add = CueType.QLAB.value
            elif event.startswith("-VIEW_CHECKBOX_"):
                self.handle_view_checkbox_changed(
                    values["-VIEW_CHECKBOX_MIC-"],
                    values["-VIEW_CHECKBOX_QLAB-"],
                    values["-VIEW_CHECKBOX_ANNOTATION-"],
                )
            elif event in ("-PREV_PAGE-", ArrowKey.LEFT.value):
                self.handle_previous_page_click()
            elif event in ("-NEXT_PAGE-", ArrowKey.RIGHT.value):
                self.handle_next_page_click()
            elif event in [key.value for key in ArrowKey]:
                self.handle_arrow_key_pressed(event)
            elif event.startswith("-IMAGE-"):
                self.handle_page_click(
                    self.window.user_bind_event.x, self.window.user_bind_event.y
                )
            elif event == "-LISTBOX-":
                page_number = int(values["-LISTBOX-"][0].split(" ")[0])
                self.render_pdf_page(page_number)

        self.window.close()

    def handle_page_click(self, x_click, y_click):
        if not self.current_page:
            return

        page = self.markup_manager.get_page(self.current_page)
        if self.cursor_mode == CursorMode.SELECT:
            self.select_cue(self.current_page, y_click)
        elif self.cursor_mode == CursorMode.CUE:
            page.create_new_cue_at_y_coordinate(y_click, self.cue_type_to_add)
            self.render_pages_in_list_box()
        elif self.cursor_mode == CursorMode.ANNOTATE:
            input_text = sg.popup_get_text(
                "Enter the text for the annotation", "Annotation"
            )
            if not input_text:
                return

            if not self.selected_cue:
                # Add a 'floating' annotation
                page.add_annotation(Annotation(x_click, y_click, input_text))
            else:
                # Add note to a selected cue
                self.selected_cue.note = input_text
        elif self.cursor_mode == CursorMode.OFFSET:
            return

        # Rerender the page
        self.render_pdf_page(self.current_page)

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
            self.render_pages_in_list_box()
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
            self.render_pdf_page(self.current_page)
        else:
            print("File loading cancelled.")

    def handle_save_file(self):
        # If it has not been saved yet, call the save as dialogue
        if not self.current_file_path:
            self.handle_save_file_as()
            return
        self.markup_manager.save_data(self.current_file_path)
        sg.popup("File has been saved successfully.", title="Saved")

    def handle_save_file_as(self):
        file_path = sg.popup_get_file(
            "Select a destination to save your markup to",
            "Save file",
            save_as=True,
            no_window=True,
            default_extension=".json",
        )

        if not file_path:
            return

        self.current_file_path = file_path
        self.markup_manager.save_data(file_path)
        sg.popup("File has been saved successfully.", title="Saved")

    def handle_export_pdf_with_markup(self):
        file_path = sg.popup_get_file(
            "Select a destination to export your pdf and markup overlay to",
            "Export file",
            save_as=True,
            no_window=True,
            default_extension=".pdf",
        )
        # TODO: DO we need to validate that there is an actual file_path here? What about cancellations
        self.pdf_manager.convert_pdf_with_overlays(
            self.markup_manager,
            file_path,
            image_size=(image_config["x"], image_config["y"]),
        )
        print("file saved! ")

    def handle_delete_key_press(self):
        # Check if there is a selected cue and if so, delete it
        if self.selected_cue:
            print("Deleting selected cue: ", self.selected_cue)
            self.markup_manager.delete_cue(self.current_page, self.selected_cue)
            self.render_pdf_page(self.current_page)
            self.render_pages_in_list_box()
            return
        print("Cannot delete! No cue selected")

    def select_cue(self, page_number, y_click):
        cue = self.markup_manager.get_cue_at_y_coordinate(page_number, y_click)

        if cue:
            self.selected_cue = cue
        else:
            self.selected_cue = None

    def handle_update_cursor_mode(self, cursor_mode):
        self.cursor_mode = cursor_mode
        self.update_button_styles()

    def handle_next_page_click(self):
        self.render_pdf_page(self.current_page + 1)

    def handle_previous_page_click(self):
        self.render_pdf_page(self.current_page - 1)

    def render_pdf_page(self, page_number):
        if page_number < 0 or page_number >= self.pdf_manager.get_num_pages():
            return

        page_image = self.pdf_manager.get_pdf_page_with_cues(
            self.markup_manager,
            self.view,
            page_number,
            (image_config["x"], image_config["y"]),
            self.selected_cue,
        )
        image_data = self.pdf_manager.convert_image_to_data(
            page_image, FileType.PNG.value
        )
        if image_data:
            self.current_page = page_number
            self.window["-IMAGE-"].update(data=image_data)
            self.window["-FILE_NUM-"].update(
                f"Page {self.current_page} of {self.pdf_manager.get_num_pages()-1}"
            )

    # TODO: update this to write both mic cues and qlab cues or add them both
    def render_pages_in_list_box(self):
        listbox_data = []
        pages = self.markup_manager.get_all_pages()
        for i in range(self.pdf_manager.get_num_pages()):
            page_num_string = str(i)
            if page_num_string not in pages:
                continue
            num_microphone_cues = len(pages[page_num_string].get_microphone_cues())
            num_q_lab_cues = len(pages[page_num_string].get_q_lab_cues())
            if num_microphone_cues > 0 or num_q_lab_cues > 0:
                listbox_data.append(
                    f"{pages[page_num_string].number} ({num_microphone_cues}, {num_q_lab_cues} cues)"
                )
            else:
                listbox_data.append(f"{page_num_string}")
        self.window["-LISTBOX-"].update(values=listbox_data)

    def handle_view_checkbox_changed(
        self, is_microphone_checked, is_qlab_checked, is_annotation_checked
    ):
        # Handle Microphone Checkbox
        if is_microphone_checked:
            self.view.add(CueType.MICROPHONE.value)
        else:
            self.view.discard(CueType.MICROPHONE.value)

        # Handle Qlab Checkbox
        if is_qlab_checked:
            self.view.add(CueType.QLAB.value)
        else:
            self.view.discard(CueType.QLAB.value)

        # Handle Annotation Checkbox
        if is_annotation_checked:
            self.view.add("annotation")
        else:
            self.view.discard("annotation")

        self.render_pdf_page(self.current_page)

    def handle_arrow_key_pressed(self, direction):
        current_page = self.markup_manager.get_page(self.current_page)

        if direction == ArrowKey.LEFT.value:
            pass
        elif direction == ArrowKey.UP.value and self.selected_cue:
            self.selected_cue = current_page.move_cue(
                self.selected_cue, YDirection.UP.value
            )
        elif direction == ArrowKey.RIGHT.value:
            pass
        elif direction == ArrowKey.DOWN.value and self.selected_cue:
            self.selected_cue = current_page.move_cue(
                self.selected_cue, YDirection.DOWN.value
            )

        self.render_pdf_page(self.current_page)

    # Fool Proof Design
    def update_button_styles(self):
        # Update button styles based on the current cursor mode
        modes = {
            CursorMode.SELECT: "-SELECT-",
            CursorMode.CUE: "-ADD_CUE-",
            CursorMode.ANNOTATE: "-ANNOTATE-",
            CursorMode.OFFSET: "-OFFSET-",
        }

        for mode, key in modes.items():
            if self.cursor_mode == mode:
                self.window[key].update(button_color=self.button_selected_color)
            else:
                self.window[key].update(button_color=self.button_normal_color)
