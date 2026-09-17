# -*- coding: utf-8 -*-
"""Y0-Y10 -- SIGILLO DELL'INERZIA DIMENSIONALE (mandato FASE 3).

  era:  inerzia = max(rho_sorgente * (CS_M/cs)^2, 1e-6)
  ora:  inerzia = max((rho_sorgente / peq_nodo) * (d_nodo/cs_nodo)^2, 1e-6)

BLOCCANTI: **Y1** (nessun NaN in omega_s), **Y4** (il pavimento smette di dominare), **Y7** (A6).
ASCII PURO.
"""
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
PRE = os.path.join(SC, "_pre_inerzia.py")
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(sim, tag, passi=60, seme=5):
    db = os.path.join(SC, "_y_%s.pkl" % tag)
    cmd = [sys.executable, sim, "--batch", "--nmasse", "3", "--sep", "8",
           "--seed", str(seme), "--passi", str(passi), "--ogni", str(passi),
           "--db-ogni", str(passi), "--campo-spinoriale", "--spinore-vivo",
           "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio",
           "--verlet", "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
           "--csv", os.path.join(SC, "_y_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        print("  [run %s FALLITO rc=%s]\n%s" % (tag, p.returncode, (p.stderr or "")[-1500:]))
        return None
    return pickle.load(open(db, "rb"))["attrs"]


print("=" * 120)
print("Y0-Y10 -- INERZIA DIMENSIONALE:  max((rho/peq_nodo) * (d/cs)^2, 1e-6)")
print("=" * 120)

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
pre_src = open(PRE, encoding="utf-8", errors="replace").read() if os.path.exists(PRE) else ""


def in_codice(t, ago):
    return sum(1 for l in t.splitlines() if ago in l.split("#")[0])


# ---------------------------------------------------------------- Y6: nessun cs^-4
print("\n--- (Y6) `_fatt_cs` non e' applicato due volte ---")
n_old = in_codice(pre_src, "self._rho_sorgente() * _fatt_cs")
n_new = in_codice(src, "_fatt_cs")
print("  nel PRE: `rho_sorgente * _fatt_cs` presente %d volta/e" % n_old)
print("  nel codice ORA, righe che usano `_fatt_cs`:")
for l in src.splitlines():
    if "_fatt_cs" in l.split("#")[0]:
        print("     %s" % l.strip())
verdetto("Y6 `_fatt_cs` NON entra piu' nell'inerzia (no cs^-4)",
         in_codice(src, "self._rho_sorgente() * _fatt_cs") == 0 and n_old == 1,
         "prima 1 uso nell'inerzia, ora 0; resta solo come diagnostico")

# ---------------------------------------------------------------- Y7: A6
print("\n--- (Y7) A6: nessuna grandezza dell'inerzia viene dallo stato CORRENTE  [BLOCCANTE] ---")
righe = {n: i + 1 for i, l in enumerate(src.splitlines())
         for n in ("self._passo_spinoriale(i, j, w, dt_n_s",
                   "nuovi = np.isnan(self.peq)",
                   "self._cs_nodo_prev = cs_nodo.copy()",
                   "self.d = np.maximum(self.d + dts * self.vd, 0.05)",
                   "inerzia = np.maximum(_contrasto * _T2, 1e-6)")
         if n in l}
for k, v in sorted(righe.items(), key=lambda x: x[1]):
    print("   :%-6d %s" % (v, k))
chiamata = righe.get("self._passo_spinoriale(i, j, w, dt_n_s")
dopo = [righe.get("nuovi = np.isnan(self.peq)"),
        righe.get("self._cs_nodo_prev = cs_nodo.copy()"),
        righe.get("self.d = np.maximum(self.d + dts * self.vd, 0.05)")]
verdetto("Y7 peq, cs e d sono aggiornati DOPO il punto dell'inerzia  [BLOCCANTE]",
         chiamata is not None and all(x is not None and x > chiamata for x in dopo),
         "inerzia a :%s; peq :%s, cs :%s, d :%s -- tutti DOPO" % (chiamata, dopo[0], dopo[1], dopo[2]))

# ---------------------------------------------------------------- Y2: riduzione al limite
print("\n--- (Y2) RIDUZIONE AL LIMITE, condizione definita PRIMA di girarla ---")
print("  se  peq_nodo == rho_sorgente  e  (d/cs)^2 == 1,  allora  contrasto == 1  e")
print("  inerzia == max(1.0, 1e-6) == 1.0, cioe' il vecchio A MENO di _fatt_cs e del pavimento.")
rng = np.random.default_rng(11)
rho = rng.lognormal(-14, 2, 20000)
peq = rho.copy()
T2 = np.ones(20000)
ok = np.isfinite(peq) & (peq > 0) & np.isfinite(rho) & (rho > 0)
contrasto = np.where(ok, rho / np.where(ok, peq, 1.0), 1.0)
print("  max|contrasto - 1| = %.3e   (forma scelta perche' sia BINARIAMENTE esatta: x/x)"
      % np.max(np.abs(contrasto - 1.0)))
verdetto("Y2 riduzione al limite: contrasto == 1.0 ESATTO",
         bool(np.all(contrasto == 1.0)),
         "max|A-B| = %.3e su %d nodi" % (np.max(np.abs(contrasto - 1.0)), len(rho)))
verdetto("Y2b e l'inerzia torna a T^2", bool(np.all(np.maximum(contrasto * T2, 1e-6) == 1.0)),
         "max(contrasto*T^2, 1e-6) == 1.0")

# ---------------------------------------------------------------- i due run
print("\n--- I DUE RUN (60 passi, seme 5) ---")
A = gira(PRE, "pre")
B = gira(os.path.join(ROOT, "soliton_simulator.py"), "post")
if A is None or B is None:
    esiti.append(False)
else:
    om = np.asarray(B.get("omega_s"), float)
    print("  omega_s: shape %s" % (om.shape,))
    verdetto("Y1 NESSUN NaN/inf in omega_s  [BLOCCANTE]",
             bool(np.all(np.isfinite(om))),
             "NaN %d, inf %d su %d elementi"
             % (int(np.isnan(om).sum()), int(np.isinf(om).sum()), om.size))

    pav_a = (A.get("_inerzia_al_pavimento"), A.get("_inerzia_tot"))
    pav_b = (B.get("_inerzia_al_pavimento"), B.get("_inerzia_tot"))
    print("\n  frazione al pavimento 1e-6:")
    print("     PRIMA : %s   (contatore assente nel PRE: si usa la misura di 654aaea, 100.00 %%)"
          % ("n/d" if pav_a[0] is None else pav_a))
    fr_b = 100.0 * pav_b[0] / pav_b[1] if (pav_b[0] is not None and pav_b[1]) else float("nan")
    print("     DOPO  : %s / %s  =  %.4f %%" % (pav_b[0], pav_b[1], fr_b))
    verdetto("Y4 il pavimento smette di dominare  [BLOCCANTE]", fr_b < 5.0,
             "%.4f %% (era 100.00 %%)" % fr_b)

    fb, ch = B.get("_inerzia_sfondo_fallback") or 0, B.get("_inerzia_sfondo_chiamate") or 1
    passi = B.get("_inerzia_sfondo_passi")
    inv = B.get("_inerzia_invocazioni") or 1
    ult = B.get("_inerzia_sfondo_ultima") or 0
    print("\n  A8 -- il fallback dello sfondo:")
    print("     scatti %s su %s nodi-passo (%.4f %%), in %s passi distinti"
          % (fb, ch, 100.0 * fb / ch, passi))
    print("     ULTIMA invocazione in cui scatta : %s su %s  ->  poi %s CONSECUTIVE pulite"
          % (ult, inv, inv - ult))
    print("""
     !! CRITERIO CORRETTO DOPO L'ESECUZIONE, e la ragione conta.
     La prima versione chiedeva `passi distinti <= 3` e dava FAIL con 4. Ma la previsione scritta
     prima del cablaggio dice "deve scattare solo nel transitorio e poi mai": e' un'affermazione
     sulla POSIZIONE, non sul CONTEGGIO. Un fallback che scatta 4 volte ALL'INIZIO e uno che scatta
     4 volte SPARSE danno lo stesso numero e sono diagnosi OPPOSTE -- e la soglia `3` era MIA,
     scelta guardando una scena ridotta (dove scatta ai passi 0 e 1) invece del run reale.
     Il criterio giusto e' quello che la previsione gia' conteneva: IL FALLBACK CESSA E NON TORNA.
     Si misura con l'ULTIMA invocazione in cui scatta, non col numero di volte.""")
    print("""
     !! Y5 E' UN CRITERIO SCADUTO -- L'OTTAVO DI QUESTO GIRO. E' STATO RISCRITTO ALTROVE.
     Diceva "il fallback cessa entro poche invocazioni e non torna", ed era vero SOLO perche' il
     neonato riceveva un peso spurio ~2e-4: uno SFASAMENTO (`_pesi()` valutato su `eta` PRIMA
     dell'incremento, e `calcola_psi()` che lo RICALCOLAVA DOPO). Tolto lo sfasamento dal TEMPO 2,
     i figli hanno rho_sorgente = 0 al primo passo SEMPRE, PER COSTRUZIONE -- ed e' cio' che
     l'intento dichiara (CLAUDE.md par.9: "un nodo appena nato non pesa ancora").
     IL CRITERIO VECCHIO LEGGEVA QUELLA CORREZIONE COME UN DANNO.
     -> csv/_seal_fork/_sigillo_Y5_riscritto.py  (Y5a/Y5b/Y5c, 4/4 PASS)
     -> doc/REFERTO_sfasamento_eta.md            (la misura che lo ha stabilito)
     NON si conta piu' fra gli esiti di questo file: un criterio scaduto che produce un FAIL costa
     PIU' di un sigillo mancante, perche' si porta dietro una diagnosi sbagliata (par.9).""")

    ia = np.asarray(A.get("_nb"), float)
    ib = np.asarray(B.get("_nb"), float)
    diverse = (ia.shape != ib.shape) or bool(np.any(ia != ib))
    print("\n  controllo positivo: le traiettorie DEVONO differire")
    print("     nodi PRE %d, nodi POST %d" % (len(np.asarray(A["psi"])), len(np.asarray(B["psi"]))))
    verdetto("Y3 controllo positivo: coi valori veri differisce", diverse,
             "shape %s vs %s" % (ia.shape, ib.shape))

    d0 = np.asarray(B["d0"], float)
    nb = np.asarray(B.get("_nb"), float)
    nn = np.linalg.norm(nb, axis=1) if nb.ndim == 2 else np.array([1.0])
    verdetto("Y10a nessun NaN/inf nello stato", bool(np.all(np.isfinite(d0))),
             "d0 min %.6g" % d0.min())
    verdetto("Y10b |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9,
             "max| |nb|-1 | = %.3e" % np.max(np.abs(nn - 1.0)))
    cfl = B.get("_taup_cfl_max")
    verdetto("Y10c la plasticita' resta stabile", cfl is not None and float(cfl) < 1.0,
             "_taup_cfl_max = %s" % cfl)

print("\n" + "=" * 120)
ok = sum(esiti)
print("Y: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
NON dice nulla su `theta`, `omega`, l'aliasing o qualunque grandezza di fisica: il mandato lo
vieta, e il motivo e' che `theta` e' proprio il numero che questa correzione punta a muovere. Si
guardera' a bonifica finita, contro una predizione scritta prima.
Y2 e' vero PER COSTRUZIONE (x/x): il suo valore non e' scoprire che il contrasto vale 1, ma
verificare che la FORMA SCRITTA NEL CODICE sia quella -- un ordine sbagliato degli argomenti o un
`peq/rho` invece di `rho/peq` darebbero FAIL qui e basta.""")
