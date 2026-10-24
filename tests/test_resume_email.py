import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "App"))
from resume_parser_local import ResumeParser


class ResumeEmailTests(unittest.TestCase):
    def test_sentence_punctuation_is_not_part_of_email(self):
        parser = ResumeParser("unused.pdf")
        for suffix in (".", ",", ";", ")", ".."):
            with self.subTest(suffix=suffix):
                self.assertEqual(
                    parser._extract_email("Contact: first.last+jobs@example.co.uk" + suffix),
                    "first.last+jobs@example.co.uk",
                )

    def test_plain_and_missing_email(self):
        parser = ResumeParser("unused.pdf")
        self.assertEqual(parser._extract_email("person@my-company.com"), "person@my-company.com")
        self.assertEqual(parser._extract_email("No email listed"), "")


if __name__ == "__main__":
    unittest.main()
