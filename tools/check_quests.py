#!/usr/bin/env python3
"""Valida os TSVs de quests deste repositório.

Uso:
    python tools/check_quests.py                 # checa os pt_*.tsv do repo
    python tools/check_quests.py --en-dir <dir>  # compara com os en_*.tsv originais
"""

import argparse
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(ROOT, "quests")


def load(path):
    rows = []
    with io.open(path, encoding="utf-8-sig") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            if "\t" not in line:
                print("  linha sem TAB em %s:%d" % (os.path.basename(path), n))
                continue
            rows.append(line.split("\t", 1))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--en-dir", default="")
    args = ap.parse_args()

    total = 0
    problems = 0
    files = sorted(f for f in os.listdir(QDIR) if f.endswith(".tsv"))
    for name in files:
        rows = load(os.path.join(QDIR, name))
        keys = [k for k, _ in rows]
        dup = len(keys) - len(set(keys))
        empty = sum(1 for _, v in rows if not v.strip())
        total += len(rows)
        problems += dup
        flag = ""
        if dup:
            flag += " duplicadas=%d" % dup
        if empty:
            flag += " vazias=%d" % empty
        print("  %-34s %4d chaves%s" % (name, len(rows), flag))

        if args.en_dir:
            en_path = os.path.join(args.en_dir, "en_" + name[3:])
            if os.path.isfile(en_path):
                en_rows = load(en_path)
                en_keys = {k for k, v in en_rows if v.strip()}
                en_all = {k for k, _ in en_rows}
                pt_keys = {k for k, v in rows}
                missing = en_keys - pt_keys
                extra = pt_keys - en_all
                if missing or extra:
                    problems += 1
                    print("     ! faltando=%d sobrando=%d" % (len(missing), len(extra)))

    print("TOTAL %d chaves em %d arquivos | problemas: %d" % (total, len(files), problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
