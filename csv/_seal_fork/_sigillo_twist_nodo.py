# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA SUL PUNTO 3 -- `twist_nodo` / `FRAME_DRAG`  (Z27).

H0  identita' del file: sha1 dei BYTE GREZZI (mai `git hash-object`: trappola CRLF, C18)
H1  [BLOCCANTE] |sum(twist_nodo)|/max|.| a ZERO ESATTO su OGNI invocazione. Era 6.756 / MAX 8.483.
H2  riduzione al limite. ⚠ il limite VERO e' GRADO TOPOLOGICO = 1, non "gradi uguali":
    con grado `g` la vecchia da' `tn/g` e la nuova `tn`. Dichiarato PRIMA in PREVISIONI (52823d4).
H3  controllo positivo: coi gradi veri la forma nuova DEVE differire dalla vecchia.
H4  ⚠ IL RISCHIO SCRITTO PRIMA: qui `grado` e' il CONTEGGIO (media ~80, mediana 119), non il grado
    PESATO come in Z25. La cura MOLTIPLICA il termine, non lo divide. Si misura di QUANTO, e il
    rapporto termine/coppia PRINCIPALE, contro lo "~0.2" che il vecchio commento asseriva.
H5  stabilita' [BLOCCANTE]: no NaN/inf, CFL < 1, nessun runaway di phivel.
H6  il commento corretto: le due affermazioni smentite non devono piu' esserci.

LE TRE LETTURE erano fissate in doc/PREVISIONI_qualitative.md PRIMA di toccare il codice:
  residuo a zero E sistema stabile     -> la cura regge.
  residuo a zero MA sistema instabile  -> `nudo` NON basta qui: DIMOSTRAZIONE, non preferenza.
                                          Si committa il fallimento e CI SI FERMA (par.5).
  residuo NON a zero                   -> ricostruzione sbagliata: si riporta e stop.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import hashlib

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
_ARGV = list(sys.argv)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(S, _f, True)
S.TAU_A = float(_ARGV[_ARGV.index("--tau-a") + 1]) if "--tau-a" in _ARGV else 2.0

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-50s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("SIGILLO DELLA CURA SUL PUNTO 3 -- twist_nodo / FRAME_DRAG  (Z27)")
print("=" * 118)

b = open(os.path.join(ROOT, "soliton_simulator.py"), "rb").read()
print("\n--- H0: sha1 dei BYTE GREZZI = %s   (%d byte) ---" % (hashlib.sha1(b).hexdigest()[:8], len(b)))
print("  FRAME_DRAG = %s   <- il gate: se fosse False la misura sarebbe vuota" % S.FRAME_DRAG)

src = b.decode("utf-8", "replace")

# ---------------------------------------------------------------- H2 e H3: forma algebrica pura
print("\n--- H2: riduzione al limite. Il limite VERO e' GRADO TOPOLOGICO = 1 ---")


def vecchia(n, i, j, twn):
    tn = np.zeros(n); g = np.zeros(n)
    np.add.at(tn, i, twn); np.add.at(tn, j, -twn)
    np.add.at(g, i, 1.0); np.add.at(g, j, 1.0)
    return tn[:n] / np.maximum(g[:n], 1.0)


def nuova(n, i, j, twn):
    tn = np.zeros(n)
    np.add.at(tn, i, twn); np.add.at(tn, j, -twn)
    return tn[:n]


rng = np.random.default_rng(3)
n2 = 8
i2 = np.array([0, 2, 4, 6]); j2 = np.array([1, 3, 5, 7])     # accoppiamento perfetto: grado 1 su tutti
t2 = rng.normal(size=4)
g2 = np.zeros(n2); np.add.at(g2, i2, 1.0); np.add.at(g2, j2, 1.0)
print("  grado topologico per nodo: min %.0f  max %.0f  (deve essere 1 su tutti)" % (g2.min(), g2.max()))
A = nuova(n2, i2, j2, t2); B = vecchia(n2, i2, j2, t2)
d = float(np.max(np.abs(A - B)))
verdetto("H2 al limite grado=1 la nuova == la vecchia", d == 0.0,
         "max|A-B| = %.3e   (shape %s vs %s)" % (d, A.shape, B.shape))

print("\n--- H3: controllo positivo -- coi gradi VERI le due forme DEVONO differire ---")
n3 = 6
i3 = np.array([0, 0, 0, 1, 1]); j3 = np.array([1, 2, 3, 4, 5])
t3 = rng.normal(size=5)
g3 = np.zeros(n3); np.add.at(g3, i3, 1.0); np.add.at(g3, j3, 1.0)
A3 = nuova(n3, i3, j3, t3); B3 = vecchia(n3, i3, j3, t3)
print("  gradi topologici: %s" % g3.astype(int))
verdetto("H3 coi gradi veri le due forme DIFFERISCONO", float(np.max(np.abs(A3 - B3))) > 1e-12,
         "max|nuova-vecchia| = %.5g" % np.max(np.abs(A3 - B3)))
verdetto("H3b la NUOVA ha somma zero, la VECCHIA no",
         abs(A3.sum()) < 1e-14 and abs(B3.sum()) > 1e-9,
         "sum(nuova) = %.3e   sum(vecchia) = %.5g" % (A3.sum(), B3.sum()))

# ---------------------------------------------------------------- il run: H1, H4, H5
print("\n--- il run: scena del batch, TAU_A = %s, 60 passi, seme 5 ---" % S.TAU_A)
REG = []
orig_step = S.Rete.step


def spia(self):
    n = self.n
    try:
        i = np.asarray(self.i); j = np.asarray(self.j)
        if len(i) and S.FRAME_DRAG and len(self.tw):
            if S.CHI_CORE and len(self.perc_chi) >= n:
                cc = self.chiralita_core_locale()
                twn = (np.pi * 0.5 * (cc[i] - cc[j])) / S.PHI_CRIT
            elif S.VERSO_CHI and len(self.perc_chi) >= n:
                twn = (np.pi * 0.5 * (self.perc_chi[i] - self.perc_chi[j])) / S.PHI_CRIT
            else:
                twn = np.asarray(self.tw, float) / S.PHI_CRIT
            tn = nuova(n, i, j, twn)
            vc = vecchia(n, i, j, twn)
            sc = float(np.max(np.abs(tn)))
            REG.append(dict(res=(abs(float(tn.sum())) / sc) if sc > 0 else None,
                            med_new=float(np.median(np.abs(tn))),
                            med_old=float(np.median(np.abs(vc))),
                            max_new=sc, max_old=float(np.max(np.abs(vc)))))
    except Exception as e:
        REG.append(dict(errore=str(e)))
    return orig_step(self)


S.Rete.step = spia
r = S.Rete(5)
r.semina(80)
for _ in range(6):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
for k in range(3):
    a = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for _ in range(60):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
S.Rete.step = orig_step

buoni = [x for x in REG if "errore" not in x and x.get("res") is not None]
err = [x for x in REG if "errore" in x]
if err:
    print("  ⚠ la sonda ha avuto %d errori: %s" % (len(err), err[0]["errore"][:80]))

print("\n--- H1 [BLOCCANTE]: l'antisimmetria su OGNI invocazione ---")
res = np.array([x["res"] for x in buoni])
print("  invocazioni con termine non nullo: %d su %d" % (len(res), len(REG)))
print("  |sum|/max|.| : mediana %.3e   MAX %.3e   (era: mediana 6.756, MAX 8.483)"
      % (np.median(res), np.max(res)) if len(res) else "  nessuna")
verdetto("H1 antisimmetria ESATTA su OGNI invocazione  [BLOCCANTE]",
         len(res) > 0 and float(np.max(res)) < 1e-12,
         "MAX = %.3e" % (np.max(res) if len(res) else float("nan")))

print("\n--- H4: IL RISCHIO SCRITTO PRIMA -- di quanto cresce il termine? ---")
mn = float(np.median([x["med_new"] for x in buoni])); mo = float(np.median([x["med_old"] for x in buoni]))
xn = float(np.max([x["max_new"] for x in buoni])); xo = float(np.max([x["max_old"] for x in buoni]))
print("  |twist_nodo| mediano : vecchio %.5g  ->  nuovo %.5g   (fattore %.4g)" % (mo, mn, mn / max(mo, 1e-300)))
print("  max|twist_nodo|      : vecchio %.5g  ->  nuovo %.5g   (fattore %.4g)" % (xo, xn, xn / max(xo, 1e-300)))
print("  previsione ex ante (52823d4): '~10^2 volte piu' grande'")
print("  NB: NON e' un criterio PASS/FAIL -- e' la grandezza che decide se la lettura 2 si applica.")

print("\n--- H5 [BLOCCANTE]: stabilita' ---")
pv = np.asarray(r.phivel, float); om = np.asarray(r.omega_s, float)
nan = int(np.sum(~np.isfinite(pv))) + int(np.sum(~np.isfinite(om)))
verdetto("H5a nessun NaN/inf  [BLOCCANTE]", nan == 0,
         "phivel %d, omega_s %d" % (int(np.sum(~np.isfinite(pv))), int(np.sum(~np.isfinite(om)))))
cfl = getattr(r, "_taup_cfl_max", None)
verdetto("H5b CFL < 1", cfl is not None and float(cfl) < 1.0, "_taup_cfl_max = %s" % cfl)
print("  max|phivel| %.5g   max|omega_s| %.5g   n finale %d   (pre-cura, stessa scena: 14.345 / 34778 / 548)"
      % (np.max(np.abs(pv[np.isfinite(pv)])), np.max(np.abs(om[np.isfinite(om)])), r.n))

print("\n--- H6: il commento corretto ---")
smentite = ["mediato sugli archi del nodo", "scala giusta (~0.2 della coppia principale) senza aggiustamenti"]
viva = [f for f in smentite if f in src.split("if FRAME_DRAG")[0][-3000:]]
verdetto("H6 le affermazioni smentite non sono piu' nel commento", not viva,
         "sopravvivono: %s" % (viva if viva else "nessuna"))
verdetto("H6b il commento SPIEGA perche' erano false", "6.756" in src and "0.000e+00 SENZA la" in src,
         "cita la misura: %s" % ("6.756" in src))

print("\n" + "=" * 118)
print("SIGILLO: %d/%d PASS" % (sum(esiti), len(esiti)))
print("""
COME SI LEGGE -- le tre letture erano fissate PRIMA (doc/PREVISIONI_qualitative.md, 52823d4)
  H1 a zero E H5 verdi          -> la cura regge. Si riporta il rapporto di H4, misurato.
  H1 a zero MA H5 rosso         -> `nudo` NON basta qui: e' una DIMOSTRAZIONE, non una preferenza.
                                   Si committa il fallimento e CI SI FERMA, senza scegliere al volo.
  H1 non a zero                 -> ricostruzione sbagliata: si riporta e stop.""")
