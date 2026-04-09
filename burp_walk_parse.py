"""
================================================================================
Burp Corpus Builder

This script walks through a directory full of Burp project files and other
text/HTTP archive exports and builds a frequency list of top-level URL paths.

It was written to help extract meaningful endpoints from files you already have
captured in Burp over time. It aggregates endpoints into a shared "corpus" that can
be saved, updated, and exported as a sorted wordlist or CSV. The idea comes from Justin Benjamin code written by Nicole Smith.

How to use:
1. Put this script in a folder where you want to run it.
2. Install optional dependencies if you want better URL extraction:
     pip3 install xnLinkFinder
   xnLinkFinder can find endpoints inside files based on real crawling logic. 
   If it is not installed, the script will still work using a simpler pattern.

   or run in a virtual environment named venv
        python3 -m venv venv

    activate it
        source venv/bin/activate

3. Run the script with:
     python3 burp_walk_parse.py --dir /path/to/folder

4. Additional flags you can use:
     --out OUTPUT        - Create a wordlist text file of top-level paths
     --csv CSVFILE       - Create a CSV file of counts and paths
     --json JSONFILE     - Save (or override) the corpus JSON file
     --clean             - Strip query parameters from URLs before counting

--------------------------------------------------------------------------------
Examples:

  python burp_walk_parse.py--dir ./all_burp_files
  python burp_walk_parse.py--dir ./exports --out wordlist.txt --csv counts.csv
  python burp_walk_parse.py--dir ./my_burp_data --clean

--------------------------------------------------------------------------------
Outputs:

  burp_corpus.json                 - Main persistent frequency database
  Whatever you specify with --out   - Plain text wordlist
  Whatever you specify with --csv   - CSV of frequency counts

================================================================================
"""

import os
import re
import json
import csv
import argparse
from collections import defaultdict
from urllib.parse import urlparse

# Try to import endpoint finder for richer extraction
try:
    from xnlinkfinder import LinkFinder
    XN_AVAILABLE = True
except ImportError:
    XN_AVAILABLE = False

# Default corpus file
CORPUS_FILE = "burp_corpus.json"

# Simple fallback URL regex (used if no LinkFinder available)
URL_REGEX = re.compile(r"https?://[^\s\"'><]+")

def normalize_path(url, strip_query=True):
    """
    Normalize a URL to its first path segment.
    E.g., https://example.com/api/v1/users -> /api
    """
    parsed = urlparse(url)
    path = parsed.path or "/"
    if strip_query:
        # Remove everything after "?" if present
        path = path.split("?")[0]
    parts = [p for p in path.split("/") if p]
    return f"/{parts[0]}" if parts else "/"

def load_corpus(filename=CORPUS_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return defaultdict(int, json.load(f))
    return defaultdict(int)

def save_corpus(corpus, filename=CORPUS_FILE):
    with open(filename, "w") as f:
        json.dump(corpus, f, indent=2)

def extract_urls_from_text(text, corpus, strip_query):
    """
    Extract URLs from a block of text.
    If LinkFinder is installed, use it first; otherwise, use regex fallback.
    """
    if XN_AVAILABLE:
        try:
            finder = LinkFinder()
            found = finder.find_urls(text, base=None)
            for url in found:
                path = normalize_path(url, strip_query)
                corpus[path] += 1
        except Exception:
            pass

    # Fallback: simple regex match
    for match in URL_REGEX.findall(text):
        path = normalize_path(match, strip_query)
        corpus[path] += 1

def process_file(file_path, corpus, strip_query):
    """
    Read a file and extract URLs.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read().decode(errors="ignore")
            extract_urls_from_text(data, corpus, strip_query)
    except Exception:
        # Some files might not be readable text
        pass

def scan_directory(root_dir, corpus, strip_query):
    """
    Walk through a directory recursively and process each file.
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Limit file types to those likely containing URLs
            if file.lower().endswith((".burp", ".xml", ".har", ".txt")):
                full_path = os.path.join(root, file)
                process_file(full_path, corpus, strip_query)

def export_wordlist(corpus, out_file):
    with open(out_file, "w") as out:
        for path, _ in sorted(corpus.items(), key=lambda i: i[1], reverse=True):
            clean = path.strip("/")
            if clean:
                out.write(clean + "\n")

def export_csv(corpus, csv_file):
    with open(csv_file, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["Count", "Path"])
        for path, count in sorted(corpus.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([count, path])

def main():
    parser = argparse.ArgumentParser(description="Build a frequency corpus from Burp exports")
    parser.add_argument("--dir", "-d", required=True, help="Directory containing files to scan")
    parser.add_argument("--out", "-o", help="Wordlist output file")
    parser.add_argument("--csv", help="CSV output file for counts")
    parser.add_argument("--json", help="Custom name for the corpus JSON file")
    parser.add_argument("--clean", action="store_true", help="Strip query parameters from URLs")

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"[!] Directory not found: {args.dir}")
        return
\
    corpus = load_corpus(args.json if args.json else CORPUS_FILE)

    scan_directory(args.dir, corpus, args.clean)
    save_corpus(corpus, args.json if args.json else CORPUS_FILE)

    print("\nTop results:")
    for path, count in sorted(corpus.items(), key=lambda x: x[1], reverse=True)[:25]:
        print(f"{count:6}  {path}")

    if args.out:
        export_wordlist(corpus, args.out)
        print(f"[+] Wordlist saved to {args.out}")

    if args.csv:
        export_csv(corpus, args.csv)
        print(f"[+] CSV saved to {args.csv}")

if __name__ == "__main__":
    main()
