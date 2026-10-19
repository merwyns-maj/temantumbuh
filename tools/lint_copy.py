#!/usr/bin/env python3
"""Lint TemanTumbuh copy for AI tells and off-voice Indonesian.

Usage: python lint_copy.py post.json [more.json ...]
Exit code 1 if any ERROR is found. Rules mirror .claude/skills/suara-temantumbuh/SKILL.md.
"""
import json
import re
import sys

ERROR, WARN = "ERROR", "WARN"

# (pattern, severity, message). Patterns are case-insensitive and matched on word boundaries where it matters.
RULES = [
    (r"[—–]", ERROR, "em/en dash: use a full stop, comma or colon"),
    (r";", ERROR, "semicolon: split into two sentences"),
    (r"\bAnda\b", ERROR, "'Anda' is too formal: use 'kamu'"),
    (r"\bdi era digital\b", ERROR, "AI opener"),
    (r"\bdalam dunia parenting\b", ERROR, "AI opener"),
    (r"\btahukah kamu\b", ERROR, "AI opener"),
    (r"\bpernahkah kamu\b", ERROR, "AI opener"),
    (r"\bmari kita\b", ERROR, "AI opener"),
    (r"\byuk simak\b", ERROR, "AI opener"),
    (r"\bsimak penjelasan\b", ERROR, "AI opener"),
    (r"\bberikut adalah\b", ERROR, "AI opener"),
    (r"\bsiapa yang di sini\b", ERROR, "AI opener"),
    (r"\btidak hanya\b.*\btetapi juga\b", ERROR, "'tidak hanya... tetapi juga' structure"),
    (r"\bbukan sekadar\b.*\bmelainkan\b", ERROR, "'bukan sekadar... melainkan' structure"),
    (r"\badalah (kunci|fondasi|pondasi)\b", ERROR, "'X adalah kunci/fondasi' cliché"),
    (r"\bpenting untuk\b", ERROR, "'penting untuk': start with the situation instead"),
    (r"\bpastikan untuk\b", ERROR, "'pastikan untuk': just say the action"),
    (r"(?<!\d\s)\bhal ini\b", ERROR, "'hal ini' as filler is textbook (after a number, like '4 hal ini', it is fine)"),
    (r"\bdengan demikian\b", ERROR, "textbook connector"),
    (r"\boleh karena itu\b", ERROR, "textbook connector"),
    (r"\bselain itu\b", ERROR, "textbook connector"),
    (r"\bperlu diingat\b", ERROR, "textbook connector"),
    (r"\bpada dasarnya\b", ERROR, "textbook connector"),
    (r"\byang mana\b(?!\s*\?)", ERROR, "'yang mana' as a relative pronoun is translation-ese (as a question it is fine)"),
    (r"\bini adalah\b", ERROR, "translation-ese"),
    (r"\bmelakukan\b", WARN, "'melakukan' + noun: use the verb (cek, coba, ...)"),
    (r"\bdapat dilakukan\b", ERROR, "passive translation-ese"),
    (r"\bmemiliki\b", WARN, "'memiliki': say 'punya'"),
    (r"\b(esensial|krusial|holistik|signifikan)\b", ERROR, "AI vocabulary"),
    (r"\boptimal\b", ERROR, "'optimal': AI vocabulary"),
    (r"\bmaksimal\b|\bmemaksimalkan\b", ERROR, "'maksimal': AI vocabulary"),
    (r"\bmomen berharga\b", ERROR, "cliché"),
    (r"\bperjalanan parenting\b", ERROR, "cliché"),
    (r"\bluar biasa\b", ERROR, "cliché"),
    (r"\b(ajaib|rahasia)\b", ERROR, "clickbait word"),
    (r"\b(game changer|worth it|literally)\b", ERROR, "forced English"),
    (r"\bbayangkan\b", ERROR, "rhetorical set-up"),
    (r"\bjawabannya\b", ERROR, "rhetorical set-up"),
    (r"\b(dijamin|pasti bisa|100%|bikin pintar|bikin gemuk)\b", ERROR, "claim not allowed"),
    # Compliance (research 2026-10-17)
    (r"\b(susu formula|sufor|susu pertumbuhan|formula lanjutan)\b", ERROR, "breast-milk substitutes: never promote (PP 28/2024 Pasal 33); rephrase or drop"),
    (r"\b(like kalau|komen amin|ketik amin|komen 1|ketik 1|follow dulu baru)\b", ERROR, "engagement bait: not eligible for the For You feed"),
    (r"\b(cegah stunting|pasti tinggi|anti stunting)\b(?!\s*\w*\s*#)", WARN, "stunting as a promise: say 'bantu' or cite a source"),
    (r"\b(tidak|sudah|saja|bagaimana|membuat|memberikan)\b", WARN, "formal form: prefer nggak/udah/aja/gimana/bikin/kasih"),
]
PARTICLES = r"\b(kok|sih|deh|lho|kan|ya|dong)\b"


def strings(node, path="$"):
    """Yield (path, text) for every string in the spec, skipping style keys."""
    skip = {"type", "theme", "motif", "series", "handle", "tips_label", "zzz", "usia", "label", "job", "source", "mascot", "art", "items", "cols", "number", "fills", "inks", "num"}
    if isinstance(node, dict):
        for k, v in node.items():
            if k in skip:
                continue
            yield from strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def lint(spec):
    issues = []
    all_text = []
    for path, text in strings(spec):
        all_text.append(text)
        for pat, sev, msg in RULES:
            if sev is None:
                continue
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                issues.append((sev, path, msg, m.group(0), text))
        # 'Bunda' alone (without 'Ayah' before it) breaks the neutral brand voice
        for m in re.finditer(r"\bBunda\b", text):
            before = text[max(0, m.start() - 6):m.start()].lower()
            if "ayah" not in before:
                issues.append((ERROR, path, "'Bunda' alone: use 'Ayah Bunda' or 'kamu'", "Bunda", text))
    joined = "\n".join(all_text)
    if joined.count("!") > 1:
        issues.append((ERROR, "$", f"{joined.count('!')} exclamation marks: max 1 per post", "!", ""))
    ell = joined.count("...") + joined.count("…")
    if ell > 1:
        issues.append((WARN, "$", f"{ell} ellipses: keep at most 1 per post", "...", ""))
    if len(re.findall(r"\bsi kecil\b", joined, flags=re.IGNORECASE)) > 1:
        issues.append((ERROR, "$", "'si kecil' more than once per post", "si kecil", ""))
    cap = spec.get("caption", "")
    if spec.get("affiliate") and not re.search(r"#iklan|#ad\b|afiliasi|affiliate", cap, flags=re.IGNORECASE):
        issues.append((ERROR, "$.caption", "affiliate post without disclosure (#iklan or 'link afiliasi')", "", cap[:60]))
    if spec.get("job") not in ("save", "send", "comment"):
        issues.append((ERROR, "$.job", "post needs one job: save, send or comment", str(spec.get("job")), ""))
    if not cap.rstrip().split("#")[0].strip().endswith("?") and "?" not in cap:
        issues.append((WARN, "$.caption", "caption has no question: questions lift comments", "", cap[:60]))
    health = spec.get("series") in ("pintar", "mpasi") or spec.get("disclaimer")
    has_source = any(sl.get("source") for sl in spec.get("slides", []))
    if health and not has_source and spec.get("series") != "main":
        issues.append((WARN, "$", "health or development post without a source line on the last slide", "", ""))
    for i, slide in enumerate(spec.get("slides", [])):
        text = " ".join(t for _, t in strings(slide))
        n = len(re.findall(PARTICLES, re.sub(r"\blho kok\b", "lhokok", text, flags=re.IGNORECASE), flags=re.IGNORECASE))
        if n > 1:
            issues.append((WARN, f"$.slides[{i}]", f"{n} particles (kok/sih/deh/ya...): max 1 per slide", "", ""))
    return issues


def main(paths):
    failed = False
    for p in paths:
        spec = json.load(open(p, encoding="utf-8"))
        issues = lint(spec)
        errors = [x for x in issues if x[0] == ERROR]
        print(f"{p}: {len(errors)} error(s), {len(issues) - len(errors)} warning(s)")
        for sev, path, msg, hit, text in issues:
            snippet = f'  "{text[:70]}"' if text else ""
            print(f"  {sev:5} {path}: {msg} [{hit}]{snippet}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
