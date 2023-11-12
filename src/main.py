from gui import Gui
from markup_manager import MarkupManager


def main():
    print("PDF Annotation Application started.")
    markup_manager = MarkupManager()
    gui = Gui(markup_manager)
    gui.launch_gui()


if __name__ == "__main__":
    main()
