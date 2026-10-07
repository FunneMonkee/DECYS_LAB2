#!/usr/bin/env python3
"""
Parse lines of the form:

    13 [17042, 5708, 25792, 18000, 19959]

(a length/position number followed by a Python-literal list of timings)
and draw a boxplot: x = length, y = time (ns/us/whatever unit the data is
in). Repeated entries for the same length (e.g. from multiple runs) are
pooled into one box. The max value within each length's pooled samples is
marked with a red star.

Reads from a file named "test_length" in the current directory and writes
"timing_boxplot.png" alongside it.

Usage:
    python boxplot_timing.py
"""

import sys
import re
import ast
from collections import defaultdict

import matplotlib.pyplot as plt


LINE_RE = re.compile(r'^\s*(\d+)\s*(\[[^\]]*\])\s*$')


def parse_data(lines):
    """Return {length: [timing, timing, ...]} pooling repeated entries."""
    data = defaultdict(list)
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m:
            # skip anything that doesn't match (blank lines, stray text, etc.)
            continue
        length = int(m.group(1))
        timings = ast.literal_eval(m.group(2))
        data[length].extend(float(t) for t in timings)
    return data


def plot_boxplot(data, out_path=None, unit="us"):
    lengths = sorted(data.keys())
    samples = [data[length] for length in lengths]

    fig, ax = plt.subplots(figsize=(max(8, len(lengths) * 0.6), 6))

    positions = list(range(1, len(lengths) + 1))

    min_vals = []
    second_max_vals = []
    max_vals = []
    for s in samples:
        sorted_s = sorted(s)
        min_vals.append(sorted_s[0])
        max_vals.append(sorted_s[-1])
        # second-highest sample (falls back to the max itself if only 1 sample)
        second_max_vals.append(sorted_s[-2] if len(sorted_s) >= 2 else sorted_s[-1])

    heights = [sm - mn for sm, mn in zip(second_max_vals, min_vals)]

    ax.bar(
        positions,
        heights,
        bottom=min_vals,
        width=0.6,
        color='steelblue',
        alpha=0.7,
        edgecolor='black',
        label='min → 2nd max',
    )

    # Mark the true max for each length with a red star
    ax.scatter(positions, max_vals, marker=6, s=140, color='red', zorder=5, label='max')

    ax.set_xticks(positions)
    ax.set_xticklabels([str(l) for l in lengths])
    ax.set_xlabel("Length")
    ax.set_ylabel(f"Time ({unit})")
    ax.set_title("Timing range (min → 2nd max) by length")
    ax.legend(loc='best')
    ax.grid(True, axis='y', linestyle='--', alpha=0.4)

    fig.tight_layout()

    if out_path:
        fig.savefig(out_path, dpi=150)
        print(f"Saved plot to {out_path}")
    else:
        plt.show()


INPUT_FILE = "test_length"
OUTPUT_FILE = "timing_boxplot.png"


def main():
    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()

    data = parse_data(lines)
    if not data:
        print("No data parsed — check input format (expected 'N [t1, t2, ...]' per line).",
              file=sys.stderr)
        sys.exit(1)

    plot_boxplot(data, out_path=OUTPUT_FILE)


if __name__ == '__main__':
    main()
