#!/usr/bin/env python3
"""Scan repository structure for kz-project-init."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


MANIFEST_NAMES = [
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "Makefile",
]

COMMAND_ENTRY_NAMES = [
    "justfile",
    "Justfile",
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
]

PYTHON_ENV_SIGNAL_NAMES = [
    ".conda.env",
    "environment.yml",
    "environment.yaml",
    "conda.yml",
    "conda.yaml",
    "requirements.txt",
    "requirements-dev.txt",
    "runtime.txt",
    "poetry.lock",
    "uv.lock",
    "Pipfile",
    "Pipfile.lock",
    "setup.py",
]

DOC_NAMES = [
    "README.md",
    "README.MD",
    "readme.md",
    "AGENTS.md",
    "project-context.md",
    "contributing.md",
    "CONTRIBUTING.md",
]

AGENT_DOC_NAMES = [
    "AGENTS.md",
    "project-context.md",
]

IGNORE_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

BMAD_HIGH_SIGNAL_FILE_NAMES = {
    "project-brief.md",
    "product-brief.md",
    "project-context.md",
    "sprint-status.md",
    "sprint-status.yaml",
    "sprint-status.yml",
    "architecture.md",
    "prd.md",
    "epics.md",
    "stories.md",
    "index.md",
    "readme.md",
    "README.md",
}

BMAD_HIGH_SIGNAL_NAME_PARTS = [
    "brief",
    "context",
    "architecture",
    "arch",
    "prd",
    "story",
    "stories",
    "sprint",
    "epic",
    "roadmap",
    "plan",
    "status",
    "requirements",
]

BMAD_ALLOWED_SUFFIXES = {".md", ".yaml", ".yml", ".txt", ".json"}


def walk_paths(root: Path):
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORE_DIR_NAMES)
        yield Path(current_root), dirnames, filenames


def find_git_roots(root: Path) -> list[Path]:
    git_roots: list[Path] = []
    for current, _, _ in walk_paths(root):
        git_marker = current / ".git"
        if git_marker.exists():
            git_roots.append(current)
    return sorted(set(git_roots))


def find_named_files(root: Path, names: list[str]) -> list[Path]:
    target_names = set(names)
    matches: list[Path] = []
    for current, _, filenames in walk_paths(root):
        for name in filenames:
            if name in target_names:
                matches.append(current / name)
    return sorted(set(matches))


def find_named_dirs(root: Path, names: list[str]) -> list[Path]:
    target_names = set(names)
    matches: list[Path] = []
    for current, dirnames, _ in walk_paths(root):
        for name in dirnames:
            if name in target_names:
                matches.append(current / name)
    return sorted(set(matches))


def find_matching_files(root: Path, predicate) -> list[Path]:
    matches: list[Path] = []
    for current, _, filenames in walk_paths(root):
        for name in filenames:
            path = current / name
            if predicate(path):
                matches.append(path)
    return sorted(set(matches))


def classify_repo_type(git_roots: list[Path], root: Path, manifests: list[Path]) -> str:
    if not git_roots:
        return "no-git"
    if len(git_roots) == 1 and git_roots[0] != root:
        return "single-subrepo"
    if len(git_roots) > 1:
        return "nested-multi-repo"
    if len(manifests) > 1:
        return "monorepo"
    return "single-repo"


def relative_paths(root: Path, paths: list[Path]) -> list[str]:
    return [str(path.relative_to(root)) for path in paths]


def is_within(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def extract_conda_env_name_hint(conda_env_file: Path | None) -> str | None:
    if conda_env_file is None or not conda_env_file.exists():
        return None

    for raw_line in read_text_safe(conda_env_file).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        return line
    return None


def detect_python_env_signals(root: Path, manifests: list[Path]) -> dict[str, object]:
    python_env_files = find_named_files(root, PYTHON_ENV_SIGNAL_NAMES)
    pyproject_files = [path for path in manifests if path.name == "pyproject.toml"]
    all_python_signal_files = sorted(set([*python_env_files, *pyproject_files]))
    conda_env_file = next((path for path in python_env_files if path.name == ".conda.env"), None)

    recommended_python_env_manager = None
    signal_names = {path.name for path in all_python_signal_files}
    if conda_env_file or {"environment.yml", "environment.yaml", "conda.yml", "conda.yaml"} & signal_names:
        recommended_python_env_manager = "conda"
    elif "poetry.lock" in signal_names:
        recommended_python_env_manager = "poetry"
    elif "uv.lock" in signal_names:
        recommended_python_env_manager = "uv"
    elif signal_names & {"requirements.txt", "requirements-dev.txt", "Pipfile", "Pipfile.lock", "setup.py"}:
        recommended_python_env_manager = "pip"

    return {
        "python_project": bool(all_python_signal_files),
        "python_env_files": relative_paths(root, all_python_signal_files),
        "conda_env_file": str(conda_env_file.relative_to(root)) if conda_env_file else None,
        "conda_env_name_hint": extract_conda_env_name_hint(conda_env_file),
        "recommended_python_env_manager": recommended_python_env_manager,
    }


def score_bmad_candidate(path: Path) -> tuple[int, str]:
    name_lower = path.name.lower()
    score = 0
    reasons: list[str] = []

    if path.suffix.lower() in BMAD_ALLOWED_SUFFIXES:
        score += 1
        reasons.append("allowed_suffix")

    if name_lower in {name.lower() for name in BMAD_HIGH_SIGNAL_FILE_NAMES}:
        score += 4
        reasons.append("high_signal_name")

    for part in BMAD_HIGH_SIGNAL_NAME_PARTS:
        if part in name_lower:
            score += 2
            reasons.append(f"name_part:{part}")
            break

    path_lower = path.as_posix().lower()
    if any(part in path_lower for part in ["story", "stories", "sprint", "epic", "architecture", "prd"]):
        score += 1
        reasons.append("path_signal")

    return score, ",".join(reasons)


def collect_bmad_context_candidates(root: Path, bmad_dirs: list[Path]) -> dict[str, object]:
    bmad_output_dirs = [path for path in bmad_dirs if path.name == "_bmad-output"]
    candidates: list[tuple[Path, int, str]] = []

    for bmad_root in bmad_output_dirs:
        for current, _, filenames in walk_paths(bmad_root):
            for filename in filenames:
                path = current / filename
                score, reasons = score_bmad_candidate(path)
                if score >= 3:
                    candidates.append((path, score, reasons))

    candidates.sort(key=lambda item: (-item[1], str(item[0].relative_to(root))))
    top_candidates = candidates[:12]

    return {
        "bmad_context_files": [str(path.relative_to(root)) for path, _, _ in top_candidates],
        "bmad_context_file_scores": [
            {
                "path": str(path.relative_to(root)),
                "score": score,
                "reasons": reasons,
            }
            for path, score, reasons in top_candidates
        ],
    }


def build_reading_priority(
    root: Path,
    docs: list[Path],
    agent_docs: list[Path],
    bmad_context_files: list[str],
) -> list[dict[str, object]]:
    items: list[tuple[int, str, str, str]] = []

    for path in agent_docs:
        rel = str(path.relative_to(root))
        if path.name == "AGENTS.md":
            items.append((100, rel, "rules", "先读执行规则、Git 路由、命令入口与收尾约束"))
        elif path.name == "project-context.md":
            items.append((90, rel, "context", "再读项目画像、结构理解框架与常见误判提醒"))

    for path in docs:
        rel = str(path.relative_to(root))
        lower_name = path.name.lower()
        if lower_name != "readme.md" or rel in {item[1] for item in items}:
            continue
        parent_parts = path.parent.parts
        if any(part.startswith(".") for part in parent_parts):
            continue
        if rel in {"README.md", "readme.md"}:
            items.append((80, rel, "readme", "补充项目目标、功能概览、运行说明与目录背景"))
            continue
        if rel.startswith("kz_dash/"):
            items.append((68, rel, "readme", "若任务涉及子仓库，再读该子仓库 README 获取局部背景"))

    for idx, rel in enumerate(bmad_context_files[:8]):
        score = 60 - idx
        items.append((score, rel, "bmad", "项目已接入 BMAD；按优先级读取这些文档强化目标、阶段、架构或 story 上下文"))

    dedup: dict[str, tuple[int, str, str, str]] = {}
    for item in items:
        path = item[1]
        if path not in dedup or item[0] > dedup[path][0]:
            dedup[path] = item

    sorted_items = sorted(dedup.values(), key=lambda item: (-item[0], item[1]))
    return [
        {
            "priority": index + 1,
            "path": path,
            "kind": kind,
            "score": score,
            "why": why,
        }
        for index, (score, path, kind, why) in enumerate(sorted_items)
    ]


def summarize_git_roots(
    root: Path,
    git_roots: list[Path],
    manifests: list[Path],
    docs: list[Path],
    bmad_dirs: list[Path],
    common_code_dirs: list[Path],
    test_dirs: list[Path],
) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    for git_root in git_roots:
        summaries.append(
            {
                "path": str(git_root.relative_to(root)),
                "manifests": relative_paths(root, [path for path in manifests if is_within(git_root, path)]),
                "docs": relative_paths(root, [path for path in docs if is_within(git_root, path)]),
                "bmad_dirs": relative_paths(root, [path for path in bmad_dirs if is_within(git_root, path)]),
                "code_dirs": relative_paths(root, [path for path in common_code_dirs if is_within(git_root, path)]),
                "test_dirs": relative_paths(root, [path for path in test_dirs if is_within(git_root, path)]),
            }
        )
    return summaries


def collect_scan(root: Path) -> dict[str, object]:
    git_roots = find_git_roots(root)
    manifests = find_named_files(root, MANIFEST_NAMES)
    command_entry_files = find_named_files(root, COMMAND_ENTRY_NAMES)
    docs = find_named_files(root, DOC_NAMES)
    bmad_dirs = find_named_dirs(root, ["_bmad", "_bmad-output"])
    common_code_dirs = find_named_dirs(root, ["src", "server", "app", "backend", "frontend"])
    test_dirs = find_named_dirs(root, ["tests", "test"])
    docs_roots = find_named_dirs(root, ["docs", "doc", "documentation"])
    snapshot_dirs = find_named_dirs(root, ["snapshots", "__snapshots__"])
    fixture_dirs = find_named_dirs(root, ["fixture", "fixtures"])
    issue_template_dirs = find_named_dirs(root, ["ISSUE_TEMPLATE"])
    agent_docs = [path for path in docs if path.name in AGENT_DOC_NAMES]
    workflow_files = find_matching_files(
        root,
        lambda path: ".github/workflows" in path.as_posix() and path.suffix in {".yml", ".yaml"},
    )
    schema_files = find_matching_files(
        root,
        lambda path: path.name.endswith(".schema.json") or "schema" in path.name.lower(),
    )
    contributing_docs = find_matching_files(
        root,
        lambda path: path.name in {"contributing.md", "CONTRIBUTING.md"},
    )
    python_env_signals = detect_python_env_signals(root, manifests)
    bmad_context = collect_bmad_context_candidates(root, bmad_dirs)
    reading_priority = build_reading_priority(
        root,
        docs,
        agent_docs,
        bmad_context["bmad_context_files"],
    )

    return {
        "root": str(root),
        "repo_type": classify_repo_type(git_roots, root, manifests),
        "git_roots": relative_paths(root, git_roots),
        "manifests": relative_paths(root, manifests),
        "command_entry_files": relative_paths(root, command_entry_files),
        "docs": relative_paths(root, docs),
        "agent_docs": relative_paths(root, agent_docs),
        "contributing_docs": relative_paths(root, contributing_docs),
        "docs_roots": relative_paths(root, docs_roots),
        "bmad_dirs": relative_paths(root, bmad_dirs),
        "bmad_context_files": bmad_context["bmad_context_files"],
        "bmad_context_file_scores": bmad_context["bmad_context_file_scores"],
        "reading_priority": reading_priority,
        "common_code_dirs": relative_paths(root, common_code_dirs),
        "test_dirs": relative_paths(root, test_dirs),
        "workflow_files": relative_paths(root, workflow_files),
        "snapshot_dirs": relative_paths(root, snapshot_dirs),
        "fixture_dirs": relative_paths(root, fixture_dirs),
        "schema_files": relative_paths(root, schema_files),
        "issue_template_dirs": relative_paths(root, issue_template_dirs),
        "python_project": python_env_signals["python_project"],
        "python_env_files": python_env_signals["python_env_files"],
        "conda_env_file": python_env_signals["conda_env_file"],
        "conda_env_name_hint": python_env_signals["conda_env_name_hint"],
        "recommended_python_env_manager": python_env_signals["recommended_python_env_manager"],
        "git_repo_summaries": summarize_git_roots(
            root,
            git_roots,
            manifests,
            docs,
            bmad_dirs,
            common_code_dirs,
            test_dirs,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Target root to scan")
    parser.add_argument(
        "--format",
        choices=["json", "pretty"],
        default="pretty",
        help="Output format",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = collect_scan(root)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"root: {result['root']}")
        print(f"repo_type: {result['repo_type']}")
        print(f"python_project: {result['python_project']}")
        print(f"conda_env_file: {result['conda_env_file'] or '<none>'}")
        print(f"conda_env_name_hint: {result['conda_env_name_hint'] or '<none>'}")
        print(
            "recommended_python_env_manager: "
            f"{result['recommended_python_env_manager'] or '<none>'}"
        )
        for key in [
            "git_roots",
            "manifests",
            "command_entry_files",
            "docs",
            "agent_docs",
            "contributing_docs",
            "docs_roots",
            "bmad_dirs",
            "bmad_context_files",
            "common_code_dirs",
            "test_dirs",
            "workflow_files",
            "snapshot_dirs",
            "fixture_dirs",
            "schema_files",
            "issue_template_dirs",
            "python_env_files",
        ]:
            print(f"{key}:")
            values = result[key]
            if not values:
                print("  - <none>")
                continue
            for value in values:
                print(f"  - {value}")
        print("reading_priority:")
        if not result["reading_priority"]:
            print("  - <none>")
        else:
            for item in result["reading_priority"]:
                print(f"  - priority: {item['priority']}")
                print(f"    path: {item['path']}")
                print(f"    kind: {item['kind']}")
                print(f"    score: {item['score']}")
                print(f"    why: {item['why']}")
        print("bmad_context_file_scores:")
        if not result["bmad_context_file_scores"]:
            print("  - <none>")
        else:
            for item in result["bmad_context_file_scores"]:
                print(f"  - path: {item['path']}")
                print(f"    score: {item['score']}")
                print(f"    reasons: {item['reasons']}")
        print("git_repo_summaries:")
        if not result["git_repo_summaries"]:
            print("  - <none>")
        else:
            for summary in result["git_repo_summaries"]:
                print(f"  - path: {summary['path']}")
                for key in ["manifests", "docs", "bmad_dirs", "code_dirs", "test_dirs"]:
                    values = summary[key]
                    if not values:
                        continue
                    print(f"    {key}:")
                    for value in values:
                        print(f"      - {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
