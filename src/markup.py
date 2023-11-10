from page import Page


class Markup:
    def __init__(self):
        self.pages = {}

    def add_page(self, page):
        self.pages[page.number] = page

    def get_page(self, page_number):
        page_number = str(page_number)
        if page_number not in self.pages:
            self.pages[page_number] = Page(page_number)
        return self.pages[page_number]

    def __repr__(self) -> str:
        return str(self.pages.items())
