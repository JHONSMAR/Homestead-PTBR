import sys, os, json, re, collections
sys.path.insert(0, r"C:\Users\mailo\AppData\Local\Temp\opencode\tr")
import translate_names as T

TRDIR = r"C:\Users\mailo\AppData\Local\Temp\opencode\tr"
MAN = {}
for _f in ("manual_values.json", "manual_values2.json", "manual_values3.json"):
    _p = os.path.join(TRDIR, _f)
    if os.path.exists(_p):
        MAN.update(json.load(open(_p, encoding="utf-8")))

BASE = r"C:\Users\mailo\AppData\Local\Temp\opencode"
OUT = os.path.join(BASE, "tr", "out")
NS = ["railways", "umbrellas", "mythicupgrades", "luphieclutteredmod", "decorativelamps"]

tot_add = 0
left_words = collections.Counter()
left_ex = {}
report = []
for ns in NS:
    gp = os.path.join(BASE, f"gap_{ns}.tsv")
    if not os.path.exists(gp):
        continue
    jp = os.path.join(OUT, ns + ".json")
    cur = json.load(open(jp, encoding="utf-8")) if os.path.exists(jp) else {}
    added = skipped = failed = 0
    for line in open(gp, encoding="utf-8"):
        k, v = line.rstrip("\n").split("\t", 1)
        if k in cur and cur[k].strip():
            skipped += 1
            continue
        t = MAN.get(v) or MAN.get(v.replace("\\n", "\n")) or T.translate_value(v)
        is_man = v in MAN or v.replace("\\n", "\n") in MAN
        ok = (is_man and bool(t)) or (t != v and "[" not in t and "%" not in t and len(t.strip()) > 0)
        if ok:
            cur[k] = t
            added += 1
        else:
            failed += 1
            for w in re.findall(r"\[(.*?)\]", t if isinstance(t, str) else ""):
                for ww in w.split():
                    left_words[ww] += 1
                    left_ex.setdefault(ww, v)
            if "[" not in (t or ""):
                for ww in re.findall(r"[A-Za-z][A-Za-z'-]+", v):
                    left_words[ww.lower()] += 1
                    left_ex.setdefault(ww.lower(), v)
    json.dump(cur, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    tot_add += added
    report.append((ns, added, failed, len(cur)))

for ns, a, f, n in report:
    print(f"{ns:22s} +{a:4d}  falhou={f:4d}  total={n}")
print("TOTAL ADD", tot_add, "| palavras restantes:", len(left_words))
for w, c in left_words.most_common(60):
    print(f"  {c:4d} {w:20s} | {left_ex[w][:55]}")
