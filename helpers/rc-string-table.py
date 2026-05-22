#!/usr/bin/env python3
"""Insert managed Windows RC string-table entries from TSV input."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


UTF8_BOM = b"\xef\xbb\xbf"
START_MARKER = "// eMule BB managed translation block: begin"
END_MARKER = "// eMule BB managed translation block: end"
DEFAULT_PROBE_START = "IDS_ENABLE_IPFILTER"
DEFAULT_PROBE_END = "IDS_ALWAYS_SHOW_TRAY_ICON"


@dataclass(frozen=True)
class RcText:
    """Decoded RC text plus enough metadata to preserve file style."""

    text: str
    newline: str
    has_utf8_bom: bool


@dataclass(frozen=True)
class RcStrings:
    """Parsed string resources plus duplicate ids found while parsing."""

    values: dict[str, str]
    duplicates: list[str]


@dataclass(frozen=True)
class RcStringEntry:
    """One parsed one-line RC string resource."""

    key: str
    value: str
    line_index: int
    prefix: str
    separator: str
    suffix: str


@dataclass(frozen=True)
class ReleaseLayoutRule:
    """Placement rule for one source-anchored release string."""

    key: str
    after: str
    before: str


def read_rc(path: Path) -> RcText:
    """Read an RC file while preserving its UTF-8 BOM and dominant newline."""

    data = path.read_bytes()
    has_bom = data.startswith(UTF8_BOM)
    text = data.decode("utf-8-sig")
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    newline = "\r\n" if crlf >= lf else "\n"
    return RcText(text=text, newline=newline, has_utf8_bom=has_bom)


def write_rc(path: Path, rc_text: RcText, text: str) -> None:
    """Write RC text with the same UTF-8 BOM and newline convention."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if rc_text.newline != "\n":
        normalized = normalized.replace("\n", rc_text.newline)
    data = normalized.encode("utf-8")
    if rc_text.has_utf8_bom:
        data = UTF8_BOM + data
    path.write_bytes(data)


def parse_tsv(path: Path | None) -> list[tuple[str, str]]:
    """Parse KEY<TAB>VALUE lines from a TSV file or stdin."""

    source = sys.stdin.read() if path is None else path.read_text(encoding="utf-8-sig")
    rows: list[tuple[str, str]] = []
    seen: Counter[str] = Counter()
    for line_no, raw_line in enumerate(source.splitlines(), 1):
        line = raw_line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            raise SystemExit(f"TSV line {line_no} must be KEY<TAB>VALUE")
        key, value = parts[0].strip(), parts[1]
        if not re.fullmatch(r"IDS_[A-Z0-9_]+", key):
            raise SystemExit(f"TSV line {line_no} has invalid resource id: {key}")
        seen[key] += 1
        rows.append((key, value))
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    if duplicates:
        raise SystemExit("Duplicate TSV resource ids: " + ", ".join(duplicates))
    return rows


def parse_id_list(path: Path | None) -> list[str]:
    """Parse required resource ids from a one-id-per-line file."""

    if path is None:
        return []
    ids: list[str] = []
    seen: Counter[str] = Counter()
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not re.fullmatch(r"IDS_[A-Z0-9_]+", line):
            raise SystemExit(f"ID list line {line_no} has invalid resource id: {line}")
        seen[line] += 1
        ids.append(line)
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    if duplicates:
        raise SystemExit("Duplicate required resource ids: " + ", ".join(duplicates))
    return ids


def parse_release_layouts(path: Path | None) -> list[ReleaseLayoutRule]:
    """Parse source-anchored release string layout rules."""

    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    layouts = data.get("layouts")
    if not isinstance(layouts, list):
        raise SystemExit(f"{path} must contain a 'layouts' list.")
    rules: list[ReleaseLayoutRule] = []
    seen: Counter[str] = Counter()
    errors: list[str] = []
    for index, item in enumerate(layouts, 1):
        if not isinstance(item, dict):
            errors.append(f"layout entry {index} must be an object")
            continue
        key = item.get("id")
        after = item.get("after")
        before = item.get("before")
        for field, value in (("id", key), ("after", after), ("before", before)):
            if not isinstance(value, str) or not re.fullmatch(r"IDS_[A-Z0-9_]+", value):
                errors.append(f"layout entry {index} has invalid {field}: {value!r}")
        if isinstance(key, str):
            seen[key] += 1
        if isinstance(key, str) and isinstance(after, str) and isinstance(before, str):
            if key in (after, before) or after == before:
                errors.append(f"layout entry {index} must use distinct id/after/before values")
            rules.append(ReleaseLayoutRule(key=key, after=after, before=before))
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    if duplicates:
        errors.append("duplicate layout ids: " + ", ".join(duplicates))
    if errors:
        raise SystemExit(f"{path} has invalid release layout entries:\n" + "\n".join(errors))
    return rules


def require_ids(rows: list[tuple[str, str]], required_ids: list[str], label: str) -> None:
    """Fail when a translation row set misses a required resource id."""

    if not required_ids:
        return
    available = {key for key, _ in rows}
    missing = [key for key in required_ids if key not in available]
    if missing:
        raise SystemExit(f"{label} is missing required resource ids:\n" + "\n".join(missing))


def normalize_control_escapes(value: str) -> str:
    """Normalize control characters to explicit RC escape markers."""

    return (
        value.replace("\r\n", r"\r\n")
        .replace("\r", r"\r\n")
        .replace("\n", r"\r\n")
        .replace("\t", r"\t")
    )


def escape_rc_string(value: str) -> str:
    """Escape a Python string value for a single-line RC string literal."""

    return normalize_control_escapes(value).replace('"', '""')


def find_resource_endif(text: str) -> re.Match[str]:
    """Find the language resource #endif that closes the active RC block."""

    match = re.search(r"\r?\n#endif\s+// .* resources", text)
    if match:
        return match
    match = re.search(r"\r?\n#endif\s*(?=\r?\n\s*\r?\n#ifndef APSTUDIO_INVOKED)", text)
    if match:
        return match
    raise SystemExit("Could not find the language resource #endif marker.")


def resource_endif_structure_warnings(path: Path) -> list[str]:
    """Return warnings for non-canonical language resource block endings."""

    lines = read_rc(path).text.splitlines()
    candidates: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if not line.strip().startswith("#endif"):
            continue
        tail = "\n".join(lines[index : index + 12])
        if "#ifndef APSTUDIO_INVOKED" in tail:
            candidates.append((index + 1, line))
    if len(candidates) != 1:
        return [f"expected one language resource #endif before TEXTINCLUDE 3, got {len(candidates)}"]
    line_no, line = candidates[0]
    if not re.fullmatch(r"\s*#endif\s+// .+ resources\s*", line):
        return [f"line {line_no}: expected '#endif    // <language> resources', got {line.strip()}"]
    separator_index = line_no
    while separator_index < len(lines) and not lines[separator_index].strip():
        separator_index += 1
    if separator_index >= len(lines) or lines[separator_index].strip() != "/////////////////////////////////////////////////////////////////////////////":
        return [f"line {line_no}: expected separator before TEXTINCLUDE 3 block"]
    return []


def strip_managed_or_probe_block(text: str, probe_start: str, probe_end: str) -> str:
    """Remove a previous managed block or one matching the probe ids."""

    line = r"\r?\n"
    managed = re.compile(
        rf"{line}{re.escape(START_MARKER)}{line}.*?{line}{re.escape(END_MARKER)}{line}",
        re.DOTALL,
    )
    text = managed.sub("\n", text)

    string_table = re.compile(r"\r?\nSTRINGTABLE\r?\nBEGIN\r?\n.*?\r?\nEND\r?\n", re.DOTALL)
    text = string_table.sub(
        lambda match: "\n" if probe_start in match.group(0) and probe_end in match.group(0) else match.group(0),
        text,
    )
    return text.rstrip() + "\n\n"


def build_string_table(rows: list[tuple[str, str]]) -> str:
    """Build a marked RC STRINGTABLE block."""

    if not rows:
        raise SystemExit("No rows to insert.")
    width = max(len(key) for key, _ in rows)
    lines = [
        START_MARKER,
        "STRINGTABLE",
        "BEGIN",
    ]
    lines.extend(f'    {key:<{width}} "{escape_rc_string(value)}"' for key, value in rows)
    lines.extend(["END", END_MARKER, ""])
    return "\n".join(lines)


PLACEHOLDER_RE = re.compile(r"%(?:%|[-+#0]*\d*(?:\.\d+)?(?:I64|I32|ll|l|h|z|t|j|L)?[A-Za-z])")
ESCAPE_RE = re.compile(r"\\r\\n|\\[nrt]")
TRANSLATABLE_RE = re.compile(r"[A-Za-z]")


def placeholders(value: str) -> list[str]:
    """Return printf-style placeholders, ignoring literal percent escapes."""

    return [item for item in PLACEHOLDER_RE.findall(value) if item != "%%"]


def format_markers(value: str) -> list[str]:
    """Return printf placeholders and literal percent markers in order."""

    markers: list[str] = []
    index = 0
    while index < len(value):
        if value[index] != "%":
            index += 1
            continue
        match = PLACEHOLDER_RE.match(value, index)
        if match:
            markers.append(match.group(0))
            index = match.end()
        else:
            markers.append("%")
            index += 1
    return markers


def escape_markers(value: str) -> list[str]:
    """Return RC line/tab escape markers that must retain paragraph shape."""

    return ESCAPE_RE.findall(normalize_control_escapes(value))


def accelerator_counts(value: str) -> tuple[int, int]:
    """Return mnemonic and literal ampersand counts for a resource string."""

    mnemonics = 0
    literals = 0
    index = 0
    while index < len(value):
        if value[index] != "&":
            index += 1
            continue
        if index + 1 < len(value) and value[index + 1] == "&":
            literals += 1
            index += 2
        else:
            mnemonics += 1
            index += 1
    return mnemonics, literals


def structural_warnings(source_value: str, target_value: str) -> list[str]:
    """Return structural localization issues that can break formatting or menus."""

    warnings: list[str] = []
    expected_format = format_markers(source_value)
    actual_format = format_markers(target_value)
    if expected_format != actual_format:
        warnings.append(f"format markers expected {expected_format}, got {actual_format}")

    expected_escapes = escape_markers(source_value)
    actual_escapes = escape_markers(target_value)
    if expected_escapes != actual_escapes:
        warnings.append(f"escape markers expected {expected_escapes}, got {actual_escapes}")

    expected_mnemonics, _ = accelerator_counts(source_value)
    actual_mnemonics, _ = accelerator_counts(target_value)
    if expected_mnemonics != actual_mnemonics:
        warnings.append(f"mnemonic accelerators expected {expected_mnemonics}, got {actual_mnemonics}")
    return warnings


def _quality_normalize(value: str) -> str:
    """Normalize text enough to spot clearly untranslated rows."""

    value = value.replace("&", "")
    value = PLACEHOLDER_RE.sub("", value)
    value = re.sub(r"\b[\w.-]+\.(?:ini|dat|met|dll|exe|log|txt|xml|tmpl|css|js|html|zip|rar|7z|part|bak)\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\b(?:https?|ed2k)://[^\s\"<>]+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"[^A-Za-z]+", " ", value)
    return " ".join(value.casefold().split())


def untranslated_warning(source_value: str, target_value: str) -> str | None:
    """Return a warning when target text looks like an unreviewed English copy."""

    source_norm = _quality_normalize(source_value)
    if not source_norm or not TRANSLATABLE_RE.search(source_norm):
        return None
    target_norm = _quality_normalize(target_value)
    if source_norm == target_norm:
        return "same normalized English text"
    return None


def load_quality_rules(path: Path | None) -> dict:
    """Load optional semantic translation quality rules."""

    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stock_lang_dir(english_rc: Path) -> Path:
    """Return the stock eMule language directory next to the English RC file."""

    return english_rc.parent / "lang"


def stock_rc_files(english_rc: Path) -> list[Path]:
    """Return all stock eMule language RC files available for release gating."""

    lang_dir = stock_lang_dir(english_rc)
    if not lang_dir.is_dir():
        raise SystemExit(f"Stock language directory does not exist: {lang_dir}")
    return sorted(path for path in lang_dir.glob("*.rc") if path.is_file())


def load_release_language_targets(path: Path | None, english_rc: Path | None) -> list[Path]:
    """Load target RC files from the canonical release language manifest."""

    if path is None:
        return []
    if english_rc is None:
        raise SystemExit("--release-languages requires --english-rc so the lang directory can be inferred.")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    languages = data.get("languages")
    if not isinstance(languages, list):
        raise SystemExit(f"{path} must contain a 'languages' list.")
    lang_dir = english_rc.parent / "lang"
    targets: list[Path] = []
    seen: set[Path] = set()
    errors: list[str] = []
    for index, item in enumerate(languages, 1):
        if not isinstance(item, dict):
            errors.append(f"language entry {index} must be an object")
            continue
        code = item.get("code")
        rc_file = item.get("rc")
        if not isinstance(code, str) or not code:
            errors.append(f"language entry {index} is missing a non-empty code")
            continue
        if not isinstance(rc_file, str) or not rc_file.endswith(".rc"):
            errors.append(f"language entry {code} is missing an .rc file name")
            continue
        target = lang_dir / rc_file
        if target in seen:
            errors.append(f"language entry {code} duplicates target {target}")
            continue
        if not target.is_file():
            errors.append(f"language entry {code} points to missing file {target}")
            continue
        seen.add(target)
        targets.append(target)
    if errors:
        raise SystemExit(f"{path} has invalid release language entries:\n" + "\n".join(errors))
    return targets


def collect_target_rcs(args: argparse.Namespace, purpose: str) -> list[Path]:
    """Collect explicit, manifest, and all-stock target RC files."""

    if not args.english_rc:
        raise SystemExit(f"--{purpose} requires --english-rc.")
    targets = list(args.target_rc or [])
    targets.extend(load_release_language_targets(args.release_languages, args.english_rc))
    if args.all_stock_targets:
        targets.extend(stock_rc_files(args.english_rc))
    if args.rc:
        targets.append(args.rc)
    if not targets:
        raise SystemExit(
            f"--{purpose} requires at least one --target-rc, --release-languages, "
            "--all-stock-targets, or --rc."
        )
    return list(dict.fromkeys(targets))


def audit_release_language_manifest(args: argparse.Namespace) -> None:
    """Fail unless the release manifest covers every stock language RC file."""

    if not args.english_rc:
        raise SystemExit("--audit-release-manifest requires --english-rc.")
    if not args.release_languages:
        raise SystemExit("--audit-release-manifest requires --release-languages.")
    manifest_targets = set(load_release_language_targets(args.release_languages, args.english_rc))
    stock_targets = set(stock_rc_files(args.english_rc))
    missing = sorted(stock_targets - manifest_targets)
    stale = sorted(manifest_targets - stock_targets)
    errors: list[str] = []
    if missing:
        errors.append("manifest is missing stock language RC files:\n" + "\n".join(str(path) for path in missing))
    if stale:
        errors.append("manifest references non-stock language RC files:\n" + "\n".join(str(path) for path in stale))
    if errors:
        raise SystemExit("\n\n".join(errors))
    print(f"OK {args.release_languages}: {len(stock_targets)} stock language RC files")


def _rules_for_target(rules: dict, target_path: Path) -> list[dict]:
    """Return global and target-language rule groups."""

    groups: list[dict] = []
    if isinstance(rules.get("global"), dict):
        groups.append(rules["global"])
    languages = rules.get("languages", {})
    if isinstance(languages, dict):
        for name in (target_path.name, target_path.stem):
            group = languages.get(name)
            if isinstance(group, dict):
                groups.append(group)
    return groups


def _rule_entries(group: dict, key: str, field: str) -> list[dict]:
    """Return generic and id-specific rule entries for a target string."""

    entries: list[dict] = []
    generic = group.get(field, [])
    if isinstance(generic, list):
        entries.extend(item for item in generic if isinstance(item, dict))
    id_rules = group.get("id_rules", {})
    if isinstance(id_rules, dict):
        id_group = id_rules.get(key, {})
        if isinstance(id_group, dict):
            specific = id_group.get(field, [])
            if isinstance(specific, list):
                entries.extend(item for item in specific if isinstance(item, dict))
    return entries


def semantic_quality_warnings(target_path: Path, key: str, value: str, rules: dict) -> list[str]:
    """Apply curated language/id rules that catch common bad translations."""

    warnings: list[str] = []
    for group in _rules_for_target(rules, target_path):
        for item in _rule_entries(group, key, "forbidden_regex"):
            pattern = item.get("pattern")
            if isinstance(pattern, str) and re.search(pattern, value, flags=re.IGNORECASE):
                warnings.append(item.get("message", f"forbidden pattern matched: {pattern}"))
        for item in _rule_entries(group, key, "required_regex"):
            pattern = item.get("pattern")
            if isinstance(pattern, str) and not re.search(pattern, value, flags=re.IGNORECASE):
                warnings.append(item.get("message", f"required pattern missing: {pattern}"))
    return warnings


def collect_strings(path: Path) -> dict[str, str]:
    """Collect RC string literals by resource id."""

    return collect_rc_strings(path).values


def _decode_rc_literal(raw_value: str) -> str:
    """Decode one RC string literal payload."""

    return raw_value.replace('""', '"')


def _string_literal_from_line(line: str) -> str | None:
    """Return the first RC string literal payload from a line, if present."""

    match = re.search(r'"((?:[^"]|"")*)"', line)
    if not match:
        return None
    return _decode_rc_literal(match.group(1))


def _parse_rc_string_line(line: str, line_index: int) -> RcStringEntry | None:
    """Parse one-line IDS_* string resources while preserving layout pieces."""

    match = re.match(r"(?P<prefix>\s*)(?P<key>IDS_[A-Z0-9_]+)(?P<separator>\s+)\"(?P<raw>(?:[^\"]|\"\")*)\"(?P<suffix>.*)$", line)
    if not match:
        return None
    return RcStringEntry(
        key=match.group("key"),
        value=_decode_rc_literal(match.group("raw")),
        line_index=line_index,
        prefix=match.group("prefix"),
        separator=match.group("separator"),
        suffix=match.group("suffix"),
    )


def collect_rc_string_entries(path: Path) -> tuple[list[RcStringEntry], list[str]]:
    """Collect one-line RC string entries in file order plus duplicate ids."""

    entries: list[RcStringEntry] = []
    seen: Counter[str] = Counter()
    for index, line in enumerate(read_rc(path).text.splitlines()):
        entry = _parse_rc_string_line(line, index)
        if entry is None:
            continue
        entries.append(entry)
        seen[entry.key] += 1
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    return entries, duplicates


def collect_rc_strings(path: Path) -> RcStrings:
    """Collect one-line and next-line RC string literals by resource id."""

    text = read_rc(path).text
    found: dict[str, str] = {}
    seen: Counter[str] = Counter()
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"\s*(IDS_[A-Z0-9_]+)\b(.*)$", line)
        if not match:
            index += 1
            continue
        key = match.group(1)
        value = _string_literal_from_line(match.group(2))
        if value is None and index + 1 < len(lines):
            value = _string_literal_from_line(lines[index + 1])
            if value is not None:
                index += 1
        if value is not None:
            seen[key] += 1
            found[key] = value
        index += 1
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    return RcStrings(values=found, duplicates=duplicates)


def _entry_by_key(entries: list[RcStringEntry], key: str, path: Path) -> RcStringEntry:
    """Return the single one-line entry for key or fail with context."""

    matches = [entry for entry in entries if entry.key == key]
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected exactly one one-line {key} entry, got {len(matches)}")
    return matches[0]


def _release_layout_source_entries(english_rc: Path, rules: list[ReleaseLayoutRule]) -> dict[str, RcStringEntry]:
    """Return source entries used as canonical layout templates."""

    source_entries, duplicates = collect_rc_string_entries(english_rc)
    if duplicates:
        raise SystemExit(f"{english_rc} has duplicate one-line resource ids:\n" + "\n".join(duplicates))
    return {rule.key: _entry_by_key(source_entries, rule.key, english_rc) for rule in rules}


def _format_release_layout_line(template: RcStringEntry, value: str) -> str:
    """Format a managed layout row using the source RC spacing and suffix."""

    return f'{template.prefix}{template.key}{template.separator}"{escape_rc_string(value)}"{template.suffix}'


def _release_layout_errors(path: Path, rules: list[ReleaseLayoutRule], templates: dict[str, RcStringEntry]) -> list[str]:
    """Return source-anchored release layout errors for one RC file."""

    entries, duplicates = collect_rc_string_entries(path)
    by_key: dict[str, list[RcStringEntry]] = {}
    for entry in entries:
        by_key.setdefault(entry.key, []).append(entry)
    errors: list[str] = []
    if duplicates:
        errors.append("duplicate one-line ids:\n" + "\n".join(duplicates))
    for rule in rules:
        after_entries = by_key.get(rule.after, [])
        managed_entries = by_key.get(rule.key, [])
        before_entries = by_key.get(rule.before, [])
        if len(after_entries) != 1:
            errors.append(f"{rule.key}: expected one anchor {rule.after}, got {len(after_entries)}")
            continue
        if len(managed_entries) != 1:
            errors.append(f"{rule.key}: expected one managed row, got {len(managed_entries)}")
            continue
        if len(before_entries) != 1:
            errors.append(f"{rule.key}: expected one anchor {rule.before}, got {len(before_entries)}")
            continue
        after_entry = after_entries[0]
        managed_entry = managed_entries[0]
        before_entry = before_entries[0]
        if not (after_entry.line_index < managed_entry.line_index < before_entry.line_index):
            errors.append(f"{rule.key}: expected order {rule.after}, {rule.key}, {rule.before}")
        expected_line = _format_release_layout_line(templates[rule.key], managed_entry.value)
        actual_line = read_rc(path).text.splitlines()[managed_entry.line_index]
        if actual_line != expected_line:
            errors.append(f"{rule.key}: row layout differs from source template")
    return errors


def audit_release_layouts(args: argparse.Namespace) -> None:
    """Audit source-anchored release string placement and row layout."""

    if not args.english_rc:
        raise SystemExit("--audit-release-layouts requires --english-rc.")
    rules = parse_release_layouts(args.release_layouts)
    if not rules:
        raise SystemExit("--audit-release-layouts requires at least one layout rule.")
    targets = collect_target_rcs(args, "audit-release-layouts")
    templates = _release_layout_source_entries(args.english_rc, rules)
    errors: list[str] = []
    for target_path in targets:
        target_errors = _release_layout_errors(target_path, rules, templates)
        if target_errors:
            errors.append(f"{target_path}: release layout mismatch:\n" + "\n".join(target_errors))
        else:
            print(f"OK {target_path}: {len(rules)} release layout row(s)")
    if errors:
        raise SystemExit("\n\n".join(errors))


def _sync_release_layout_target(path: Path, rules: list[ReleaseLayoutRule], templates: dict[str, RcStringEntry]) -> bool:
    """Rewrite managed release layout rows in one target while preserving labels."""

    rc_text = read_rc(path)
    lines = rc_text.text.splitlines()
    changed = False
    for rule in rules:
        entries = []
        for index, line in enumerate(lines):
            entry = _parse_rc_string_line(line, index)
            if entry is not None:
                entries.append(entry)
        matching = [entry for entry in entries if entry.key == rule.key]
        if not matching:
            raise SystemExit(f"{path}: {rule.key} is missing; add a reviewed translation before sync.")
        values = {entry.value for entry in matching}
        if len(values) > 1:
            raise SystemExit(f"{path}: duplicate {rule.key} rows have conflicting translations.")
        value = matching[0].value
        old_line = lines[matching[0].line_index]
        # Remove duplicate or misplaced managed rows before reinserting at the source anchor.
        remove_indexes = {entry.line_index for entry in matching}
        lines = [line for index, line in enumerate(lines) if index not in remove_indexes]
        entries = []
        for index, line in enumerate(lines):
            entry = _parse_rc_string_line(line, index)
            if entry is not None:
                entries.append(entry)
        after_entry = _entry_by_key(entries, rule.after, path)
        before_entry = _entry_by_key(entries, rule.before, path)
        if after_entry.line_index >= before_entry.line_index:
            raise SystemExit(f"{path}: expected {rule.after} before {rule.before} for {rule.key}.")
        new_line = _format_release_layout_line(templates[rule.key], value)
        insert_at = after_entry.line_index + 1
        lines.insert(insert_at, new_line)
        changed = changed or len(matching) > 1 or matching[0].line_index != insert_at or old_line != new_line

    new_text = "\n".join(lines) + ("\n" if rc_text.text.endswith(("\n", "\r\n")) else "")
    if new_text != rc_text.text.replace("\r\n", "\n").replace("\r", "\n"):
        before_values = collect_rc_strings(path).values
        write_rc(path, rc_text, new_text)
        after_values = collect_rc_strings(path).values
        changed_values = [
            key for key in sorted(set(before_values) & set(after_values))
            if before_values[key] != after_values[key]
        ]
        removed_values = sorted(set(before_values) - set(after_values))
        added_values = sorted(set(after_values) - set(before_values))
        allowed = {rule.key for rule in rules}
        unexpected = [key for key in changed_values + removed_values + added_values if key not in allowed]
        if unexpected:
            raise SystemExit(f"{path}: release layout sync changed unrelated resource ids:\n" + "\n".join(unexpected))
        changed = True
    return changed


def sync_release_layouts(args: argparse.Namespace) -> None:
    """Sync source-anchored release string placement and layout."""

    if not args.english_rc:
        raise SystemExit("--sync-release-layouts requires --english-rc.")
    rules = parse_release_layouts(args.release_layouts)
    if not rules:
        raise SystemExit("--sync-release-layouts requires at least one layout rule.")
    targets = collect_target_rcs(args, "sync-release-layouts")
    templates = _release_layout_source_entries(args.english_rc, rules)
    changed_count = 0
    for target_path in targets:
        if _sync_release_layout_target(target_path, rules, templates):
            changed_count += 1
            print(f"SYNC {target_path}")
        else:
            print(f"OK {target_path}: already synced")
    print(f"Synced {changed_count}/{len(targets)} target RC file(s).")


def _required_or_source_ids(required_ids: list[str], source: dict[str, str]) -> list[str]:
    """Return explicit required ids or all source ids in source order."""

    return required_ids if required_ids else list(source)


def cross_reference(args: argparse.Namespace) -> None:
    """Cross-reference source and target RC string resources."""

    targets = collect_target_rcs(args, "cross-reference")

    source = collect_rc_strings(args.english_rc)
    required_ids = _required_or_source_ids(parse_id_list(args.require_ids), source.values)
    allowed_identical_ids = set(parse_id_list(args.allow_identical_ids))
    quality_rules = load_quality_rules(args.quality_rules)
    missing_in_source = [key for key in required_ids if key not in source.values]
    if source.duplicates:
        raise SystemExit(
            f"{args.english_rc} has duplicate resource ids:\n" + "\n".join(source.duplicates)
        )
    if missing_in_source:
        raise SystemExit(
            f"{args.english_rc} is missing required resource ids:\n" + "\n".join(missing_in_source)
        )

    errors: list[str] = []
    for target_path in targets:
        target = collect_rc_strings(target_path)
        target_ids = set(target.values)
        missing = [key for key in required_ids if key not in target_ids]
        extra = sorted(key for key in target_ids if key not in source.values)
        structural_errors = []
        quality_warnings = []
        for key in required_ids:
            if key not in target.values:
                continue
            for warning in structural_warnings(source.values[key], target.values[key]):
                structural_errors.append(f"{key}: {warning}")
            if args.quality_audit and key not in allowed_identical_ids:
                warning = untranslated_warning(source.values[key], target.values[key])
                if warning:
                    quality_warnings.append(f"{key}: {warning}")
            for warning in semantic_quality_warnings(target_path, key, target.values[key], quality_rules):
                quality_warnings.append(f"{key}: {warning}")
        if target.duplicates:
            errors.append(f"{target_path}: duplicate ids:\n" + "\n".join(target.duplicates))
        structure_warnings = resource_endif_structure_warnings(target_path)
        if structure_warnings:
            errors.append(f"{target_path}: resource block structure:\n" + "\n".join(structure_warnings))
        if missing:
            errors.append(f"{target_path}: missing ids:\n" + "\n".join(missing))
        if structural_errors:
            errors.append(f"{target_path}: structural mismatch:\n" + "\n".join(structural_errors))
        if quality_warnings:
            message = f"{target_path}: quality warnings:\n" + "\n".join(quality_warnings)
            if args.fail_on_quality_warning:
                errors.append(message)
            else:
                print(message)
        extra_text = f", {len(extra)} ids not present in source" if extra else ""
        if extra and args.show_extra:
            extra_text += " (" + ", ".join(extra) + ")"
        print(f"OK {target_path}: {len(required_ids) - len(missing)}/{len(required_ids)} required ids{extra_text}")
    if errors:
        raise SystemExit("\n\n".join(errors))


def missing_report(args: argparse.Namespace) -> None:
    """Print required release ids missing from target RC files."""

    targets = collect_target_rcs(args, "missing-report")

    source = collect_rc_strings(args.english_rc)
    required_ids = _required_or_source_ids(parse_id_list(args.require_ids), source.values)
    missing_in_source = [key for key in required_ids if key not in source.values]
    if missing_in_source:
        raise SystemExit(
            f"{args.english_rc} is missing required resource ids:\n" + "\n".join(missing_in_source)
        )

    any_missing = False
    for target_path in targets:
        target = collect_rc_strings(target_path)
        missing = [key for key in required_ids if key not in target.values]
        status = "MISSING" if missing else "OK"
        print(f"{status} {target_path}: {len(missing)}/{len(required_ids)} missing")
        if missing:
            any_missing = True
            for key in missing:
                print(f"  {key}\t{source.values[key]}")
    if any_missing and args.fail_on_missing:
        raise SystemExit("Missing release localization ids found.")


def validate_placeholders(english_rc: Path, rows: list[tuple[str, str]]) -> None:
    """Fail when translated structural markers differ from English."""

    english = collect_strings(english_rc)
    errors: list[str] = []
    for key, value in rows:
        if key not in english:
            continue
        for warning in structural_warnings(english[key], value):
            errors.append(f"{key}: {warning}")
    if errors:
        raise SystemExit("Structural marker mismatch:\n" + "\n".join(errors))


def apply_block(args: argparse.Namespace) -> None:
    """Apply a TSV-backed managed block to one RC file."""

    if not args.rc:
        raise SystemExit("--rc is required unless --cross-reference uses --target-rc.")
    rows = parse_tsv(args.tsv)
    required_ids = parse_id_list(args.require_ids)
    require_ids(rows, required_ids, "TSV")
    if args.english_rc:
        validate_placeholders(args.english_rc, rows)
    rc_text = read_rc(args.rc)
    endif = find_resource_endif(rc_text.text)
    before = rc_text.text[: endif.start()]
    after = rc_text.text[endif.start() :]
    before = strip_managed_or_probe_block(before, args.probe_start, args.probe_end)
    write_rc(args.rc, rc_text, before + build_string_table(rows) + after)


def audit_block(args: argparse.Namespace) -> None:
    """Audit one RC file for required ids and optional placeholder parity."""

    if not args.rc:
        raise SystemExit("--rc is required for --audit.")
    rows = list(collect_strings(args.rc).items())
    required_ids = parse_id_list(args.require_ids)
    require_ids(rows, required_ids, str(args.rc))
    if args.english_rc:
        validate_placeholders(args.english_rc, rows)
    print(f"OK {args.rc}")


def main() -> int:
    """Command-line entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rc", type=Path, help="RC file to edit or audit.")
    parser.add_argument(
        "--tsv",
        type=Path,
        help="KEY<TAB>VALUE translation input. Reads stdin when omitted.",
    )
    parser.add_argument(
        "--english-rc",
        type=Path,
        help="Optional English RC file used for printf placeholder validation.",
    )
    parser.add_argument(
        "--target-rc",
        type=Path,
        action="append",
        help="Target RC file for --cross-reference. Can be passed more than once.",
    )
    parser.add_argument(
        "--release-languages",
        type=Path,
        help="JSON release language manifest whose RC files are added as --target-rc entries.",
    )
    parser.add_argument(
        "--release-layouts",
        type=Path,
        help="JSON release layout manifest for source-anchored managed string placement.",
    )
    parser.add_argument(
        "--all-stock-targets",
        action="store_true",
        help="Add every stock eMule srchybrid/lang/*.rc file as a target.",
    )
    parser.add_argument(
        "--require-ids",
        type=Path,
        help="Optional one-id-per-line file of resource ids that must be present.",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Only audit the RC file for required ids/placeholders; do not edit.",
    )
    parser.add_argument(
        "--cross-reference",
        action="store_true",
        help="Compare English/source resource ids against target RC files.",
    )
    parser.add_argument(
        "--missing-report",
        action="store_true",
        help="Print required ids missing from target RC files.",
    )
    parser.add_argument(
        "--audit-release-manifest",
        action="store_true",
        help="Require --release-languages to enumerate every stock eMule language RC file.",
    )
    parser.add_argument(
        "--audit-release-layouts",
        action="store_true",
        help="Audit source-anchored release string placement and row layout.",
    )
    parser.add_argument(
        "--sync-release-layouts",
        action="store_true",
        help="Rewrite source-anchored release string rows while preserving labels.",
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Make --missing-report exit non-zero when any target is missing ids.",
    )
    parser.add_argument(
        "--quality-audit",
        action="store_true",
        help="During --cross-reference, report required ids that still look like copied English.",
    )
    parser.add_argument(
        "--allow-identical-ids",
        type=Path,
        help="Optional one-id-per-line list of resource ids where identical text is acceptable.",
    )
    parser.add_argument(
        "--quality-rules",
        type=Path,
        help="Optional JSON file with language/id-specific semantic translation quality rules.",
    )
    parser.add_argument(
        "--fail-on-quality-warning",
        action="store_true",
        help="Turn --quality-audit warnings into errors.",
    )
    parser.add_argument(
        "--show-extra",
        action="store_true",
        help="During --cross-reference, print target ids that are not present in the English source.",
    )
    parser.add_argument("--probe-start", default=DEFAULT_PROBE_START)
    parser.add_argument("--probe-end", default=DEFAULT_PROBE_END)
    args = parser.parse_args()
    if args.audit_release_manifest:
        audit_release_language_manifest(args)
    elif args.audit_release_layouts:
        audit_release_layouts(args)
    elif args.sync_release_layouts:
        sync_release_layouts(args)
    elif args.cross_reference:
        cross_reference(args)
    elif args.missing_report:
        missing_report(args)
    elif args.audit:
        audit_block(args)
    else:
        apply_block(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
