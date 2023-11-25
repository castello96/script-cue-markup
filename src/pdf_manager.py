import os
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import io

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
                print(f"info: {info}, num_pages: {num_pages}")
                return self.pdf, num_pages
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return None, 0

    def get_num_pages(self):
        if not self.pdf:
            return 0
        return len(self.pdf.pages)

    def convert_pdf_with_overlays(self, markup_manager, output_pdf_path):
        temp_pdf_paths = []

        for i in range(len(self.pdf.pages)):
            # Get the page as an image with overlays
            page_image = self.get_pdf_page_with_cues(
                markup_manager, i, image_size=(1350, 1050)
            )

            # Convert image to PDF data and write to a temp file
            page_pdf_data = self.convert_image_to_data(page_image, FileType.PDF.value)
            temp_pdf_path = f"{output_pdf_path.split('.')[0]}_temp_page_{i}.pdf"
            with open(temp_pdf_path, "wb") as temp_pdf_file:
                temp_pdf_file.write(page_pdf_data)
            temp_pdf_paths.append(temp_pdf_path)

        # Combine all temp PDFs into one final PDF
        with open(output_pdf_path, "wb") as final_pdf_file:
            writer = PyPDF2.PdfWriter()
            for temp_pdf in temp_pdf_paths:
                with open(temp_pdf, "rb") as temp_pdf_file:
                    reader = PyPDF2.PdfReader(temp_pdf_file)
                    writer.add_page(reader.pages[0])
            writer.write(final_pdf_file)

        print(f"[convert_pdf_with_overlays]: Combined PDF saved as {output_pdf_path}")

        # Clean up temporary files
        for temp_pdf in temp_pdf_paths:
            os.remove(temp_pdf)
            print(f"Removed temporary file: {temp_pdf}")

    def get_pdf_page_with_cues(
        self, markup_manager, page_number=0, image_size=(900, 700), selected_cue=None
    ):
        # Convert page to image
        page_image = self.convert_pdf_page_to_image(page_number, image_size)
        # Draw cues on image
        self.draw_cues_on_image(
            markup_manager, page_image, page_number, image_size[0], selected_cue
        )
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
        self, markup_manager, page_image, page_number, image_width, selected_cue
    ):
        cues = markup_manager.get_page(page_number).cues

        text_height = 15
        draw = ImageDraw.Draw(page_image)
        font = ImageFont.truetype("./fonts/arial/arial.ttf", text_height)

        for cue in cues:
            if selected_cue and selected_cue == cue:
                fill = (0, 127, 0)
            else:
                fill = (127, 0, 0)

            text = f"{page_number}.{cue.number}"
            text_width = draw.textlength(text, font=font)

            # Calculate the width of the rectangle based on text width
            rect_width = text_width + 4  # Adding a little extra space around the text

            # Calculate X and Y coordinates to center the text in the rectangle
            rect_start_x = (rect_width - text_width) // 2
            rect_start_y = cue.y_coordinate - text_height - 1

            # Drawing the line
            draw.line(
                (0, cue.y_coordinate, image_width, cue.y_coordinate),
                fill=fill,
                width=2,
            )

            # Drawing the rectangle
            draw.rectangle(
                (0, cue.y_coordinate - text_height - 2, rect_width, cue.y_coordinate),
                outline=fill,
                width=2,
            )

            # Drawing the text centered in the rectangle
            draw.text(
                (rect_start_x, rect_start_y),
                text,
                fill=fill,
                font=font,
            )

    def convert_image_to_data(self, page_image, file_type: FileType):
        bio = io.BytesIO()
        page_image.save(bio, format=file_type)
        image_data = bio.getvalue()
        return image_data
