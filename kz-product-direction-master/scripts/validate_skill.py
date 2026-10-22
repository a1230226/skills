#!/usr/bin/env python3
"""工程化校验 kz-product-direction-master Skill 本身。"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "scripts/validate_skill.py",
    "references/workflows/product_direction_mapping.md",
    "references/templates/product_direction_brief_template.md",
    "references/templates/product_direction_reference_template.md",
    "references/examples/index.md",
    "references/examples/input-template-product-direction-workflow.md",
    "references/examples/input-template-core-chain-breakdown-education-ai.md",
    "references/directions/education_ai.md",
]


def _read_text(path: Path):
    return path.read_text(encoding="utf-8")


def _extract_frontmatter(markdown: str):
    match = re.match(r"\A---\s*\n([\s\S]*?)\n---\s*\n", markdown)
    if not match:
        return None
    return match.group(1)


def _has_required_frontmatter(frontmatter: str):
    required_keys = ["name:", "description:", "version:"]
    return all(key in frontmatter for key in required_keys)


def _extract_head_version(markdown: str):
    match = re.search(r"^> \*\*版本\*\*: v([0-9]+\.[0-9]+\.[0-9]+)\s*$", markdown, re.MULTILINE)
    return match.group(1) if match else None


def _extract_history_version(markdown: str):
    match = re.search(r"^## 版本历史\s*\n\s*\n- \*\*v([0-9]+\.[0-9]+\.[0-9]+)\*\*", markdown, re.MULTILINE)
    return match.group(1) if match else None


def _extract_frontmatter_version(frontmatter: str):
    match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", frontmatter, re.MULTILINE)
    return match.group(1) if match else None


def verify(skill_dir: Path):
    errors = []

    for relative in REQUIRED_FILES:
        if not (skill_dir / relative).exists():
            errors.append("Missing required file: " + relative)

    skill_md = skill_dir / "SKILL.md"
    content = ""
    frontmatter = None
    if not skill_md.exists():
        errors.append("Missing SKILL.md: " + str(skill_md))
    else:
        try:
            content = _read_text(skill_md)
        except Exception as e:
            errors.append("Failed to read SKILL.md: " + str(e))

    if content:
        frontmatter = _extract_frontmatter(content)
        if not frontmatter:
            errors.append("SKILL.md missing YAML frontmatter (--- ... ---)")
        elif not _has_required_frontmatter(frontmatter):
            errors.append("SKILL.md frontmatter must include name/description/version")

        if "## @工作流:" not in content:
            errors.append("SKILL.md must include a '## @工作流:' section")
        if "### @步骤1:" not in content:
            errors.append("SKILL.md must include at least one '### @步骤1:' section")
        if "## 版本历史" not in content:
            errors.append("SKILL.md must include a '## 版本历史' section")
        if "[TODO" in content or "YYYY-MM-DD" in content:
            errors.append("SKILL.md still contains TODO or placeholder date text")

        if frontmatter:
            fm_version = _extract_frontmatter_version(frontmatter)
            head_version = _extract_head_version(content)
            history_version = _extract_history_version(content)
            if not fm_version or not head_version or not history_version:
                errors.append("Version must exist in frontmatter, header block, and first history entry")
            elif len({fm_version, head_version, history_version}) != 1:
                errors.append("Version mismatch among frontmatter/header/history")

            history_entries = re.findall(r"^- \*\*v[0-9]+\.[0-9]+\.[0-9]+\*\*", content, re.MULTILINE)
            if len(history_entries) > 5:
                errors.append("Version history must keep at most 5 entries")

    if errors:
        for message in errors:
            print("ERROR: " + message)
        return 1

    print("OK: basic skill structure checks passed")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, help="Skill folder path")
    args = parser.parse_args()

    skill_dir = Path(args.skill).resolve()
    if not skill_dir.exists():
        print("ERROR: skill folder not found: " + str(skill_dir))
        sys.exit(1)

    sys.exit(verify(skill_dir))

if __name__ == "__main__":
    main()
