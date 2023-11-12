# TODO: Fix this import and script running stuff
try:
    from .page import Page  # When imported as a package
except ImportError:
    from page import Page  # When run as a standalone script


class Markup:
    def __init__(self, pages={}):
        self.pages = pages

    def add_page(self, page):
        page_number = str(page.number)
        self.pages[page_number] = page

    def get_page(self, page_number):
        page_number = str(page_number)
        if page_number not in self.pages:
            self.pages[page_number] = Page(int(page_number))
        return self.pages[page_number]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Markup):
            # don't attempt to compare against unrelated types
            return False

        return self.pages == other.pages

    def __repr__(self):
        pages_repr = ", ".join(
            f"{number}: {repr(page)}" for number, page in self.pages.items()
        )
        return f"Markup(pages={{ {pages_repr} }})"
