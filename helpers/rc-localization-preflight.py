#!/usr/bin/env python3
"""Run the full release-localization policy preflight and report all failures."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


@dataclass(frozen=True)
class AuditResult:
    """One localization audit result."""

    label: str
    returncode: int
    output: str


def build_parser() -> argparse.ArgumentParser:
    """Builds the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="Canonical workspace root. Defaults to EMULEBB_WORKSPACE_ROOT or path discovery.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print successful child-audit output instead of only failure details.",
    )
    return parser


def tooling_root() -> Path:
    """Returns the emulebb-tooling repository root."""

    return Path(__file__).resolve().parents[1]


def resolve_workspace_root(candidate: Path | None) -> Path:
    """Resolve the canonical workspace root used by localization checks."""

    if candidate is not None:
        return candidate.resolve()
    env_root = os_environ("EMULEBB_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).resolve()
    current = tooling_root()
    for parent in (current, *current.parents):
        if (parent / "repos" / "emulebb-tooling").is_dir() and (parent / "workspaces").is_dir():
            return parent
    raise RuntimeError("Unable to resolve EMULEBB_WORKSPACE_ROOT for localization preflight.")


def os_environ(name: str) -> str:
    """Return one environment value without importing os globally for tests."""

    import os

    return os.environ.get(name, "")


def load_rc_helper() -> ModuleType:
    """Load rc-string-table.py as a module for shared RC parsing helpers."""

    helper = tooling_root() / "helpers" / "rc-string-table.py"
    spec = importlib.util.spec_from_file_location("emulebb_rc_string_table", helper)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load RC helper: {helper}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def required_paths(root: Path) -> dict[str, Path]:
    """Return all localization policy paths used by this preflight."""

    tools = root / "repos" / "emulebb-tooling"
    app = root / "workspaces" / "workspace" / "app" / "emulebb-main"
    return {
        "helper": tools / "helpers" / "rc-string-table.py",
        "english_rc": app / "srchybrid" / "emule.rc",
        "resource_h": app / "srchybrid" / "resource.h",
        "release_languages": tools / "helpers" / "rc-release-languages.json",
        "release_layouts": tools / "helpers" / "rc-release-localization-layout.json",
        "required_ids": tools / "helpers" / "rc-release-localization-ids.txt",
        "ignored_source_ids": tools / "helpers" / "rc-release-localization-ignored-ids.txt",
        "allow_identical": tools / "helpers" / "rc-translation-identical-ok-ids.txt",
        "quality_rules": tools / "helpers" / "rc-translation-quality-rules.json",
    }


def assert_policy_files(paths: dict[str, Path]) -> list[str]:
    """Return missing required localization-policy files."""

    return [f"{label}: {path}" for label, path in paths.items() if not path.is_file()]


def run_child(label: str, command: list[str], cwd: Path) -> AuditResult:
    """Run a child audit and capture output for aggregate reporting."""

    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return AuditResult(label=label, returncode=completed.returncode, output=completed.stdout)


def child_audits(paths: dict[str, Path]) -> list[AuditResult]:
    """Run the canonical helper audits without failing fast."""

    tools = tooling_root()
    helper = paths["helper"]
    english_rc = paths["english_rc"]
    return [
        run_child(
            "release language manifest audit",
            [
                sys.executable,
                str(helper),
                "--audit-release-manifest",
                "--english-rc",
                str(english_rc),
                "--release-languages",
                str(paths["release_languages"]),
            ],
            tools,
        ),
        run_child(
            "release localization layout audit",
            [
                sys.executable,
                str(helper),
                "--audit-release-layouts",
                "--english-rc",
                str(english_rc),
                "--release-languages",
                str(paths["release_languages"]),
                "--release-layouts",
                str(paths["release_layouts"]),
            ],
            tools,
        ),
        run_child(
            "release localization coverage and quality audit",
            [
                sys.executable,
                str(helper),
                "--cross-reference",
                "--quality-audit",
                "--fail-on-quality-warning",
                "--allow-identical-ids",
                str(paths["allow_identical"]),
                "--quality-rules",
                str(paths["quality_rules"]),
                "--english-rc",
                str(english_rc),
                "--require-ids",
                str(paths["required_ids"]),
                "--release-languages",
                str(paths["release_languages"]),
            ],
            tools,
        ),
    ]


def load_release_targets(release_languages: Path, english_rc: Path) -> list[Path]:
    """Load release RC target files from the canonical language manifest."""

    data = json.loads(release_languages.read_text(encoding="utf-8-sig"))
    languages = data.get("languages", [])
    targets: list[Path] = []
    for item in languages:
        if isinstance(item, dict) and isinstance(item.get("rc"), str):
            targets.append(english_rc.parent / "lang" / item["rc"])
    return targets


def resource_h_ids(resource_h: Path) -> set[str]:
    """Return IDS_* defines available in resource.h."""

    text = resource_h.read_text(encoding="utf-8-sig")
    return set(re.findall(r"(?m)^#define\s+(IDS_[A-Z0-9_]+)\s+\d+\b", text))


def format_list(items: list[str], limit: int = 40) -> str:
    """Format a bounded list for failure output."""

    if len(items) <= limit:
        return "\n".join(items)
    shown = "\n".join(items[:limit])
    return f"{shown}\n... {len(items) - limit} more"


def source_manifest_audit(paths: dict[str, Path], rc_helper: ModuleType) -> list[str]:
    """Return source/manifest drift errors not covered by child audits."""

    source = rc_helper.collect_rc_strings(paths["english_rc"])
    required_ids = rc_helper.parse_id_list(paths["required_ids"])
    ignored_ids = rc_helper.parse_id_list(paths["ignored_source_ids"])
    source_ids = list(source.values)
    source_set = set(source_ids)
    required_set = set(required_ids)
    ignored_set = set(ignored_ids)
    errors: list[str] = []

    if source.duplicates:
        errors.append("English RC duplicate IDS entries:\n" + format_list(source.duplicates))

    overlap = sorted(required_set & ignored_set)
    if overlap:
        errors.append("IDs cannot be both required and ignored:\n" + format_list(overlap))

    unknown_source = [key for key in source_ids if key not in required_set and key not in ignored_set]
    if unknown_source:
        errors.append(
            "English RC has IDS entries not classified by release localization policy. "
            "Add each ID to rc-release-localization-ids.txt or rc-release-localization-ignored-ids.txt:\n"
            + format_list(unknown_source)
        )

    stale_ignored = [key for key in ignored_ids if key not in source_set]
    if stale_ignored:
        errors.append(
            "Ignored localization IDs are no longer present in English RC:\n" + format_list(stale_ignored)
        )

    missing_required = [key for key in required_ids if key not in source_set]
    if missing_required:
        errors.append("Required localization IDs are missing from English RC:\n" + format_list(missing_required))

    ordered_required = [key for key in source_ids if key in required_set]
    if ordered_required != required_ids:
        mismatch = []
        for index, (actual, expected) in enumerate(zip(required_ids, ordered_required), 1):
            if actual != expected:
                mismatch.append(f"{index}: required file has {actual}, source order has {expected}")
                break
        if len(required_ids) != len(ordered_required):
            mismatch.append(f"required count {len(required_ids)} differs from source-present count {len(ordered_required)}")
        errors.append("Required localization IDs must follow English RC source order:\n" + "\n".join(mismatch))

    defined_ids = resource_h_ids(paths["resource_h"])
    missing_defines = [key for key in required_ids if key not in defined_ids]
    if missing_defines:
        errors.append("Required localization IDs are missing from resource.h:\n" + format_list(missing_defines))

    layout_data = json.loads(paths["release_layouts"].read_text(encoding="utf-8-sig"))
    layout_ids = [
        item.get("id")
        for item in layout_data.get("layouts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    ungated_layout_ids = [key for key in layout_ids if key not in required_set]
    if ungated_layout_ids:
        errors.append("Release layout IDs must also be required localization IDs:\n" + format_list(ungated_layout_ids))

    for target in load_release_targets(paths["release_languages"], paths["english_rc"]):
        target_strings = rc_helper.collect_rc_strings(target)
        extra = sorted(key for key in target_strings.values if key not in source_set)
        if extra:
            errors.append(f"{target}: target RC has IDs not present in English RC:\n" + format_list(extra))
    return errors


def print_result(result: AuditResult, verbose: bool) -> None:
    """Print one successful child result when requested."""

    if result.returncode == 0:
        if verbose and result.output:
            print(result.output, end="" if result.output.endswith("\n") else "\n")
        print(f"OK {result.label}")


def main(argv: list[str] | None = None) -> int:
    """Run the aggregate preflight."""

    args = build_parser().parse_args(argv)
    root = resolve_workspace_root(args.workspace_root)
    paths = required_paths(root)
    missing = assert_policy_files(paths)
    if missing:
        print("Release localization preflight failed: required files are missing:", file=sys.stderr)
        print(format_list(missing), file=sys.stderr)
        return 1

    results = child_audits(paths)
    rc_helper = load_rc_helper()
    drift_errors = source_manifest_audit(paths, rc_helper)

    failures: list[str] = []
    for result in results:
        if result.returncode != 0:
            output = result.output.strip() or "(no output)"
            failures.append(f"{result.label} failed:\n{output}")
        else:
            print_result(result, args.verbose)
    if drift_errors:
        failures.append("source/manifest drift audit failed:\n" + "\n\n".join(drift_errors))

    if failures:
        print("Release localization preflight failed.", file=sys.stderr)
        print("\n\n".join(failures), file=sys.stderr)
        return 1
    print("Release localization preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
