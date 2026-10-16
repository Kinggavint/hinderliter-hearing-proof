#!/usr/bin/env python3
"""Pre-deploy NAP guard. Fails (exit 1) if any repo file contains a banned
phone number, or any tel: link / schema "telephone" is not the phone in
data/nap.json. Run: python3 scripts/check_nap.py"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nap = json.load(open(os.path.join(ROOT, "data", "nap.json")))
GOOD = re.sub(r"\D", "", nap["phone_e164"])[-10:]
BANNED = set(nap["banned_numbers"])
SKIP_DIRS = {".git", "node_modules"}
SKIP_FILES = {os.path.join("data", "nap.json"), os.path.join("scripts", "check_nap.py")}
EXTS = (".html", ".htm", ".json", ".js", ".xml", ".txt", ".py", ".md", ".css", ".yml", ".yaml")

PHONE_ANY = re.compile(r"\(?\b(\d{3})\)?[\s.\-]*(\d{3})[\s.\-]*(\d{4})\b")
TEL = re.compile(r"""tel:([+(0-9][^"'<>\s]*(?:\s\d[^"'<>]*)?)""", re.I)
SCHEMA_TEL = re.compile(r'"telephone"\s*:\s*"([^"]*)"')

def ten(s):
    d = re.sub(r"\D", "", s)
    return d[-10:] if len(d) >= 10 else d

errors = []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for fn in fns:
        p = os.path.join(dp, fn); rel = os.path.relpath(p, ROOT)
        if rel in SKIP_FILES or not fn.lower().endswith(EXTS):
            continue
        try:
            text = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for m in PHONE_ANY.finditer(line):
                if "".join(m.groups()) in BANNED:
                    errors.append(f"{rel}:{n}: banned number {m.group(0)}")
            for rx, kind in ((TEL, "tel: link"), (SCHEMA_TEL, "schema telephone")):
                for m in rx.finditer(line):
                    if ten(m.group(1)) != GOOD:
                        errors.append(f"{rel}:{n}: {kind} '{m.group(1).strip()}' != {nap['phone_display']}")

if errors:
    print("NAP CHECK FAILED (source of truth: data/nap.json)")
    print("\n".join(errors))
    sys.exit(1)
print(f"NAP check passed: every tel:/schema phone is {nap['phone_display']}; no banned numbers.")
