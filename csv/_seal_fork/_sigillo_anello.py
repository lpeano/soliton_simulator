# -*- coding: utf-8 -*-
"""SIGILLO P0-P10 -- la cura dell'ANELLO ISTANTANEO in `ritmo()` (mandato par.3).

Progettazione: doc/TASK_HISTORY/2026-09-18_anello-istantaneo.md (fd198ba)
Previsioni scritte PRIMA: doc/PREVISIONI_qualitative.md (631ff15)

P1 e' il BLOCCANTE, e il modo in cui e' costruito va dichiarato:
  il limite e' `med_prec = med_corrente`. Il sigillo avvolge `ritmo()` del blob NUOVO con un wrapper
  che RICOSTRUISCE `f` con la stessa legge e INIETTA `median(|f|)` in `_med_f_prec` prima di
  chiamare. Se la ricostruzione fosse sbagliata, P1 FALLISCE: non passa in silenzio.
  Il wrapper sta QUI, mai nel simulatore.
Il blob VECCHIO si estrae con `git cat-file -p` IN BINARIO (mai `git hash-object`: trappola CRLF C18).
ASCII PURO.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import hashlib
import importlib.util

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(QUI, "..", ".."))
os.chdir(ROOT)

BLOB_RIF = "f8f46683"   # sha1 dei BYTE GREZZI del blob PRE-CURA. ANCORATO, non "HEAD".
PASSI = 120
SEME = 5
ESITI = []


def ok(nome, cond, det=""):
    ESITI.append((nome, bool(cond)))
    print("  [%s] %-6s %s" % ("PASS" if cond else "FAIL", nome, det))


def sha_byte(p):
    b = open(p, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def carica(path, nome):
    spec = importlib.util.spec_from_file_location(nome, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    _argv = sys.argv
    sys.argv = ["soliton_simulator.py"]
    try:
        spec.loader.exec_module(m)
    finally:
        sys.argv = _argv
    for f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
              "SPINORE_CORRETTO"):
        setattr(m, f, True)
    return m


print("=" * 118)
print("SIGILLO ANELLO ISTANTANEO -- P0..P10")
print("=" * 118)

# ------------------------------------------------------------------ P0
vecchio = os.path.join(QUI, "_old_sim_pre_anello.py")
with open(vecchio, "wb") as fh:
    # [CORREZIONE 2026-09-18, dopo il FAIL committato in c818208] SI ESTRAE PER SHA DEL BLOB, MAI
    # PER `HEAD:`. `HEAD` si sposta col lavoro: al primo commit della cura il "vecchio" e' diventato
    # il NUOVO, e il sigillo ha confrontato il codice curato CON SE STESSO (P2 dava
    # `max|A-B| = 0.000e+00` con shape UGUALI: identita' perfetta per la ragione sbagliata).
    # E' la stessa ragione per cui il gate e' ancorato al BLOB e non al commit (par.2.6): un
    # riferimento che si muove non e' un riferimento.
    fh.write(subprocess.check_output(["git", "cat-file", "-p", BLOB_RIF]))
sv = sha_byte(vecchio); sn = sha_byte(os.path.join(ROOT, "soliton_simulator.py"))
print("\n--- P0 -- i due blob (sha1 dei BYTE GREZZI, non git hash-object) ---")
ok("P0", sv[:8] == BLOB_RIF, "vecchio %s (atteso %s)   nuovo %s" % (sv[:8], BLOB_RIF, sn[:8]))

VEC = carica(vecchio, "_sim_vecchio")
NUO = carica(os.path.join(ROOT, "soliton_simulator.py"), "_sim_nuovo")
print("  TAU_A = %s   TAU_LOC = %s   DT = %s   (letti dal modulo, non dal comando: P6)"
      % (NUO.TAU_A, NUO.TAU_LOC, NUO.DT))


def costruisci(M):
    r = M.Rete(SEME)
    r.semina(80)
    for _ in range(6):
        M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    Nc = M.N_CRITICO() if callable(getattr(M, "N_CRITICO", None)) else 200
    for k in range(3):
        a = 2 * np.pi * k / 3
        r.nuova_massa(int(Nc * 0.6), raggio=M._size_video(k, 0.8),
                      centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
    r.aggiorna_pesi_concorrenza()
    return r


def gira(M, passi=PASSI, campiona=None):
    r = costruisci(M)
    snap = {}
    for k in range(passi):
        M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
        if campiona and (k + 1) in campiona:
            snap[k + 1] = float(np.median(np.asarray(r.eta[:r.n], float))) if len(getattr(r, "eta", [])) else float("nan")
    return r, snap


def confronta(a, b, eti):
    """LA RIGA DELLE SHAPE PRIMA DI TUTTO: `max|A-B| = 0` puo' significare NESSUN CONFRONTO."""
    campi = ["psi", "phivel", "eta", "d", "d0", "omega_s", "_nb"]
    print("    %-12s n: %d contro %d" % (eti, a.n, b.n))
    diverse = 0; mx = 0.0; conf = 0
    for c in campi:
        A = np.asarray(getattr(a, c, np.zeros(0))); B = np.asarray(getattr(b, c, np.zeros(0)))
        if A.shape != B.shape:
            diverse += 1
            print("      %-9s SHAPE DIVERSE %s contro %s  <- NESSUN CONFRONTO" % (c, A.shape, B.shape))
            continue
        conf += 1
        d = float(np.max(np.abs(A - B))) if A.size else 0.0
        mx = max(mx, d)
        print("      %-9s shape %-12s max|A-B| = %.3e" % (c, str(A.shape), d))
    return mx, diverse, conf


# ------------------------------------------------------------------ P1
print("\n--- P1 [BLOCCANTE] -- riduzione al limite: `med_prec := med_corrente` -> BYTE-IDENTICO ---")
_rit_nuovo = NUO.Rete.ritmo


def _f_ricostruito(self, M):
    """la STESSA legge di `ritmo()`, righe per righe. Se sbaglio, P1 FALLISCE: non passa in silenzio."""
    if self._psi_prec is None or len(self._psi_prec) != self.n:
        return None
    a = np.angle(self.psi) - np.angle(self._psi_prec)
    signed = ((a + np.pi) % (2 * np.pi) - np.pi) / M.DT
    _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
    if (M.CAMPO_SPINORIALE and _ps is not None and _psp is not None
            and len(_ps) == self.n and len(_psp) == self.n):
        a = np.angle(np.asarray(_ps)[:, 0]) - np.angle(np.asarray(_psp)[:, 0])
        signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / M.DT
    return signed if M.TEMPO_PROPRIO_ORIENTATO else np.abs(signed)


def ritmo_forzato(self):
    if NUO.TAU_LOC != 0.0 and not (NUO.TEMPO_SEGNO and len(getattr(self, "tw", []))):
        f = _f_ricostruito(self, NUO)
        if f is not None:
            self._med_f_prec = max(float(np.median(np.abs(f))), 1e-9)
    return _rit_nuovo(self)


NUO.Rete.ritmo = ritmo_forzato
rv, _ = gira(VEC)
rn, _ = gira(NUO)
NUO.Rete.ritmo = _rit_nuovo
mx, div, conf = confronta(rv, rn, "P1")
ok("P1", div == 0 and conf >= 5 and mx == 0.0,
   "shape divergenti %d, array confrontati %d, max|A-B| = %.3e" % (div, conf, mx))

# ------------------------------------------------------------------ P2
print("\n--- P2 -- controllo positivo: coi valori VERI DEVE differire ---")
rn2, snap = gira(NUO, campiona={1, 60, 120})
mx2, div2, conf2 = confronta(rv, rn2, "P2")
ok("P2", (div2 > 0) or (mx2 > 0.0), "shape divergenti %d, max|A-B| = %.3e (0 con shape uguali = FAIL)" % (div2, mx2))

# ------------------------------------------------------------------ P3 / P4 / P5 / P6 / P7
print("\n--- P3 -- A3 SI SCIOGLIE: `median(x)` non vale piu' 1 per identita' ---")
MX = []
_rit2 = NUO.Rete.ritmo


def spia(self):
    out = _rit2(self)
    try:
        f = _f_ricostruito(self, NUO)
        mp = getattr(self, "_med_f_prec", None)
        if f is not None and mp:
            MX.append(float(np.median(np.abs(f)) / mp))
    except Exception:
        pass
    return out


NUO.Rete.ritmo = spia
rn3, _ = gira(NUO)
NUO.Rete.ritmo = _rit2
MXa = np.array([v for v in MX if np.isfinite(v)])
scarto = float(np.max(np.abs(MXa - 1.0))) if MXa.size else 0.0
print("    median(x) su %d passi: p05 %.6g  mediana %.6g  p95 %.6g   max|med-1| = %.6g"
      % (MXa.size, np.percentile(MXa, 5), np.median(MXa), np.percentile(MXa, 95), scarto))
ok("P3", MXa.size > 50 and scarto > 1e-6, "il punto fisso ESATTO (0.000e+00) e' sciolto" if scarto > 1e-6
   else "median(x) vale ANCORA 1: l'anello NON e' rotto")

print("\n--- P4 -- A6: `med` viene dallo STATO PRECEDENTE ---")
src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8").read()
scrive_in_ritmo = "self._med_f_prec =" in src.split("def ritmo(")[1].split("def _passo_spinoriale")[0]
promuove_in_step = "self._med_f_prec = _mu" in src
ok("P4", (not scrive_in_ritmo) and promuove_in_step,
   "ritmo() scrive _med_f_prec: %s (deve essere False)   step() promuove: %s" % (scrive_in_ritmo, promuove_in_step))

print("\n--- P5 -- A8: i contatori ---")
for c in ("_ritmo_chiamate", "_ritmo_med_assente", "_ritmo_med_identico", "_ritmo_med_non_promosso",
          "_ritmo_f_tutto_nullo", "_ritmo_med_sul_pavimento", "_ritmo_sicurezza"):
    print("    %-28s %s" % (c, getattr(rn2, c, 0)))
ch = max(getattr(rn2, "_ritmo_chiamate", 1), 1)
ass = getattr(rn2, "_ritmo_med_assente", 0)
ok("P5", ass <= 2 and (ass / ch) < 0.05,
   "`med` assente %d su %d chiamate = %.2f %% (atteso ~0 a regime: solo l'avvio)" % (ass, ch, 100.0 * ass / ch))

print("\n--- P6 -- `Z33` come conseguenza: il gauge degenere ---")
nul = getattr(rn2, "_ritmo_f_tutto_nullo", 0); pav = getattr(rn2, "_ritmo_med_sul_pavimento", 0)
npr = getattr(rn2, "_ritmo_med_non_promosso", 0)
print("    f tutto nullo %d   med sul pavimento %d   med NON promosso %d   su %d chiamate"
      % (nul, pav, npr, ch))
print("    (prima della cura: 1 passo su 31 = 3.2 %%. `med` NON promosso e' il presidio che impedisce")
print("     alla degenerazione di ROVESCIARSI in saturazione al passo dopo.)")
ok("P6", npr >= pav - 1, "ogni `med` sul pavimento NON e' stato promosso (%d >= %d - 1)" % (npr, pav))

print("\n--- P7 -- IL GAUGE NON E' CAMBIATO: `r_unit` e il codominio di `r` ---")
RR = []
_rit3 = NUO.Rete.ritmo


def spia_r(self):
    out = _rit3(self)
    if out is not None and np.ndim(out):
        RR.append(np.asarray(out, float).copy())
    return out


NUO.Rete.ritmo = spia_r
rn4, _ = gira(NUO)
NUO.Rete.ritmo = _rit3
allr = np.concatenate(RR[-30:]) if RR else np.zeros(1)
r_unit_src = "r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6" in src
print("    r: min %.6g  p05 %.6g  MEDIANA %.6g  p95 %.6g  max %.6g   (prima: p05 0.1108, med 1, max 1.41419)"
      % (allr.min(), np.percentile(allr, 5), np.median(allr), np.percentile(allr, 95), allr.max()))
ok("P7", r_unit_src and allr.max() <= 1.4142136 + 1e-6 and allr.min() > 0,
   "`r_unit` invariato nel sorgente: %s ; tetto %.7f <= sqrt(2)" % (r_unit_src, allr.max()))

print("\n--- P8 -- `Z9`: `ramp = min(1, eta/TAU_A)` mediano ai passi 1 / 60 / 120 ---")
ta = float(NUO.TAU_A)
for k in (1, 60, 120):
    e = snap.get(k, float("nan"))
    print("    passo %-4d eta mediano %.6g   ramp %.6g" % (k, e, min(1.0, e / ta) if e == e else float("nan")))
print("    riferimento del mandato: 0.0002 / 0.0102 / 0.0212  (TAU_A = 50, scena STORICA).")
print("    ⚠ QUI TAU_A = %s: i due non sono confrontabili direttamente, e NON li confronto." % ta)
ok("P8", all(snap.get(k, float("nan")) == snap.get(k, float("nan")) for k in (1, 60, 120)),
   "riportato, NON confrontato con numeri di un'altra scena (A3c)")

print("\n--- P9 -- stabilita' ---")
fin = np.all(np.isfinite(rn2.psi[:rn2.n])) and np.all(np.isfinite(np.asarray(rn2.d)))
rpos = bool(allr.min() > 0)
nbn = np.asarray(getattr(rn2, "_nb", np.zeros((1, 3))), float)
nbok = bool(np.max(np.abs(np.linalg.norm(nbn[:rn2.n], axis=1) - 1.0)) < 1e-6) if nbn.size else True
ok("P9", fin and rpos and nbok, "no NaN/inf: %s   r > 0: %s   ||nb| - 1| < 1e-6: %s" % (fin, rpos, nbok))

print("\n" + "=" * 118)
p = sum(1 for _, v in ESITI if v)
print("ESITO: %d/%d PASS" % (p, len(ESITI)))
for n, v in ESITI:
    if not v:
        print("   FAIL: %s" % n)
print("=" * 118)
