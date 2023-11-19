import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import io


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

    # TODO: This function should check for cues on this page a draw them before returning the image
    def get_page_as_png_image_data(self, page_number=0, image_size=(100, 100)):
        images = convert_from_path(
            self.file_path, first_page=page_number + 1, last_page=page_number + 1
        )
        if images:
            page_image = images[0]
            page_image.thumbnail(image_size, Image.LANCZOS)
            bio = io.BytesIO()
            page_image.save(bio, format="PNG")
            image_data = bio.getvalue()
            return image_data
        return None
