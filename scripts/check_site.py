#!/usr/bin/env python3
"""Check a built Jekyll site without third-party dependencies.

Usage: python3 scripts/check_site.py _site [--baseurl /youzhou-math]
"""

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


NAVIGATION = {
    "Home": "index.html",
    "Research": "research/index.html",
    "Notes": "notes/index.html",
    "Talks": "talks/index.html",
    "CV": "cv/index.html",
}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


@dataclass
class Reference:
    tag: str
    attrs: dict
    line: int
    in_navigation: bool = False
    visible: bool = True
    text: list = field(default_factory=list)

    @property
    def url(self):
        return self.attrs.get("src" if self.tag in {"img", "script"} else "href")

    @property
    def label(self):
        return " ".join("".join(self.text).split())


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.references = []
        self.refreshes = []
        self.ids = set()
        self.navigation_depth = 0
        self.open_anchors = []
        self.visibility_stack = []
        self.source = path.read_text(encoding="utf-8")
        self.feed(self.source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        hidden = (
            (self.visibility_stack and self.visibility_stack[-1][1])
            or tag in {"head", "script", "style", "template"}
            or "hidden" in attributes
            or (attributes.get("aria-hidden") or "").lower() == "true"
            or "sr-only" in (attributes.get("class") or "").split()
            or bool(re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)\b", attributes.get("style") or "", re.IGNORECASE))
        )
        if tag not in VOID_TAGS:
            self.visibility_stack.append((tag, bool(hidden)))
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag == "nav":
            self.navigation_depth += 1
        if tag == "meta" and (attributes.get("http-equiv") or "").lower() == "refresh":
            self.refreshes.append(Reference(tag, attributes, self.getpos()[0]))
        if tag in {"a", "link", "img", "script"}:
            reference = Reference(tag, attributes, self.getpos()[0], self.navigation_depth > 0, not hidden)
            self.references.append(reference)
            if tag == "a":
                self.open_anchors.append(reference)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.visibility_stack) - 1, -1, -1):
            if self.visibility_stack[index][0] == tag:
                del self.visibility_stack[index:]
                break
        if tag == "nav":
            self.navigation_depth = max(0, self.navigation_depth - 1)
        elif tag == "a" and self.open_anchors:
            self.open_anchors.pop()

    def handle_data(self, data):
        if self.visibility_stack and self.visibility_stack[-1][1]:
            return
        for anchor in self.open_anchors:
            anchor.text.append(data)


def normalize_baseurl(value):
    if value in {"", "/"}:
        return ""
    if not value.startswith("/") or value.startswith("//"):
        raise ValueError("baseurl must be empty or start with a single '/' (for example /youzhou-math)")
    if "?" in value or "#" in value or any(part in {".", ".."} for part in value.split("/")):
        raise ValueError("baseurl must be a URL path without a query, fragment, or dot segments")
    return value.rstrip("/")


def infer_baseurl(home):
    suffix = "/assets/css/style.css"
    for reference in home.references:
        if reference.tag != "link" or not reference.url:
            continue
        parts = urlsplit(reference.url)
        if not parts.scheme and not parts.netloc:
            path = unquote(parts.path)
            if path.endswith(suffix):
                return normalize_baseurl(path[:-len(suffix)])
            if path == "assets/css/style.css":
                return ""
    raise ValueError("cannot infer baseurl from the homepage stylesheet; supply --baseurl explicitly")


def resolve_local(reference, page, root, baseurl):
    """Return (target, fragment), or None for a non-local URL."""
    parts = urlsplit(reference.url)
    if parts.scheme or parts.netloc:
        return None
    url_path = unquote(parts.path)
    if not url_path:
        target = page.path
    elif url_path.startswith("/"):
        if baseurl and url_path != baseurl and not url_path.startswith(baseurl + "/"):
            raise ValueError(f"root URL {reference.url!r} is outside baseurl {baseurl!r}")
        target = root / url_path[len(baseurl):].lstrip("/")
    else:
        target = page.path.parent / url_path
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"URL {reference.url!r} escapes the site output directory") from exc
    if target.is_dir() or url_path.endswith("/"):
        target /= "index.html"
    return target, unquote(parts.fragment)


def canonical_links(page):
    return [
        reference for reference in page.references
        if reference.tag == "link" and "canonical" in (reference.attrs.get("rel") or "").lower().split()
    ]


def validate_redirect(page, pages, root, baseurl, site_origin):
    """Validate the narrowly defined local redirects exempt from main navigation."""
    if len(page.refreshes) != 1:
        raise ValueError("redirect must have exactly one meta refresh")
    content = page.refreshes[0].attrs.get("content") or ""
    match = re.fullmatch(r"\s*0(?:\.0+)?\s*;\s*url\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s\"']+))\s*", content, re.IGNORECASE)
    if not match:
        raise ValueError("redirect meta refresh must be parseable as '0; url=/local/path/'")
    redirect_url = next(value for value in match.groups() if value is not None)
    parts = urlsplit(redirect_url)
    if parts.scheme or parts.netloc or not redirect_url.startswith("/") or redirect_url.startswith("//") or "\\" in redirect_url or parts.query or parts.fragment:
        raise ValueError("redirect target must be a root-relative local URL without query or fragment")
    reference = Reference("a", {"href": redirect_url}, page.refreshes[0].line)
    resolved = resolve_local(reference, page, root, baseurl)
    target = resolved[0]
    if target not in pages or not target.is_file():
        raise ValueError(f"redirect target must be an existing HTML page: {redirect_url!r}")
    if target == page.path:
        raise ValueError("redirect must not point to itself")
    if pages[target].refreshes:
        raise ValueError("redirect must point directly to a normal page, not another redirect")

    fallback = [
        reference for reference in page.references
        if reference.tag == "a" and reference.visible and reference.label
    ]
    if len(fallback) != 1 or fallback[0].url != redirect_url:
        raise ValueError("redirect must have exactly one visible fallback link with the same href as meta refresh")
    canonicals = canonical_links(page)
    if len(canonicals) != 1 or not canonicals[0].url:
        raise ValueError("redirect must have exactly one canonical link")
    canonical = urlsplit(canonicals[0].url)
    if canonical.query or canonical.fragment or canonical.path != parts.path:
        raise ValueError("redirect canonical path must match the meta refresh URL without query or fragment")
    if canonical.scheme or canonical.netloc:
        if canonical.scheme.lower() not in {"http", "https"} or (canonical.scheme.lower(), canonical.netloc.lower()) != site_origin:
            raise ValueError("redirect canonical must use the same site origin as the homepage")
    elif not canonical.path.startswith("/"):
        raise ValueError("redirect canonical must be root-relative or use the homepage origin")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Jekyll output directory, usually _site")
    parser.add_argument("--baseurl", help="URL prefix; inferred from index.html when omitted")
    args = parser.parse_args()
    root = args.output.resolve()
    if not root.is_dir() or not (root / "index.html").is_file():
        parser.error(f"{root} must contain a built site with index.html")

    errors = []
    pages = {}
    for path in sorted(root.rglob("*.html")):
        try:
            pages[path] = Page(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(root)}: cannot parse HTML: {exc}")
    if root / "index.html" not in pages:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    try:
        baseurl = normalize_baseurl(args.baseurl) if args.baseurl is not None else infer_baseurl(pages[root / "index.html"])
    except ValueError as exc:
        parser.error(str(exc))

    def error(page, message, reference=None):
        location = str(page.path.relative_to(root))
        if reference is not None:
            location += f":{reference.line}"
        errors.append(f"{location}: {message}")

    local_count = fragment_count = pdf_count = external_count = 0
    resolved_references = {}
    for page in pages.values():
        if re.search(r"\{\{.*?\}\}|\{%.*?%\}", page.source, flags=re.DOTALL):
            error(page, "unrendered Liquid expression found")
        for reference in page.references:
            if reference.url is None:
                continue
            try:
                resolved = resolve_local(reference, page, root, baseurl)
            except ValueError as exc:
                error(page, str(exc), reference)
                continue
            if resolved is None:
                external_count += 1
                continue
            target, fragment = resolved
            resolved_references[id(reference)] = target
            local_count += 1
            if not target.is_file():
                error(page, f"missing local target for {reference.url!r}: {target.relative_to(root)}", reference)
            if reference.tag == "a" and target.suffix.lower() == ".pdf":
                pdf_count += 1
                rel = set((reference.attrs.get("rel") or "").lower().split())
                if (reference.attrs.get("target") or "").lower() != "_blank":
                    error(page, f"PDF link {reference.url!r} must use target=\"_blank\"", reference)
                if not {"noopener", "noreferrer"}.issubset(rel):
                    error(page, f"PDF link {reference.url!r} must include rel=\"noopener noreferrer\"", reference)
            elif reference.tag == "a" and (reference.attrs.get("target") or "").lower() == "_blank":
                error(page, f"internal link {reference.url!r} must open in the current tab", reference)
            if fragment and target.suffix.lower() == ".html" and target in pages:
                fragment_count += 1
                # Text-fragment directives can accompany a normal element id.
                element_id = fragment.split(":~:text=", 1)[0]
                if element_id and element_id not in pages[target].ids:
                    error(page, f"missing fragment #{element_id} in {target.relative_to(root)}", reference)

    home_canonicals = canonical_links(pages[root / "index.html"])
    site_origin = None
    if len(home_canonicals) == 1 and home_canonicals[0].url:
        home_url = urlsplit(home_canonicals[0].url)
        if home_url.scheme and home_url.netloc:
            site_origin = (home_url.scheme.lower(), home_url.netloc.lower())
    redirect_count = 0
    for page in pages.values():
        if page.refreshes:
            try:
                validate_redirect(page, pages, root, baseurl, site_origin)
            except ValueError as exc:
                error(page, str(exc), page.refreshes[0])
            else:
                redirect_count += 1
                continue
        navigation = [reference for reference in page.references if reference.tag == "a" and reference.in_navigation]
        for label, destination in NAVIGATION.items():
            matches = [reference for reference in navigation if reference.label == label]
            if len(matches) != 1:
                error(page, f"navigation must contain {label!r} exactly once (found {len(matches)})")
                continue
            reference = matches[0]
            if resolved_references.get(id(reference)) != root / destination:
                error(page, f"{label} navigation must link to {destination}", reference)
        active = [reference for reference in navigation if "aria-current" in reference.attrs]
        relative = page.path.relative_to(root)
        is_404 = relative == Path("404.html") or relative == Path("404/index.html")
        if (not is_404 and len(active) != 1) or (is_404 and len(active) > 1):
            error(page, f"expected {'at most' if is_404 else 'exactly'} one active navigation link (found {len(active)})")
        for reference in active:
            if reference.attrs.get("aria-current") != "page":
                error(page, "active navigation must use aria-current=\"page\"", reference)
            expected_label = "Home" if relative == Path("index.html") else next(
                (label for label, destination in NAVIGATION.items() if label != "Home" and relative.parts[0] == Path(destination).parts[0]),
                None,
            )
            if is_404:
                error(page, "404 navigation should have no active page", reference)
            elif expected_label and reference.label != expected_label:
                error(page, f"active navigation should be {expected_label!r}, found {reference.label!r}", reference)

    for directory in ("docs", "scripts"):
        if (root / directory).exists():
            errors.append(f"{directory}/: maintenance directory must be excluded from the built site")
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_file() and path.name.lower().startswith("readme"):
            errors.append(f"{relative}: maintenance file must be excluded from the built site")

    print(f"Checked {len(pages)} HTML pages ({redirect_count} validated redirects), {local_count} local references, {fragment_count} fragments, and {pdf_count} PDF links.")
    print(f"Baseurl: {baseurl!r}. Skipped {external_count} external or non-file references; no network requests made.")
    if errors:
        for message in errors:
            print(f"ERROR {message}", file=sys.stderr)
        print(f"FAILED: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("PASS: navigation, redirects, local files, anchors, PDF behavior, and output exclusions are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
