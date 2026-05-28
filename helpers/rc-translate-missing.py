#!/usr/bin/env python3
"""Translate missing Windows RC string resources into a managed string table.

Existing target translations are preserved by default. Use --manual-tsv for
curated translations of newly missing ids before falling back to machine
translation.
"""

from __future__ import annotations

import argparse
import csv
import concurrent.futures
import importlib.util
import json
import re
import sys
import time
from pathlib import Path


TOOL_DIR = Path(__file__).resolve().parent
STRING_TABLE_HELPER = TOOL_DIR / "rc-string-table.py"
DEFAULT_CACHE = TOOL_DIR.parent / ".local" / "rc-translation-cache.json"
DEFAULT_PROTECT_TERMS = [
    "eMuleBB",
    "eMule",
    "eMule Plus",
    "eMuleFuture",
    "eDonkey",
    "eD2K",
    "Kad",
    "Kademlia",
    "ED2K",
    "TCP",
    "UDP",
    "UPnP",
    "NAT-PMP",
    "PCP",
    "HTTP",
    "HTTPS",
    "REST",
    "REST API",
    "JSON",
    "CSV",
    "MRTG",
    "IRC",
    "IP",
    "IPv4",
    "IPv6",
    "LowID",
    "HighID",
    "WebServer",
    "Web UI",
    "Windows",
    "Windows Firewall",
    "FFmpeg",
    "VLC",
    "MediaInfo",
    "MediaInfo.dll",
    "ffmpeg.exe",
]
FILENAME_RE = re.compile(
    r"\b[\w.-]+\.(?:ini|dat|met|dll|exe|log|txt|xml|tmpl|css|js|html|zip|rar|7z|part|bak)\b",
    re.IGNORECASE,
)
URL_RE = re.compile(r"\b(?:https?|ed2k)://[^\s\"<>]+", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"%(?:%|[-+ #0]*\d*(?:\.\d+)?[hlI64]*[A-Za-z])|%")
ESCAPE_RE = re.compile(r"\\(?:r\\n|n|r|t)")
TOKEN_RE = re.compile(r"QZX(\d+)XZQ")
ESCAPE_GROUP_RE = re.compile(r"(?:\\r\\n|\\n|\\r|\\t)+")
FORMAT_MARKER_RE = re.compile(r"%(?:%|[-+ #0]*\d*(?:\.\d+)?[hlI64]*[A-Za-z])|%")


def load_rc_helper():
    """Load the RC string-table helper module from the same directory."""

    spec = importlib.util.spec_from_file_location("rc_string_table", STRING_TABLE_HELPER)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load helper: {STRING_TABLE_HELPER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_translator(target: str):
    """Create a GoogleTranslator instance with an actionable dependency error."""

    try:
        from deep_translator import GoogleTranslator
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency. Install with: python -m pip install --user deep-translator"
        ) from exc
    return GoogleTranslator(source="en", target=target)


def load_cache(path: Path) -> dict[str, dict[str, str]]:
    """Load the translation cache."""

    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(path: Path, cache: dict[str, dict[str, str]]) -> None:
    """Persist the translation cache atomically enough for one local process."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_token(tokens: list[str], value: str) -> str:
    """Add a protected value and return its token."""

    token = f"QZX{len(tokens)}XZQ"
    tokens.append(value)
    return token


def protect_text(text: str, extra_terms: list[str]) -> tuple[str, list[str]]:
    """Protect placeholders and literals that translators must not alter."""

    tokens: list[str] = []
    protected = text
    for regex in (URL_RE, FILENAME_RE, PLACEHOLDER_RE, ESCAPE_RE):
        protected = regex.sub(lambda match: add_token(tokens, match.group(0)), protected)
    for term in sorted(DEFAULT_PROTECT_TERMS + extra_terms, key=len, reverse=True):
        protected = re.sub(re.escape(term), lambda match: add_token(tokens, match.group(0)), protected)
    return protected, tokens


def restore_text(text: str, tokens: list[str]) -> str:
    """Restore protected tokens after translation."""

    restored = text
    for match in sorted(TOKEN_RE.findall(restored), key=lambda value: int(value), reverse=True):
        index = int(match)
        if 0 <= index < len(tokens):
            restored = restored.replace(f"QZX{match}XZQ", tokens[index])
    for old, new in (
        (" \\r\\n ", "\\r\\n"),
        ("\\r\\n ", "\\r\\n"),
        (" \\r\\n", "\\r\\n"),
        (" \\n ", "\\n"),
        ("\\n ", "\\n"),
        (" \\n", "\\n"),
        (" \\t ", "\\t"),
        ("\\t ", "\\t"),
        (" \\t", "\\t"),
    ):
        restored = restored.replace(old, new)
    return restored


def restore_escape_layout(source: str, translated: str) -> str:
    """Reinsert RC escape groups when translation collapses protected paragraph separators."""

    source_groups = ESCAPE_GROUP_RE.findall(source)
    if not source_groups:
        return translated
    if ESCAPE_RE.findall(translated) == ESCAPE_RE.findall(source):
        return translated

    result = ESCAPE_GROUP_RE.sub(" ", translated).strip()
    if not result:
        return translated
    for group in source_groups:
        source_offset = source.find(group)
        ratio = source_offset / max(len(source), 1)
        target_index = max(1, min(len(result), round(len(result) * ratio)))
        punctuation = [". ", "! ", "? ", ": ", "; ", "。", "！", "؟ ", "؟", "؟ "]
        candidates = []
        for marker in punctuation:
            start = 0
            while True:
                found = result.find(marker, start)
                if found == -1:
                    break
                candidates.append(found + len(marker))
                start = found + len(marker)
        if candidates:
            target_index = min(candidates, key=lambda item: abs(item - target_index))
        result = result[:target_index].rstrip() + group + result[target_index:].lstrip()
    return result


def format_markers(value: str) -> list[str]:
    """Return RC printf and literal-percent markers in order."""

    return FORMAT_MARKER_RE.findall(value)


def restore_format_markers(source: str, translated: str) -> str:
    """Append source markers that a translation engine dropped from placeholder-heavy text."""

    source_markers = format_markers(source)
    if not source_markers:
        return translated
    target_markers = format_markers(translated)
    if target_markers == source_markers:
        return translated
    index = 0
    missing: list[str] = []
    for marker in source_markers:
        if index < len(target_markers) and target_markers[index] == marker:
            index += 1
        else:
            missing.append(marker)
    if index != len(target_markers) or not missing:
        return translated
    return translated.rstrip() + " " + " ".join(missing)


def normalize_mnemonic(source: str, translated: str) -> str:
    """Keep one menu mnemonic when the English source had one."""

    if "&" not in source:
        return translated.replace("&", "")
    translated = translated.replace("&", "")
    match = re.search(r"\w", translated, re.UNICODE)
    if not match:
        return translated
    return translated[: match.start()] + "&" + translated[match.start() :]


def translate_value(translator, source: str, extra_terms: list[str]) -> str:
    """Translate one RC string value while preserving RC-sensitive tokens."""

    protected, tokens = protect_text(source.replace("&", ""), extra_terms)
    if not re.search(r"[A-Za-z]", protected):
        return normalize_mnemonic(source, restore_text(protected, tokens))
    for attempt in range(5):
        try:
            translated = translator.translate(protected)
            if translated is None:
                raise RuntimeError("translator returned no text")
            restored = restore_text(translated, tokens)
            restored = restore_escape_layout(source, restored)
            restored = restore_format_markers(source, restored)
            return normalize_mnemonic(source, restored)
        except Exception:
            if attempt == 4:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise AssertionError("unreachable")


def translate_values_batch(translator, sources: list[str], extra_terms: list[str], batch_size: int) -> list[str]:
    """Translate several RC string values, falling back per-string on batch failure."""

    results: list[str] = []
    prepared: list[tuple[str, str, list[str]]] = []
    for source in sources:
        protected, tokens = protect_text(source.replace("&", ""), extra_terms)
        if not re.search(r"[A-Za-z]", protected):
            results.append(normalize_mnemonic(source, restore_text(protected, tokens)))
        else:
            prepared.append((source, protected, tokens))
            results.append("")

    translated_by_source: dict[int, str] = {}
    for start in range(0, len(prepared), batch_size):
        chunk = prepared[start : start + batch_size]
        protected_values = [protected for _, protected, _ in chunk]
        try:
            translated_values = translator.translate_batch(protected_values)
        except Exception:
            translated_values = [None] * len(chunk)
        if translated_values is None or len(translated_values) != len(chunk):
            translated_values = [None] * len(chunk)
        for offset, (source, protected, tokens) in enumerate(chunk):
            translated = translated_values[offset]
            if translated is None:
                translated_by_source[start + offset] = translate_value(translator, source, extra_terms)
            else:
                restored = restore_text(translated, tokens)
                restored = restore_escape_layout(source, restored)
                restored = restore_format_markers(source, restored)
                translated_by_source[start + offset] = normalize_mnemonic(source, restored)

    prepared_index = 0
    final: list[str] = []
    for source, current in zip(sources, results):
        if current:
            final.append(current)
        else:
            final.append(translated_by_source[prepared_index])
            prepared_index += 1
    return final


def managed_rows(rc_helper, path: Path) -> list[tuple[str, str]]:
    """Return rows from the existing managed block, if any."""

    text = rc_helper.read_rc(path).text
    block = re.search(
        r"// eMuleBB managed translation block: begin.*?// eMuleBB managed translation block: end",
        text,
        re.S,
    )
    if not block:
        return []
    return [
        (key, raw.replace('""', '"'))
        for key, raw in re.findall(r'^\s*(IDS_[A-Z0-9_]+)\s+"((?:[^"]|"")*)"', block.group(0), re.M)
    ]


def collect_missing_ids(source: dict[str, str], target: dict[str, str], required: list[str]) -> list[str]:
    """Return missing ids in source order, optionally constrained by required ids."""

    wanted = required if required else list(source)
    return [key for key in wanted if key in source and key not in target]


def stock_lang_dir(source_rc: Path) -> Path:
    """Return the stock eMule language directory for a source RC file."""

    return source_rc.parent / "lang"


def stock_rc_files(source_rc: Path) -> list[Path]:
    """Return all stock eMule language RC files available next to source RC."""

    lang_dir = stock_lang_dir(source_rc)
    if not lang_dir.is_dir():
        raise SystemExit(f"Stock language directory does not exist: {lang_dir}")
    return sorted(path for path in lang_dir.glob("*.rc") if path.is_file())


def ensure_stock_target(source_rc: Path, target_rc: Path) -> None:
    """Fail unless target_rc is one of the stock eMule language RC files."""

    lang_dir = stock_lang_dir(source_rc).resolve()
    target = target_rc.resolve()
    if target.parent != lang_dir or target.suffix.lower() != ".rc":
        raise SystemExit(
            f"{target_rc} is not a stock eMule language RC under {lang_dir}."
        )


def apply_rows(rc_helper, path: Path, rows: list[tuple[str, str]]) -> None:
    """Rewrite the managed block with the provided rows."""

    rc_text = rc_helper.read_rc(path)
    endif = rc_helper.find_resource_endif(rc_text.text)
    before = rc_helper.strip_managed_or_probe_block(
        rc_text.text[: endif.start()],
        rc_helper.DEFAULT_PROBE_START,
        rc_helper.DEFAULT_PROBE_END,
    )
    rc_helper.write_rc(path, rc_text, before + rc_helper.build_string_table(rows) + rc_text.text[endif.start() :])


def release_validation_rows(
    rows: list[tuple[str, str]],
    required_ids: list[str],
) -> list[tuple[str, str]]:
    """Return rows that must satisfy release structural marker checks."""

    if not required_ids:
        return rows
    required = set(required_ids)
    return [(key, value) for key, value in rows if key in required]


def verify_non_managed_unchanged(
    rc_helper,
    path: Path,
    before: dict[str, str],
    managed_keys: set[str],
) -> None:
    """Fail if applying a managed block changed stock/non-managed strings."""

    after = rc_helper.collect_rc_strings(path).values
    changed = [
        key
        for key in sorted(set(before) & set(after))
        if key not in managed_keys and before[key] != after[key]
    ]
    removed = [key for key in sorted(set(before) - set(after)) if key not in managed_keys]
    if changed or removed:
        details = []
        if changed:
            details.append("changed non-managed ids:\n" + "\n".join(changed))
        if removed:
            details.append("removed non-managed ids:\n" + "\n".join(removed))
        raise SystemExit(f"{path}: managed update touched stock translations:\n" + "\n\n".join(details))


def write_review_packet(
    path: Path,
    source: dict[str, str],
    keys: list[str],
    drafts: dict[str, str],
    manual_keys: set[str],
    cached_before: set[str],
) -> None:
    """Write a review TSV with English source, draft translation, and provenance."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["KEY", "ENGLISH", "DRAFT", "NOTES"])
        for key in keys:
            if key in manual_keys:
                note = "manual"
            elif key in cached_before:
                note = "cache"
            elif drafts.get(key):
                note = "machine-draft"
            else:
                note = "missing-manual-translation"
            writer.writerow([key, source[key], drafts.get(key, ""), note])


def run(args: argparse.Namespace) -> None:
    """Translate missing strings and update the target RC managed block."""

    if not args.target_rc:
        raise SystemExit("--target-rc is required unless --all-stock-targets is used.")
    if not args.target_lang:
        raise SystemExit("--target-lang is required unless --all-stock-targets is used.")
    if args.require_stock_target:
        ensure_stock_target(args.source_rc, args.target_rc)

    rc_helper = load_rc_helper()
    source = rc_helper.collect_rc_strings(args.source_rc)
    target = rc_helper.collect_rc_strings(args.target_rc)
    required = rc_helper.parse_id_list(args.require_ids)
    manual_rows = rc_helper.parse_tsv(args.manual_tsv) if args.manual_tsv else []
    manual_map = dict(manual_rows)
    if manual_rows:
        rc_helper.validate_placeholders(args.source_rc, manual_rows)
    existing_rows = managed_rows(rc_helper, args.target_rc)
    existing_map = dict(existing_rows)
    missing = collect_missing_ids(source.values, target.values, required)
    cache = {} if args.ignore_cache else load_cache(args.cache)
    cache_key = f"{args.target_lang}:{args.target_rc.name}"
    cache.setdefault(cache_key, {})
    cached_before = set(cache[cache_key])

    new_rows: list[tuple[str, str]] = []
    refreshed_keys: list[str] = []
    if args.refresh_manual:
        refreshed_rows: list[tuple[str, str]] = []
        for key, value in existing_rows:
            if key in manual_map:
                refreshed = manual_map[key]
                if refreshed != value:
                    refreshed_keys.append(key)
                refreshed_rows.append((key, refreshed))
            else:
                refreshed_rows.append((key, value))
        existing_rows = refreshed_rows
        existing_map = dict(existing_rows)

    manual_keys = [key for key in missing if key in manual_map and key not in existing_map]
    for key in manual_keys:
        cache[cache_key][key] = manual_map[key]
    if manual_keys and not args.ignore_cache:
        save_cache(args.cache, cache)
    uncached_keys = [key for key in missing if key not in existing_map and key not in cache[cache_key]]
    translator = load_translator(args.target_lang) if uncached_keys and not args.no_machine_translate else None
    for start in range(0, len(uncached_keys), args.batch_size):
        chunk_keys = uncached_keys[start : start + args.batch_size]
        if args.no_machine_translate:
            break
        translated_values = translate_values_batch(
            translator,
            [source.values[key] for key in chunk_keys],
            args.protect_term,
            args.batch_size,
        )
        for key, value in zip(chunk_keys, translated_values):
            cache[cache_key][key] = value
        if not args.ignore_cache:
            save_cache(args.cache, cache)
        translated_count = min(start + len(chunk_keys), len(uncached_keys))
        if args.progress:
            print(f"{args.target_rc.name}: cached {translated_count}/{len(uncached_keys)} new translations")

    missing_translation_keys = [
        key for key in missing if key not in existing_map and key not in cache[cache_key]
    ]
    if args.review_packet:
        review_keys = [key for key in missing if key not in existing_map]
        write_review_packet(
            args.review_packet,
            source.values,
            review_keys,
            cache[cache_key],
            set(manual_keys),
            cached_before,
        )
    if missing_translation_keys and not (args.draft_only or args.dry_run):
        raise SystemExit(
            "Missing translations; provide --manual-tsv, allow machine translation, or use --draft-only:\n"
            + "\n".join(missing_translation_keys)
        )

    for key in missing:
        if key in existing_map:
            continue
        if key not in cache[cache_key]:
            continue
        new_rows.append((key, cache[cache_key][key]))

    rows = existing_rows + new_rows
    if not args.dry_run and not args.draft_only:
        if new_rows or refreshed_keys:
            rc_helper.validate_placeholders(args.source_rc, release_validation_rows(rows, required))
            original_values = dict(target.values)
            apply_rows(rc_helper, args.target_rc, rows)
            verify_non_managed_unchanged(
                rc_helper,
                args.target_rc,
                original_values,
                {key for key, _ in rows},
            )
        else:
            print(f"{args.target_rc}: no new curated managed rows")
    print(
        f"{args.target_rc}: preserved {len(target.values) - len(missing)} existing rows, "
        f"added {len(new_rows)} rows ({len(manual_keys)} manual), "
        f"refreshed {len(refreshed_keys)} rows, "
        f"missing drafts {len(missing_translation_keys)}, managed rows {len(rows)}"
    )


def _batch_one(base_args: argparse.Namespace, target_rc: Path) -> str:
    """Generate one stock review packet in draft-only mode."""

    child_args = argparse.Namespace(**vars(base_args))
    child_args.target_rc = target_rc
    child_args.target_lang = target_rc.stem
    child_args.review_packet = base_args.review_dir / f"{target_rc.stem}.tsv"
    child_args.progress = 0
    run(child_args)
    return str(child_args.review_packet)


def _apply_one_stock_target(base_args: argparse.Namespace, target_rc: Path) -> str:
    """Apply curated managed translations to one stock language RC file."""

    child_args = argparse.Namespace(**vars(base_args))
    child_args.target_rc = target_rc
    child_args.target_lang = target_rc.stem
    child_args.review_packet = None
    child_args.progress = 0
    candidate = base_args.manual_dir / f"{target_rc.stem}.tsv"
    child_args.manual_tsv = candidate if candidate.is_file() else None
    run(child_args)
    return str(target_rc)


def run_all_stock_targets(args: argparse.Namespace) -> None:
    """Generate or apply stock-language managed translation updates."""

    if not args.no_machine_translate:
        raise SystemExit("--all-stock-targets requires --no-machine-translate; all-language release updates must use curated TSVs.")
    if args.manual_tsv:
        raise SystemExit("--all-stock-targets does not accept --manual-tsv; use --manual-dir for per-language TSVs.")
    if args.jobs < 1:
        raise SystemExit("--jobs must be at least 1.")

    targets = stock_rc_files(args.source_rc)
    if args.draft_only:
        if not args.review_dir:
            raise SystemExit("--all-stock-targets --draft-only requires --review-dir.")
        args.review_dir.mkdir(parents=True, exist_ok=True)
        print(f"Generating {len(targets)} stock eMule review packet(s) under {args.review_dir}")
        if args.jobs == 1:
            outputs = [_batch_one(args, target) for target in targets]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
                outputs = list(executor.map(lambda target: _batch_one(args, target), targets))
        for output in outputs:
            print(f"REVIEW {output}")
        return

    if args.dry_run:
        raise SystemExit("--all-stock-targets apply mode does not support --dry-run; use --draft-only for review packets.")
    if not args.manual_dir:
        raise SystemExit("--all-stock-targets apply mode requires --manual-dir with one <lang-rc-stem>.tsv file per target needing rows.")
    if args.jobs != 1:
        raise SystemExit("--all-stock-targets apply mode writes RC files and must run with --jobs 1.")
    print(f"Applying curated managed translations to {len(targets)} stock eMule RC file(s)")
    for target in targets:
        print(f"APPLY {_apply_one_stock_target(args, target)}")


def main() -> int:
    """Command-line entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-rc", type=Path, required=True, help="English/source RC file.")
    parser.add_argument("--target-rc", type=Path, help="Target language RC file.")
    parser.add_argument("--target-lang", help="deep-translator target language code.")
    parser.add_argument("--require-ids", type=Path, help="Optional one-id-per-line resource id list.")
    parser.add_argument(
        "--manual-tsv",
        type=Path,
        help="Optional KEY<TAB>VALUE file with curated translations for newly missing ids.",
    )
    parser.add_argument(
        "--manual-dir",
        type=Path,
        help="Directory containing <target-rc-stem>.tsv files for --all-stock-targets apply mode.",
    )
    parser.add_argument(
        "--refresh-manual",
        action="store_true",
        help="Replace existing managed rows when their ids are present in a curated manual TSV.",
    )
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="Translation cache path.")
    parser.add_argument("--protect-term", action="append", default=[], help="Additional literal term to preserve.")
    parser.add_argument("--progress", type=int, default=25, help="Progress interval; 0 disables progress.")
    parser.add_argument("--batch-size", type=int, default=25, help="Number of strings to request per batch.")
    parser.add_argument("--dry-run", action="store_true", help="Translate/cache but do not rewrite the target RC.")
    parser.add_argument(
        "--draft-only",
        action="store_true",
        help="Create cache/review output only; never rewrite the target RC.",
    )
    parser.add_argument(
        "--no-machine-translate",
        action="store_true",
        help="Do not call machine translation; require manual TSV or existing cache.",
    )
    parser.add_argument(
        "--review-packet",
        type=Path,
        help="Write KEY/ENGLISH/DRAFT/NOTES TSV for manual or Codex review.",
    )
    parser.add_argument(
        "--review-dir",
        type=Path,
        help="Directory for --all-stock-targets review packet TSVs.",
    )
    parser.add_argument(
        "--all-stock-targets",
        action="store_true",
        help="Generate draft-only review packets for every stock eMule language RC file.",
    )
    parser.add_argument(
        "--require-stock-target",
        action="store_true",
        help="Refuse target RC files outside the stock eMule srchybrid/lang directory.",
    )
    parser.add_argument(
        "--ignore-cache",
        action="store_true",
        help="Ignore .local translation cache and do not save new cache entries.",
    )
    parser.add_argument("--jobs", type=int, default=1, help="Parallel jobs for --all-stock-targets.")
    args = parser.parse_args()
    if args.all_stock_targets:
        run_all_stock_targets(args)
    else:
        run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
