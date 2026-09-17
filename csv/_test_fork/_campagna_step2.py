# -*- coding: utf-8 -*-
"""CAMPAGNA STEP 2 — il test a VARIABILE SINGOLA sulla prima componente promossa.

Predizione scritta e committata PRIMA: doc/PREDIZIONE_step2_U1.md (commit b7cb537).

DISEGNO (par.1 della predizione, qui solo ESEGUITO, non deciso):
  variabile unica : --senza-step2  contro  il DEFAULT (Step 2 ON)
  semi            : 4 per braccio (P3: con 2 semi t(0.025,1) = 12.706, IC95 inutilizzabile)
  passi           : 500, gli stessi della baseline esistente
  fisso           : --cs-dinamico (par.4, CI VA SEMPRE) + la config del fork
  ESCLUSI         : --tau-luce (sigillo FALLITO), --rumore-colorato (N2 FAIL),
                    --tw-spinore (voce W, spento per decisione di Luca)

PERCHE' UN DRIVER E NON OTTO COMANDI A MANO: perche' i due bracci devono differire per UNA SOLA
COSA, e scriverla una volta sola e' l'unico modo di garantirlo. Un braccio sbagliato a mano e' il
modo piu' facile di produrre otto run inutili.

NB CONCORRENZA: la macchina ha 12 CPU logiche e sta gia' girando due render video di Luca. Si
lanciano MAX_PAR run per volta, non tutti e otto: i run sono deterministici (seme fisso), quindi
la concorrenza non cambia i NUMERI, solo il tempo.
ASCII PURO: tre script sono gia' morti su UnicodeEncodeError in cp1252 (par.9).
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
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OSS = os.path.join(HERE, "_osserva_vuoto.py")
PY = sys.executable

PASSI = 500
OGNI = 50
SEMI = [1, 2, 3, 4]
MAX_PAR = 4          # 12 CPU logiche, due render video gia' in corso

# I DUE BRACCI. L'UNICA differenza e' `extra`: tutto il resto e' la stessa lista, per costruzione.
BRACCI = [
    ("s2ON", []),                        # DEFAULT: lo Step 2 e' fisica di default dal 2026-09-16
    ("s2OFF", ["--senza-step2"]),        # DIAGNOSTICO: l'unico modo di spegnerlo da oggi
]
COMUNE = ["--cs-dinamico"]               # par.4: CI VA SEMPRE. Senza, cade anche il tau dello Strato 1.


def cmd(tag, seed, extra):
    return [PY, OSS, "--seed", str(seed), "--passi", str(PASSI), "--ogni", str(OGNI),
            "--tag", tag] + COMUNE + list(extra)


def main():
    lavori = [(tag, s, cmd(tag, s, ex)) for tag, ex in BRACCI for s in SEMI]
    print("=" * 92)
    print("CAMPAGNA STEP 2 -- %d run (%d semi x %d bracci), %d passi, campione ogni %d"
          % (len(lavori), len(SEMI), len(BRACCI), PASSI, OGNI))
    print("  braccio ON  : DEFAULT (nessun flag: dal 2026-09-16 l'assenza significa ACCESO)")
    print("  braccio OFF : --senza-step2")
    print("  comune      : %s" % " ".join(COMUNE))
    print("  concorrenza : %d run per volta" % MAX_PAR)
    print("=" * 92, flush=True)

    t0 = time.time()
    attivi = []          # (tag, seed, Popen, log, t_avvio)
    coda = list(lavori)
    esiti = []
    while coda or attivi:
        while coda and len(attivi) < MAX_PAR:
            tag, seed, c = coda.pop(0)
            log = open(os.path.join(HERE, "_camp_%s_s%d.log" % (tag, seed)), "w")
            p = subprocess.Popen(c, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
            attivi.append((tag, seed, p, log, time.time()))
            print("[avvio ] %-6s seme %d   (%.1f min dall'inizio)"
                  % (tag, seed, (time.time() - t0) / 60.0), flush=True)
        fermi = [a for a in attivi if a[2].poll() is not None]
        if not fermi:
            time.sleep(5)      # attesa di un PROCESSO, non polling di uno stato: non c'e' altro modo
            continue
        for a in fermi:
            tag, seed, p, log, ta = a
            log.close()
            attivi.remove(a)
            esiti.append((tag, seed, p.returncode))
            print("[FINE  ] %-6s seme %d   rc=%d   durata %.1f min   (%.1f min dall'inizio)"
                  % (tag, seed, p.returncode, (time.time() - ta) / 60.0,
                     (time.time() - t0) / 60.0), flush=True)

    print("=" * 92)
    ok = sum(1 for e in esiti if e[2] == 0)
    for tag, seed, rc in sorted(esiti):
        print("  %-6s seme %d   %s" % (tag, seed, "OK" if rc == 0 else "FALLITO rc=%d" % rc))
    print("CAMPAGNA: %d/%d run OK in %.1f minuti" % (ok, len(esiti), (time.time() - t0) / 60.0))
    print("=" * 92)
    return 0 if ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
