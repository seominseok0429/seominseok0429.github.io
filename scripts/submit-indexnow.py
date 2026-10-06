"""Notify IndexNow about deployed canonical pages; preview unless --submit is set."""

import argparse
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://seominseok0429.github.io"
KEY_FILE = "954cf3b72217415380cf3ef657fa4ead.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
HEADERS = {"User-Agent": "MinseokSeo-IndexNow/1.0"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", help="New or updated canonical URLs")
    parser.add_argument("--all", action="store_true", help="Select every sitemap URL (initial setup)")
    parser.add_argument("--submit", action="store_true", help="Verify the live key and send the notification")
    args = parser.parse_args()
    if args.all == bool(args.urls):
        parser.error("Choose explicit URLs or --all, but not both.")

    key = (ROOT / KEY_FILE).read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[a-zA-Z0-9-]{8,128}", key) or KEY_FILE != key + ".txt":
        raise ValueError("Invalid IndexNow verification file.")
    entries = ET.parse(ROOT / "sitemap.xml").findall(
        "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
        "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
    )
    canonical = list(dict.fromkeys((entry.text or "").strip() for entry in entries))
    for url in canonical:
        parsed = urllib.parse.urlsplit(url)
        if (parsed.scheme != "https" or parsed.netloc != urllib.parse.urlsplit(ORIGIN).netloc
                or parsed.query or parsed.fragment):
            raise ValueError(f"Unexpected sitemap URL: {url!r}")
    urls = canonical if args.all else list(dict.fromkeys(args.urls))
    if not urls or len(urls) > 10000:
        raise ValueError("Select between 1 and 10,000 URLs.")
    if any(url not in canonical for url in urls):
        parser.error("Only canonical URLs in sitemap.xml are supported by this script.")

    key_url = ORIGIN + "/" + KEY_FILE
    payload = {"host": urllib.parse.urlsplit(ORIGIN).netloc, "key": key,
               "keyLocation": key_url, "urlList": urls}
    if not args.submit:
        print(json.dumps({"mode": "preview", "endpoint": ENDPOINT, "urls": urls}, indent=2))
        return

    # Wait for the Pages deployment before running this command. A local file
    # alone does not prove ownership to the receiving search engine.
    request = urllib.request.Request(key_url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200 or response.geturl() != key_url:
            raise ValueError("The verification file is not published at its expected URL.")
        if response.read().decode("utf-8").strip() != key:
            raise ValueError("The live verification file does not match the local key.")

    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={**HEADERS, "Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        status = response.status
        if status not in (200, 202):
            raise ValueError(f"Unexpected IndexNow HTTP status: {status}")
    print(json.dumps({"http_status": status, "url_count": len(urls), "urls": urls,
                      "result": "received" if status == 200 else "received; key validation pending",
                      "note": "Receipt does not confirm indexing or AI search inclusion."}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, ET.ParseError, urllib.error.URLError) as error:
        raise SystemExit(f"IndexNow submission failed: {error}") from error
