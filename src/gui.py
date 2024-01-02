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


main_window_config = {
    "x": 1300,
    "y": 825,
    "left_col_screen_percentage": 0.25,
    "right_col_screen_percentage": 0.75,
}
image_config = {
    "x": main_window_config["x"] * main_window_config["right_col_screen_percentage"],
    "y": main_window_config["y"] * 0.95,
}
annotation_window_config = {"x": 800, "y": 400}
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
            ["&File", ["&Load PDF", "&Load Markup", "&Save As", "&Save", "&Export"]],
            ["&Edit", ["&Undo", "&Redo", "&Annotations"]],
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
                    size=(30, 55),  # TODO: Make this y size dynamic
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
                        main_window_config["x"]
                        * main_window_config["left_col_screen_percentage"],
                        None,
                    ),
                    expand_y=True,
                ),
                sg.Col(
                    self.col_page_view,
                    size=(
                        main_window_config["x"]
                        * main_window_config["right_col_screen_percentage"],
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
            size=(main_window_config["x"], main_window_config["y"]),
            finalize=True,
        )

        self.window.bind("<Motion>", "Motion")

    def launch_gui(self):
        ### DEBUG
        test_pdf_file_path = "/Users/nicholascastello/Documents/Theatre/Librettos/Holy Rollers Libretto.pdf"
        test_markup_file_path = (
            "/Users/nicholascastello/Documents/Theatre/Librettos/session_data.json"
        )
        self.window["-FILENAME-"].update(test_pdf_file_path)
        self.pdf_manager.open_pdf(test_pdf_file_path)
        self.render_pdf_page(self.current_page)
        self.markup_manager.load_data(test_markup_file_path)
        self.render_pages_in_list_box()

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
            elif event == "Annotations":
                self.handle_open_annotation_editor()
            elif event in ("-SELECT-", "s"):
                self.handle_update_cursor_mode(CursorMode.SELECT)
            elif event in ("-ADD_CUE-", "c"):
                self.handle_update_cursor_mode(CursorMode.CUE)
            elif event in ("-ANNOTATE-", "a"):
                self.handle_annotate_clicked()
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

            page.add_annotation(Annotation(x_click, y_click, input_text))

        # Rerender the page
        self.render_pdf_page(self.current_page)

    def handle_annotate_clicked(self):
        self.handle_update_cursor_mode(CursorMode.ANNOTATE)
        if self.selected_cue:
            input_text = sg.popup_get_text(
                "Enter the text for the cue annotation", "Annotation"
            )
            if not input_text:
                return

            self.selected_cue.note = input_text

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
            self.render_pages_in_list_box()
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

    def render_pages_in_list_box(self):
        listbox_data = []
        pages = self.markup_manager.get_all_pages()
        for i in range(self.pdf_manager.get_num_pages()):
            page_num_string = str(i)
            if page_num_string not in pages:
                listbox_data.append(f"{page_num_string}")
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

    def handle_open_annotation_editor(self):
        page = self.markup_manager.get_page(self.current_page)
        annotations = page.get_annotations()
        table_data = []
        for annotation in annotations:
            row = [annotation.note, annotation.x_coordinate, annotation.y_coordinate]
            table_data.append(row)
        self.run_annotation_editor(table_data, page)

    def run_annotation_editor(self, annotations, page):
        layout = [
            [
                sg.Table(
                    values=annotations,
                    headings=["Text", "X-coordinate", "Y-coordinate"],
                    display_row_numbers=True,
                    enable_events=True,
                    key="-TABLE-",
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [
                sg.Button("Add"),
                sg.Button("Edit"),
                sg.Button("Delete"),
                sg.Button("Close"),
            ],
        ]

        window = sg.Window(
            "Edit Annotations",
            layout,
            size=(annotation_window_config["x"], annotation_window_config["y"]),
        )

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Close":
                break
            elif event == "Add":
                new_annotation_data = self.edit_annotation_popup(["", "", ""])
                if new_annotation_data:
                    annotations.append(new_annotation_data)
                    window["-TABLE-"].update(values=annotations)
                    annotation = Annotation(
                        note=new_annotation_data[0],
                        x_coordinate=new_annotation_data[1],
                        y_coordinate=new_annotation_data[2],
                    )
                    page.add_annotation(annotation)
                    self.render_pdf_page(self.current_page)
            elif event == "Edit":
                selected_row = values["-TABLE-"][0]
                annotation = page.get_annotation_by_attributes(
                    annotations[selected_row][0],
                    annotations[selected_row][1],
                    annotations[selected_row][2],
                )
                updated_data = self.edit_annotation_popup(annotations[selected_row])
                if updated_data:  # If changes were made
                    annotations[selected_row] = updated_data
                    window["-TABLE-"].update(values=annotations)
                    annotation.update(
                        note=updated_data[0],
                        x_coordinate=updated_data[1],
                        y_coordinate=updated_data[2],
                    )
                    self.render_pdf_page(self.current_page)
            elif event == "Delete":
                selected_row = values["-TABLE-"][0]
                annotation = page.get_annotation_by_attributes(
                    annotations[selected_row][0],
                    annotations[selected_row][1],
                    annotations[selected_row][2],
                )
                print(f"Attempting to delete {selected_row} from {annotations}")
                del annotations[selected_row]
                window["-TABLE-"].update(values=annotations)
                page.delete_annotation(annotation)
                self.render_pdf_page(self.current_page)

        window.close()

    def edit_annotation_popup(self, annotation_data):
        column_labels = [
            [sg.Text("Note")],
            [sg.Text("X-coordinate")],
            [sg.Text("Y-coordinate")],
        ]

        column_inputs = [
            [sg.InputText(annotation_data[0], key="note", size=(20, 1))],
            [sg.InputText(annotation_data[1], key="x_pos", size=(20, 1))],
            [sg.InputText(annotation_data[2], key="y_pos", size=(20, 1))],
        ]

        layout = [
            [
                sg.Column(column_labels, vertical_alignment="top"),
                sg.Column(column_inputs, vertical_alignment="top"),
            ],
            [sg.Button("Save"), sg.Button("Cancel")],
            [sg.Text("", size=(40, 1), key="error_msg", text_color="red")],
        ]

        window = sg.Window("Edit Annotation", layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            elif event == "Save":
                # Validate x and y positions are integers
                x_pos, y_pos = values["x_pos"], values["y_pos"]
                # TODO: Also validate x and y are within page size bounds
                if not (x_pos.isdigit() and y_pos.isdigit()):
                    window["error_msg"].update("X and Y positions must be integers.")
                    continue
                # Return updated values
                window.close()
                return [values["note"], int(x_pos), int(y_pos)]

    # Fool Proof Design
    def update_button_styles(self):
        # Update button styles based on the current cursor mode
        modes = {
            CursorMode.SELECT: "-SELECT-",
            CursorMode.CUE: "-ADD_CUE-",
            CursorMode.ANNOTATE: "-ANNOTATE-",
        }

        for mode, key in modes.items():
            if self.cursor_mode == mode:
                self.window[key].update(button_color=self.button_selected_color)
            else:
                self.window[key].update(button_color=self.button_normal_color)
