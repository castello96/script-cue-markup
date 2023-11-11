import unittest
from src.cue import Cue
from src.page import Page


class TestPage(unittest.TestCase):
    def setUp(self) -> None:
        self.cue1 = Cue(10, 1)
        self.cue2 = Cue(20, 2)
        self.cue3 = Cue(30, 3)
        self.cue4 = Cue(40, 4)
        self.test_page = Page(1, [self.cue1, self.cue2, self.cue3, self.cue4])

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
        self.test_page.remove_cue(self.cue1)
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(20, 1), Cue(30, 2), Cue(40, 3)],
        )

    def test_remove_cue_at_middle(self):
        self.test_page.remove_cue(self.cue2)
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(30, 2), Cue(40, 3)],
        )

    def test_remove_cue_at_end(self):
        self.test_page.remove_cue(self.cue4)
        self.assertEqual(len(self.test_page.cues), 3)
        self.assertEqual(
            self.test_page.cues,
            [Cue(10, 1), Cue(20, 2), Cue(30, 3)],
        )


if __name__ == "__main__":
    unittest.main()
