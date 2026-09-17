# -*- coding: utf-8 -*-
"""RECUPERO RETROATTIVO: quale COMANDO produce quale `.pkl`.

I `.pkl` non sono nel repo (binari, ~18 MB l'uno, oltre 650 MB) e non devono esserci. Ma il sistema
e' DETERMINISTICO: il dato E' il comando. Questo script ricostruisce il comando **dalle fonti gia'
nel repo** -- il blocco di condizioni in testa a ogni `.cond.csv`, che porta seme, flag e percorsi --
**non a memoria**.

TRE ESITI, dichiarati: RICOSTRUITO / PARZIALE (si scrive COSA manca) / NON RICOSTRUIBILE.

!! NON apre i `.pkl` (18 MB l'uno: competerebbero per I/O con un eventuale run). Legge solo i CSV.
!! NON rilancia nulla.
ASCII PURO.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# I flag booleani del simulatore, nella forma in cui vanno sulla riga di comando.
# Ricavati dai nomi `dest` che l'argparse usa: dest con underscore -> flag con trattino.
IGNORA = {"csv", "sync_db", "db_cleanup", "db_ogni", "ogni", "passi", "seed", "seed_effettivo",
          "batch", "outdir", "tag", "riprendi_da", "no_osserva", "dt"}


def flag(nome):
    return "--" + nome.replace("_", "-")


def leggi_condizioni(path):
    """Il blocco di testa di un .cond.csv e' un JSON: lo si legge, non lo si indovina."""
    try:
        testo = open(path, encoding="utf-8", errors="replace").read(20000)
    except Exception as e:
        return None, "illeggibile: %s" % e
    i = testo.find("{")
    if i < 0:
        return None, "nessun blocco di condizioni JSON in testa"
    # raw_decode bilancia le graffe: il regex non-greedy troncava al primo `}` interno,
    # e i percorsi Windows nel JSON contengono backslash che ingannano una regex.
    try:
        obj, _ = json.JSONDecoder().raw_decode(testo[i:])
        return obj, None
    except Exception as e:
        return None, "blocco JSON non interpretabile: %s" % e


righe = []
pkls = sorted(glob.glob(os.path.join(HERE, "*.pkl")))
print("=" * 120)
print("RECUPERO RETROATTIVO -- quale COMANDO produce quale .pkl")
print("=" * 120)
print("  .pkl trovati: %d" % len(pkls))

for pk in pkls:
    base = os.path.basename(pk)
    stem = base[:-4]
    # il .cond.csv puo' chiamarsi <stem>.cond.csv oppure <base>.cond.csv
    cand = [os.path.join(HERE, stem + ".cond.csv"), os.path.join(HERE, base + ".cond.csv")]
    csvp = next((c for c in cand if os.path.exists(c)), None)
    if csvp is None:
        righe.append((base, "NON RICOSTRUIBILE", "nessun .cond.csv corrispondente", "", "", ""))
        continue
    cond, err = leggi_condizioni(csvp)
    if cond is None:
        righe.append((base, "NON RICOSTRUIBILE", err, os.path.basename(csvp), "", ""))
        continue

    seme = cond.get("seed_effettivo", cond.get("seed"))
    passi = cond.get("passi")
    # IL BLOB NON STA NEL .cond.csv: sta nel .vuoto.csv dell'OSSERVATORE, che porta le colonne
    # di certificazione P6 (blob, seed, e i flag). Due file diversi, due meta' della stessa prova.
    blob = cond.get("blob") or cond.get("BLOB") or cond.get("git_blob")
    vuoto = os.path.join(HERE, stem + ".vuoto.csv")
    blob_src = "cond.csv"
    if blob is None and os.path.exists(vuoto):
        try:
            import csv as _csv
            with open(vuoto, newline="", encoding="utf-8", errors="replace") as fh:
                _r = next(_csv.DictReader(fh), None)
            if _r:
                blob = _r.get("blob") or None
                if blob:
                    blob_src = "vuoto.csv"
        except Exception:
            pass
    attivi = [flag(k) for k, v in sorted(cond.items())
              if v is True and k not in IGNORA and not k.isupper()]
    num = []
    for k in ("nmasse", "sep", "gamma_turbo", "elast_c", "lam", "dt"):
        v = cond.get(k)
        if v is not None and k not in IGNORA:
            if k == "gamma_turbo" and float(v) == 1.0:
                continue
            num.append("%s %s" % (flag(k), v))

    mancano = []
    if seme is None:
        mancano.append("SEME")
    if passi is None:
        mancano.append("PASSI")
    if blob is None:
        mancano.append("BLOB del simulatore")

    cmd = "python soliton_simulator.py --batch"
    if num:
        cmd += " " + " ".join(num)
    if seme is not None:
        cmd += " --seed %s" % seme
    if passi is not None:
        cmd += " --passi %s" % passi
    if attivi:
        cmd += " " + " ".join(attivi)
    cmd += " --csv csv/_test_fork/%s.cond.csv --sync-db csv/_test_fork/%s --db-cleanup" % (stem, base)

    esito = "RICOSTRUITO" if not mancano else "PARZIALE"
    righe.append((base, esito, ("manca: " + ", ".join(mancano)) if mancano else "",
                  os.path.basename(csvp), str(seme), str(passi),
                  (blob[:8] if blob else "-"), cmd, blob_src if blob else "-"))

print("\n%-34s %-14s %-40s" % ("file .pkl", "esito", "note"))
print("-" * 120)
for r in righe:
    print("%-34s %-14s %-10s %-36s" % (r[0], r[1], (r[6] if len(r) > 6 else "-"), r[2][:36]))

ric = sum(1 for r in righe if r[1] == "RICOSTRUITO")
par = sum(1 for r in righe if r[1] == "PARZIALE")
nor = sum(1 for r in righe if r[1] == "NON RICOSTRUIBILE")
print("-" * 120)
print("TOTALE %d   ->   RICOSTRUITI %d   PARZIALI %d   NON RICOSTRUIBILI %d" % (len(righe), ric, par, nor))
if nor:
    print("\nI NON RICOSTRUIBILI (e' la parte che conta):")
    for r in righe:
        if r[1] == "NON RICOSTRUIBILE":
            print("   %-34s %s" % (r[0], r[2]))

# ------------------------------------------------------------------ la tabella per l'inventario
out = os.path.join(HERE, "_comandi_pkl.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("<!-- generato da _ricostruisci_comandi_pkl.py: NON scrivere a mano -->\n\n")
    f.write("| `.pkl` | esito | seme | passi | comando |\n|---|---|---|---|---|\n")
    for r in righe:
        cmd = r[7] if len(r) > 7 else ""
        bl = r[6] if len(r) > 6 else "-"
        note = (" *(%s)*" % r[2]) if r[2] else ""
        f.write("| `%s` | **%s**%s | %s | %s | `%s` |\n"
                % (r[0], r[1], note, r[4] if len(r) > 4 else "?", r[5] if len(r) > 5 else "?", cmd))
print("\ntabella scritta in %s" % out)
print("""
!! COSA QUESTA RICOSTRUZIONE NON GARANTISCE
Il comando e' ricostruito dal blocco di condizioni che il run ha SCRITTO DA SE'. E' la fonte piu'
affidabile disponibile -- meglio dei messaggi di commit, che sono prosa -- ma:
 - se il .cond.csv NON porta il BLOB del simulatore, l'esito e' PARZIALE: si sa COSA e' stato
   lanciato, non SU QUALE CODICE. E su questo repo il blob e' cambiato 14 volte in tre giorni.
 - il blob dello SCRIPT DRIVER (`_osserva_vuoto.py` e i driver di campagna) non e' nel CSV: dove un
   driver ha aggiunto flag propri, il comando qui e' quello del SIMULATORE, non del driver.""")
