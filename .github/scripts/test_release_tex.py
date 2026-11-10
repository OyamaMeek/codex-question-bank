import subprocess
import tempfile
import unittest
from pathlib import Path

import release_tex


class PushPlanTests(unittest.TestCase):
    def setUp(self):
        work = Path(__file__).resolve().parents[2] / ".release-work"
        work.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Release Tests")
        self.git("config", "user.email", "release-tests@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.first = "output/27302阶段模拟卷.tex"
        self.wide = "output/302数学二分节真题集（原生LaTeX横屏版）.tex"
        self.a4 = "output/302数学二分节真题集（原生LaTeX常规版）.tex"
        self.facsimile = "output/302数学二分节真题集.tex"
        self.resource = "output/302-question-facsimiles.pdf"
        for path in (self.first, self.wide, self.a4, self.facsimile, self.resource):
            self.write(path, "initial")
        self.before = self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def write(self, name, contents):
        path = self.repo / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    def commit(self, note=""):
        self.git("add", "-A")
        self.git("commit", "-qm", f"Update\n\n{note}")
        return self.git("rev-parse", "HEAD")

    def test_combines_commits_and_includes_shared_entry(self):
        self.write(self.first, "fix")
        self.commit("Release-Note: 修正第一卷的积分公式")
        self.write(self.wide, "new solutions")
        after = self.commit("Release-Note: 补充真题解析")
        plan = release_tex.plan(self.repo, self.before, after)
        self.assertEqual(set(plan["files"]), {self.first, self.wide, self.a4})
        self.assertEqual(plan["notes"], "- 修正第一卷的积分公式\n- 补充真题解析")

    def test_rebuilds_only_the_tex_that_uses_a_changed_asset(self):
        self.write(self.resource, "updated facsimile")
        plan = release_tex.plan(self.repo, self.before, self.commit())
        self.assertEqual(plan["files"], [self.facsimile])
        self.assertIn("更新《302数学二分节真题集》", plan["notes"])

    def test_ignores_readme_changes_and_removed_standalone_sources(self):
        self.write("README.md", "new instructions")
        (self.repo / self.first).unlink()
        plan = release_tex.plan(self.repo, self.before, self.commit())
        self.assertEqual(plan["files"], [])

    def test_missing_shared_source_still_selects_its_dependent(self):
        (self.repo / self.wide).unlink()
        plan = release_tex.plan(self.repo, self.before, self.commit())
        self.assertEqual(plan["files"], [self.a4])


class ReleaseVersionTests(unittest.TestCase):
    def release(self, tag, *, draft=False, run_id=100):
        return {"id": 44, "tag_name": tag, "draft": draft,
                "body": f"更新模拟卷\n\n<!-- latex-release-run: {run_id} -->"}

    def test_starts_at_one_and_sorts_versions_numerically(self):
        self.assertEqual(release_tex.next_release([], [], "101"), ("v0.0.1", None))
        releases = [self.release("v0.0.9"), self.release("v0.0.10")]
        self.assertEqual(release_tex.next_release(releases, [], "101"), ("v0.0.11", None))

    def test_stops_at_999(self):
        self.assertEqual(release_tex.next_release([self.release("v0.0.998")], [], "101"),
                         ("v0.0.999", None))
        with self.assertRaisesRegex(ValueError, "v0.0.999"):
            release_tex.next_release([self.release("v0.0.999")], [], "101")

    def test_retry_resumes_its_draft_and_skips_its_published_release(self):
        draft = self.release("v0.0.1", draft=True)
        self.assertEqual(release_tex.next_release([draft], [], "100"), ("v0.0.1", 44))
        self.assertEqual(release_tex.next_release([self.release("v0.0.1")], [], "100"),
                         (None, None))

    def test_does_not_bypass_an_unfinished_release_or_reuse_a_tag(self):
        with self.assertRaisesRegex(ValueError, "草稿"):
            release_tex.next_release([self.release("v0.0.1", draft=True)], [], "101")
        with self.assertRaisesRegex(ValueError, "标签"):
            release_tex.next_release([], ["v0.0.1"], "101")


if __name__ == "__main__":
    unittest.main()
