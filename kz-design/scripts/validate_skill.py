#!/usr/bin/env python3
"""Package-time validation entry for kz-design."""

import argparse
import re
import sys
import zipfile
from pathlib import Path

ALLOWED_FILES = {
    "SKILL.md",
    "references/design-workflow.md",
    "references/design-quality-rules.md",
    "references/style-profiles.md",
    "references/visual-style-primitives.md",
    "references/implementation-handoff.md",
    "references/output-playbooks.md",
    "references/verification.md",
    "scripts/validate_skill.py",
    "dist/kz-design.skill",
}

PACKAGE_ALLOWED_FILES = {"kz-design/" + rel_path for rel_path in ALLOWED_FILES if rel_path != "dist/kz-design.skill"}

FORBIDDEN_ROOT_FILES = {
    "design.md",
    "README.md",
    "README.zh.md",
    "CHANGELOG.md",
}

FORBIDDEN_SOURCE_TERMS = [
    "hua" + "shu",
    "Hua" + "shu",
    "花" + "叔",
    "hua" + "shu-design",
    "skills" + "1",
    "color-font" + "-skill",
    "design-style" + "-skill",
    "slide-making" + "-skill",
    "ppt-orchestra" + "-skill",
    "mini" + "max-docx",
    "mini" + "max-pdf",
    "mini" + "max-xlsx",
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


def _frontmatter_value(frontmatter: str, key: str):
    match = re.search(rf"(?m)^{re.escape(key)}\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def _header_value(markdown: str, label: str):
    match = re.search(rf"(?m)^> \*\*{re.escape(label)}\*\*:\s*(.+?)\s*$", markdown)
    if not match:
        return None
    return match.group(1).strip()


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
        else:
            version = _frontmatter_value(frontmatter, "version:")
            if not version or not re.match(r"^\d+\.\d+\.\d+$", version):
                errors.append("SKILL.md version must be semver like 1.0.0")
            elif _header_value(content, "版本") != "v" + version:
                errors.append("Header version must match frontmatter version")
            elif f"**v{version}**" not in content:
                errors.append("Version history must include v" + version)

        if "## @工作流:" not in content:
            errors.append("SKILL.md must include a '## @工作流:' section")

        if not re.search(r"(?m)^### @步骤\d+:", content):
            errors.append("SKILL.md must include at least one '### @步骤N:' section")

        for marker in ["<!-- @类型:", "<!-- @验证点:", "<!-- @验证方式:", "- @动作:"]:
            if marker not in content:
                errors.append("SKILL.md missing required semantic marker: " + marker)

        if "| 场景 | 命中信号 | 跳转到 |" not in content:
            errors.append("SKILL.md must include the decision matrix table")

        if "### @步骤1: 强规则摘要" not in content:
            errors.append("SKILL.md must include hard rules summary")

        ids = set(re.findall(r"<!-- @ID:\s*([a-z0-9-]+)\s*-->", content))
        for target in re.findall(r"@跳转到:\s*([a-z0-9-]+)", content):
            if target not in ids:
                errors.append("Router jumps to missing ID: " + target)

        for forbidden in ["TODO", "YYYY-MM-DD"]:
            if forbidden in content:
                errors.append("SKILL.md still contains placeholder text: " + forbidden)

        if "## 版本历史" not in content:
            errors.append("SKILL.md must include a '## 版本历史' section")

        if "${DESIGN_OUTPUT_DIR}" not in content:
            errors.append("SKILL.md must define the default output directory contract")

        if "validation-notes.md" not in content:
            errors.append("SKILL.md must require validation notes for design artifacts")

    required_refs = [
        "references/design-workflow.md",
        "references/design-quality-rules.md",
        "references/style-profiles.md",
        "references/visual-style-primitives.md",
        "references/implementation-handoff.md",
        "references/output-playbooks.md",
        "references/verification.md",
    ]
    for rel_path in required_refs:
        if not (skill_dir / rel_path).exists():
            errors.append("Missing reference: " + rel_path)

    style_profiles_path = skill_dir / "references" / "style-profiles.md"
    if style_profiles_path.exists():
        style_profiles = _read_text(style_profiles_path)
        for profile_name in [
            "信息建筑型",
            "编辑叙事型",
            "工具效率型",
            "产品发布型",
            "东方留白型",
            "温暖生活型",
            "实验视觉型",
            "高密度智能型",
        ]:
            if f"## {profile_name}" not in style_profiles:
                errors.append("style-profiles.md missing profile: " + profile_name)
        for marker in ["aesthetic thesis", "禁止事项", "验证重点", "profile 是方向起点"]:
            if marker not in style_profiles:
                errors.append("style-profiles.md missing required marker: " + marker)

    handoff_path = skill_dir / "references" / "implementation-handoff.md"
    if handoff_path.exists():
        handoff = _read_text(handoff_path)
        for marker in [
            "通用设计交接包",
            "系统适配层",
            "design-brief.md",
            "ui-spec.md",
            "implementation-handoff.md",
            "HTML 是视觉验证",
            "Theme Package",
            "Visualization Spec",
            "Data provenance",
            "Provider",
            "Reference link",
            "Freshness",
        ]:
            if marker not in handoff:
                errors.append("implementation-handoff.md missing required marker: " + marker)

    visual_primitives_path = skill_dir / "references" / "visual-style-primitives.md"
    if visual_primitives_path.exists():
        visual_primitives = _read_text(visual_primitives_path)
        for marker in [
            "配色策略",
            "布局语法",
            "Theme Package",
            "品牌提取型",
            "中性底单强调",
            "海报锚点",
            "工作台分区",
            "形态密度",
            "外层圆角",
            "信息密度决定间距",
            "胶囊通透",
            "组合协议",
            "外部主题引入协议",
        ]:
            if marker not in visual_primitives:
                errors.append("visual-style-primitives.md missing required marker: " + marker)

    output_playbooks_path = skill_dir / "references" / "output-playbooks.md"
    if output_playbooks_path.exists():
        output_playbooks = _read_text(output_playbooks_path)
        for marker in [
            "Landing / 品牌页",
            "utility copy",
            "每个 section 只做一件事",
            "Visualization Spec",
            "趋势用 line/area",
            "截断坐标轴",
            "页面角色",
            "内容页子类型",
            "章节分隔",
        ]:
            if marker not in output_playbooks:
                errors.append("output-playbooks.md missing required marker: " + marker)

    verification_path = skill_dir / "references" / "verification.md"
    if verification_path.exists():
        verification = _read_text(verification_path)
        for marker in [
            "固定画布验证",
            "导出保真验证",
            "文字可选择",
            "链接",
            "图表保留",
        ]:
            if marker not in verification:
                errors.append("verification.md missing required marker: " + marker)

    design_quality_path = skill_dir / "references" / "design-quality-rules.md"
    if design_quality_path.exists():
        design_quality = _read_text(design_quality_path)
        for marker in ["首屏识别测试", "真实视觉锚点", "每个 section"]:
            if marker not in design_quality:
                errors.append("design-quality-rules.md missing required marker: " + marker)

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_path = str(path.relative_to(skill_dir))
        if rel_path in ALLOWED_FILES:
            continue
        if path.name in FORBIDDEN_ROOT_FILES or path.parent == skill_dir:
            errors.append("Unexpected root-level or draft file in skill package source: " + rel_path)
        elif rel_path.startswith(("references/", "scripts/")):
            errors.append("Unexpected file not declared in package allowlist: " + rel_path)

        if not rel_path.startswith("dist/"):
            text = _read_text(path)
            for term in FORBIDDEN_SOURCE_TERMS:
                if term in text:
                    errors.append("Forbidden source reference found in " + rel_path)

    package_path = skill_dir / "dist" / "kz-design.skill"
    if package_path.exists():
        try:
            with zipfile.ZipFile(package_path) as archive:
                names = [name for name in archive.namelist() if not name.endswith("/")]
                for name in names:
                    if name not in PACKAGE_ALLOWED_FILES:
                        errors.append("Unexpected file in packaged skill: " + name)
                    data = archive.read(name).decode("utf-8", errors="ignore")
                    for term in FORBIDDEN_SOURCE_TERMS:
                        if term in data:
                            errors.append("Forbidden source reference found in package file: " + name)
        except zipfile.BadZipFile:
            errors.append("Invalid packaged skill archive: " + str(package_path))

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
