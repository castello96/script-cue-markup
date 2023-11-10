from cue_manager import CueManager

cue_manager = None


def launch_gui():
    global cue_manager

    cue_manager = CueManager()
    while True:
        print("\nMenu:")
        print("c) Click")
        print("l) Load file")
        print("s) Save file")
        print("q) Quit")
        choice = input("Enter your choice: ").lower()

        if choice == "c":
            page_number = input("Enter a page number")
            y_click = input('Enter a y_coordinate to simulate a "click"')
            handle_click(page_number, y_click)
        elif choice == "l":
            file_path = input("Enter a file path to load")
            handle_load_file(file_path)
        elif choice == "s":
            handle_save_file()
        elif choice == "q":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")


# Example of handling a click event
def handle_click(page_number, y_click):
    if cue_manager is None:
        print("CueManager is not initialized.")
        return

    intent = cue_manager.infer_click_intent(page_number, y_click)

    print("intent", intent)

    if intent["action"] == "select":
        # Select the cue for potential deletion or other actions
        select_cue(intent["cue"])
    elif intent["action"] == "add":
        # Add a new cue at the y-coordinate
        cue_manager.add_cue(page_number, intent["y-coordinate"])
        # After adding a cue, you may want to re-render the PDF page
        render_pdf_page(page_number)


def handle_load_file(file_path):
    print("loading file ", file_path)


def handle_save_file(file_path):
    # Will need a file save dialogue here
    print("file saved! ")


def select_cue():
    pass


def render_pdf_page(page_number):
    pass


def draw_line(reader, page_number, y_coordinate, cue_number):
    # Since we cannot directly draw on the PDF using PyPDF2, we need to define
    # what we mean by drawing a line. We can prepare the data for drawing
    # which will be used by the front end.
    pass
