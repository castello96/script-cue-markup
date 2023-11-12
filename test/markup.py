import unittest
from src.cue import Cue
from src.page import Page
from src.markup import Markup


class TestMarkup(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cues = [Cue(10, 1), Cue(20, 2)]
        self.test_page1 = Page(1, self.test_cues)
        self.test_page2 = Page(2, self.test_cues)
        self.test_markup = Markup(
            {
                "1": self.test_page1,
            }
        )

    def test_add_page(self):
        self.test_markup.add_page(self.test_page2)
        self.assertEqual(
            self.test_markup, Markup({"1": self.test_page1, "2": self.test_page2})
        )

    def test_get_existing_page(self):
        self.assertEqual(self.test_markup.get_page(1), self.test_page1)

    def test_get_nonexisting_page(self):
        self.assertEqual(self.test_markup.get_page(2), Page(2, []))

    def test_equality_comparison_different_types(self):
        self.assertFalse(self.test_markup == self.test_page1)

    def test_equality_comparison_equal(self):
        self.assertTrue(
            self.test_markup
            == Markup(
                {
                    "1": self.test_page1,
                }
            )
        )

    def test_equality_comparison_non_equal(self):
        self.assertFalse(
            self.test_markup
            == Markup(
                {
                    "2": self.test_page2,
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
