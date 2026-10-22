#!/usr/bin/env python3
"""Deterministic validation for the kz-bmad-run skill."""

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


def _extract_value(frontmatter: str, key: str):
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else None


def _extract_body_version(content: str):
    match = re.search(r"^> \*\*版本\*\*: v([0-9]+\.[0-9]+\.[0-9]+)$", content, re.MULTILINE)
    return match.group(1) if match else None


def _extract_history_versions(content: str):
    return re.findall(r"^-\s+\*\*v([0-9]+\.[0-9]+\.[0-9]+)\*\*", content, re.MULTILINE)


def validate(skill_dir: Path):
    errors = []

    skill_md = skill_dir / "SKILL.md"
    workflow_map = skill_dir / "references" / "workflow-map.md"
    git_root_routing = skill_dir / "references" / "git-root-routing.md"
    pre_dev_story_confirmation = skill_dir / "references" / "pre-dev-story-confirmation.md"
    workflow_content = ""
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
            name = _extract_value(frontmatter, "name")
            description = _extract_value(frontmatter, "description")
            version = _extract_value(frontmatter, "version")
            if name != "kz-bmad-run":
                errors.append("frontmatter name must be 'kz-bmad-run'")
            if not description or "TODO" in description:
                errors.append("frontmatter description must be finalized and non-TODO")

            body_version = _extract_body_version(content)
            if not body_version:
                errors.append("SKILL.md must include a body version line like '> **版本**: vX.Y.Z'")
            elif version != body_version:
                errors.append("frontmatter version and body version line must match")

            history_versions = _extract_history_versions(content)
            if not history_versions:
                errors.append("SKILL.md version history must include at least one version entry")
            else:
                if version != history_versions[0]:
                    errors.append("frontmatter version and latest version history entry must match")
                if len(history_versions) > 5:
                    errors.append("SKILL.md version history must keep at most 5 entries")

        if "## @工作流:" not in content:
            errors.append("SKILL.md must include a '## @工作流:' section")

        if "## 版本历史" not in content:
            errors.append("SKILL.md must include a '## 版本历史' section")

        required_strings = [
            "bmad-help",
            "bmad-create-story",
            "bmad-dev-story",
            "bmad-code-review",
            "AGENTS.md",
            "${PROJECT_RULES_ENTRY}",
            "sprint-status.yaml",
            "${PROJECT_ROOT}",
            "${GIT_MAIN_BRANCH}",
            "${ACTIVE_GIT_ROOT}",
            "${REPO_FILE_MAP}",
            "${STORY_SCOPE}",
            "${MERGE_BLOCKERS}",
            "临时 worktree",
            "git-root-routing.md",
            "pre-dev-story-confirmation.md",
            "scripts/validate_skill.py",
            "开发前确认摘要",
            "挂起项",
        ]
        for item in required_strings:
            if item not in content:
                errors.append(f"SKILL.md missing required text: {item}")

        forbidden_strings = [
            "/Users/kingzeus/Development/dash/speech",
            "`speech` 仓库中的 BMAD",
            "scripts/verify.py",
            "${PROJECT_GIT_SOP}",
            "docs/bmad-git-sop.md",
        ]
        for item in forbidden_strings:
            if item in content:
                errors.append(f"SKILL.md must not contain forbidden text: {item}")

        if "TODO" in content or "YYYY-MM-DD" in content:
            errors.append("SKILL.md still contains template placeholders (TODO or YYYY-MM-DD)")

    if not workflow_map.exists():
        errors.append("Missing references/workflow-map.md")
    else:
        try:
            workflow_content = _read_text(workflow_map)
        except Exception as e:
            errors.append("Failed to read workflow-map.md: " + str(e))

    if not git_root_routing.exists():
        errors.append("Missing references/git-root-routing.md")
    else:
        try:
            git_root_content = _read_text(git_root_routing)
        except Exception as e:
            errors.append("Failed to read git-root-routing.md: " + str(e))
            git_root_content = ""

        for item in [
            "${ACTIVE_GIT_ROOT}",
            "${REPO_FILE_MAP}",
            "${STORY_SCOPE}",
            "${MERGE_BLOCKERS}",
            "最近祖先仓库优先",
            "untracked",
            "worktree",
        ]:
            if item not in git_root_content:
                errors.append(f"git-root-routing.md missing required text: {item}")

    if not pre_dev_story_confirmation.exists():
        errors.append("Missing references/pre-dev-story-confirmation.md")
    else:
        try:
            pre_dev_content = _read_text(pre_dev_story_confirmation)
        except Exception as e:
            errors.append("Failed to read pre-dev-story-confirmation.md: " + str(e))
            pre_dev_content = ""

        for item in [
            "bmad-dev-story",
            "开发前确认摘要",
            "本 story 要开发什么",
            "本轮明确不做什么",
            "关键验收点",
            "是否需要先补充或修正 story",
        ]:
            if item not in pre_dev_content:
                errors.append(f"pre-dev-story-confirmation.md missing required text: {item}")

    if workflow_content:
        required_workflow_strings = [
            "${PROJECT_ROOT}",
            "${PROJECT_RULES_ENTRY}",
            "${GIT_MAIN_BRANCH}",
            "${ACTIVE_GIT_ROOT}",
            "${REPO_FILE_MAP}",
            "${STORY_SCOPE}",
            "${MERGE_BLOCKERS}",
            "AGENTS.md",
            "sprint-status.yaml",
            "git-root-routing.md",
            "pre-dev-story-confirmation.md",
            "开发前确认摘要",
            "挂起项",
            "worktree",
        ]
        for item in required_workflow_strings:
            if item not in workflow_content:
                errors.append(f"workflow-map.md missing required text: {item}")

        forbidden_workflow_strings = [
            "/Users/kingzeus/Development/dash/speech",
            "切到 `master`",
            "合并回 `master`",
            "scripts/verify.py",
            "${PROJECT_GIT_SOP}",
            "docs/bmad-git-sop.md",
        ]
        for item in forbidden_workflow_strings:
            if item in workflow_content:
                errors.append(f"workflow-map.md must not contain forbidden text: {item}")

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

    sys.exit(validate(skill_dir))


if __name__ == "__main__":
    main()
