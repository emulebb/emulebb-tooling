#!/usr/bin/env python3
"""Production helpers for the static eMuleBB pages site."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


SITE_BASE_URL = "https://emulebb.github.io"
PICO_CDN = "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css"
PROHIBITED_ASSET_PATTERN = re.compile(
    r"emule-logo|Logo\.jpg|favicon|screenshot",
    re.IGNORECASE,
)
ALLOWED_IMAGE_SRC_PATTERN = re.compile(
    r"^(?:\.\./)*assets/(?:team/[a-z0-9-]+|brand/emulebb-broadband-edition-logo)\.png$"
)


@dataclass(frozen=True)
class PageSpec:
    """Describes one canonical static page emitted by the pages site."""

    hreflang: str
    html_lang: str
    directory: str
    priority: str

    @property
    def relative_file(self) -> Path:
        """Return the site-relative index file for the page."""

        if self.directory:
            return Path(self.directory) / "index.html"
        return Path("index.html")

    @property
    def url(self) -> str:
        """Return the canonical public URL for the page."""

        if self.directory:
            return f"{SITE_BASE_URL}/{self.directory}/"
        return f"{SITE_BASE_URL}/"

    @property
    def stylesheet_href(self) -> str:
        """Return the expected relative stylesheet href for the page."""

        return f"{relative_prefix(self)}styles.css"


CANONICAL_PAGES = (
    PageSpec("en", "en", "", "1.0"),
    PageSpec("ar-AE", "ar-AE", "ar-ae", "0.8"),
    PageSpec("eu", "eu", "eu", "0.8"),
    PageSpec("bg", "bg", "bg", "0.8"),
    PageSpec("ca", "ca", "ca", "0.8"),
    PageSpec("cs", "cs", "cs", "0.8"),
    PageSpec("da", "da", "da", "0.8"),
    PageSpec("el", "el", "el", "0.8"),
    PageSpec("es", "es", "es", "0.8"),
    PageSpec("ast", "ast", "ast", "0.8"),
    PageSpec("et", "et", "et", "0.8"),
    PageSpec("fa", "fa", "fa", "0.8"),
    PageSpec("fi", "fi", "fi", "0.8"),
    PageSpec("br", "br", "br", "0.8"),
    PageSpec("pt-BR", "pt-BR", "pt-br", "0.8"),
    PageSpec("pt-PT", "pt-PT", "pt-pt", "0.8"),
    PageSpec("gl", "gl", "gl", "0.8"),
    PageSpec("he", "he", "he", "0.8"),
    PageSpec("hu", "hu", "hu", "0.8"),
    PageSpec("it", "it", "it", "0.8"),
    PageSpec("ja", "ja", "ja", "0.8"),
    PageSpec("ko", "ko", "ko", "0.8"),
    PageSpec("lt", "lt", "lt", "0.8"),
    PageSpec("lv", "lv", "lv", "0.8"),
    PageSpec("mt", "mt", "mt", "0.8"),
    PageSpec("nb", "nb", "nb", "0.8"),
    PageSpec("ru", "ru", "ru", "0.8"),
    PageSpec("de", "de", "de", "0.8"),
    PageSpec("fr", "fr", "fr", "0.8"),
    PageSpec("pl", "pl", "pl", "0.8"),
    PageSpec("nl", "nl", "nl", "0.8"),
    PageSpec("nn", "nn", "nn", "0.8"),
    PageSpec("ro", "ro", "ro", "0.8"),
    PageSpec("sl", "sl", "sl", "0.8"),
    PageSpec("sq", "sq", "sq", "0.8"),
    PageSpec("sv", "sv", "sv", "0.8"),
    PageSpec("tr", "tr", "tr", "0.8"),
    PageSpec("uk", "uk", "uk", "0.8"),
    PageSpec("ug-CN", "ug-CN", "ug-cn", "0.8"),
    PageSpec("ca-ES-valencia", "ca-ES-valencia", "ca-valencia", "0.8"),
    PageSpec("ca-ES-valencia-x-racv", "ca-ES-valencia-x-racv", "ca-valencia-racv", "0.8"),
    PageSpec("vi", "vi", "vi", "0.8"),
    PageSpec("zh-CN", "zh-CN", "zh-cn", "0.8"),
    PageSpec("zh-TW", "zh-TW", "zh-tw", "0.8"),
)
LANGUAGE_PAGE = PageSpec("en", "en", "languages", "0.7")
FAQ_LOCALE_DIRECTORIES = (
    ("en", "en", "faq"),
    ("it", "it", "it/faq"),
    ("es", "es", "es/faq"),
    ("pt-BR", "pt-BR", "pt-br/faq"),
    ("fr", "fr", "fr/faq"),
    ("de", "de", "de/faq"),
    ("pl", "pl", "pl/faq"),
    ("nl", "nl", "nl/faq"),
    ("ru", "ru", "ru/faq"),
    ("uk", "uk", "uk/faq"),
    ("zh-CN", "zh-CN", "zh-cn/faq"),
    ("ja", "ja", "ja/faq"),
)
FAQ_PAGES = tuple(
    PageSpec(hreflang, html_lang, directory, "0.8")
    for hreflang, html_lang, directory in FAQ_LOCALE_DIRECTORIES
)
ENGLISH_FAQ_PAGE = FAQ_PAGES[0]
EXPECTED_HREFLANGS = {page.hreflang for page in CANONICAL_PAGES} | {"x-default"}
EXPECTED_FAQ_HREFLANGS = {page.hreflang for page in FAQ_PAGES} | {"x-default"}


class ParsedPage(HTMLParser):
    """Collect the small set of HTML fields required by the pages checks."""

    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.robots: list[str] = []
        self.canonicals: list[str] = []
        self.sitemaps: list[str] = []
        self.stylesheets: list[str] = []
        self.alternates: dict[str, str] = {}
        self.og_urls: list[str] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = {name.lower(): value or "" for name, value in attrs}
        if tag == "html":
            self.html_lang = attrs_by_name.get("lang")
        if "id" in attrs_by_name:
            self.ids.add(attrs_by_name["id"])
        if tag == "a" and "href" in attrs_by_name:
            self.hrefs.append(attrs_by_name["href"])
        if tag == "img":
            self.images.append(attrs_by_name)
        if tag == "meta":
            if attrs_by_name.get("name") == "robots":
                self.robots.append(attrs_by_name.get("content", ""))
            if attrs_by_name.get("property") == "og:url":
                self.og_urls.append(attrs_by_name.get("content", ""))
        if tag != "link":
            return

        rel_tokens = set(attrs_by_name.get("rel", "").split())
        href = attrs_by_name.get("href", "")
        if "canonical" in rel_tokens:
            self.canonicals.append(href)
        if "sitemap" in rel_tokens:
            self.sitemaps.append(href)
        if "stylesheet" in rel_tokens:
            self.stylesheets.append(href)
        if "alternate" in rel_tokens and "hreflang" in attrs_by_name:
            self.alternates[attrs_by_name["hreflang"]] = href


def parse_args() -> argparse.Namespace:
    """Parse the command line for static page production helpers."""

    parser = argparse.ArgumentParser(
        description="Validate and produce shared files for eMuleBB static pages."
    )
    parser.add_argument(
        "--pages-root",
        type=Path,
        default=None,
        help=(
            "Path to the emulebb-pages checkout. Defaults to EMULEBB_PAGES_ROOT, "
            "then common EMULEBB_WORKSPACE_ROOT-relative layouts."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Validate static HTML, sitemap, and assets.")

    sitemap = subparsers.add_parser(
        "write-sitemap",
        help="Render sitemap.xml from the canonical page list.",
    )
    sitemap.add_argument(
        "--lastmod",
        default=dt.date.today().isoformat(),
        help="ISO date for sitemap lastmod values. Defaults to today.",
    )
    sitemap.add_argument(
        "--check",
        action="store_true",
        help="Fail if sitemap.xml differs instead of rewriting it.",
    )

    subparsers.add_parser("list-locales", help="Print the canonical page locale map.")
    return parser.parse_args()


def candidate_pages_roots(explicit: Path | None) -> list[Path]:
    """Return candidate emulebb-pages roots without hardcoding machine paths."""

    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit)
    if os.environ.get("EMULEBB_PAGES_ROOT"):
        candidates.append(Path(os.environ["EMULEBB_PAGES_ROOT"]))
    if os.environ.get("EMULEBB_WORKSPACE_ROOT"):
        workspace_root = Path(os.environ["EMULEBB_WORKSPACE_ROOT"])
        candidates.extend(
            [
                workspace_root / "repos" / "emulebb-pages",
                workspace_root.parent / "emulebb-pages",
            ]
        )

    cwd = Path.cwd()
    candidates.extend([cwd, cwd / "emulebb-pages", cwd.parent / "emulebb-pages"])
    for parent in Path(__file__).resolve().parents:
        candidates.append(parent / "emulebb-pages")
        if parent.name == "emulebb-pages":
            candidates.append(parent)

    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def resolve_pages_root(explicit: Path | None) -> Path:
    """Find an emulebb-pages checkout and fail with actionable guidance."""

    for candidate in candidate_pages_roots(explicit):
        if (candidate / "index.html").is_file() and (candidate / "styles.css").is_file():
            return candidate
    raise SystemExit(
        "Could not find emulebb-pages. Pass --pages-root or set EMULEBB_PAGES_ROOT."
    )


def read_text(path: Path) -> str:
    """Read a UTF-8 text file with a path-focused error message."""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: not valid UTF-8") from exc


def parse_page(path: Path) -> ParsedPage:
    """Parse one HTML page into validation metadata."""

    parser = ParsedPage()
    parser.feed(read_text(path))
    return parser


def expect(errors: list[str], condition: bool, message: str) -> None:
    """Append a validation error when a condition fails."""

    if not condition:
        errors.append(message)


def relative_prefix(page: PageSpec) -> str:
    """Return the relative prefix from a generated page to the site root."""

    if not page.directory:
        return ""
    return "../" * len(page.directory.split("/"))


def validate_page(pages_root: Path, page: PageSpec, errors: list[str]) -> None:
    """Validate one canonical localized HTML page."""

    path = pages_root / page.relative_file
    expect(errors, path.is_file(), f"{page.relative_file}: missing page")
    if not path.is_file():
        return

    text = read_text(path)
    parsed = parse_page(path)
    expect(errors, text.lower().count("<!doctype html>") == 1, f"{page.relative_file}: expected one doctype")
    expect(errors, parsed.html_lang == page.html_lang, f"{page.relative_file}: html lang should be {page.html_lang}")
    expect(errors, parsed.robots == ["index,follow"], f"{page.relative_file}: robots should be index,follow")
    expect(errors, parsed.canonicals == [page.url], f"{page.relative_file}: canonical should be {page.url}")
    expect(errors, parsed.og_urls == [page.url], f"{page.relative_file}: og:url should be {page.url}")
    expect(errors, parsed.sitemaps == [f"{SITE_BASE_URL}/sitemap.xml"], f"{page.relative_file}: sitemap link mismatch")
    expect(errors, PICO_CDN in parsed.stylesheets, f"{page.relative_file}: missing Pico CSS CDN")
    expect(errors, page.stylesheet_href in parsed.stylesheets, f"{page.relative_file}: missing {page.stylesheet_href}")
    expect(
        errors,
        set(parsed.alternates) == EXPECTED_HREFLANGS,
        f"{page.relative_file}: hreflang set mismatch",
    )
    for alt in CANONICAL_PAGES:
        expect(
            errors,
            parsed.alternates.get(alt.hreflang) == alt.url,
            f"{page.relative_file}: alternate {alt.hreflang} URL mismatch",
        )
    expect(
        errors,
        parsed.alternates.get("x-default") == SITE_BASE_URL + "/",
        f"{page.relative_file}: x-default alternate URL mismatch",
    )
    for href in parsed.hrefs:
        if href.startswith("#"):
            expect(errors, href[1:] in parsed.ids, f"{page.relative_file}: missing anchor target {href}")
    validate_images(page.relative_file, parsed, errors)


def validate_images(relative_file: Path, parsed: ParsedPage, errors: list[str]) -> None:
    """Allow only the header brand logo and section-local Team/lore images."""

    for attrs in parsed.images:
        src = attrs.get("src", "")
        alt = attrs.get("alt", "")
        if not ALLOWED_IMAGE_SRC_PATTERN.match(src):
            errors.append(f"{relative_file}: unsupported image source: {src}")
        if not alt.strip():
            errors.append(f"{relative_file}: image is missing alt text: {src}")


def validate_language_page(pages_root: Path, errors: list[str]) -> None:
    """Validate the indexable language selector page."""

    path = pages_root / LANGUAGE_PAGE.relative_file
    expect(errors, path.is_file(), f"{LANGUAGE_PAGE.relative_file}: missing language page")
    if not path.is_file():
        return

    text = read_text(path)
    parsed = parse_page(path)
    expect(errors, text.lower().count("<!doctype html>") == 1, f"{LANGUAGE_PAGE.relative_file}: expected one doctype")
    expect(errors, parsed.html_lang == "en", f"{LANGUAGE_PAGE.relative_file}: html lang should be en")
    expect(errors, parsed.robots == ["index,follow"], f"{LANGUAGE_PAGE.relative_file}: robots should be index,follow")
    expect(errors, parsed.canonicals == [LANGUAGE_PAGE.url], f"{LANGUAGE_PAGE.relative_file}: canonical mismatch")
    expect(errors, parsed.og_urls == [LANGUAGE_PAGE.url], f"{LANGUAGE_PAGE.relative_file}: og:url should be {LANGUAGE_PAGE.url}")
    expect(errors, set(parsed.alternates) == EXPECTED_HREFLANGS, f"{LANGUAGE_PAGE.relative_file}: hreflang set mismatch")
    expect(errors, PICO_CDN in parsed.stylesheets, f"{LANGUAGE_PAGE.relative_file}: missing Pico CSS CDN")
    expect(errors, LANGUAGE_PAGE.stylesheet_href in parsed.stylesheets, f"{LANGUAGE_PAGE.relative_file}: missing {LANGUAGE_PAGE.stylesheet_href}")
    for page in CANONICAL_PAGES:
        expected_href = f"../{page.directory}/" if page.directory else "../"
        expect(errors, expected_href in parsed.hrefs, f"{LANGUAGE_PAGE.relative_file}: missing link to {page.url}")
    expect(errors, not (pages_root / "pt" / "index.html").exists(), "pt/index.html: generic chooser should not exist")
    validate_images(LANGUAGE_PAGE.relative_file, parsed, errors)


def validate_faq_page(pages_root: Path, page: PageSpec, errors: list[str]) -> None:
    """Validate one indexable FAQ page."""

    path = pages_root / page.relative_file
    expect(errors, path.is_file(), f"{page.relative_file}: missing FAQ page")
    if not path.is_file():
        return

    text = read_text(path)
    parsed = parse_page(path)
    expect(errors, text.lower().count("<!doctype html>") == 1, f"{page.relative_file}: expected one doctype")
    expect(errors, '"@type": "FAQPage"' in text, f"{page.relative_file}: missing FAQPage structured data")
    expect(errors, text.count("<article>") == 9, f"{page.relative_file}: expected 9 FAQ entries")
    expect(errors, parsed.html_lang == page.html_lang, f"{page.relative_file}: html lang should be {page.html_lang}")
    expect(errors, parsed.robots == ["index,follow"], f"{page.relative_file}: robots should be index,follow")
    expect(errors, parsed.canonicals == [page.url], f"{page.relative_file}: canonical should be {page.url}")
    expect(errors, parsed.og_urls == [page.url], f"{page.relative_file}: og:url should be {page.url}")
    expect(errors, parsed.sitemaps == [f"{SITE_BASE_URL}/sitemap.xml"], f"{page.relative_file}: sitemap link mismatch")
    expect(errors, PICO_CDN in parsed.stylesheets, f"{page.relative_file}: missing Pico CSS CDN")
    expect(errors, page.stylesheet_href in parsed.stylesheets, f"{page.relative_file}: missing {page.stylesheet_href}")
    expect(
        errors,
        set(parsed.alternates) == EXPECTED_FAQ_HREFLANGS,
        f"{page.relative_file}: FAQ hreflang set mismatch",
    )
    for alt in FAQ_PAGES:
        expect(
            errors,
            parsed.alternates.get(alt.hreflang) == alt.url,
            f"{page.relative_file}: FAQ alternate {alt.hreflang} URL mismatch",
        )
    expect(
        errors,
        parsed.alternates.get("x-default") == ENGLISH_FAQ_PAGE.url,
        f"{page.relative_file}: FAQ x-default alternate URL mismatch",
    )
    validate_images(page.relative_file, parsed, errors)


def validate_sitemap(pages_root: Path, errors: list[str]) -> None:
    """Validate sitemap.xml against the canonical page list."""

    path = pages_root / "sitemap.xml"
    expect(errors, path.is_file(), "sitemap.xml: missing file")
    if not path.is_file():
        return

    try:
        root = ET.fromstring(read_text(path))
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml: XML parse error: {exc}")
        return

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [node.text or "" for node in root.findall(".//sm:loc", namespace)]
    expected_locs = [page.url for page in (*CANONICAL_PAGES, LANGUAGE_PAGE, *FAQ_PAGES)]
    expect(errors, locs == expected_locs, "sitemap.xml: loc list does not match canonical locale order")
    priorities = [node.text or "" for node in root.findall(".//sm:priority", namespace)]
    expect(
        errors,
        priorities == [page.priority for page in (*CANONICAL_PAGES, LANGUAGE_PAGE, *FAQ_PAGES)],
        "sitemap.xml: priority list does not match canonical locale order",
    )


def validate_prohibited_assets(pages_root: Path, errors: list[str]) -> None:
    """Ensure static pages do not regain prohibited image dependencies."""

    paths = [pages_root / "styles.css", pages_root / "index.html", pages_root / LANGUAGE_PAGE.relative_file]
    paths.extend(pages_root / page.relative_file for page in CANONICAL_PAGES if page.directory)
    paths.extend(pages_root / page.relative_file for page in FAQ_PAGES)
    for path in paths:
        if not path.is_file():
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            if PROHIBITED_ASSET_PATTERN.search(line):
                relative = path.relative_to(pages_root)
                errors.append(f"{relative}:{line_number}: prohibited asset reference")


def validate_site(pages_root: Path) -> int:
    """Run the static site validation suite."""

    errors: list[str] = []
    for page in CANONICAL_PAGES:
        validate_page(pages_root, page, errors)
    validate_language_page(pages_root, errors)
    for page in FAQ_PAGES:
        validate_faq_page(pages_root, page, errors)
    validate_sitemap(pages_root, errors)
    validate_prohibited_assets(pages_root, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Validated static pages in {pages_root}")
    return 0


def render_sitemap(lastmod: str) -> str:
    """Render sitemap.xml from the canonical page table."""

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in (*CANONICAL_PAGES, LANGUAGE_PAGE, *FAQ_PAGES):
        lines.extend(
            [
                "  <url>",
                f"    <loc>{page.url}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                f"    <priority>{page.priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def write_sitemap(pages_root: Path, lastmod: str, check: bool) -> int:
    """Write or check sitemap.xml for the static pages site."""

    try:
        dt.date.fromisoformat(lastmod)
    except ValueError as exc:
        raise SystemExit(f"--lastmod must be an ISO date, got {lastmod!r}") from exc

    path = pages_root / "sitemap.xml"
    rendered = render_sitemap(lastmod)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if check:
        if existing != rendered:
            print("sitemap.xml is out of date", file=sys.stderr)
            return 1
        print("sitemap.xml is current")
        return 0
    path.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Wrote {path}")
    return 0


def list_locales() -> int:
    """Print the canonical locale routing table."""

    for page in CANONICAL_PAGES:
        directory = page.directory or "."
        print(f"{page.hreflang}\t{page.html_lang}\t{directory}\t{page.url}")
    print(f"x-default\ten\t.\t{SITE_BASE_URL}/")
    return 0


def main() -> int:
    """Dispatch the selected helper command."""

    args = parse_args()
    if args.command == "list-locales":
        return list_locales()

    pages_root = resolve_pages_root(args.pages_root)
    if args.command == "validate":
        return validate_site(pages_root)
    if args.command == "write-sitemap":
        return write_sitemap(pages_root, args.lastmod, args.check)
    raise AssertionError(f"Unhandled command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
