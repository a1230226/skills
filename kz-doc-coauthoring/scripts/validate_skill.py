#!/usr/bin/env python3
"""
Package-time validation entry for kz-doc-coauthoring.

The shared skill packager looks for scripts/validate_skill.py, so this wrapper
delegates to the existing verify.py checks without duplicating validation logic.
"""

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from verify import verify  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, help="Skill folder path")
    args = parser.parse_args()

    skill_dir = Path(args.skill).resolve()
    if not skill_dir.exists():
        print("ERROR: skill folder not found: " + str(skill_dir))
        return 1

    return verify(skill_dir)


if __name__ == "__main__":
    sys.exit(main())
