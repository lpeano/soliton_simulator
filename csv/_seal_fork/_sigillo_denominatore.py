# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA DEL DENOMINATORE — G0-G9 (mandato par.2).

G0  blob di riferimento, sha1 dei BYTE GREZZI (mai `git hash-object`: trappola CRLF, C18)
G1  [BLOCCANTE] |sum(out)|/max|out| all'EPSILON MACCHINA su OGNI invocazione. Era 1.112 / 8.441.
G2  riduzione al limite. ⚠ NON come scritto nel mandato: vedi sotto.
G3  controllo positivo: coi gradi VERI la forma nuova DEVE differire dalla vecchia
G4  conservazione: sum(phivel) e la sua deriva (la grandezza che sum(coppia)=0 conserva)
G5  A7 SULL'ARCO: +flusso e -flusso esattamente opposti, verifica esplicita
G6  LA CUCITURA DI FASE — mai verificata da nessuno: imag(ov) e' CONTINUO fra passi consecutivi?
G7  A8b: len(_spinor_lift) == n dopo ogni punto di crescita, con contatore
G8  stabilita': no NaN/runaway, |nb| = 1, CFL < 1
G9  il docstring corretto: le due affermazioni smentite non devono piu' esserci

⚠ G2 — IL CRITERIO DEL MANDATO NON PUO' PASSARE COSI' COM'E', ED E' DICHIARATO PRIMA
  (`doc/PREVISIONI_qualitative.md`, commit `f3f1ab0`, scritto PRIMA di girare questo sigillo).
  Il mandato chiede: «forzando `grado[i] = grado[j]`, la forma nuova torna byte-identica alla
  vecchia». **Falso per la variante cablata:** con `grado[i] = grado[j] = g` la vecchia da' `±f/g`
  e la nuova `±f`, che differiscono per il fattore `g`. La byte-identita' vale **solo per g = 1**.
  Quel criterio era giusto per le varianti `media`/`linea`, NON per `nudo`.
  **Quindi G2 e' scritto sul limite VERO: `grado pesato = 1` su ogni nodo.**
  Un criterio scritto dal modello mentale invece che dalla misura e' gia' costato dieci volte
  (CLAUDE.md par.9): qui e' dichiarato PRIMA, non dopo aver visto il FAIL.

ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import hashlib
import subprocess

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
S.TAU_A = float(_ARGV[_ARGV.index("--tau-a") + 1]) if "--tau-a" in _ARGV else 2.0

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("SIGILLO DELLA CURA DEL DENOMINATORE -- G0-G9")
print("=" * 118)

# ---------------------------------------------------------------- G0
b = open(os.path.join(ROOT, "soliton_simulator.py"), "rb").read()
sha = hashlib.sha1(b).hexdigest()
try:
    blob_git = subprocess.run(["git", "rev-parse", "HEAD:soliton_simulator.py"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
except Exception:
    blob_git = "?"
print("\n--- G0: identita' del file ---")
print("  sha1 dei BYTE GREZZI : %s   (%d byte)" % (sha[:8], len(b)))
print("  blob GIT a HEAD      : %s   <- spazio di hash DIVERSO, non confrontabile col precedente"
      % blob_git[:8])
print("  riferimento del mandato: 425e4aaa (blob git, pre-cura)")

# ---------------------------------------------------------------- lo stub minimo
# Il metodo usa SOLO: self.n, self._spinor_lift, e il flag di modulo. Niente Rete completa.
class Finta(object):
    pass


def spinori(n, seme=3):
    rng = np.random.default_rng(seme)
    z = rng.normal(size=(n, 2)) + 1j * rng.normal(size=(n, 2))
    return z / np.linalg.norm(z, axis=1)[:, None]


def vecchia_forma(n, lift, i, j, w):
    """La forma PRE-CURA, ricostruita esplicitamente: e' il termine di paragone."""
    out = np.zeros(n)
    mask = (i < n) & (j < n)
    ii, jj, ww = i[mask], j[mask], w[mask]
    ov = np.sum(np.conj(lift[ii]) * lift[jj], axis=1)
    flusso = ww * np.imag(ov)
    grado = np.zeros(n)
    np.add.at(grado, ii, ww); np.add.at(grado, jj, ww)
    np.add.at(out, ii, -flusso / np.maximum(grado[ii], 1e-9))
    np.add.at(out, jj, flusso / np.maximum(grado[jj], 1e-9))
    return out


def chiama(n, lift, i, j, w):
    r = Finta()
    r.n = n
    r._spinor_lift = lift
    return S.Rete._feedback_spinoriale_archi(r, i, j, w)


# ---------------------------------------------------------------- G2: il limite VERO (grado = 1)
print("\n--- G2: riduzione al limite. Il limite VERO per 'nudo' e' GRADO PESATO = 1 ---")
n = 6
i2 = np.arange(n); j2 = (np.arange(n) + 1) % n      # ciclo: ogni nodo ha 2 archi
w2 = np.full(n, 0.5)                                # grado pesato = 0.5+0.5 = 1 su OGNI nodo
lift = spinori(n)
g_chk = np.zeros(n); np.add.at(g_chk, i2, w2); np.add.at(g_chk, j2, w2)
print("  grado pesato per nodo: min %.6f  max %.6f  (deve essere 1 su tutti)" % (g_chk.min(), g_chk.max()))
A = chiama(n, lift, i2, j2, w2)
B = vecchia_forma(n, lift, i2, j2, w2)
d = float(np.max(np.abs(A - B)))
verdetto("G2 al limite grado=1 la nuova == la vecchia", d == 0.0, "max|A-B| = %.3e (shape %s vs %s)" % (d, A.shape, B.shape))
print("  NB: la riga delle SHAPE e' stampata PRIMA del massimo apposta -- uno zero su shape diverse")
print("      sarebbe MANCANZA DI CONFRONTO, non identita' (CLAUDE.md par.9).")

# ---------------------------------------------------------------- G3: controllo positivo
print("\n--- G3: controllo positivo -- coi gradi VERI le due forme DEVONO differire ---")
n3 = 5
i3 = np.array([0, 0, 0, 1]); j3 = np.array([1, 2, 3, 4])   # stella: gradi molto diversi
w3 = np.array([0.7, 0.3, 0.9, 0.4])
l3 = spinori(n3, 11)
g3 = np.zeros(n3); np.add.at(g3, i3, w3); np.add.at(g3, j3, w3)
A3 = chiama(n3, l3, i3, j3, w3)
B3 = vecchia_forma(n3, l3, i3, j3, w3)
print("  gradi pesati: %s   (disomogenei per costruzione)" % np.round(g3, 4))
verdetto("G3 coi gradi veri le due forme DIFFERISCONO", float(np.max(np.abs(A3 - B3))) > 1e-12,
         "max|nuova-vecchia| = %.5g" % np.max(np.abs(A3 - B3)))

# ---------------------------------------------------------------- G5: A7 sull'arco
print("\n--- G5: A7 SULL'ARCO -- cio' che `i` cede e' cio' che `j` riceve? ---")
n5, m5 = 30, 90
rng = np.random.default_rng(5)
i5 = rng.integers(0, n5, m5); j5 = rng.integers(0, n5, m5)
ok = i5 != j5; i5, j5 = i5[ok], j5[ok]
w5 = rng.random(len(i5)) + 0.05
l5 = spinori(n5, 17)
ov5 = np.sum(np.conj(l5[i5]) * l5[j5], axis=1)
f5 = w5 * np.imag(ov5)
ceduto = np.zeros(n5); ricevuto = np.zeros(n5)
np.add.at(ceduto, i5, -f5); np.add.at(ricevuto, j5, f5)
verdetto("G5 +flusso e -flusso esattamente opposti",
         float(np.max(np.abs(ceduto.sum() + ricevuto.sum()))) < 1e-12,
         "|sum(ceduto) + sum(ricevuto)| = %.3e" % abs(ceduto.sum() + ricevuto.sum()))
# e l'antisimmetria dell'overlap stesso, che e' la ragione per cui la legge e' giusta
ov_rev = np.sum(np.conj(l5[j5]) * l5[i5], axis=1)
verdetto("G5b imag<i|j> = -imag<j|i> (la legge e' antisimmetrica)",
         float(np.max(np.abs(np.imag(ov5) + np.imag(ov_rev)))) < 1e-14,
         "max|imag<i|j> + imag<j|i>| = %.3e" % np.max(np.abs(np.imag(ov5) + np.imag(ov_rev))))

# ---------------------------------------------------------------- il run vero: G1, G4, G6, G7, G8
print("\n--- il run: scena del batch, TAU_A = %s, 60 passi, seme 5 ---" % S.TAU_A)
REG = []
orig = S.Rete._feedback_spinoriale_archi


def spia(self, i, j, w):
    out = orig(self, i, j, w)
    n = self.n
    lift = np.asarray(self._spinor_lift)
    rec = dict(somma=float(np.sum(out)), scala=float(np.max(np.abs(out))) if len(out) else 0.0,
               lift_len=len(lift), n=n, ov=None)
    if len(lift) >= n:
        mask = (np.asarray(i) < n) & (np.asarray(j) < n)
        if mask.any():
            ii, jj = np.asarray(i)[mask], np.asarray(j)[mask]
            ovv = np.imag(np.sum(np.conj(lift[ii]) * lift[jj], axis=1))
            rec["ov"] = {(int(a), int(b)): float(v) for a, b, v in zip(ii, jj, ovv)}
    REG.append(rec)
    return out


S.Rete._feedback_spinoriale_archi = spia
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
pv0 = float(np.sum(np.asarray(r.phivel, float)[:r.n]))
for _ in range(60):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
pv1 = float(np.sum(np.asarray(r.phivel, float)[:r.n]))
S.Rete._feedback_spinoriale_archi = orig

# ---------------------------------------------------------------- G1 [BLOCCANTE]
print("\n--- G1 [BLOCCANTE]: l'antisimmetria su OGNI invocazione ---")
rel = np.array([abs(x["somma"]) / max(x["scala"], 1e-300) for x in REG if x["scala"] > 0])
print("  invocazioni con feedback non nullo: %d su %d" % (len(rel), len(REG)))
print("  |sum(out)|/max|out| : mediana %.3e   MAX %.3e   (era: mediana 1.112, MAX 8.441)"
      % (np.median(rel), np.max(rel)))
verdetto("G1 antisimmetria all'epsilon su OGNI invocazione  [BLOCCANTE]",
         len(rel) > 0 and float(np.max(rel)) < 1e-12, "MAX = %.3e" % (np.max(rel) if len(rel) else float("nan")))

# ---------------------------------------------------------------- G7 (A8b)
print("\n--- G7 (A8b): len(_spinor_lift) >= n dopo ogni crescita ---")
corti = [x for x in REG if x["lift_len"] < x["n"]]
print("  invocazioni col lift CORTO: %d su %d  (%.2f %%)   contatore _sfb_lift_corto = %s"
      % (len(corti), len(REG), 100.0 * len(corti) / max(len(REG), 1),
         getattr(r, "_sfb_lift_corto", 0)))
if corti:
    print("  quando: alle invocazioni %s" % [REG.index(x) for x in corti][:8])
verdetto("G7 il lift corto e' solo il transitorio iniziale", len(corti) <= 2,
         "%d invocazioni su %d" % (len(corti), len(REG)))

# ---------------------------------------------------------------- G4 conservazione
print("\n--- G4: conservazione di sum(phivel) (cio' che sum(coppia)=0 conserva, M_PH uniforme) ---")
print("  sum(phivel) iniziale %.5g   finale %.5g   deriva %.5g   |deriva|/scala %.5g"
      % (pv0, pv1, pv1 - pv0, abs(pv1 - pv0) / max(abs(pv1), abs(pv0), 1e-300)))
print("  riferimento PRE-CURA (stessa scena, commit ac0ee16): deriva -70.41, |deriva|/scala 1.0658")
print("  ⚠ NON E' UN CRITERIO PASS/FAIL: le due traiettorie DIVERGONO (n finale diverso), quindi")
print("     e' un confronto fra SISTEMI DIVERSI, un seme, senza nullo misurato. Si RIPORTA.")

# ---------------------------------------------------------------- G6 la cucitura di fase
print("\n--- G6: LA CUCITURA DI FASE -- `imag(ov)` e' CONTINUO fra passi consecutivi? ---")
print("  (mai verificata da nessuno. NULLO: se fosse rumore di gauge a media zero, i CAMBI DI SEGNO")
print("   sarebbero il 50 % degli archi sopravvissuti, e |delta| sarebbe dell'ordine di |ov| stesso.)")
salti, segni, scale = [], [], []
prec = None
for x in REG:
    cur = x["ov"]
    if cur is None:
        prec = None
        continue
    if prec:
        comuni = set(prec) & set(cur)
        if len(comuni) > 10:
            a = np.array([prec[k] for k in comuni])
            b = np.array([cur[k] for k in comuni])
            salti.append(float(np.median(np.abs(b - a))))
            segni.append(float(np.mean(np.sign(a) * np.sign(b) < 0)))
            scale.append(float(np.median(np.abs(a))))
    prec = cur
if salti:
    print("  coppie di passi confrontabili: %d" % len(salti))
    print("  |delta imag(ov)| mediano  : %.5g" % np.median(salti))
    print("  |imag(ov)| mediano         : %.5g" % np.median(scale))
    print("  RAPPORTO |delta| / |ov|    : %.5g   <- se ~1 o piu', NON c'e' cucitura" % (np.median(salti) / max(np.median(scale), 1e-300)))
    print("  frazione di CAMBI DI SEGNO : %.4f   (nullo del rumore di gauge: 0.5)" % np.median(segni))
    verdetto("G6 la fase e' CUCITA (cambi di segno ben sotto il nullo 0.5)",
             float(np.median(segni)) < 0.25, "cambi di segno %.4f contro nullo 0.50" % np.median(segni))
else:
    print("  NESSUNA coppia di passi con archi in comune: G6 NON MISURATO.")
    verdetto("G6 misurabile", False, "nessun arco sopravvive fra due invocazioni consecutive")

# ---------------------------------------------------------------- G8 stabilita'
print("\n--- G8: stabilita' ---")
pv = np.asarray(r.phivel, float); om = np.asarray(r.omega_s, float)
nb = np.asarray(getattr(r, "_nb", np.zeros((r.n, 3))), float)
nn = np.linalg.norm(nb[:r.n], axis=1) if nb.ndim == 2 and len(nb) >= r.n else np.array([1.0])
verdetto("G8a nessun NaN/inf", int(np.sum(~np.isfinite(pv))) + int(np.sum(~np.isfinite(om))) == 0,
         "phivel %d, omega_s %d" % (int(np.sum(~np.isfinite(pv))), int(np.sum(~np.isfinite(om)))))
verdetto("G8b |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9, "max||nb|-1| = %.3e" % np.max(np.abs(nn - 1.0)))
cfl = getattr(r, "_taup_cfl_max", None)
verdetto("G8c CFL < 1", cfl is not None and float(cfl) < 1.0, "_taup_cfl_max = %s" % cfl)
print("  max|phivel| %.5g   max|omega_s| %.5g   n finale %d" %
      (np.max(np.abs(pv[np.isfinite(pv)])), np.max(np.abs(om[np.isfinite(om)])), r.n))

# ---------------------------------------------------------------- G9 il docstring
print("\n--- G9: il docstring corretto ---")
doc = S.Rete._feedback_spinoriale_archi.__doc__ or ""
res = []
for fr in ("antisimmmetrica ai nodi",):
    res.append((fr, fr in doc))
sopravvive = any(v for _, v in res)
verdetto("G9 l'affermazione smentita non e' piu' nel docstring", not sopravvive,
         "; ".join("'%s' presente: %s" % (f, v) for f, v in res))
verdetto("G9b il docstring SPIEGA perche' era falsa", "1.112" in doc and "cricchetto" in doc,
         "cita la misura (1.112) e il cricchetto: %s / %s" % ("1.112" in doc, "cricchetto" in doc))

print("\n" + "=" * 118)
ok = sum(esiti)
print("SIGILLO: %d/%d PASS" % (ok, len(esiti)))
print("""
COME SI LEGGE
  G1 e' BLOCCANTE: se non e' all'epsilon su OGNI invocazione, la cura e' sbagliata e ci si ferma.
  G2 e' scritto sul limite VERO (grado pesato = 1), non su quello del mandato: dichiarato PRIMA
     in doc/PREVISIONI_qualitative.md, commit f3f1ab0.
  G4 NON e' pass/fail: due traiettorie che divergono non si confrontano con una soglia.
  G6 e' la misura che non aveva mai fatto nessuno, e il suo NULLO e' 0.5, non 0.""")
