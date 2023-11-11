import unittest
from src.cue import Cue


class TestCue(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cue = Cue(10, 1)
        self.test_dict = {"y_coordinate": 10, "number": 1}

    def test_to_dict(self):
        self.assertEqual(self.test_cue.to_dict(), self.test_dict)

    def test_from_dict(self):
        self.assertEqual(Cue.from_dict(self.test_dict), self.test_cue)

    def test_update(self):
        self.test_cue.update(20, 2)
        self.assertEqual(self.test_cue, Cue(20, 2))


if __name__ == "__main__":
    unittest.main()
