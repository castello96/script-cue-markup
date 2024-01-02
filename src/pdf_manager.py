import os
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import io
from pypdf import PdfMerger
from cue_types import CueType

from gui import FileType


class PdfManager:
    # TODO: Does this need to be a singleton?
    def __init__(self) -> None:
        self.file_path = None
        self.pdf = None

    def open_pdf(self, file_path):
        self.file_path = file_path
        try:
            with open(file_path, "rb") as file:
                self.pdf = PyPDF2.PdfReader(file)
                # Do something with the reader object, like counting pages
                num_pages = len(self.pdf.pages)
                info = self.pdf.metadata
                return self.pdf, num_pages
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return None, 0

    def get_num_pages(self):
        if not self.pdf:
            return 0
        return len(self.pdf.pages)

    def convert_pdf_with_overlays(
        self, markup_manager, view, output_pdf_path, image_size=(1350, 1050)
    ):
        temp_pdf_paths = []

        for i in range(len(self.pdf.pages)):
            page_image = self.get_pdf_page_with_cues(
                markup_manager, view, i, image_size=image_size
            )
            page_pdf_data = self.convert_image_to_data(page_image, FileType.PDF.value)
            temp_pdf_path = f"{output_pdf_path.split('.')[0]}_temp_page_{i}.pdf"

            with open(temp_pdf_path, "wb") as temp_pdf_file:
                temp_pdf_file.write(page_pdf_data)
                temp_pdf_file.flush()
                os.fsync(temp_pdf_file.fileno())
            temp_pdf_paths.append(temp_pdf_path)

        with open(output_pdf_path, "wb") as final_pdf_file:
            merger = PdfMerger()
            for temp_pdf in temp_pdf_paths:
                merger.append(temp_pdf)
            merger.write(final_pdf_file)

        for temp_pdf in temp_pdf_paths:
            os.remove(temp_pdf)

        print(f"[convert_pdf_with_overlays]: Combined PDF saved as {output_pdf_path}")

    def get_pdf_page_with_cues(
        self,
        markup_manager,
        view,
        page_number=0,
        image_size=(900, 700),
        selected_cue=None,
    ):
        # Convert page to image #TODO: This could return none
        page_image = self.convert_pdf_page_to_image(page_number, image_size)
        page = markup_manager.get_page(page_number)

        if CueType.MICROPHONE.value in view:
            # Draw microphone cues on image
            microphone_cues = page.get_microphone_cues()
            self.draw_cues_on_image(
                page_image,
                page_number,
                image_size[0],
                microphone_cues,
                (127, 0, 0),
                selected_cue,
            )

        if CueType.QLAB.value in view:
            # Draw qlab cues on image
            q_lab_cues = page.get_q_lab_cues()
            self.draw_cues_on_image(
                page_image,
                page_number,
                image_size[0],
                q_lab_cues,
                (0, 0, 127),
                selected_cue,
            )

        if (
            "annotation" in view
        ):  # TODO: Dont use a string for "annotation." Use const variable
            # Draw floating annotations
            annotations = page.get_annotations()
            self.draw_annotations_on_image(page_image, annotations)

        return page_image

    def convert_pdf_page_to_image(self, page_number, image_size):
        images = convert_from_path(
            self.file_path,
            first_page=page_number + 1,
            last_page=page_number + 1,
            dpi=300,
        )
        if not images:
            return None

        page_image = images[0]
        page_image.thumbnail(image_size, Image.LANCZOS)
        return page_image

    def draw_cues_on_image(
        self, page_image, page_number, image_width, cues, fill_color, selected_cue
    ):
        cue_number_height = 15
        cue_note_height = 9
        selected_fill_color = (0, 127, 0)
        draw = ImageDraw.Draw(page_image)
        cue_number_font = ImageFont.truetype(
            "./fonts/arial/arial.ttf", cue_number_height
        )
        cue_note_font = ImageFont.truetype("./fonts/arial/arial.ttf", cue_note_height)

        for cue in cues:
            if selected_cue and selected_cue == cue:
                fill = selected_fill_color
            else:
                fill = fill_color

            text = f"{page_number}.{cue.number}"
            text_width = draw.textlength(text, font=cue_number_font)

            # Calculate the width of the rectangle based on text width
            rect_width = text_width + 4  # Adding a little extra space around the text

            # Calculate X and Y coordinates to center the text in the rectangle
            rect_start_x = (rect_width - text_width) // 2
            rect_start_y = cue.y_coordinate - cue_number_height - 1

            # Drawing the line
            draw.line(
                (0, cue.y_coordinate, image_width, cue.y_coordinate),
                fill=fill,
                width=2,
            )

            # Drawing the rectangle
            draw.rectangle(
                (
                    0,
                    cue.y_coordinate - cue_number_height - 2,
                    rect_width,
                    cue.y_coordinate,
                ),
                outline=fill,
                width=2,
            )

            # Drawing the text centered in the rectangle
            draw.text(
                (rect_start_x, rect_start_y),
                text,
                fill=fill,
                font=cue_number_font,
            )

            # Draw the cue note
            if cue.note:
                draw.text(
                    (rect_start_x, rect_start_y + 20),
                    cue.note,
                    fill=fill,
                    font=cue_note_font,
                )

    def draw_annotations_on_image(self, page_image, annotations):
        annotation_height = 10
        annotation_font = ImageFont.truetype(
            "./fonts/arial/arial.ttf", annotation_height
        )
        draw = ImageDraw.Draw(page_image)

        for annotation in annotations:
            draw.text(
                (annotation.x_coordinate, annotation.y_coordinate),
                annotation.note,
                fill=(0, 0, 0),
                font=annotation_font,
            )

    def convert_image_to_data(self, page_image, file_type: FileType):
        bio = io.BytesIO()
        page_image.save(bio, format=file_type)
        image_data = bio.getvalue()
        return image_data
