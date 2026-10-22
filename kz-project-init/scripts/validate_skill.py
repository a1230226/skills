#!/usr/bin/env python3
"""Deterministic validation for the kz-project-init skill."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter(markdown: str) -> str | None:
    match = re.match(r"\A---\s*\n([\s\S]*?)\n---\s*\n", markdown)
    return match.group(1) if match else None


def extract_frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else None


def extract_body_version(content: str) -> str | None:
    match = re.search(r"^> \*\*版本\*\*: v([0-9]+\.[0-9]+\.[0-9]+)$", content, re.MULTILINE)
    return match.group(1) if match else None


def extract_history_versions(content: str) -> list[str]:
    return re.findall(r"^-\s+\*\*v([0-9]+\.[0-9]+\.[0-9]+)\*\*", content, re.MULTILINE)


def validate(skill_dir: Path) -> int:
    errors: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    repo_discovery = skill_dir / "references" / "repo-discovery.md"
    output_contract = skill_dir / "references" / "output-contract.md"
    repo_operating_system = skill_dir / "references" / "repo-operating-system.md"
    template = skill_dir / "assets" / "AGENTS.template.md"
    scan_repo = skill_dir / "scripts" / "scan_repo.py"

    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        content = read_text(skill_md)
        scan_repo_content = read_text(scan_repo) if scan_repo.exists() else ""
        output_contract_content = read_text(output_contract) if output_contract.exists() else ""
        template_content = read_text(template) if template.exists() else ""
        frontmatter = extract_frontmatter(content)
        if not frontmatter:
            errors.append("SKILL.md missing YAML frontmatter")
        else:
            name = extract_frontmatter_value(frontmatter, "name")
            description = extract_frontmatter_value(frontmatter, "description")
            version = extract_frontmatter_value(frontmatter, "version")
            body_version = extract_body_version(content)
            history_versions = extract_history_versions(content)

            if name != "kz-project-init":
                errors.append("frontmatter name must be kz-project-init")
            if not description:
                errors.append("frontmatter description must be non-empty")
            if not version:
                errors.append("frontmatter version missing")
            if version and body_version and version != body_version:
                errors.append("frontmatter version and body version must match")
            if version and history_versions and version != history_versions[0]:
                errors.append("frontmatter version and latest history entry must match")
            if len(history_versions) > 5:
                errors.append("version history must keep at most 5 entries")

        required_strings = [
            "AGENTS.md",
            "project-context.md",
            "scripts/scan_repo.py",
            "repo-discovery.md",
            "output-contract.md",
            "nested-multi-repo",
            "single-subrepo",
            "OUTPUT_LANGUAGE",
            "English",
            "repo-operating-system.md",
            "command_entry_files",
            "workflow_files",
            "高风险事实先确认",
            ".conda.env",
            "确认 Python 环境事实",
            "提炼项目画像",
            "_bmad-output/",
            "BMAD",
            "conda.yml",
            "environment.yml",
            "用户确认",
            "本轮完成度",
            "主线目标是否完成",
            "已执行的验证",
            "未完成 / 阻塞项",
            "下一刀建议",
            "整体目标完成度",
            "百分比口径",
            "任务收尾说明",
            "reading_priority",
        ]
        for item in required_strings:
            if item not in content:
                errors.append(f"SKILL.md missing required text: {item}")

        output_contract_required_strings = [
            "本轮完成度",
            "主线目标是否完成",
            "已完成的关键改动",
            "已执行的验证",
            "未完成 / 阻塞项",
            "下一刀建议",
            "整体目标完成度",
            "百分比口径",
            "先回答主线是否完成",
            "不要只写“任务已完成”",
            "外部阻塞",
            "验证缺口",
            "可选优化",
        ]
        for item in output_contract_required_strings:
            if item not in output_contract_content:
                errors.append(f"output-contract.md missing required text: {item}")

        if "## @工作流:" not in content:
            errors.append("SKILL.md must include at least one @工作流 section")

        scan_repo_required_strings = [
            "python_project",
            "python_env_files",
            "conda_env_file",
            "conda_env_name_hint",
            "recommended_python_env_manager",
            "bmad_context_files",
            "bmad_context_file_scores",
            "reading_priority",
            "_bmad-output",
            ".conda.env",
            "environment.yml",
            "conda.yml",
        ]
        for item in scan_repo_required_strings:
            if item not in scan_repo_content:
                errors.append(f"scan_repo.py missing required text: {item}")

        template_required_strings = [
            "## Python 环境",
            "`.conda.env`",
            "推荐 conda 环境",
            "用户确认状态",
            "Git 根路由",
            "分支与收尾约定",
            "本地入口与门禁映射",
            "复杂拓扑补充说明",
            "## 任务收尾说明",
            "本轮完成度",
            "主线目标是否完成",
            "已完成的关键改动",
            "已执行的验证",
            "未完成 / 阻塞项",
            "下一刀建议",
            "整体目标完成度（多阶段任务时）",
            "百分比口径（多阶段任务时）",
        ]
        for item in template_required_strings:
            if item not in template_content:
                errors.append(f"AGENTS.template.md missing required text: {item}")

    for path in [
        repo_discovery,
        output_contract,
        repo_operating_system,
        template,
        scan_repo,
    ]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(skill_dir)}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("OK: basic skill structure checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, help="Skill folder path")
    args = parser.parse_args()
    return validate(Path(args.skill).resolve())


if __name__ == "__main__":
    sys.exit(main())
