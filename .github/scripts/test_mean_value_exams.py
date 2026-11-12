from pathlib import Path
import math
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
FILES = [ROOT / f"output/中值定理阶段模拟卷{number}.tex" for number in (1, 2, 3)]


class MeanValueExamTests(unittest.TestCase):
    def test_three_complete_papers(self):
        for path in FILES:
            with self.subTest(path=path.name):
                source = path.read_text()
                questions = re.findall(r"^\\Question\{(\d+)\}\{([^}]+)\}\{(\d+)\}\{([^}]+)\}", source, re.M)
                self.assertEqual([int(q[0]) for q in questions], list(range(1, 13)))
                self.assertEqual([q[1] for q in questions], ["单项选择"] * 4 + ["填空"] * 4 + ["解答"] * 4)
                self.assertEqual(sum(int(q[2]) for q in questions), 100)
                blocks = re.split(r"^\\Question\{", source, flags=re.M)[1:]
                for block in blocks:
                    self.assertEqual(block.count(r"\Solution"), 1)
                    for label in (r"\Known", r"\Method", r"\Derive", r"\Check"):
                        self.assertEqual(block.count(label), 1)
                self.assertEqual(source.count(r"\Choices{"), 4)
                self.assertIn("paperwidth=800bp,paperheight=600bp", source)
                self.assertIn(r"\operatorname*{lim}\limits", source)
                self.assertNotIn(r"\tfrac", source)
                self.assertNotIn(r"\int", source)
                for line in source.splitlines():
                    if not line.startswith("%") and "references/" not in line:
                        self.assertNotRegex(line, r"(?<=[0-9a-z)])/+(?=[0-9a-z(])")

    def test_selected_limits_from_original_expressions(self):
        for x in (-0.001, 0.001):
            cases = {
                "1-1": ((x - math.sin(x)) / (x*x * math.log1p(x/6)), 1),
                "1-9": ((1-math.cos(x)) * (x-math.log1p(math.tan(x))) / math.sin(x)**4, 0.25),
                "2-4": (0.75 * (2-math.sin(x)/x-math.cos(x)) / x**2, 0.5),
                "2-5": ((1/(1+x*x)-math.cos(x))/x**2, -0.5),
                "2-6": ((math.sqrt(1+x*x)-math.cos(x))/(x*math.sin(x)), 1),
                "2-9": ((2*math.sin(x)-4*x*x+2*math.log1p(-x)) / -math.expm1(5*x*x), 1),
                "2-10": ((x*(x-1)+math.exp(x*x)*math.sin(x))/x**2, 1),
                "3-3": ((math.tan(x)+x*(-1+x*x/3))/x**3, 2/3),
                "3-5": ((2+x)/math.sin(x)-2/x, 1),
                "3-6": ((-x+2*x*x+math.log1p(x)) / (math.expm1(x*x)+1-math.cos(x)), 1),
                "3-8": (math.exp(math.log(math.expm1(x)/math.sin(x))/math.tan(x)), math.sqrt(math.e)),
                "3-9": ((x*(2+5*x)-math.expm1(2*math.sin(x))) / math.log1p(-x*x), -3),
            }
            for question, (actual, expected) in cases.items():
                with self.subTest(question=question, x=x):
                    self.assertAlmostEqual(actual, expected, delta=0.003)

    def test_parameter_derivatives_and_functional_identity(self):
        step = 0.0001
        y = lambda x: math.exp(math.exp(2*x))
        self.assertAlmostEqual((y(step)-2*y(0)+y(-step))/step**2, 8*math.e, delta=0.00001)
        f = lambda x: math.log(x)/x
        for x in (0.2, 1, 2, 5):
            for y in (0.3, 1, 3):
                self.assertAlmostEqual(f(x*y), f(x)/y+f(y)/x)
        self.assertAlmostEqual((f(1+step)-f(1-step))/(2*step), 1, delta=0.000001)

    def test_recurrence_for_initial_values_on_both_sides_of_three(self):
        for initial in (2.01, 2.1, 2.5, 3, 3.1, 4, 10, 100):
            value = initial
            for _ in range(1500):
                self.assertGreater(value, 2)
                following = value - (value-3)/(value-2)
                self.assertGreaterEqual(following, 3)
                if value >= 3:
                    self.assertLessEqual(following, value)
                value = following
            self.assertAlmostEqual(value, 3)


if __name__ == "__main__":
    unittest.main()
