# -*- coding: utf-8 -*-
"""CAMPAGNA cs_floor RELAZIONALE -- 4 SEMI, UN SOLO BRACCIO, tutte le leggi SANE del fork.

Predizione scritta e committata PRIMA del cablaggio e PRIMA dei run:
doc/PREDIZIONE_cs_floor_relazionale.md (commit da4116c, aggiornata in 48d5ce2).
Sigillo del cablaggio: csv/_seal_fork/_sigillo_cs_floor.py, 16/16 PASS, R1 byte-identico.
Blob del simulatore: 827d3bf8 (la correzione di difetto e' DENTRO, senza flag).

DISEGNO (decisione di Luca, qui solo ESEGUITO):
  bracci  : UNO SOLO. --tau-luce ACCESA in tutti e quattro i run.
  semi    : 4  -> t(0.025, 3) = 3.182. Col 2x2 sarebbero 2 semi per braccio e t(0.025,1) = 12.706,
            cioe' un IC95 inutilizzabile (P3). Il referto dello Step 2 ha appena mostrato quanto
            costa la mancanza di potenza: meta' dei suoi nulli non diceva nulla.
  passi   : 500, come la baseline e come la campagna Step 2.

PERCHE' NON SERVE UN BRACCIO OFF: le due predizioni che decidono sono ASSOLUTE, non contrasti.
  P1  cs_std/cs deve salire dall'attuale 0.2216% all'ordine del 10%. FALSIFICATORE: se resta
      SOTTO l'1%, la modifica NON ha funzionato (sotto l'1% d/cs e' indistinguibile da d, C13).
  P2  la traiettoria di cs_std/cs deve diventare PIATTA (< x3 fra passo 50 e 500) contro il x20
      della forma vecchia, perche' I/Lam e' scale-free.

⚠ DUE MARCHI, DICHIARATI E NON NASCOSTI (par.5: un run su un ramo non certificato va detto):
  --tau-luce        sigillo FALLITO (T2/T3/T4, voce A del registro).
  --rumore-colorato sigillo INCOMPLETO (N2 FAIL, crash a N7, voce D).

⚠ E IL CONFRONTO COL PASSATO NON E' UN CONTROLLO: nessun run esistente differisce per il solo
  cs_floor. Contro base_ON si differisce anche per lo Step 2 (li' STEP2=0); contro s2ON di oggi
  anche per --tau-luce (li' TAU_LUCE=0). Il prima/dopo si CITA, non si SOTTRAE.

ASCII PURO (tre script gia' morti su cp1252).
"""
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

BRACCI = [("csrel", [])]          # un solo braccio: la variabile A/B e' il SEME
COMUNE = [
    "--cs-dinamico",        # par.4: CI VA SEMPRE. Senza, cade anche il tau dello Strato 1.
    "--tau-luce",           # MARCHIO: sigillo FALLITO (voce A). Ramo NON CERTIFICATO.
    "--rumore-colorato",    # MARCHIO: sigillo INCOMPLETO (N2 FAIL, voce D).
    # le OTTO giudicate SANE dall'audit di lettura (doc/COMPONENTI_PROMOSSE.md, sezione E.ter):
    "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
    "--viriale", "--olon-part",
    # NON si passano: le nove ESCLUSE PER DIMOSTRAZIONE (sezione E), ne' ZETA_LOC (difetto X2 del
    # nodo mediano), ne' kuramoto / turbo / sync / regime.
    # --step2-orologio NON si passa: dal 2026-09-16 e' FISICA DI DEFAULT.
]


def cmd(tag, seed, extra):
    return [PY, OSS, "--seed", str(seed), "--passi", str(PASSI), "--ogni", str(OGNI),
            "--tag", tag] + COMUNE + list(extra)


def main():
    lavori = [(tag, s, cmd(tag, s, ex)) for tag, ex in BRACCI for s in SEMI]
    print("=" * 92)
    print("CAMPAGNA cs_floor RELAZIONALE -- %d run (%d semi, %d braccio), %d passi, campione ogni %d"
          % (len(lavori), len(SEMI), len(BRACCI), PASSI, OGNI))
    print("  braccio unico: --tau-luce ACCESA (marchio: sigillo fallito, voce A)")
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
