# -*- coding: utf-8 -*-
"""LA MISURA CHE DECIDE FRA (A) NORMALIZZAZIONE e (B) INERZIA MASCHERATA. (mandato par.1)

⚠ IL MANDATO CHIEDE `L_tot = sum(I*|omega|)`. **NON E' LO STRUMENTO GIUSTO PER QUESTO TERMINE**, e
la ragione si verifica dal sorgente prima di misurare (e questo script la stampa):

  - il feedback e' chiamato in UN SOLO punto (`:3113`) e finisce in `coppia`;
  - `coppia` va a `:3195/3197`  ->  `delta_phivel = dt_n_s * (coppia - ...) / M_PH`  ->  `phivel`;
  - **`M_PH = 1.0` e' una COSTANTE GLOBALE** (`:206`), non una massa per nodo;
  - l'UNICA divisione per l'inerzia del file e' `:2283`, dentro `_passo_spinoriale`, e divide
    **`correzione`** (un 3-vettore), non `coppia`. **`omega_s` non vede mai il feedback.**

DUE CONSEGUENZE, ed e' per questo che lo script misura ALTRO:

 (1) **La premessa della lettura (B) NON REGGE.** (B) dice: *«e' un'inerzia mascherata, l'inerzia
     vera e' gia' a valle, dividere due volte e' un difetto»*. **A valle non c'e' nessuna inerzia
     per nodo: c'e' `M_PH = 1.0`.** Non c'e' nessuna doppia divisione da togliere.

 (2) **In QUESTO settore `sum(out) = 0` E' la legge di conservazione**, non un criterio di forma.
     Il mandato avverte giustamente che `sum(coppia)` non e' fisica *quando la massa e' diversa per
     nodo* — `sum(I*omega)` con `I` variabile. **Ma qui la massa e' UNIFORME:**
         d/dt sum(phivel) = sum(coppia) / M_PH
     quindi **`sum(coppia) = 0` <=> `sum(phivel)` si conserva**, esattamente. **L'avvertenza del
     mandato vale per il settore dello SPIN, non per questo.**

QUINDI SI MISURA: la DERIVA di `sum(phivel)` (la grandezza conservata di QUESTO settore), il suo
salto attraverso le MITOSI, e `sum(out)`. `L_tot` si riporta come SECONDARIO, per vedere se la
variante rompe altro -- non come criterio.

TRE VARIANTI, a parita' di tutto il resto:
  (0) ATTUALE   out[i] -= f/g_i ; out[j] += f/g_j      denominatori DIVERSI
  (1) SENZA     out[i] -= f     ; out[j] += f          nessun denominatore      <- la lettura (B)
  (2) SIMM      out[i] -= f/g_ij; out[j] += f/g_ij     g_ij = sqrt(g_i*g_j)     <- la lettura (A)

⚠ LA VARIANTE (2) NON E' LA CURA PROPOSTA. `sqrt(g_i*g_j)` e' UNA SCELTA (A1), messa qui SOLO per
  vedere se la SIMMETRIZZAZIONE in se' cambia il quadro. Quale denominatore simmetrico vada usato
  e' una domanda successiva, e va DERIVATA.

Nessuna legge del file e' toccata: le varianti sostituiscono il metodo per la durata della misura.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio                                    # PRESIDIO: encoding + timbro git (Z22)
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
print("DENOMINATORE DEL FEEDBACK: (A) normalizzazione o (B) inerzia mascherata?   [TAU_A=%s, %d passi]"
      % (S.TAU_A, PASSI))
print("=" * 118)

# ------------------------------------------------------- la verifica strutturale, PRIMA di misurare
src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
righe = src.splitlines()
def trova(fr):
    for k, l in enumerate(righe, 1):
        if fr in l.split("#")[0]:
            return k
    return -1

print("\n--- LA CATENA DEL FEEDBACK, dal sorgente (decide QUALE grandezza si conserva) ---")
print("   :%-6d chiamata unica      _fb = self._feedback_spinoriale_archi(i, j, w)" % trova("_fb = self._feedback_spinoriale_archi"))
print("   :%-6d applicazione        coppia += _fb" % trova("coppia += _fb"))
print("   :%-6d integrazione        delta_phivel = ... / M_PH" % trova("delta_phivel = dt_n_s * (coppia - G_PH"))
print("   :%-6d M_PH = %-13s <- COSTANTE GLOBALE, non una massa per nodo" % (trova("M_PH     ="), S.M_PH))
print("   :%-6d l'unica /inerzia    omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - ...)"
      % trova("omega_new = omega_src + dtn_c"))
print("""
  -> il feedback agisce su `phivel` (settore FASE, massa UNIFORME M_PH).
  -> `omega_s` e `inerzia` (settore SPIN) NON lo vedono: `/inerzia` divide `correzione`, non `coppia`.
  -> (B) «l'inerzia vera e' gia' a valle» NON REGGE: a valle c'e' una COSTANTE.
  -> e in un settore a massa uniforme, `sum(coppia) = 0`  <=>  `sum(phivel)` si conserva.""")

# ------------------------------------------------------- le tre varianti
orig = S.Rete._feedback_spinoriale_archi
DIAG = {"somme": [], "scale": []}


def fabbrica(modo):
    def metodo(self, i, j, w):
        out = np.zeros(self.n)
        self._spin_feedback_last = 0.0
        self._sfb_chiamate = getattr(self, "_sfb_chiamate", 0) + 1
        if not S.SPIN_FEEDBACK:
            return out
        if len(self._spinor_lift) < self.n:
            self._sfb_lift_corto = getattr(self, "_sfb_lift_corto", 0) + 1
            return out
        mask = (i < self.n) & (j < self.n)
        if not mask.any():
            return out
        self._sfb_applicato = getattr(self, "_sfb_applicato", 0) + 1
        ii, jj, ww = i[mask], j[mask], w[mask]
        ov = np.sum(np.conj(self._spinor_lift[ii]) * self._spinor_lift[jj], axis=1)
        flusso = ww * np.imag(ov)
        grado = np.zeros(self.n)
        np.add.at(grado, ii, ww); np.add.at(grado, jj, ww)
        if modo == "attuale":
            np.add.at(out, ii, -flusso / np.maximum(grado[ii], 1e-9))
            np.add.at(out, jj, flusso / np.maximum(grado[jj], 1e-9))
        elif modo == "senza":
            np.add.at(out, ii, -flusso)
            np.add.at(out, jj, flusso)
        elif modo == "simm":
            g = np.sqrt(np.maximum(grado[ii], 1e-9) * np.maximum(grado[jj], 1e-9))
            np.add.at(out, ii, -flusso / g)
            np.add.at(out, jj, flusso / g)
        DIAG["somme"].append(float(np.sum(out)))
        DIAG["scale"].append(float(np.max(np.abs(out))) if len(out) else 0.0)
        self._spin_feedback_last = float(np.mean(np.abs(flusso))) if len(flusso) else 0.0
        return out
    return metodo


def gira(modo):
    DIAG["somme"].clear(); DIAG["scale"].clear()
    S.Rete._feedback_spinoriale_archi = fabbrica(modo)
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
    tr = []
    for kk in range(PASSI):
        n0 = r.n
        pv0 = float(np.sum(np.asarray(r.phivel, float)[:n0]))
        S.scuoti_vuoto(r); r.step()
        n1 = r.n
        pv1 = float(np.sum(np.asarray(r.phivel, float)[:n1]))
        r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
        n2 = r.n
        pv2 = float(np.sum(np.asarray(r.phivel, float)[:n2]))
        om = np.asarray(r.omega_s, float)
        # NON si calcola `L_tot = sum(I*|omega|)`: il simulatore NON espone l'array
        # dell'inerzia (e' una LOCALE di `_passo_spinoriale`; `L_tot` nasce dalle colonne
        # CSV della campagna). Metterci `I = 1` darebbe un `sum(|omega|)` TRAVESTITO da
        # L_tot: il fallback silenzioso che P5 vieta. Si riporta col PROPRIO nome.
        L = float(np.sum(np.linalg.norm(om[:n2], axis=1))) if om.ndim == 2 else float("nan")
        tr.append(dict(passo=kk, n=n2, nati=n2 - n1,
                       pv_pre=pv0, pv_post=pv1, pv_fine=pv2,
                       d_step=pv1 - pv0, d_mit=pv2 - pv1, L=L))
    return r, tr


ris = {}
for modo in ("attuale", "senza", "simm"):
    try:
        ris[modo] = gira(modo)
    except Exception as e:
        ris[modo] = (None, "ERRORE: %s: %s" % (type(e).__name__, e))
        print("\n  !! la variante '%s' e' ESPLOSA: %s" % (modo, e))
    finally:
        S.Rete._feedback_spinoriale_archi = orig
    if isinstance(ris[modo][1], list):
        ris[modo] = (ris[modo][0], ris[modo][1], list(DIAG["somme"]), list(DIAG["scale"]))

# ------------------------------------------------------- G1 in anticipo: |sum(out)|/max|out|
print("\n--- (G1) |sum(out)| / max|out| -- l'antisimmetria, per variante ---")
print("  %-10s %-16s %-16s %-16s" % ("variante", "mediana", "MAX", "invocazioni"))
for modo in ("attuale", "senza", "simm"):
    v = ris[modo]
    if len(v) < 4:
        print("  %-10s ESPLOSA" % modo); continue
    somme, scale = v[2], v[3]
    rel = [abs(s) / max(sc, 1e-300) for s, sc in zip(somme, scale) if sc > 0]
    print("  %-10s %-16.3e %-16.3e %-16d" % (modo, np.median(rel), np.max(rel), len(rel)))
print("  (l'epsilon macchina e' ~1e-16; 'attuale' misurato prima: mediana 1.112, MAX 8.441)")

# ------------------------------------------------------- il criterio DI QUESTO SETTORE
print("\n--- IL CRITERIO FISICO DI QUESTO SETTORE: la deriva di sum(phivel) ---")
print("  (massa UNIFORME M_PH -> d/dt sum(phivel) = sum(coppia)/M_PH: se sum(out)=0, si conserva)")
print("  %-10s %-14s %-14s %-14s %-14s %-9s" %
      ("variante", "sum|d_step|", "sum|d_mit|", "deriva TOT", "|deriva|/scala", "n finale"))
for modo in ("attuale", "senza", "simm"):
    v = ris[modo]
    if len(v) < 4:
        print("  %-10s ESPLOSA" % modo); continue
    tr = v[1]
    ds = sum(abs(x["d_step"]) for x in tr)
    dm = sum(abs(x["d_mit"]) for x in tr)
    tot = tr[-1]["pv_fine"] - tr[0]["pv_pre"]
    scala = max(abs(tr[-1]["pv_fine"]), abs(tr[0]["pv_pre"]), 1e-300)
    print("  %-10s %-14.5g %-14.5g %-14.5g %-14.5g %-9d"
          % (modo, ds, dm, tot, abs(tot) / scala, tr[-1]["n"]))
print("""  NB: `d_mit` NON e' un difetto: la mitosi AGGIUNGE nodi, e un nodo nuovo porta il suo phivel.
  Va letto come TERMINE DI SORGENTE noto, non come violazione. Conta il confronto FRA varianti.""")

# ------------------------------------------------------- L_tot, SECONDARIO
print(chr(10) + "--- sum(|omega_s|) -- SECONDARIO, e NON e' L_tot: manca l'inerzia ---")
print("  %-10s %-16s %-16s %-16s" % ("variante", "al passo 0", "finale", "rapporto"))
for modo in ("attuale", "senza", "simm"):
    v = ris[modo]
    if len(v) < 4:
        print("  %-10s ESPLOSA" % modo); continue
    tr = v[1]
    L0, L1 = tr[0]["L"], tr[-1]["L"]
    print("  %-10s %-16.5g %-16.5g %-16.5g" % (modo, L0, L1, (L1 / L0) if L0 else float("nan")))

# ------------------------------------------------------- stabilita'
print("\n--- stabilita' (nessuna variante deve esplodere) ---")
for modo in ("attuale", "senza", "simm"):
    v = ris[modo]
    if len(v) < 4 or v[0] is None:
        print("  %-10s ESPLOSA" % modo); continue
    r = v[0]
    pv = np.asarray(r.phivel, float); om = np.asarray(r.omega_s, float)
    print("  %-10s NaN/inf: phivel %d  omega_s %d   max|phivel| %.5g   max|omega_s| %.5g"
          % (modo, int(np.sum(~np.isfinite(pv))), int(np.sum(~np.isfinite(om))),
             float(np.max(np.abs(pv[np.isfinite(pv)]))) if np.any(np.isfinite(pv)) else float("nan"),
             float(np.max(np.abs(om[np.isfinite(om)]))) if np.any(np.isfinite(om)) else float("nan")))

print("\n" + "=" * 118)
print("""COME SI LEGGE -- le letture erano fissate PRIMA
  'senza' conserva MEGLIO di 'attuale'   -> compatibile con (B). MA la premessa di (B) e' gia'
                                            caduta dal sorgente: a valle non c'e' inerzia per nodo.
  'simm'  conserva e 'senza' no          -> (A): il difetto e' l'ASIMMETRIA, non la divisione.
  'senza' e 'simm' conservano UGUALE     -> la misura NON distingue: e allora si dice, e ci si ferma.
E in ogni caso `sum(out)` (G1) e' una VERIFICA ALGEBRICA, non statistica: li' non c'e' da scegliere.""")
