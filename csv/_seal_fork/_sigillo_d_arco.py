# -*- coding: utf-8 -*-
"""V1 -- SIGILLO DELLA CORREZIONE `d_arco` (par.1 del mandato). **Cablata DA SOLA.**

Il difetto:  d_arco = 0.5 * (self.d[self.i] + self.d[self.j])
`d`/`d0` sono PER ARCO; `i`/`j` sono indici di NODO. Shape giusta, VALORI sbagliati.
La cura:     d_arco = self.d        (e `self.d0` nel ramo TAU_USA_D0, oggi spento)

CRITERIO BLOCCANTE (V1d): `d_arco` deve DIVENTARE la lunghezza vera dell'arco.

⚠ IL CRITERIO DEL MANDATO ERA *"correlazione da -0.349 a +1.000 esatto"*, ed e' stato CORRETTO
  DUE VOLTE dopo averlo eseguito, in entrambi i casi perche' la MISURA ha smentito il criterio
  (par.9: un criterio si scrive da una misura, non dal proprio modello del codice):
  1. **+1.000 "esatto" non regge attraverso `np.corrcoef`**: su un seme su quattro il risultato e'
     `0.99999999999999978`, cioe' 1 - 2.2e-16. Non e' un difetto della cura, e' arrotondamento di
     un CALCOLO -- e sotto c'e' un'IDENTITA' (`d_arco` *e'* `self.d`), che si verifica con
     `np.array_equal` ed e' esatta su 4 semi su 4. **Si testa l'identita', non la sua immagine
     numerica.**
  2. **-0.349 era UN SEME.** Su quattro: -0.3488 / +0.1444 / +0.0319 / +0.3760. Il segno non e'
     concorde: il vecchio `d_arco` non e' anticorrelato, e' SCORRELATO.

⚠ E V1d, DA SOLO, E' TAUTOLOGICO -- va detto invece di spacciarlo per prova. `d_arco = self.d`
  correlato con `self.d` da' 1 per definizione. Il contenuto vero del sigillo sta in V1c (il
  vecchio NON lo era, su 4 semi) e in V1f (la cura non e' inerte: cambia il 100 % degli archi).

I criteri qui sotto sono scritti DALLA MISURA, non dal modello mentale del codice (par.9): ogni
soglia e' o un'identita' algebrica (1.0 esatto) o un valore gia' misurato e committato.
Dati: i .pkl gia' committati. ASCII PURO.
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
import os
import pickle
import re
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SIM = os.path.join(ROOT, "soliton_simulator.py")
FILES = sorted(glob.glob(os.path.join(ROOT, "csv", "_test_fork", "_vuoto_s2ON_s?.pkl")))
CS_M = 2.0

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("V1 -- SIGILLO `d_arco`: l'array per-ARCO non si indicizza con indici di NODO")
print("=" * 118)

# ------------------------------------------------------------------ V1a: il sorgente e' cambiato
src = open(SIM, "r", encoding="utf-8", errors="replace").read()
ref = subprocess.run(["git", "cat-file", "-p", "827d3bf8"], cwd=ROOT,
                     capture_output=True).stdout.decode("utf-8", "replace")

vecchio_d = "d_arco = 0.5 * (self.d[self.i] + self.d[self.j])"
vecchio_d0 = "d_arco = 0.5 * (self.d0[self.i] + self.d0[self.j])"


def in_codice(testo, ago):
    """Occorrenze nel CODICE ESEGUIBILE, non nei commenti.
    CRITERIO CORRETTO AL PRIMO GIRO: la versione ingenua (`ago in testo`) dava FAIL su una
    correzione giusta, perche' il commento che documenta la cura CITA la riga vecchia. E' lo
    stesso errore gia' fatto contando le occorrenze della stringa GAMMA (par.9): quinta volta
    che un criterio guarda il testo invece del codice."""
    return sum(1 for ln in testo.splitlines() if ago in ln.split("#")[0])


print("\n--- (a) il SORGENTE: il difetto c'era nel riferimento e non c'e' piu' ---")
print("  (si contano le occorrenze nel CODICE, escludendo i commenti: il commento della cura cita")
print("   la riga vecchia, ed e' evidenza voluta -- par.9, 'il codice di una legge esclusa non si")
print("   cancella mai')")
rd, rd0 = in_codice(ref, vecchio_d), in_codice(ref, vecchio_d0)
sd, sd0 = in_codice(src, vecchio_d), in_codice(src, vecchio_d0)
print("  nel blob 827d3bf8 (riferimento): ramo `d` = %d   ramo `d0` = %d" % (rd, rd0))
print("  sul disco ORA                  : ramo `d` = %d   ramo `d0` = %d" % (sd, sd0))
print("  nel COMMENTO sul disco, come evidenza  : %d citazione/i"
      % sum(1 for ln in src.splitlines() if vecchio_d in ln and vecchio_d not in ln.split("#")[0]))
verdetto("V1a il difetto e' SPARITO da entrambi i rami",
         rd == 1 and rd0 == 1 and sd == 0 and sd0 == 0,
         "riferimento 1+1 nel codice; disco 0+0")

m = re.findall(r"^\s*d_arco = (.+?)$", src, re.M)
print("  assegnazioni di d_arco sul disco: %s" % m)
verdetto("V1b la cura e' ESATTAMENTE `self.d` / `self.d0`",
         m == ["self.d0", "self.d"], "trovate %d assegnazioni: %s" % (len(m), m))

# --------------------------------------------------------- V1c-V1f: i DATI, dai .pkl committati
print("\n--- (c) i DATI: correlazione con la lunghezza VERA dell'arco ---")
r_vecchi, r_nuovi, letti, tau_pre, tau_post = [], [], [], [], []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    i = np.asarray(A["i"], int)
    j = np.asarray(A["j"], int)
    d = np.asarray(A["d"], float)
    n = len(np.asarray(A["psi"]))
    I = np.abs(np.asarray(A["psi"])) ** 2
    csn = A.get("_cs_nodo_prev")

    # i due d_arco, sulla STESSA popolazione di archi
    d_vecchio = 0.5 * (d[i] + d[j])          # il codice di 827d3bf8
    d_nuovo = d                              # la cura
    ok = np.isfinite(d_vecchio) & np.isfinite(d_nuovo) & (d > 0)
    r_vecchi.append(np.corrcoef(d_vecchio[ok], d[ok])[0, 1])
    r_nuovi.append(np.array_equal(d_nuovo, d))   # IDENTITA', non correlazione: vedi V1d
    letti.append(len(np.unique(np.concatenate([i, j]))) / float(len(d)))

    # tau_p_loc PRIMA e DOPO (stesso fattore elastico: si isola d_arco)
    rho_arco = 0.5 * (I[i] + I[j])
    rho_med = max(float(np.median(I)), 1e-9)
    fatt = 1.0 + 100.0 * np.maximum(rho_arco / rho_med - 1.0, 0.0)
    if csn is not None and len(np.asarray(csn)) >= n:
        c = np.asarray(csn, float)
        cs_arco = 2.0 * c[i] * c[j] / np.maximum(c[i] + c[j], 1e-12)
    else:
        cs_arco = np.full(len(i), CS_M)
    tau_pre.append(d_vecchio / np.maximum(cs_arco, 1e-9) * fatt)
    tau_post.append(d_nuovo / np.maximum(cs_arco, 1e-9) * fatt)

rv = float(np.mean(r_vecchi))
print("  correlazione d_arco(VECCHIO) <-> lunghezza vera, per seme:")
print("    %s      media %+.4f" % (["%+.4f" % x for x in r_vecchi], rv))
print("  il valore che avrebbe se rappresentasse cio' che dichiara: +1.0000 (identita')")
print("""
  ATTENZIONE, CORREZIONE A UN NUMERO CHE HO SCRITTO IO (doc/REFERTO_U7_fallito.md, commit fb9c8e4):
  li' avevo scritto "correlazione -0.349, ANTICORRELATA" come se fosse IL fatto. Era UN SEME.
  Su quattro semi il SEGNO NON E' NEMMENO CONCORDE. Il difetto quindi non e' "informazione col
  segno sbagliato" (che sarebbe comunque informazione): e' RUMORE. La diagnosi ne esce PIU' forte,
  non piu' debole -- ma il numero che avevo scritto non reggeva, ed e' P3: mai una statistica
  senza barra, e per una barra fra semi servono >= 4 semi.""")
segni = set(np.sign(r_vecchi))
verdetto("V1c il VECCHIO d_arco non rappresenta la lunghezza d'arco",
         len(segni) > 1 and max(abs(x) for x in r_vecchi) < 0.5,
         "segno NON concorde fra semi (%s), |r|max = %.4f contro 1.0 atteso"
         % ("/".join("%+d" % s for s in sorted(segni)), max(abs(x) for x in r_vecchi)))
verdetto("V1d il NUOVO d_arco E' la lunghezza dell'arco  [BLOCCANTE]",
         all(bool(x) for x in r_nuovi),
         "np.array_equal(d_arco, d) = True su %d/%d semi (IDENTITA', non correlazione)"
         % (sum(bool(x) for x in r_nuovi), len(r_nuovi)))

print("\n--- (e) la LOCALIZZAZIONE: quanti archi il ramo vecchio leggeva davvero ---")
fr = float(np.mean(letti))
print("  frazione di archi il cui indice era raggiungibile da i/j: %.4f %%  -> mai letti %.2f %%"
      % (100.0 * fr, 100.0 * (1.0 - fr)))
verdetto("V1e il ramo vecchio ignorava >90 %% degli archi", (1.0 - fr) > 0.90,
         "mai letti %.2f %% (referto: 98.34 %%)" % (100.0 * (1.0 - fr)))

print("\n--- (f) CONTROLLO POSITIVO: la cura NON e' inerte, e non rompe nulla ---")
tp = np.concatenate(tau_pre)
tq = np.concatenate(tau_post)
diff = float(np.mean(tp != tq))
print("  tau_p_loc PRIMA : mediana %.6g   min %.6g   max %.6g" % (np.median(tp), tp.min(), tp.max()))
print("  tau_p_loc DOPO  : mediana %.6g   min %.6g   max %.6g" % (np.median(tq), tq.min(), tq.max()))
print("  archi in cui tau_p_loc CAMBIA: %.4f %%" % (100.0 * diff))
verdetto("V1f controllo positivo: tau_p_loc cambia", diff > 0.5, "cambia sul %.2f %% degli archi" % (100.0 * diff))
verdetto("V1g stabilita': tau_p_loc DOPO finito e > 0",
         bool(np.all(np.isfinite(tq)) and np.all(tq > 0)),
         "min = %.6g, NaN/inf = %d" % (tq.min(), int((~np.isfinite(tq)).sum())))
verdetto("V1h la SHAPE non cambia (il difetto era nei VALORI)",
         len(tp) == len(tq), "%d = %d elementi" % (len(tp), len(tq)))

print("\n" + "=" * 118)
ok = sum(esiti)
print("V1: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
NON dice che la plasticita' ora sia giusta: `fattore_elasticita` e' rimasto quello vecchio, di
proposito (una correzione alla volta, par.1). Dice solo che il PRIMO fattore di tau_p_loc ha
smesso di essere la lunghezza di un altro arco.
NON e' un sigillo di byte-identita': la correzione CAMBIA il comportamento su ogni arco, ed e' cio'
che V1f verifica. Una byte-identita' qui sarebbe un FALLIMENTO, non un successo.
EFFETTO COLLATERALE DICHIARATO: `d_arco` e' usato anche dal ramo GUSCIO_MORBIDO (:3257), che e'
OFF di default (:658). Con quel flag ON, anche quel termine cambia -- non perche' sia stato
toccato, ma perche' condivide la variabile corretta.""")
