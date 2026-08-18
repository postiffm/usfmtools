#!/usr/bin/env python3
"""
Compare the verse/chapter numbering of two .acc files.

Each line of a .acc file looks like:
    Gen. 1:1 In the beginning God created the heaven and the earth.

This script does NOT compare the verse text. It only compares the
sequence of (book, chapter, verse) references, reporting where the
two files' numbering falls out of sync (missing verses, extra verses,
or renumbering such as a chapter boundary shifting).

After each discrepancy, it resynchronizes by scanning ahead to find
the next reference the two files have in common, so a single missing
or renumbered verse doesn't cascade into a wall of noise.
"""

import argparse
import re
import sys
from dataclasses import dataclass

LINE_RE = re.compile(r"^(\S+)\s+(\d+):(\d+)\s")


@dataclass(frozen=True)
class Ref:
    book: str
    chapter: int
    verse: int
    line_num: int

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse}"


def parse_acc(path):
    refs = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                continue
            m = LINE_RE.match(line)
            if not m:
                print(f"WARNING: {path}:{line_num}: unrecognized line format: {line!r}",
                      file=sys.stderr)
                continue
            book, chap, verse = m.group(1), int(m.group(2)), int(m.group(3))
            refs.append(Ref(book, chap, verse, line_num))
    return refs


def format_range(refs):
    """Compact human-readable description of a run of refs."""
    if not refs:
        return "(none)"
    if len(refs) == 1:
        return str(refs[0])
    return f"{refs[0]} - {refs[-1]} ({len(refs)} verses)"


def find_resync(refs_a, i, refs_b, j, lookahead=200):
    """
    Look ahead from refs_a[i:] and refs_b[j:] for the nearest matching
    reference in both, so we can resynchronize after a mismatch.
    Returns (new_i, new_j) pointing at the first matching pair, or
    (len(refs_a), len(refs_b)) if none found within the lookahead window.
    """
    window_a = refs_a[i:i + lookahead]
    window_b = refs_b[j:j + lookahead]
    keys_b = {(r.book, r.chapter, r.verse): k for k, r in enumerate(window_b)}

    best = None
    for k, r in enumerate(window_a):
        key = (r.book, r.chapter, r.verse)
        if key in keys_b:
            total = k + keys_b[key]
            if best is None or total < best[0]:
                best = (total, i + k, j + keys_b[key])

    if best is None:
        return len(refs_a), len(refs_b)
    return best[1], best[2]


def compare(refs_a, refs_b, name_a, name_b, lookahead=200):
    i = j = 0
    n, m = len(refs_a), len(refs_b)
    discrepancies = []

    while i < n and j < m:
        a, b = refs_a[i], refs_b[j]
        if (a.book, a.chapter, a.verse) == (b.book, b.chapter, b.verse):
            i += 1
            j += 1
            continue

        # Mismatch: find where the two streams resynchronize.
        new_i, new_j = find_resync(refs_a, i, refs_b, j, lookahead)
        missing_from_b = refs_a[i:new_i]   # present in A, absent in B
        missing_from_a = refs_b[j:new_j]   # present in B, absent in A

        discrepancies.append((missing_from_b, missing_from_a))
        i, j = new_i, new_j

    # Anything left over once one file runs out entirely.
    if i < n:
        discrepancies.append((refs_a[i:], []))
    if j < m:
        discrepancies.append(([], refs_b[j:]))

    report(discrepancies, name_a, name_b)


def report(discrepancies, name_a, name_b):
    total_missing_a = 0  # verses missing from file A
    total_missing_b = 0  # verses missing from file B
    total_renumbered = 0
    books_affected = set()

    for idx, (only_in_a, only_in_b) in enumerate(discrepancies, start=1):
        for r in only_in_a:
            books_affected.add(r.book)
        for r in only_in_b:
            books_affected.add(r.book)

        if only_in_a and not only_in_b:
            total_missing_b += len(only_in_a)
            print(f"[{idx}] {name_b} is missing: {format_range(only_in_a)}")
        elif only_in_b and not only_in_a:
            total_missing_a += len(only_in_b)
            print(f"[{idx}] {name_a} is missing: {format_range(only_in_b)}")
        else:
            total_renumbered += max(len(only_in_a), len(only_in_b))
            print(f"[{idx}] Renumbering: {name_a} has {format_range(only_in_a)} "
                  f"where {name_b} has {format_range(only_in_b)}")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Discrepancy blocks found: {len(discrepancies)}")
    print(f"Verses present in {name_a} but missing from {name_b}: {total_missing_b}")
    print(f"Verses present in {name_b} but missing from {name_a}: {total_missing_a}")
    print(f"Verses involved in chapter/verse renumbering: {total_renumbered}")
    print(f"Books affected: {len(books_affected)}"
          + (f" ({', '.join(sorted(books_affected))})" if books_affected else ""))
    if not discrepancies:
        print("No discrepancies found. Chapter/verse numbering is fully aligned.")


def main():
    parser = argparse.ArgumentParser(
        description="Compare chapter/verse alignment between two .acc files.")
    parser.add_argument("file_a", help="First .acc file")
    parser.add_argument("file_b", help="Second .acc file")
    parser.add_argument("--lookahead", type=int, default=3000,
                         help="How many verses ahead to search for resync (default: 3000). "
                              "Lower this for faster (but less accurate) runs on very large files.")
    args = parser.parse_args()

    refs_a = parse_acc(args.file_a)
    refs_b = parse_acc(args.file_b)

    compare(refs_a, refs_b, args.file_a, args.file_b, lookahead=args.lookahead)


if __name__ == "__main__":
    main()
