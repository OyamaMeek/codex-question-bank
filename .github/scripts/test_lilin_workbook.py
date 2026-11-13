from pathlib import Path
import math
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "output/李林高数上册分节题集.tex"


class LilinWorkbookTests(unittest.TestCase):
    def test_scope_and_separate_solutions(self):
        text = SOURCE.read_text()
        origins = re.findall(r"^% SOURCE line=(\d+) pdf_page=(\d+) section=([\d.]+)$", text, re.M)
        self.assertEqual(len(origins), 419)
        self.assertEqual(len({row[0] for row in origins}), 419)
        self.assertEqual(len(re.findall(r"^\\SectionHeading", text, re.M)), 19)
        blocks = re.split(r"^\\Question\{", text, flags=re.M)[1:]
        self.assertEqual([int(block.split("}")[0]) for block in blocks], list(range(1, 420)))
        for block in blocks:
            self.assertEqual(len(re.findall(r"^\\Solution$", block, re.M)), 1)
            self.assertIn(r"\vfill", block.split(r"\Solution")[0])
            self.assertIn(r"\clearpage", block.split(r"\Solution")[1])
        self.assertIn("paperwidth=800bp,paperheight=600bp", text)
        self.assertIn(r"\operatorname*{lim}\limits", text)
        self.assertNotIn(r"\tfrac", text)
        for image in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text):
            self.assertTrue((SOURCE.parent / image).is_file(), image)

    def test_original_pdf_formula_corrections(self):
        text = SOURCE.read_text()
        for line, formula in (
            (509, r"\frac{\mathrm{e}^{ax}+x^2-ax-1}{\frac14x^2}"),
            (1091, r"a^{2} f'''(x_{0})"),
            (2904, r"a>0,f(t)"),
        ):
            question = re.search(rf"% SOURCE line={line} .*?\n(.*?)\\Solution", text, re.S)[1]
            self.assertIn(formula, question)

    def test_corrected_continuity_limits(self):
        for x in (-0.001, -0.0001):
            self.assertAlmostEqual(math.log1p(-x**3)/(x-math.asin(x)), 6, delta=0.001)
        for x in (0.0001, 0.001):
            self.assertAlmostEqual((math.expm1(-x)+x+x*x)/(x*x/4), 6, delta=0.002)


if __name__ == "__main__":
    unittest.main()
