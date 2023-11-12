import unittest
from src.cue import Cue
from src.page import Page


class TestPage(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cues = [Cue(10, 1), Cue(20, 2), Cue(30, 3), Cue(40, 4)]
        self.test_page = Page(
            1,
            self.test_cues,
        )

    def test_add_cue_to_beginning(self):
        self.test_page.add_cue(5)
        self.assertEqual(len(self.test_page.cues), 5)
        self.assertEqual(
            self.test_page.cues,
            [Cue(5, 1), Cue(10, 2), Cue(20, 3), Cue(30, 4), Cue(40, 5)],
        )

    def test_add_cue_to_middle(self):
        self.test_page.add_cue(25)
        self.assertEqual(len(self.test_page.cues), 5)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(20, 2), Cue(25, 3), Cue(30, 4), Cue(40, 5)],
        )

    def test_add_cue_to_end(self):
        self.test_page.add_cue(50)
        self.assertEqual(len(self.test_page.cues), 5)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(20, 2), Cue(30, 3), Cue(40, 4), Cue(50, 5)],
        )

    def test_remove_cue_at_beginning(self):
        self.test_page.remove_cue(self.test_cues[0])
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(20, 1), Cue(30, 2), Cue(40, 3)],
        )

    def test_remove_cue_at_middle(self):
        self.test_page.remove_cue(self.test_cues[1])
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(30, 2), Cue(40, 3)],
        )

    def test_remove_cue_at_end(self):
        self.test_page.remove_cue(self.test_cues[len(self.test_cues) - 1])
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(20, 2), Cue(30, 3)],
        )

    def test_equality_comparison_different_types(self):
        self.assertFalse(self.test_page == self.test_cues[0])

    def test_equality_comparison_equal(self):
        self.assertTrue(self.test_page == Page(1, self.test_cues))

    def test_equality_comparison_non_equal_page_number(self):
        self.assertFalse(self.test_page == Page(2, self.test_cues))

    def test_equality_comparison_non_equal_cues(self):
        self.assertFalse(self.test_page == Page(1, [Cue(10, 1)]))


if __name__ == "__main__":
    unittest.main()
