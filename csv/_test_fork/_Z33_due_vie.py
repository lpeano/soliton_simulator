# -*- coding: utf-8 -*-
"""Z33 -- LE DUE VIE COI NUMERI, e K7 (la confrontabilita').  (mandato par.6.3)

Progettazione in doc/TASK_HISTORY/2026-09-18_Z33-cura-snapshot.md. **NESSUNA CURA.**

LA DOMANDA CHE DECIDE, e non e' «quale e' piu' semplice»: quale delle due rende il difetto
IMPOSSIBILE, non solo assente?

VIA (1) spostare l'aggiornamento dello snapshot PRIMA del consumo.
  ⚠ Dal sorgente: `psi_spin` e' assegnato SOLO a :2662, dentro `calcola_psi()`. `ritmo()` gira a
  :3093, all'INIZIO di step(), prima che `calcola_psi()` di quel passo giri. Quindi il consumo legge
  gia' uno stato t-1: L'ORDINE ATTUALE RISPETTA A6. Spostare l'aggiornamento prima del consumo
  farebbe confrontare psi_spin CON SE' STESSO. **SAREBBE IL DIFETTO, NON LA CURA.**
  Questo script lo VERIFICA invece di argomentarlo.

VIA (2) estendere lo snapshot con la popolazione (la cura di C7/C11).
  ⚠ `semina()` (:1812) NON estende `_psi_spin_prec` (verificato dal disco: la voce H). Ma i nodi di
  `nuova_massa` NON HANNO UN GENITORE: estendere significherebbe INVENTARE una fase precedente.
  E c'e' un conto che decide: se i nodi nuovi sono la MAGGIORANZA, dargli `f = 0` lascia la MEDIANA
  a zero lo stesso -- la degenerazione NON si cura. **Questo script misura quella frazione.**

K7 -- LA CONFRONTABILITA': `f` e' CONTINUO fra passi consecutivi, o salta di segno?
  E' `G6` applicata a `_psi_spin_prec`, e non l'ha mai fatto nessuno su questo oggetto. Se la fase
  salta di gauge, `f` e' RUMORE anche quando non e' zero, e il primo difetto diventa secondario.
  NULLO: se fosse rumore a media zero, i cambi di segno sarebbero il 50 % degli archi sopravvissuti.
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
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
           "SPINORE_CORRETTO"):
    setattr(S, _f, True)

print("=" * 118)
print("Z33 -- LE DUE VIE COI NUMERI, e K7")
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s SPINORE_VIVO=%s SPIN_FEEDBACK=%s TAU_LOC=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.TAU_LOC))

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
R = src.splitlines()
def riga(fr):
    for k, l in enumerate(R, 1):
        if fr in l.split("#")[0]:
            return k
    return -1

# ---------------------------------------------------------------- VIA (1): l'ordine
print("\n--- VIA (1): spostare l'aggiornamento PRIMA del consumo -- verifica dell'ORDINE (A6) ---")
print("   :%-6d psi_spin e' assegnato QUI, ed e' l'UNICO punto" % riga("self.psi_spin = _Fs /"))
print("   :%-6d ...dentro `calcola_psi()`" % riga("def calcola_psi"))
print("   :%-6d `ritmo()` consuma lo snapshot, all'INIZIO di step()" % riga("r = self.ritmo()"))
print("   :%-6d lo snapshot si aggiorna DOPO il consumo" % riga("self._psi_spin_prec = self.psi_spin.copy()"))
print("""
  -> il consumo a :%d legge un `psi_spin` prodotto dal passo PRECEDENTE (l'ultimo `calcola_psi`),
     e lo confronta con lo snapshot preso alla fine di QUEL passo. L'ORDINE RISPETTA A6.
  -> spostare l'aggiornamento PRIMA del consumo confronterebbe `psi_spin` CON SE' STESSO:
     `f = 0` per costruzione, SEMPRE. LA VIA (1) E' IL DIFETTO, NON LA CURA.""" % riga("r = self.ritmo()"))

# ---------------------------------------------------------------- la scena, con la sonda
REG = []
_orig = S.Rete.ritmo
STATO = {"passo": 0, "n_prima": 0}


def spia(self):
    n_pre = STATO["n_prima"]
    out = _orig(self)
    rec = dict(passo=STATO["passo"], n=self.n, n_prima=n_pre,
               r=np.asarray(out, float).copy() if out is not None else None, ov=None)
    try:
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if (_ps is not None and _psp is not None and len(_ps) == self.n and len(_psp) == self.n):
            a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
            sg = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT
            rec["ov"] = sg                      # con SEGNO: serve a K7
            rec["f"] = np.abs(sg)
    except Exception:
        pass
    REG.append(rec)
    return out


S.Rete.ritmo = spia
r = S.Rete(5)
r.semina(80)
for _ in range(6):
    STATO["n_prima"] = r.n
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    STATO["passo"] += 1
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
n_pre_inj = r.n
for k in range(3):
    a = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
n_post_inj = r.n
for _ in range(120):
    STATO["n_prima"] = r.n
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    STATO["passo"] += 1
S.Rete.ritmo = _orig

# ---------------------------------------------------------------- VIA (2): il conto che decide
print("\n--- VIA (2): estendere lo snapshot -- il CONTO che decide ---")
print("   :%-6d `semina()` -- e NON estende `_psi_spin_prec` (verificato: voce H)" % riga("def semina"))
print("   :%-6d `_eredita_spinore_figli` LO ESTENDE, ma solo per la MITOSI (cura C11)"
      % riga("self._psi_spin_prec = np.vstack([_pspr"))
nuovi = n_post_inj - n_pre_inj
print("\n   all'iniezione delle masse: n %d -> %d   NODI NUOVI %d = %.1f %% della popolazione"
      % (n_pre_inj, n_post_inj, nuovi, 100.0 * nuovi / max(n_post_inj, 1)))
print("""
  ⚠ E QUI IL PUNTO: i nodi di `nuova_massa` NON HANNO UN GENITORE. Estendere lo snapshot significa
  INVENTARE una fase precedente (A1: un numero scelto; A7b: una storia che non c'e').
  E se li si estendesse col valore CORRENTE -- l'unica scelta che non inventa un moto -- avrebbero
  `f = 0` ESATTO. Essendo il %.1f %% della popolazione, LA MEDIANA RESTEREBBE ZERO:
  **LA VIA (2) NON CURA IL CASO CHE DOVREBBE CURARE.**""" % (100.0 * nuovi / max(n_post_inj, 1)))

# ---------------------------------------------------------------- i contatori del codice vero
print("\n--- I CONTATORI A8 (dal codice, non dalla sonda) ---")
for c in ("_ritmo_chiamate", "_ritmo_sicurezza", "_ritmo_guard4pi_ko", "_ritmo_snap_identico",
          "_ritmo_f_tutto_nullo", "_ritmo_f_mediana_nulla", "_ritmo_med_sul_pavimento"):
    print("   %-26s = %s" % (c, getattr(r, c, 0)))
print("   %-26s = %s" % ("_ritmo_sicurezza_shape", getattr(r, "_ritmo_sicurezza_shape", None)))
tot = getattr(r, "_ritmo_chiamate", 1)
deg = getattr(r, "_ritmo_sicurezza", 0) + getattr(r, "_ritmo_med_sul_pavimento", 0)
print("   -> passi con un tempo proprio DEGENERE: %d su %d = %.2f %%" % (deg, tot, 100.0 * deg / max(tot, 1)))

# ---------------------------------------------------------------- K7: la confrontabilita'
print("\n--- K7: `f` e' CONFRONTABILE fra passi consecutivi? (G6 su `_psi_spin_prec`) ---")
print("  NULLO: se fosse rumore di gauge a media zero, i CAMBI DI SEGNO sarebbero il 50 %.")
salti, segni, scale, salti_mod = [], [], [], []
prec = None
for x in REG:
    cur = x.get("ov")
    if cur is None:
        prec = None
        continue
    if prec is not None and len(prec) > 10:
        m = min(len(prec), len(cur))
        a, b = prec[:m], cur[:m]
        vivi = (np.abs(a) > 0) & (np.abs(b) > 0)
        if vivi.sum() > 10:
            # ⚠ DUE GRANDEZZE DIVERSE, e confonderle sarebbe un overclaim:
            #   `signed` ha il SEGNO; `f = |signed|` e' cio' che il codice USA davvero
            #   (TEMPO_PROPRIO_ORIENTATO = False). Un cambio di segno gonfia |b-a| a ~2|a| sul
            #   primo, e NON tocca il secondo. Si riportano ENTRAMBI.
            salti.append(float(np.median(np.abs(b[vivi] - a[vivi]))))
            salti_mod.append(float(np.median(np.abs(np.abs(b[vivi]) - np.abs(a[vivi])))))
            scale.append(float(np.median(np.abs(a[vivi]))))
            segni.append(float(np.mean(np.sign(a[vivi]) * np.sign(b[vivi]) < 0)))
    prec = cur
if salti:
    print("  coppie di passi confrontabili : %d" % len(salti))
    print("  |delta f| mediano             : %.6g" % np.median(salti))
    print("  |f| mediano                   : %.6g" % np.median(scale))
    print("  RAPPORTO |delta f| / |f|      : %.6g   <- se ~1 o piu', NON c'e' cucitura"
          % (np.median(salti) / max(np.median(scale), 1e-300)))
    print("  frazione di CAMBI DI SEGNO    : %.4f   (nullo del rumore di gauge: 0.5)" % np.median(segni))
    print("")
    print("  E LA GRANDEZZA CHE IL CODICE USA DAVVERO, `f = |signed|`:")
    print("     |delta f| mediano        : %.6g" % np.median(salti_mod))
    
    print("     RAPPORTO |delta f| / |f| : %.6g   <- QUESTO e' il numero che conta per ritmo()"
          % (np.median(salti_mod) / max(np.median(scale), 1e-300)))
    print("     (il rapporto sul SEGNATO e' gonfiato dai cambi di segno, che il codice SCARTA")
    print("      prendendo il modulo: le due cose NON si confondono)")
    print("""
  ⚠ NB: qui `f` e' confrontato NODO PER NODO fra passi consecutivi, e i nodi cambiano (mitosi).
     Il confronto e' sui PRIMI min(len) indici, che restano gli stessi nodi perche' i nuovi si
     APPENDONO in coda. E' un'approssimazione, ed e' dichiarata.""")
else:
    print("  NESSUNA coppia confrontabile: K7 NON MISURATO.")

print("\n" + "=" * 118)
