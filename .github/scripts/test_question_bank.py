import hashlib
from pathlib import Path
import re
import unittest


SOURCE = Path(__file__).resolve().parents[2] / "output/302数学二分节真题集（原生LaTeX横屏版）.tex"
COUNTS = [1, 10, 5, 23, 8, 8, 28, 0, 12, 9, 25, 11, 11, 12, 25, 13, 17, 16, 0]
HEAD = re.compile(
    r"\\QuestionPage\{([^{}]+)\}\{([^{}]+)\}\{(\d+) 年第 (\d+) 题\}"
    r"\{(\d+(?:、\d+)*)\}\{([^{}]+)\}\{(\d+) / 234\}\{(\*{1,5})\}"
)


class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text()
        cls.sections = re.split(r"(?=^\\SectionHeading\{)", cls.source, flags=re.M)[1:]

    def test_question_identity_and_section_counts(self):
        identities = re.findall(r"^% Q (\d+) (\d+)$", self.source, re.M)
        self.assertEqual(len(identities), 234)
        self.assertEqual(len(set(identities)), 234)
        self.assertEqual(hashlib.sha256(str(sorted(identities)).encode()).hexdigest(),
                         "b201d7886afc28e8454c0aad1e060a7dc4c552f94eeb9347d55294a8a7e715ff")
        self.assertEqual([len(re.findall(r"^% Q ", s, re.M)) for s in self.sections], COUNTS)

    def test_ratings_and_stable_section_order(self):
        self.assertEqual(len(HEAD.findall(self.source)), 234)
        for section in self.sections:
            heads = HEAD.findall(section)
            order = [(len(h[7]), int(h[6])) for h in heads]
            self.assertEqual(order, sorted(order), section.splitlines()[0])

    def test_complete_solutions_match_questions(self):
        blocks = re.split(r"^% Q ", self.source, flags=re.M)[1:]
        for block in blocks:
            identity = block.splitlines()[0]
            year, number = identity.split()
            header = HEAD.search(block)
            self.assertIsNotNone(header, identity)
            self.assertEqual(header.group(3, 4), (year, number), identity)
            self.assertEqual(block.count(r"\begin{QuestionSolution}"), 1, identity)
            self.assertEqual(block.count(r"\end{QuestionSolution}"), 1, identity)
            self.assertIn(r"\begin{QuestionSolution}{" + f"{year} 年第 {number} 题" + "}", block)
            solution = block.split(r"\begin{QuestionSolution}", 1)[1].split(r"\end{QuestionSolution}", 1)[0]
            for label in ("已知与目标", "方法与条件", "推导", "结论与检查"):
                self.assertIn(r"\textbf{" + label + "}", solution, identity)

    def test_readable_stacked_fractions(self):
        self.assertFalse(r"\tfrac" in self.source, "源稿仍有紧缩分式")
        self.assertNotRegex(self.source, r"[¼½¾⅐-⅞]")
        for line in self.source.splitlines():
            if (line.startswith("%") or line.startswith(r"\QuestionPage{")
                    or "svg" in line or r"\arabic{BankQuestion}" in line):
                continue
            self.assertNotIn("/", line, line[:160])

    def test_delimiter_commands(self):
        self.assertFalse(re.search(r"(?<!\\)\b(?:left|right)\s*\(", self.source),
                         "公式括号命令缺少反斜杠")


if __name__ == "__main__":
    unittest.main()
