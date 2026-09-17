# -*- coding: utf-8 -*-
"""SCELTA DEL DENOMINATORE: d'ARCO oppure NESSUNO? (mandato par.1)

Il vincolo, gia' stabilito:
  - deve vivere sull'ARCO (non sul nodo), altrimenti l'antisimmetria si rompe;
  - deve essere SIMMETRICO in i/j PER COSTRUZIONE;
  - `w` e' ESCLUSO: `flusso = w*imag(ov)`, dividere per `w` lo CANCELLA.

⚠ LA DOMANDA CHE DECIDE, e che il mandato pone giustamente: **il denominatore d'arco CONSERVA LA
  FUNZIONE ORIGINALE?** Il docstring dice che la divisione serve perche' *«un nodo con cento archi
  non deve accumulare cento volte»*, cioe' vuole una grandezza **INTENSIVA** (una MEDIA sui vicini),
  non **ESTENSIVA** (una SOMMA). E qui c'e' un punto che va misurato, non assunto:

      out[k] = SOMMA_{archi di k} (+-f / den_arco)

  resta una **SOMMA su un numero di termini che cresce col grado**. Un denominatore d'arco riduce
  ogni termine, ma **non toglie che i termini siano di piu'**. **Se dopo la cura `|out|` cresce
  ancora col grado, la cura ripristina l'ANTISIMMETRIA ma NON la funzione dichiarata** — e questo
  va detto, non nascosto.

SI MISURA, per ogni variante, la PENDENZA di log|out| contro log(grado):
   ~ +1.0  -> ESTENSIVA e coerente (i contributi si sommano in fase)
   ~ +0.5  -> ESTENSIVA a segni casuali (random walk sui vicini)
   ~  0.0  -> INTENSIVA (e' cio' che il docstring dichiara di volere)
   < 0     -> penalizza i nodi connessi
Il valore SOTTO IPOTESI NULLA non e' zero: se i flussi hanno segno casuale, la somma nuda cresce
gia' come sqrt(grado). **Quel +0.5 va sottratto mentalmente prima di dire «cresce col grado».**

QUATTRO VARIANTI:
  (0) ATTUALE  f/g_i  e  f/g_j          denominatori NODALI diversi        <- il difetto
  (1) NUDO     f      e  f              nessun denominatore, zero scelte
  (2) MEDIA    f/((g_i+g_j)/2)          d'arco, simmetrico                 <- candidato del mandato
  (3) LINEA    f/(g_i+g_j-2w)           d'arco: il GRADO DELL'ARCO nel grafo linea
                                        (quanti archi toccano questo arco) -- l'unico candidato che
                                        non e' una scelta fra media/min/max, ma un oggetto DERIVATO
Le varianti (2) e (3) sono riportate ENTRAMBE proprio per non spacciare una scelta per derivazione.

Osserva e delega: nessuna legge del file e' toccata, il metodo e' sostituito per la sola durata.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
_ARGV = list(sys.argv)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO", "SPIN_FEEDBACK"):
    setattr(S, _f, True)
S.TAU_A = float(_ARGV[_ARGV.index("--tau-a") + 1]) if "--tau-a" in _ARGV else S.TAU_A
PASSI = int(_ARGV[_ARGV.index("--passi") + 1]) if "--passi" in _ARGV else 60

print("=" * 118)
print("SCELTA DEL DENOMINATORE: d'arco o nessuno?   [TAU_A=%s, %d passi, 1 seme]" % (S.TAU_A, PASSI))
print("=" * 118)

MODI = ("attuale", "nudo", "media", "linea")
orig = S.Rete._feedback_spinoriale_archi
D = {}


def fabbrica(modo, reg):
    def metodo(self, i, j, w):
        out = np.zeros(self.n)
        self._spin_feedback_last = 0.0
        if not S.SPIN_FEEDBACK or len(self._spinor_lift) < self.n:
            return out
        mask = (i < self.n) & (j < self.n)
        if not mask.any():
            return out
        ii, jj, ww = i[mask], j[mask], w[mask]
        ov = np.sum(np.conj(self._spinor_lift[ii]) * self._spinor_lift[jj], axis=1)
        flusso = ww * np.imag(ov)
        grado = np.zeros(self.n)
        np.add.at(grado, ii, ww); np.add.at(grado, jj, ww)
        gi = np.maximum(grado[ii], 1e-9); gj = np.maximum(grado[jj], 1e-9)
        if modo == "attuale":
            np.add.at(out, ii, -flusso / gi); np.add.at(out, jj, flusso / gj)
        elif modo == "nudo":
            np.add.at(out, ii, -flusso); np.add.at(out, jj, flusso)
        else:
            den = (gi + gj) * 0.5 if modo == "media" else np.maximum(gi + gj - 2.0 * ww, 1e-9)
            np.add.at(out, ii, -flusso / den); np.add.at(out, jj, flusso / den)
        # conteggio archi per nodo (grado TOPOLOGICO, non pesato): e' l'ascissa della pendenza
        gtop = np.zeros(self.n)
        np.add.at(gtop, ii, 1.0); np.add.at(gtop, jj, 1.0)
        reg.append(dict(somma=float(np.sum(out)), scala=float(np.max(np.abs(out))),
                        out=np.abs(out).copy(), gtop=gtop.copy(),
                        medio=float(np.median(np.abs(out)))))
        self._spin_feedback_last = float(np.mean(np.abs(flusso))) if len(flusso) else 0.0
        return out
    return metodo


def gira(modo):
    reg = []
    S.Rete._feedback_spinoriale_archi = fabbrica(modo, reg)
    r = S.Rete(5)
    r.semina(80)
    for _ in range(6):
        S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
    for k in range(3):
        ang = 2 * np.pi * k / 3
        r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                      centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    r.aggiorna_pesi_concorrenza()
    pv0 = float(np.sum(np.asarray(r.phivel, float)[:r.n]))
    for kk in range(PASSI):
        S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    pv1 = float(np.sum(np.asarray(r.phivel, float)[:r.n]))
    return r, reg, pv0, pv1


for modo in MODI:
    try:
        D[modo] = gira(modo)
    except Exception as e:
        D[modo] = ("ERRORE", "%s: %s" % (type(e).__name__, e), 0.0, 0.0)
        print("  !! variante '%s' ESPLOSA: %s" % (modo, e))
    finally:
        S.Rete._feedback_spinoriale_archi = orig

# --------------------------------------------------------------- G1
print("\n--- (G1) |sum(out)| / max|out| -- L'ANTISIMMETRIA. E' la conservazione, non una forma ---")
print("  %-10s %-16s %-16s %-10s" % ("variante", "mediana", "MAX", "invocaz."))
for modo in MODI:
    r, reg = D[modo][0], D[modo][1]
    if r == "ERRORE":
        print("  %-10s ESPLOSA" % modo); continue
    rel = [abs(x["somma"]) / max(x["scala"], 1e-300) for x in reg if x["scala"] > 0]
    print("  %-10s %-16.3e %-16.3e %-10d" % (modo, np.median(rel), np.max(rel), len(rel)))
print("  (epsilon macchina ~1e-16. 'attuale' e' il difetto: mediana 1.112, MAX 8.441)")

# --------------------------------------------------------------- la pendenza contro il grado
print("\n--- LA DOMANDA DEL MANDATO: |out| cresce col GRADO? pendenza di log|out| vs log(grado) ---")
print("  nullo: +0.5 = somma di contributi a SEGNO CASUALE (random walk). 0.0 = INTENSIVA.")
print("  %-10s %-12s %-12s %-10s %-34s" % ("variante", "pendenza", "r", "n nodi", "|out| mediano per grado 2/4/8"))
for modo in MODI:
    r, reg = D[modo][0], D[modo][1]
    if r == "ERRORE":
        print("  %-10s ESPLOSA" % modo); continue
    # si usano le ULTIME 10 invocazioni: il regime, non il transitorio (lezione del 2.706)
    O = np.concatenate([x["out"] for x in reg[-10:]])
    G = np.concatenate([x["gtop"] for x in reg[-10:]])
    m = (O > 0) & (G > 0)
    x, y = np.log(G[m]), np.log(O[m])
    b = np.polyfit(x, y, 1)[0] if m.sum() > 10 else float("nan")
    rr = float(np.corrcoef(x, y)[0, 1]) if m.sum() > 10 else float("nan")
    bins = []
    for g in (2, 4, 8):
        sel = m & (np.abs(G - g) < 0.5)
        bins.append(float(np.median(O[sel])) if sel.sum() > 3 else float("nan"))
    print("  %-10s %-12.4f %-12.4f %-10d %-34s"
          % (modo, b, rr, int(m.sum()), "  ".join("%.4g" % v for v in bins)))

# --------------------------------------------------------------- ampiezza e conservazione
print("\n--- AMPIEZZA del termine e DERIVA di sum(phivel) ---")
print("  %-10s %-16s %-16s %-14s %-9s" % ("variante", "|out| mediano", "max|out|", "deriva phivel", "n finale"))
for modo in MODI:
    r, reg = D[modo][0], D[modo][1]
    if r == "ERRORE":
        print("  %-10s ESPLOSA" % modo); continue
    med = float(np.median([x["medio"] for x in reg[-10:]]))
    mx = float(np.max([x["scala"] for x in reg]))
    print("  %-10s %-16.5g %-16.5g %-14.5g %-9d" % (modo, med, mx, D[modo][3] - D[modo][2], r.n))

# --------------------------------------------------------------- stabilita'
print("\n--- stabilita' ---")
for modo in MODI:
    r = D[modo][0]
    if r == "ERRORE":
        print("  %-10s ESPLOSA" % modo); continue
    pv = np.asarray(r.phivel, float); om = np.asarray(r.omega_s, float)
    print("  %-10s NaN/inf phivel %d  omega_s %d   max|phivel| %.5g" %
          (modo, int(np.sum(~np.isfinite(pv))), int(np.sum(~np.isfinite(om))),
           float(np.max(np.abs(pv[np.isfinite(pv)]))) if np.any(np.isfinite(pv)) else float("nan")))

print("\n" + "=" * 118)
print("""COME SI LEGGE
  G1 decide la CORRETTEZZA: tutte le varianti d'arco e 'nudo' devono stare all'epsilon.
  La PENDENZA decide se la cura conserva anche la FUNZIONE dichiarata dal docstring:
    se 'media'/'linea' hanno pendenza vicina a quella di 'attuale', la funzione e' conservata;
    se hanno la pendenza di 'nudo', il denominatore d'arco NON e' una normalizzazione: e' un
    fattore di scala, e allora 'nudo' -- che non ha scelte -- e' preferibile (A1, par.3).""")
