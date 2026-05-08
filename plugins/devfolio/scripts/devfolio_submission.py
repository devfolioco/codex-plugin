#!/usr/bin/env python3
"""Validate, summarize, and preview Devfolio-style project submissions.

The script is intentionally API-light. Devfolio publishing is commonly done
through the authenticated web app, while some hackathons provide their own
preview endpoints. This helper keeps the local submission data tidy before
Codex or the user performs the final publish step.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


TEMPLATE: dict[str, Any] = {
    "name": "",
    "tagline": "",
    "description": "",
    "problem": "",
    "solution": "",
    "challenges": "",
    "technologies": [],
    "links": [
        {"type": "source", "url": ""},
        {"type": "demo", "url": ""},
    ],
    "videoDemo": "",
    "screenshots": [],
    "tracks": [],
    "submissionMetadata": {
        "hackathon": "",
        "team": "",
        "prizes": [],
        "notes": "",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"error: file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"error: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")

    if not isinstance(data, dict):
        raise SystemExit("error: submission JSON must be an object")
    return data


def is_http_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def iter_links(data: dict[str, Any]) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    raw_links = data.get("links", [])
    if isinstance(raw_links, list):
        for index, item in enumerate(raw_links):
            if isinstance(item, str):
                links.append((f"links[{index}]", item))
            elif isinstance(item, dict):
                links.append((f"links[{index}].url", str(item.get("url", "")).strip()))

    for field in ("repo", "repository", "source", "deployedUrl", "demoUrl", "videoDemo"):
        value = str(data.get(field, "")).strip()
        if value:
            links.append((field, value))

    return links


def validate_submission(data: dict[str, Any], base_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in ("name", "tagline", "problem"):
        if not str(data.get(field, "")).strip():
            errors.append(f"missing required field: {field}")

    technologies = data.get("technologies", [])
    if not isinstance(technologies, list) or not [item for item in technologies if str(item).strip()]:
        errors.append("technologies must be a non-empty list")

    if not str(data.get("description", "")).strip() and not str(data.get("solution", "")).strip():
        warnings.append("add a description or solution so judges can understand the hack quickly")

    if not str(data.get("challenges", "")).strip():
        warnings.append("add challenges encountered; Devfolio commonly asks for this")

    links = iter_links(data)
    for label, url in links:
        if url and not is_http_url(url):
            warnings.append(f"{label} is not an http(s) URL: {url}")

    link_values = [url for _, url in links]
    if not any("github.com" in url or "gitlab.com" in url or "bitbucket.org" in url for url in link_values):
        warnings.append("add a public source repository link if the hackathon requires open source code")

    video = str(data.get("videoDemo", "")).strip()
    if not video:
        warnings.append("add a public demo video URL when available")
    elif not any(host in video for host in ("youtube.com", "youtu.be", "vimeo.com")):
        warnings.append("videoDemo is present, but YouTube or Vimeo is usually easiest for judges")

    screenshots = data.get("screenshots", [])
    if not isinstance(screenshots, list) or not screenshots:
        warnings.append("add screenshots; Devfolio commonly uses the first image as the cover")
    elif isinstance(screenshots, list):
        for index, item in enumerate(screenshots):
            value = str(item).strip()
            if value and not is_http_url(value) and not (base_dir / value).exists():
                warnings.append(f"screenshots[{index}] does not exist relative to {base_dir}: {value}")

    return errors, warnings


def command_template(_: argparse.Namespace) -> int:
    print(json.dumps(TEMPLATE, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    path = Path(args.file).resolve()
    data = load_json(path)
    errors, warnings = validate_submission(data, path.parent)

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: submission passed validation with {len(warnings)} warning(s)")
    return 0


def command_summary(args: argparse.Namespace) -> int:
    data = load_json(Path(args.file).resolve())
    links = iter_links(data)

    print(f"# {data.get('name', 'Untitled Project')}")
    if data.get("tagline"):
        print(f"\n{data['tagline']}")
    for field in ("problem", "solution", "challenges"):
        value = str(data.get(field, "")).strip()
        if value:
            print(f"\n## {field.title()}\n{value}")
    technologies = data.get("technologies", [])
    if isinstance(technologies, list) and technologies:
        print("\n## Technologies")
        for item in technologies:
            print(f"- {item}")
    if links:
        print("\n## Links")
        for label, url in links:
            if url:
                print(f"- {label}: {url}")
    return 0


def command_preview(args: argparse.Namespace) -> int:
    path = Path(args.file).resolve()
    data = load_json(path)
    errors, warnings = validate_submission(data, path.parent)
    if errors and not args.force:
        for message in errors:
            print(f"ERROR: {message}")
        print("\nRefusing to preview invalid submission. Pass --force to send anyway.")
        return 1

    body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(
        args.endpoint,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"error: preview endpoint returned HTTP {exc.code}: {detail}")
        return 1
    except urllib.error.URLError as exc:
        print(f"error: preview request failed: {exc.reason}")
        return 1

    if warnings:
        for message in warnings:
            print(f"WARN: {message}")
        print()
    print(payload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser("template", help="print a starter submission JSON")
    template_parser.set_defaults(func=command_template)

    validate_parser = subparsers.add_parser("validate", help="validate a submission JSON file")
    validate_parser.add_argument("file")
    validate_parser.set_defaults(func=command_validate)

    summary_parser = subparsers.add_parser("summary", help="print a judge-readable summary")
    summary_parser.add_argument("file")
    summary_parser.set_defaults(func=command_summary)

    preview_parser = subparsers.add_parser("preview", help="POST submission JSON to a preview endpoint")
    preview_parser.add_argument("file")
    preview_parser.add_argument("--endpoint", required=True, help="hackathon-provided preview endpoint")
    preview_parser.add_argument("--timeout", type=float, default=20.0)
    preview_parser.add_argument("--force", action="store_true", help="send even if local validation has errors")
    preview_parser.set_defaults(func=command_preview)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
