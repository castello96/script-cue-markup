from gui import Gui
from pdf_manager import PdfManager
from markup_manager import MarkupManager


def main():
    print("PDF Annotation Application started.")
    pdf_manager = PdfManager()
    markup_manager = MarkupManager()
    gui = Gui(pdf_manager, markup_manager)
    gui.launch_gui()


if __name__ == "__main__":
    main()
