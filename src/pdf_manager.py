import PyPDF2


def open_pdf(filepath):
    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfFileReader(file)
            # Do something with the reader object, like counting pages
            num_pages = reader.numPages
            return reader, num_pages
    except FileNotFoundError:
        print(f"The file {filepath} was not found.")
        return None, 0
