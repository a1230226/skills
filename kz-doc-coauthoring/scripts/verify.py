#!/usr/bin/env python3
"""
Verify script for kz-doc-coauthoring

This script provides deterministic checks that complement SKILL.md instructions.
"""

import argparse
from pathlib import Path
import re
import sys


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


def _extract_frontmatter_value(frontmatter: str, key: str):
    match = re.search(rf"(?m)^{re.escape(key)}\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        value = value[1:-1].strip()
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        value = value[1:-1].strip()
    return value


def _extract_version_from_frontmatter(frontmatter: str):
    value = _extract_frontmatter_value(frontmatter, "version:")
    if not value:
        return None
    if not re.match(r"^\d+\.\d+\.\d+$", value):
        return None
    return value


def _extract_author_from_frontmatter(frontmatter: str):
    match = re.search(r"(?m)^\s*author:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        value = value[1:-1].strip()
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        value = value[1:-1].strip()
    return value


def _extract_header_value(markdown: str, label: str):
    match = re.search(rf"(?m)^> \*\*{re.escape(label)}\*\*:\s*(.+?)\s*$", markdown)
    if not match:
        return None
    return match.group(1).strip()


def _validate_project_markdown(path: Path, label: str, require_workflow: bool = False):
    errors = []
    try:
        content = _read_text(path)
    except Exception as e:
        return ["Failed to read " + label + ": " + str(e)]

    frontmatter = _extract_frontmatter(content)
    if not frontmatter:
        errors.append(label + " missing YAML frontmatter (--- ... ---)")
        return errors

    if not _has_required_frontmatter(frontmatter):
        errors.append(label + " frontmatter must include name/description/version")

    version = _extract_version_from_frontmatter(frontmatter)
    if not version:
        errors.append(label + " frontmatter version must be semver like 1.0.0")
    else:
        header_version = _extract_header_value(content, "版本")
        if header_version != f"v{version}":
            errors.append(label + " header version must match frontmatter version")
        if f"**v{version}**" not in content:
            errors.append(label + " version history must include v" + version)

    if "## 版本历史" not in content:
        errors.append(label + " must include a '## 版本历史' section")

    if require_workflow:
        if "## @工作流:" not in content:
            errors.append(label + " must include a '## @工作流:' section")
        if not re.search(r"(?m)^### @步骤\d+:", content):
            errors.append(label + " must include at least one '### @步骤N:' section")
        if "- @动作:" not in content:
            errors.append(label + " must include at least one '- @动作:' line")

    return errors


def _validate_examples(skill_dir: Path):
    errors = []
    examples_dir = skill_dir / "references" / "examples"
    if not examples_dir.exists():
        return errors

    index_path = examples_dir / "index.md"
    if not index_path.exists():
        errors.append("Missing references/examples/index.md")
    else:
        index_content = _read_text(index_path)
        if "| 示例文件 | 场景内容 | 对应工作流 |" not in index_content:
            errors.append("references/examples/index.md missing examples table header")
        if "| 用户常见说法 | 命中矩阵行 | 建议先打开 |" not in index_content:
            errors.append("references/examples/index.md missing decision matrix lookup table")

    template_files = sorted(examples_dir.glob("input-template-*.md"))
    if len(template_files) < 3:
        errors.append("references/examples should include at least 3 input-template examples")

    required_sections = [
        "## 适用场景",
        "## 建议提供的信息",
        "## 可直接复制输入模板",
    ]
    for path in template_files:
        label = str(path.relative_to(skill_dir))
        errors.extend(_validate_project_markdown(path, label))
        content = _read_text(path)
        for section in required_sections:
            if section not in content:
                errors.append(label + " missing section: " + section)
        if "不负责工作流路由" not in content:
            errors.append(label + " must state '不负责工作流路由'")

    return errors


def verify(skill_dir: Path):
    errors = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md: " + str(skill_md))
    else:
        try:
            content = _read_text(skill_md)
        except Exception as e:
            errors.append("Failed to read SKILL.md: " + str(e))
            content = ""

        frontmatter = _extract_frontmatter(content) if content else None
        if not frontmatter:
            errors.append("SKILL.md missing YAML frontmatter (--- ... ---)")
        elif not _has_required_frontmatter(frontmatter):
            errors.append("SKILL.md frontmatter must include name/description/version")

        version = _extract_version_from_frontmatter(frontmatter) if frontmatter else None
        if frontmatter and not version:
            errors.append("SKILL.md frontmatter version must be semver like 1.0.0")

        if "## @工作流:" not in content:
            errors.append("SKILL.md must include a '## @工作流:' section")

        if "## @工作流: 意图识别与路由" not in content:
            errors.append("SKILL.md must include router workflow '意图识别与路由'")

        if "@跳转到:" not in content:
            errors.append("SKILL.md router must include at least one '@跳转到:'")

        ids = set(re.findall(r"<!-- @ID:\s*([a-z0-9-]+)\s*-->", content))
        for target in re.findall(r"@跳转到:\s*([a-z0-9-]+)", content):
            if target not in ids:
                errors.append("Router jumps to missing step ID: " + target)

        if "| 场景 | 命中信号 | 跳转到 |" not in content:
            errors.append("SKILL.md router must include the decision matrix table")

        if "### @步骤1: 强规则摘要" not in content:
            errors.append("SKILL.md must include a hard rules summary step")

        if "step-reader-testing 或 step-final-review" in content:
            errors.append("SKILL.md router must not use ambiguous reader/final-review jumps")

        if not re.search(r"(?m)^### @步骤\d+:", content):
            errors.append("SKILL.md must include at least one '### @步骤N:' section")

        if "## 最小模板规范" not in content:
            errors.append("SKILL.md must include a '## 最小模板规范' section")

        if "${DOC_PATH}" not in content:
            errors.append("SKILL.md must define and use ${DOC_PATH}")

        template_path = skill_dir / "references" / "templates" / "document-type-outlines.md"
        if "[文档类型默认骨架](references/templates/document-type-outlines.md)" not in content:
            errors.append("SKILL.md must link to document type outlines reference")
        elif not template_path.exists():
            errors.append("Missing document type outlines reference: " + str(template_path))
        else:
            errors.extend(
                _validate_project_markdown(
                    template_path,
                    str(template_path.relative_to(skill_dir)),
                    require_workflow=True,
                )
            )

        validate_skill = skill_dir / "scripts" / "validate_skill.py"
        if not validate_skill.exists():
            errors.append("Missing scripts/validate_skill.py wrapper")

        if "<!-- @产物: ${DOC_PATH} -->" not in content:
            errors.append("SKILL.md must declare output artifact via '@产物: ${DOC_PATH}'")

        if "- @动作:" not in content:
            errors.append("SKILL.md must include at least one '- @动作:' line")

        if "@验证点:" not in content:
            errors.append("SKILL.md must include '@验证点:' in step metadata")

        if "@验证方式:" not in content:
            errors.append("SKILL.md must include '@验证方式:' in step metadata")

        if "## 版本历史" not in content:
            errors.append("SKILL.md must include a '## 版本历史' section")
        elif version and f"**v{version}**" not in content:
            errors.append(f"SKILL.md version history must include v{version}")
        else:
            history = content.split("## 版本历史", 1)[1]
            history_items = re.findall(r"(?m)^- \*\*v\d+\.\d+\.\d+\*\*", history)
            if len(history_items) > 5:
                errors.append("SKILL.md version history must keep at most 5 entries")

        if version:
            header_version = _extract_header_value(content, "版本")
            if header_version != f"v{version}":
                errors.append("Header version must match frontmatter version")

        author = _extract_author_from_frontmatter(frontmatter) if frontmatter else None
        if author:
            header_author = _extract_header_value(content, "作者")
            if header_author != author:
                errors.append("Header author must match frontmatter metadata.author")

    errors.extend(_validate_examples(skill_dir))

    if errors:
        for message in errors:
            print("ERROR: " + message)
        return 1

    print("OK: basic skill structure checks passed")


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
