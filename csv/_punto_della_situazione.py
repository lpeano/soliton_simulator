# -*- coding: utf-8 -*-
"""IL PUNTO DELLA SITUAZIONE — generato DALLA CODA UNICA, non a memoria.

⚠ SOLA LETTURA. Legge `doc/STATO_RUN.md` e `git log`, non esegue niente e non tocca nessun run.

⚠ PERCHE' GENERATO E NON SCRITTO: un punto della situazione scritto a memoria **dice cio' che
  ricordo**, non cio' che il repo contiene — ed e' esattamente il modo in cui un task
  dimenticato resta dimenticato. Qui la fonte e' **la coda**, e cio' che non c'e' **non compare**:
  **se un task manca dalla tabella, manca dalla coda**, e quello e' il difetto da correggere.

⚠ LO STATO si legge dal MARCATORE della riga, che e' una convenzione del file:
  `✅` fatto · `▶` in corso · `⏸` in coda · `⚠` con riserva.
  Una riga **senza marcatore** compare come `(senza marcatore)`: e' un difetto della coda, non
  un task senza stato, e si vede.
ASCII PURO nel sorgente.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
CODA = os.path.join(RADICE, "doc", "STATO_RUN.md")
OUT = os.path.join(RADICE, "doc", "PUNTO_DELLA_SITUAZIONE.md")

MARCATORI = [("✅", "FATTO"), ("▶", "IN CORSO"), ("⏸", "IN CODA"),
             ("❌", "BLOCCATO"), ("⚠", "CON RISERVA")]
# le sezioni della coda che NON sono task: i difetti e i sospetti hanno una forma diversa
NON_TASK = re.compile(r"^(D[0-9]{2}|S[0-9]{2})$")


def stato(cella):
    for m, nome in MARCATORI:
        if m in cella:
            return nome
    return "(senza marcatore)"


def righe(percorso):
    t = io.open(percorso, encoding="utf-8", errors="replace").read()
    out = []
    for r in t.split("\n"):
        m = re.match(r"\|\s*\*\*([A-Z0-9][A-Za-z0-9\-]*)\*\*\s*\|", r)
        if not m:
            continue
        c = [x.strip() for x in r.split("|")]
        idn = m.group(1)
        out.append({"id": idn, "cosa": c[2] if len(c) > 2 else "",
                    "stato": stato(c[4] if len(c) > 4 else ""),
                    "nota": c[4] if len(c) > 4 else "", "difetto": bool(NON_TASK.match(idn))})
    return out


def ultimo_commit(chiave):
    """L'ultimo commit che NOMINA la chiave nel messaggio. Se non c'e', si dice."""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%h %cd", "--date=format:%H:%M",
                            "--grep=%s" % chiave, "-i"],
                           cwd=RADICE, capture_output=True, text=True)
        s = (r.stdout or "").strip()
        return s if s else "—"
    except Exception:
        return "—"


def collaudo(W):
    """`P1-sexies`: il lettore su righe a risposta NOTA, e il caso che DEVE fallire."""
    W("COLLAUDO (`P1-sexies`)\n" + "-" * 90 + "\n")
    e = []
    ok1 = (stato("✅ fatto") == "FATTO") and (stato("▶ in corso") == "IN CORSO")
    W("K1 i marcatori si leggono -> %s\n" % ("OK" if ok1 else "*** NO ***"))
    e.append(ok1)
    ok2 = (stato("nessun marcatore qui") == "(senza marcatore)")
    W("K2 IL CASO CHE DEVE FALLIRE: una riga SENZA marcatore -> %s\n"
      % ("OK: compare come tale, non sparisce e non viene inventata"
         if ok2 else "*** una riga senza stato passerebbe per fatta ***"))
    e.append(ok2)
    ok3 = NON_TASK.match("D07") is not None and NON_TASK.match("G4") is None
    W("K3 i difetti si distinguono dai task -> %s\n" % ("OK" if ok3 else "*** NO ***"))
    e.append(ok3)
    ok = all(e)
    W("-" * 90 + "\n  -> %s\n\n" % ("si genera" if ok else "*** NON genero ***"))
    return ok


def main():
    W_ = sys.stdout.write
    if not collaudo(W_):
        return 1
    rr = righe(CODA)
    task = [x for x in rr if not x["difetto"]]
    dif = [x for x in rr if x["difetto"]]
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# IL PUNTO DELLA SITUAZIONE — **generato dalla CODA UNICA**\n\n")
    W("> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo\n")
    W("> `doc/STATO_RUN.md`. **Non e' scritto a memoria**, ed e' il punto: **se un task manca\n")
    W("> qui, manca dalla coda** — e quello e' il difetto da correggere.\n\n")
    ordine = ["IN CORSO", "CON RISERVA", "IN CODA", "(senza marcatore)", "BLOCCATO", "FATTO"]
    for s in ordine:
        gruppo = [x for x in task if x["stato"] == s]
        if not gruppo:
            continue
        W("## %s — %d\n\n" % (s, len(gruppo)))
        W("| id | cosa | ultimo commit che lo nomina |\n|---|---|---|\n")
        for x in gruppo:
            cosa = re.sub(r"\s+", " ", x["cosa"])[:150]
            W("| **`%s`** | %s | `%s` |\n" % (x["id"], cosa, ultimo_commit(x["id"])))
        W("\n")
    st = {}
    for x in dif:
        k = "CURATO" if "CURATO" in x["nota"].upper() and "INEFFICACE" not in x["nota"].upper() \
            else ("NON E' UN DIFETTO" if "NON E' UN DIFETTO" in x["nota"].upper()
                  else ("ALTRO" if x["id"].startswith("D") and "APERTO" not in x["nota"].upper()
                        else "APERTO"))
        st.setdefault(k, []).append(x["id"])
    W("## DIFETTI E SOSPETTI — %d righe\n\n" % len(dif))
    W("| stato | quanti | quali |\n|---|--:|---|\n")
    for k in sorted(st):
        W("| %s | %d | %s |\n" % (k, len(st[k]), " ".join("`%s`" % y for y in st[k])))
    W("\n**ID massimo usato:** difetti `%s` · sospetti `%s`. **Gli ID non si riusano.**\n"
      % (max([x["id"] for x in dif if x["id"].startswith("D")] or ["—"]),
         max([x["id"] for x in dif if x["id"].startswith("S")] or ["—"])))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
