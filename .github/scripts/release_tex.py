import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode


WIDE_SOURCE = "output/302数学二分节真题集（原生LaTeX横屏版）.tex"
DEPENDENTS = {
    WIDE_SOURCE: "output/302数学二分节真题集（原生LaTeX常规版）.tex",
    "output/302-question-facsimiles.pdf": "output/302数学二分节真题集.tex",
}
ASSET_NAMES = {
    WIDE_SOURCE: "math-ii-past-exams-landscape.pdf",
    DEPENDENTS[WIDE_SOURCE]: "math-ii-past-exams-a4.pdf",
    DEPENDENTS["output/302-question-facsimiles.pdf"]: "math-ii-past-exams-facsimile.pdf",
    "output/27302阶段模拟卷.tex": "27302-mock-exam-1.pdf",
    "output/27302阶段模拟卷（第二至五卷及补充练习）.tex": "27302-mock-exams-2-5.pdf",
}
VERSION = re.compile(r"v0\.0\.([1-9][0-9]*)")


def git(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo, encoding="utf-8")


def plan(repo, before, after):
    tracked = set(git(repo, "ls-tree", "-rz", "--name-only", after, "--", "output/").split("\0"))
    initial = before == "0" * 40
    changed = tracked if initial else set(git(
        repo, "diff", "--no-renames", "--name-only", "-z", before, after, "--", "output/"
    ).split("\0"))
    affected = changed | {DEPENDENTS[path] for path in changed & DEPENDENTS.keys()}
    files = sorted(path for path in affected & tracked if path.endswith(".tex"))
    if not files:
        return {"files": [], "notes": ""}

    inputs = set(files) | {path for path, entry in DEPENDENTS.items() if entry in files}
    commits = after if initial else f"{before}..{after}"
    summaries = git(repo, "log", "--reverse", "--format=%(trailers:key=Release-Note,valueonly,unfold)",
                    commits, "--", *sorted(changed & inputs)).splitlines()
    notes = "\n".join(f"- {line}" for line in dict.fromkeys(line.strip() for line in summaries if line.strip()))
    if not notes:
        titles = "、".join(f"《{Path(path).stem}》" for path in files)
        notes = f"更新{titles}的 PDF。"
    return {"files": files, "notes": notes}


def next_release(releases, tags, run_id):
    versions = [release for release in releases if VERSION.fullmatch(release["tag_name"])]
    marker = f"\n\n<!-- latex-release-run: {run_id} -->"
    for release in versions:
        if (release["body"] or "").endswith(marker):
            return (release["tag_name"], release["id"]) if release["draft"] else (None, None)

    for release in versions:
        if release["draft"]:
            raise ValueError(f"{release['tag_name']} 仍是草稿，请先重跑对应的发布任务。")

    latest = max((int(VERSION.fullmatch(release["tag_name"])[1]) for release in versions), default=0)
    if latest >= 999:
        raise ValueError("已达到 v0.0.999，后续版本须经用户批准。")
    tag = f"v0.0.{latest + 1}"
    if tag in tags:
        raise ValueError(f"标签 {tag} 已存在，但没有对应的 Release。")
    return tag, None


def compile_pdfs(files, destination):
    destination.mkdir()
    for name in files:
        source = Path(name)
        asset = destination / asset_name(name)
        subprocess.run(["tectonic", "--untrusted", "--outdir", str(destination), "--", source.name],
                       cwd=source.parent, check=True)
        pdf = destination / source.with_suffix(".pdf").name
        if not pdf.is_file() or pdf.stat().st_size == 0:
            raise ValueError(f"未生成 PDF：{source}")
        pdf.rename(asset)


def asset_name(source):
    if source in ASSET_NAMES:
        return ASSET_NAMES[source]
    return f"document-{hashlib.sha256(source.encode()).hexdigest()[:12]}.pdf"


def github(endpoint, *args):
    response = subprocess.check_output(["gh", "api", endpoint, *args], encoding="utf-8")
    return json.loads(response) if response else None


def publish(release_plan, directory):
    repository = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    endpoint = f"repos/{repository}/releases"
    releases = github(f"{endpoint}?per_page=100", "--paginate", "--slurp")
    tags = git(Path.cwd(), "ls-remote", "--tags", "--refs", "origin", "refs/tags/v0.0.*")
    tag, draft_id = next_release(
        [release for page in releases for release in page],
        {line.split()[1].removeprefix("refs/tags/") for line in tags.splitlines()},
        run_id,
    )
    if tag is None:
        print("本次推送的 Release 已发布。")
        return

    if draft_id is None:
        body = f"{release_plan['notes']}\n\n<!-- latex-release-run: {run_id} -->"
        draft = github(endpoint, "--method", "POST", "-f", f"tag_name={tag}", "-f", f"name={tag}",
                       "-f", f"target_commitish={os.environ['GITHUB_SHA']}", "-f", f"body={body}",
                       "-F", "draft=true")
        draft_id = draft["id"]

    draft_endpoint = f"{endpoint}/{draft_id}"
    assets = github(f"{draft_endpoint}/assets", "--paginate", "--slurp")
    existing = {asset["name"]: asset for page in assets for asset in page}
    for source in release_plan["files"]:
        name = asset_name(source)
        previous = existing.get(name)
        if previous and previous["state"] == "uploaded" and previous["size"] > 0:
            continue
        if previous:
            github(f"{endpoint}/assets/{previous['id']}", "--method", "DELETE")
        query = urlencode({"name": name, "label": Path(source).with_suffix(".pdf").name})
        pdf = directory / name
        size = pdf.stat().st_size
        asset = github(f"https://uploads.github.com/{draft_endpoint}/assets?{query}", "--method", "POST",
                       "-H", "Content-Type: application/pdf", "-H", f"Content-Length: {size}",
                       "--input", str(pdf))
        if asset["state"] != "uploaded" or asset["size"] != size:
            raise ValueError(f"PDF 附件上传不完整：{name}")

    release = github(draft_endpoint, "--method", "PATCH", "-F", "draft=false")
    print(release["html_url"])


if __name__ == "__main__":
    command, first, second = sys.argv[1:]
    try:
        if command == "plan":
            print(json.dumps(plan(Path.cwd(), first, second), ensure_ascii=False))
        else:
            release_plan = json.loads(Path(first).read_text(encoding="utf-8"))
            destination = Path(second).resolve()
            if command == "compile":
                compile_pdfs(release_plan["files"], destination)
            elif command == "publish":
                publish(release_plan, destination)
            else:
                raise ValueError(f"未知命令：{command}")
    except (ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
