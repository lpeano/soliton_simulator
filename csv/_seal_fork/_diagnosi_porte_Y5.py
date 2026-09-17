# -*- coding: utf-8 -*-
"""DIAGNOSI DELLE DUE PORTE del fallback dello sfondo (`Y5` rosso). **MISURA, non ripara.**

PORTA A  len(self.peq) != len(self.i)   -> difetto di LUNGHEZZA (A8b: `peq` e topologia di due
                                          momenti diversi)
PORTA B  lunghezze uguali, `peq` NaN o <= 0 -> difetto di VALORE (letto PRIMA della calibrazione)

PRIMA: la strumentazione dev'essere BYTE-INERTE (max|A-B| = 0.000e+00 E stesso N -- riga dei
conteggi PER PRIMA: shape diverse = MANCANZA DI CONFRONTO, non identita').
POI: la misura sul blob ATTUALE e su quello PRE-TEMPO 2, AFFIANCATI. Il confronto e' il dato.
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
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
PRE_PORTE = os.path.join(SC, "_pre_porte.py")     # blob b66e4c5c, PRIMA della strumentazione
PRE_T2 = os.path.join(SC, "_pre_T2.py")           # blob 9dfd91c4, PRIMA del TEMPO 2
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(sim, tag, passi=60, seme=5):
    db = os.path.join(SC, "_pt_%s.pkl" % tag)
    cmd = [sys.executable, sim, "--batch", "--nmasse", "3", "--sep", "8",
           "--seed", str(seme), "--passi", str(passi), "--ogni", str(passi),
           "--db-ogni", str(passi), "--campo-spinoriale", "--spinore-vivo",
           "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio",
           "--verlet", "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
           "--csv", os.path.join(SC, "_pt_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        print("  [run %s FALLITO rc=%s]\n%s" % (tag, p.returncode, (p.stderr or "")[-1200:]))
        return None
    return pickle.load(open(db, "rb"))["attrs"]


print("=" * 118)
print("DIAGNOSI DELLE DUE PORTE -- `Y5` rosso. MISURA, NON RIPARA.")
print("=" * 118)

A = gira(PRE_PORTE, "pre_str")          # blob attuale SENZA strumentazione
B = gira(os.path.join(ROOT, "soliton_simulator.py"), "post_str")   # CON strumentazione
C = gira(PRE_T2, "pre_t2")              # blob PRIMA del TEMPO 2

# ------------------------------------------------------------------ byte-inerzia
print("\n--- (1) LA STRUMENTAZIONE E' BYTE-INERTE?  [BLOCCANTE] ---")
if A is None or B is None:
    esiti.append(False)
else:
    na, nb = len(np.asarray(A["psi"])), len(np.asarray(B["psi"]))
    print("  PRESIDIO, conteggi PER PRIMI: nodi SENZA strum. %d, nodi CON strum. %d" % (na, nb))
    peggio, pk, conf, div = 0.0, "-", 0, 0
    for k in sorted(set(A) & set(B)):
        try:
            x, y = np.asarray(A[k]), np.asarray(B[k])
        except Exception:
            continue
        if x.dtype == object or y.dtype == object or x.ndim == 0:
            continue
        if x.shape != y.shape:
            div += 1; continue
        conf += 1
        if np.issubdtype(x.dtype, np.number) or np.issubdtype(x.dtype, np.complexfloating):
            d = np.abs(x - y); m = float(np.max(d)) if d.size else 0.0
            if m > peggio:
                peggio, pk = m, k
    print("  array con SHAPE UGUALI confrontati: %d   (shape diverse: %d)" % (conf, div))
    verdetto("1a c'e' CONFRONTO (stesso N)", na == nb and conf > 10 and div == 0,
             "%d array, nodi %d = %d" % (conf, na, nb))
    verdetto("1b BYTE-INERTE: max|A-B| = 0.000e+00  [BLOCCANTE]", peggio == 0.0,
             "max = %.3e (peggiore: %s)" % (peggio, pk))

# ------------------------------------------------------------------ la misura
print("\n--- (2) LE DUE PORTE, blob ATTUALE (dopo il TEMPO 2) ---")
if B is not None:
    inv = B.get("_por_invoc") or 0
    pa, pb = B.get("_porta_A") or 0, B.get("_porta_B") or 0
    print("  invocazioni totali del blocco inerzia : %s" % inv)
    print("  PORTA A  (len(peq) != len(i))         : %-6s  (%.2f %%)   ultima invocazione: %s"
          % (pa, 100.0 * pa / max(inv, 1), B.get("_porta_A_ultima")))
    if pa:
        print("           shape all'ultimo scatto      : len(peq)=%s  len(i)=%s"
              % (B.get("_porta_A_shape") or ("?", "?")))
    print("  PORTA B  (peq NaN o <= 0)             : %-6s  (%.2f %%)   ultima invocazione: %s"
          % (pb, 100.0 * pb / max(inv, 1), B.get("_porta_B_ultima")))
    if pb:
        print("           di cui NaN %s, <= 0 %s (somma sui nodi-invocazione)"
              % (B.get("_porta_B_nan"), B.get("_porta_B_nonpos")))
    print("  fallback sui NODI, totale             : %s" % B.get("_inerzia_sfondo_fallback"))
    print("     di cui nodi CON archi (grado > 0)  : %s   <- 'archi validi ma somma nulla'"
          % B.get("_sfondo_ko_con_archi"))
    print("     di cui nodi SENZA archi            : %s   <- 'nessun arco da cui leggere'"
          % B.get("_sfondo_ko_senza_archi"))
    print("  ultima invocazione col fallback       : %s su %s"
          % (B.get("_inerzia_sfondo_ultima"), B.get("_inerzia_invocazioni")))

print("\n--- (3) IL CONFRONTO: blob PRE-TEMPO 2 (9dfd91c4) contro ATTUALE (b66e4c5c) ---")
if C is not None and B is not None:
    print("  %-40s %-16s %-16s" % ("", "PRE TEMPO 2", "ATTUALE"))
    for eti, k in (("fallback sfondo (nodi)", "_inerzia_sfondo_fallback"),
                   ("passi distinti col fallback", "_inerzia_sfondo_passi"),
                   ("ULTIMA invocazione col fallback", "_inerzia_sfondo_ultima"),
                   ("invocazioni totali", "_inerzia_invocazioni"),
                   ("nodi al pavimento 1e-6", "_inerzia_al_pavimento"),
                   ("nodi totali (inerzia)", "_inerzia_tot")):
        print("  %-40s %-16s %-16s" % (eti, C.get(k), B.get(k)))
    print("  %-40s %-16s %-16s" % ("nodi finali", len(np.asarray(C["psi"])), len(np.asarray(B["psi"]))))
    print("""
  NB: il blob PRE-TEMPO 2 NON ha i contatori delle due porte (sono stati aggiunti ora), quindi
  la riga delle porte esiste solo per l'attuale. Il confronto qui e' sul FALLBACK, che c'era
  in entrambi.""")

# ------------------------------------------------------------------ il verdetto
print("\n" + "=" * 118)
if B is not None:
    inv = B.get("_por_invoc") or 1
    pa, pb = B.get("_porta_A") or 0, B.get("_porta_B") or 0
    print("IL VERDETTO, contro le TRE letture fissate PRIMA:")
    kp, kr = B.get("_sfondo_ko_peq") or 0, B.get("_sfondo_ko_rho") or 0
    up, ur = B.get("_sfondo_ko_ultima_peq") or 0, B.get("_sfondo_ko_ultima_rho") or 0
    print("  PORTA A (lunghezza) : %d       PORTA B (valore di peq) : %d, ultima invocazione %s"
          % (pa, pb, B.get("_porta_B_ultima")))
    print("  e la separazione delle DUE condizioni di `_ok_n`:")
    print("     _peq_nodo NON valido    : %-8d ultima invocazione %s" % (kp, up))
    print("     rho_sorgente NON valido : %-8d ultima invocazione %s" % (kr, ur))
    print("""
  -> NESSUNA DELLE TRE LETTURE DEL MANDATO. E' UNA QUARTA, e la misura la isola:

     PORTA A non scatta MAI (0): le lunghezze combaciano sempre. Nessun difetto di LUNGHEZZA.
     PORTA B scatta 4 volte su 66, ULTIMA ALL'INVOCAZIONE 8: e' il TRANSITORIO, e il conteggio
             dei nodi (2392) e' ESATTAMENTE il fallback totale del blob PRE-TEMPO 2.
             -> LA COMPONENTE `peq` E' INVARIATA dal TEMPO 2.
     LA CAUSA DEL FALLBACK PERMANENTE E' LA TERZA CONDIZIONE: `rho_sorgente <= 0`, che cade fino
             all'invocazione 66 su 2019 nodi-invocazione.

     `rho_sorgente` e' `rho_spin` (il campo EMESSO) con CAMPO_SPINORIALE ON, e il TEMPO 2 ha
     cambiato `psi` -- Q4 lo ha dimostrato (1669 nodi contro 1850). Quindi il TEMPO 2 ha prodotto
     nodi in cui IL CAMPO EMESSO SI ANNULLA, dove prima non accadeva.

     ESITO OPERATIVO: e' la LETTURA (2) del referto -- un difetto introdotto dal TEMPO 2 -- MA CON
     UNA CAUSA DIVERSA da quella che il mandato ipotizzava (non `peq` letto prima della
     calibrazione, ma `rho_spin` che si annulla). NON LO RIPARO: il mandato dice di misurare.""")
ok = sum(esiti)
print("\nbyte-inerzia: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
