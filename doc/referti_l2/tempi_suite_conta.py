# -*- coding: utf-8 -*-
r"""**I TEMPI DEI COMMIT E DELLA SUITE** *(Luca `2026-11-15` `23:49`; SOLO LETTURA: nessun collaudo, hook o file del nucleo cambiato)*.

    python doc/referti_l2/tempi_suite_conta.py <cartella dei log> <registro delle corse> > doc/referti_l2/tempi_suite.txt
    (oggi: lo scratchpad della sessione, con commit_log_*.txt, c2_*.txt e suite_*.txt; doc/REGISTRO_CORSE_mattone.md del ramo strumento-mattone)

**1.** **I log di `committa2.py`** *(fuori dal repo: `commit_log_<HHMMSS>.txt`, ogni riga `[secondi] testo` dall'avvio di `git commit`)*: **un PASSO e' una riga che comincia con
`[ETICHETTA]`** *(`[TIMBRO] <file>`: uno script del hook; `[H-...]`: un presidio)*; **il suo tempo: fino al passo dopo** *(l'ultimo: fino all'ultima riga)*. **Il commit, il ramo e il totale dalla
riga `R3` dell'uscita di `committa2`** *(`c2_*.txt` che nomina quel log)*; **«fuori dai hook» = il totale `R3` meno l'ultima riga del log** *(i lucchetti, `git commit` stesso, il push: NON separati, il log non li ha)*.
**Il carico: le corse APERTE in quell'istante** *(dagli eventi `APERTO`/`CHIUSO` del registro; le suite e le prove fuori registro NON contate)*.
**2.** **Il tempo di OGNI collaudo dalle tabelle che `collauda.py` stampa** *(«il collaudo / dove / secondi / esito»)* **nelle uscite delle suite gia' girate** *(`suite_*.txt` del giorno)*.
**3.** **Quali collaudi usano la somma «esatta»** *(`fsum`)*: **la parola `"esatta"` nel file del collaudo** *(solo il file diretto: un modulo importato che la usa NON si vede, dichiarato)*; **in fila o in parallelo: dal codice di `collauda.py`.**
"""
import ast
import datetime as dt
import glob
import hashlib
import io
import json
import os
import re
import statistics
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = "2026-11-15"


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()[:8]


def eventi(reg):
    ev = []
    for r in io.open(reg, encoding="utf-8"):
        r = r.strip()
        if r.startswith("- {"):
            try:
                d = json.loads(r[2:])
            except ValueError:
                continue
            if d.get("ev") in ("APERTO", "CHIUSO") and d.get("ora") and d.get("nome"):
                ev.append((dt.datetime.fromisoformat(d["ora"]).replace(tzinfo=None), d["ev"], d["nome"]))
    return sorted(ev)


def aperte(ev, t):
    s = set()
    for o, e, n in ev:
        if o > t:
            break
        if e == "APERTO":
            s.add(n)
        else:
            s.discard(n)
    return sorted(s)


def passi(f):
    righe = []
    for r in io.open(f, encoding="utf-8", errors="replace"):
        m = re.match(r"\[\s*([0-9.]+) s\] (.*)$", r.rstrip("\n"))
        if m:
            righe.append((float(m.group(1)), m.group(2)))
    out = []
    for i, (t, x) in enumerate(righe):
        m = re.match(r"\[([A-Za-z0-9-]+)\]\s*(\S*)", x)
        if m:
            nome = "[%s] %s" % (m.group(1), m.group(2)) if m.group(1) == "TIMBRO" else "[%s]" % m.group(1)
            out.append([nome, t])
    fine = righe[-1][0] if righe else 0.0
    for i, p in enumerate(out):
        p.append((out[i + 1][1] if i + 1 < len(out) else fine) - p[1])
    return out, fine


def main(argv):
    d, reg = argv[0], argv[1]
    ev = eventi(reg)
    print("=" * 130)
    print("I TEMPI DEI COMMIT E DELLA SUITE (Luca 2026-11-15 23:49): SOLO LETTURA; il registro %s (sha1 %s)" % (os.path.basename(reg), sha1(reg)))
    print("=" * 130)
    # ### 1. i commit
    c2 = {}
    for f in glob.glob(os.path.join(d, "c2_*.txt")):
        t = io.open(f, encoding="utf-8", errors="replace").read()
        m = re.search(r"commit_log_(\d{6})\.txt", t)
        if m:
            c2[m.group(1)] = t
    # ### i nomi dei log NON hanno la data: si prendono quelli MODIFICATI nel GIORNO (dopo mezzanotte il nome dell'ora tornerebbe indietro)
    logs = sorted(f for f in glob.glob(os.path.join(d, "commit_log_*.txt")) if dt.date.fromtimestamp(os.path.getmtime(f)).isoformat() == GIORNO)
    print("### 1. I COMMIT: %d log di committa2.py (il primo %s, l'ultimo %s)" % (len(logs), os.path.basename(logs[0]), os.path.basename(logs[-1])))
    print("  %-8s %-20s %-10s %7s %7s %7s  %-6s %s" % ("l'ora", "il ramo", "il commit", "totale", "hook", "fuori", "aperte", "i 3 passi piu' lenti"))
    tutti = {}
    tot_hook = []
    for f in logs:
        hh = re.search(r"commit_log_(\d{6})", f).group(1)
        pp, fine = passi(f)
        t = c2.get(hh, "")
        m3 = re.search(r"R3 il commit su (\S+) \(HEAD (\w+)\)", t)
        mt = re.search(r"R3 uscita (\d+) in (\d+) s", t)
        m5 = re.search(r"R5 COMMIT OK: (\w+)", t)
        tot = float(mt.group(2)) if mt else float("nan")
        ora = dt.datetime.strptime(GIORNO + " " + hh, "%Y-%m-%d %H%M%S")
        ap = aperte(ev, ora)
        for nome, _t0, s in pp:
            tutti.setdefault(nome, []).append(s)
        tot_hook.append(fine)
        lenti = sorted(pp, key=lambda p: -p[2])[:3]
        print("  %s %-20s %-10s %7.0f %7.1f %7.1f  %-6d %s" % ("%s:%s:%s" % (hh[:2], hh[2:4], hh[4:]), (m3.group(1) if m3 else "?")[:20], (m5.group(1) if m5 else "NON OK" if mt else "?"),
                                                            tot, fine, tot - fine, len(ap), "; ".join("%s %.1f" % (n[:34], s) for n, _t, s in lenti)))
    print("  (le corse aperte per nome sono nel registro; 'fuori' = il totale R3 meno l'ultima riga del log: i lucchetti, git commit, il push)")
    print("-" * 130)
    print("### OGNI PASSO DEI HOOK, su tutti i log (in ordine della mediana): il passo, quante volte, la mediana, il massimo, la quota della mediana sul totale mediano dei hook %.1f s" % statistics.median(tot_hook))
    for nome in sorted(tutti, key=lambda n: -statistics.median(tutti[n])):
        v = tutti[nome]
        print("  %-48s %3d  %7.1f  %7.1f  %5.1f%%" % (nome, len(v), statistics.median(v), max(v), 100.0 * statistics.median(v) / statistics.median(tot_hook)))
    print("=" * 130)
    # ### 2. i collaudi
    tab = {}
    suite_usate = []
    for f in sorted(glob.glob(os.path.join(d, "suite_*.txt"))):
        if dt.date.fromtimestamp(os.path.getmtime(f)).isoformat() != GIORNO:
            continue
        t = io.open(f, encoding="utf-8", errors="replace").read()
        if "il collaudo                            dove" not in t:
            continue
        righe = re.findall(r"^  (.+?)\s+(pre-commit|solo-CI)\s+([0-9.]+)\s+(\S+)\s*$", t, re.M)
        if len(righe) < 60:
            continue
        suite_usate.append("%s (%d)" % (os.path.basename(f), len(righe)))
        for nome, dove, s, es in righe:
            tab.setdefault((nome.strip(), dove), []).append(float(s))
    print("### 2. I COLLAUDI: dalle tabelle di %d suite del %s: %s" % (len(suite_usate), GIORNO, ", ".join(suite_usate)))
    # ### i file dei collaudi, dal codice di collauda.py (ast, nessun import)
    src = io.open(os.path.join(RADICE, "primo_ordine", "collauda.py"), encoding="utf-8").read()
    lista = None
    for nodo in ast.parse(src).body:
        if isinstance(nodo, ast.Assign) and any(getattr(x, "id", None) == "COLLAUDI" for x in nodo.targets):
            lista = ast.literal_eval(nodo.value)
    file_di = {n: c.split()[0] for n, c, _d in lista}
    esatta = {}
    for n, f in file_di.items():
        p = os.path.join(RADICE, f)
        esatta[n] = ("\"esatta\"" in io.open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else None
    med = {k: statistics.median(v) for k, v in tab.items()}
    tot = sum(med.values())
    tot_pc = sum(v for (n, dv), v in med.items() if dv == "pre-commit")
    print("  %-62s %-10s %4s %8s %8s %6s  %-7s %s" % ("il collaudo", "dove", "n", "mediana", "max", "quota", "esatta", "il file"))
    for (n, dv) in sorted(med, key=lambda k: -med[k]):
        print("  %-62s %-10s %4d %8.2f %8.2f %5.1f%%  %-7s %s" % (n[:62], dv, len(tab[(n, dv)]), med[(n, dv)], max(tab[(n, dv)]), 100.0 * med[(n, dv)] / tot,
                                                               {True: "SI", False: "no", None: "?"}[esatta.get(n)], file_di.get(n, "? (il nome della tabella non e' nella lista)")))
    primi = sorted(med.values(), reverse=True)[:5]
    print("-" * 130)
    print("### IN TUTTO (le mediane) %.1f s; il pre-commit %.1f s, solo-CI %.1f s; I PRIMI 5: %.1f s, il %.1f%% del totale" % (tot, tot_pc, tot - tot_pc, sum(primi), 100.0 * sum(primi) / tot))
    print("### la somma \"esatta\" nel file del collaudo: %d su %d (%s)" % (sum(1 for v in esatta.values() if v), len(esatta), ", ".join(n for n, v in esatta.items() if v) or "nessuno"))
    gira = re.search(r"def gira\(cmd\):.*?subprocess\.run\(\[sys\.executable\] \+ pezzi", src, re.S) is not None
    ciclo = re.search(r"for nome, cmd, dove in scelti:\s*\n\s*s, rc, uscita = gira\(cmd\)", src) is not None
    print("### IN FILA O IN PARALLELO: dal codice di collauda.py: un ciclo `for nome, cmd, dove in scelti: ... gira(cmd)` (%s) e gira() fa subprocess.run (%s), che ASPETTA la fine: %s"
          % (ciclo, gira, "IN FILA, uno alla volta" if (ciclo and gira) else "### NON RICONOSCIUTO dal codice"))
    print("### i file letti, sha1: %s" % ", ".join("%s %s" % (os.path.basename(f), sha1(f)) for f in [reg, os.path.join(RADICE, "primo_ordine", "collauda.py")]))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    sys.exit(main(sys.argv[1:]))
