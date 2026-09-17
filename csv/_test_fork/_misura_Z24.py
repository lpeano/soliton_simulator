# -*- coding: utf-8 -*-
"""Z24 — I TRE PUNTI COLLO STESSO SCHEMA: sono DAVVERO cricchetti? (mandato par.1)

«Dimostrato in FORMA» non basta: Z24 dice che nessuno li ha MISURATI. E il giro appena chiuso ha
mostrato quanto conti la differenza -- la forma sembrava antisimmetrica, la misura diceva 1.112.

⚠ LE RIGHE DEL MANDATO (`:2082`, `:2294`, `:3154`) SONO PRE-CURA E SONO SHIFTATE: il docstring
  aggiunto a `_feedback_spinoriale_archi` ha spostato tutto cio' che sta dopo. Trovati per NOME
  (CLAUDE.md par.0), sul blob attuale valgono `:2116`, `:2328`, `:3188`.

⚠ E I TRE NON SONO LO STESSO SCHEMA. Verificato dal sorgente PRIMA di misurare, come il mandato
  chiede di non assumere:

  PUNTO 1 -- `B` (`:2114-2116`)
      np.add.at(B, ii, contrib_j * refl)      <-- ENTRAMBI col segno PIU'
      np.add.at(B, jj, contrib_i * refl)
      B = B / np.maximum(deg[:, None], 1e-9)
    NON e' uno scambio: e' una MEDIA PESATA dei Bloch dei vicini, cioe' un CAMPO LOCALE.
    `sum(B)` non ha ragione di essere zero, e non e' un difetto che non lo sia.
    L'oggetto di cui `doc/MAPPA_accoppiamenti_spin.md` parla NON e' `B`: e' la COPPIA derivata
    `correzione = cross(B, nb)` (`:2289`), e li' la domanda e' legittima.
    -> si misura `sum(correzione)`, NON `sum(B)`.

  PUNTO 2 -- `_otw` (`:2326-2328`)
      np.add.at(_otw, ii, _axis * _twh[:, None])   <-- ENTRAMBI col segno PIU'
      np.add.at(_otw, jj, _axis * _twh[:, None])
    Come sopra: NON e' uno scambio, e per di piu' il termine e' aggiunto DIRETTAMENTE a `omega_new`
    (`:2328`), NON e' una coppia -- e' un incremento di velocita' angolare. CLAUDE.md lo dice gia':
    «unico fra i termini del blocco, `_otw` NON e' diviso per l'inerzia».
    E' sotto `TW_SPINORE`, che e' **False di default per decisione di Luca**: DIFETTO LATENTE.

  PUNTO 3 -- `twist_nodo` (`:3186-3188`)
      np.add.at(twist_nodo, i, twn); np.add.at(twist_nodo, j, -twn)   <-- +twn / -twn: SCAMBIO
      coppia = coppia + twist_nodo[:self.n] / np.maximum(grado[:self.n], 1.0)
    **QUESTO E' ESATTAMENTE LO SCHEMA DI Z25**: accumulo antisimmetrico, poi divisione per il grado
    DEL NODO. E per il referto `a15716c` «dentro» e «dopo» sono la STESSA COSA, perche' `grado[k]`
    si raccoglie fuori dalla somma.
    **ED E' ATTIVO: `FRAME_DRAG = True` di default** (`:685`) -- gira in OGNI run mai fatto.
    E finisce in `coppia` -> `delta_phivel / M_PH`, con `M_PH = 1.0` UNIFORME: quindi qui
    `sum = 0` E' la conservazione, esattamente come nel caso gia' curato.

QUINDI SI MISURA, per ciascuno, `|sum(.)| / max|.|` contro l'epsilon macchina (~1e-16), su OGNI
invocazione -- ma sull'oggetto GIUSTO di quel punto, non su quello che l'analogia suggerirebbe.
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
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(S, _f, True)
S.TAU_A = float(_ARGV[_ARGV.index("--tau-a") + 1]) if "--tau-a" in _ARGV else 2.0
TW = "--tw" in _ARGV          # per CARATTERIZZARE il punto 2, che di default e' spento
S.TW_SPINORE = bool(TW)

print("=" * 118)
print("Z24 -- i tre punti collo 'stesso schema' sono davvero cricchetti?   [TW_SPINORE=%s]" % TW)
print("=" * 118)

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
righe = src.splitlines()


def riga(fr):
    for k, l in enumerate(righe, 1):
        if fr in l.split("#")[0]:
            return k
    return -1


print("\n--- LE RIGHE, sul blob ATTUALE (quelle del mandato sono PRE-CURA e shiftate) ---")
for fr, eti in (("B = B / np.maximum(deg", "punto 1 -- B"),
                ("_otw / np.maximum(_degt", "punto 2 -- _otw"),
                ("twist_nodo[:self.n] / np.maximum(grado", "punto 3 -- twist_nodo")):
    print("   :%-6d %-22s %s" % (riga(fr), eti, fr))
print("   :%-6d %-22s %s" % (riga("FRAME_DRAG = True"), "il GATE del punto 3", "FRAME_DRAG = True  <- ATTIVO DI DEFAULT"))
print("   :%-6d %-22s %s" % (riga("TW_SPINORE = False"), "il GATE del punto 2", "TW_SPINORE = False <- LATENTE"))

# ---------------------------------------------------------------- le sonde
REG = {"correzione": [], "otw": [], "twist": [], "B": []}
orig_ps = S.Rete._passo_spinoriale


def rel(v):
    """|sum| / max|.| su un array (n,) o (n,3): per i vettori si usa la NORMA della somma."""
    v = np.asarray(v, float)
    if v.ndim == 2:
        s = float(np.linalg.norm(v.sum(axis=0)))
        m = float(np.max(np.linalg.norm(v, axis=1))) if len(v) else 0.0
    else:
        s = abs(float(v.sum()))
        m = float(np.max(np.abs(v))) if len(v) else 0.0
    return (s / m) if m > 0 else None


# Punto 1 e 2: vivono dentro _passo_spinoriale, e sono LOCALI. Si ricostruiscono con le STESSE
# espressioni del sorgente, sugli STESSI ingressi, subito prima di delegare.
def spia_ps(self, i, j, w, dt_n, *a, **k):
    n = self.n
    try:
        _nbv = getattr(self, "_nb", None)
        if _nbv is None or len(_nbv) < n:
            REG.setdefault("salti_nb", []).append(1)   # P5: il ramo si CONTA, non e' un errore
            return orig_ps(self, i, j, w, dt_n, *a, **k)
        nb = np.asarray(_nbv, float)[:n]
        nb_vic = np.asarray(getattr(self, "_nb_prec", _nbv), float)[:n]
        ii = np.asarray(i); jj = np.asarray(j); ww = np.asarray(w, float)
        mask = (ii < n) & (jj < n)
        ii, jj, wl = ii[mask], jj[mask], ww[mask]
        if len(ii) and len(nb) >= n:
            chi_nodi = self.perc_chi[:n].astype(float)
            cl = (chi_nodi[ii] * chi_nodi[jj]).astype(float)
            refl = np.where(cl[:, None] > 0, np.array([1.0, 1.0, -1.0]), np.array([1.0, 1.0, 1.0]))
            B = np.zeros((n, 3)); deg = np.zeros(n)
            np.add.at(B, ii, nb_vic[jj] * wl[:, None] * refl); np.add.at(deg, ii, wl)
            np.add.at(B, jj, nb_vic[ii] * wl[:, None] * refl); np.add.at(deg, jj, wl)
            B = B / np.maximum(deg[:, None], 1e-9)
            REG["B"].append(rel(B))
            REG["correzione"].append(rel(np.cross(B, nb)))
            # LA DOMANDA CHE DECIDE SE LA CURA DI Z25 SI APPLICA QUI: il residuo dipende dal
            # DENOMINATORE, o dalla STRUTTURA? Si rifa' `B` senza divisione e con un denominatore
            # d'ARCO simmetrico, e si guarda se `sum(correzione)` va all'epsilon.
            Bn = np.zeros((n, 3))
            np.add.at(Bn, ii, nb_vic[jj] * wl[:, None] * refl)
            np.add.at(Bn, jj, nb_vic[ii] * wl[:, None] * refl)
            REG.setdefault("corr_nudo", []).append(rel(np.cross(Bn, nb)))
            gs = np.sqrt(np.maximum(deg[ii], 1e-9) * np.maximum(deg[jj], 1e-9))
            Bs = np.zeros((n, 3))
            np.add.at(Bs, ii, nb_vic[jj] * wl[:, None] * refl / gs[:, None])
            np.add.at(Bs, jj, nb_vic[ii] * wl[:, None] * refl / gs[:, None])
            REG.setdefault("corr_simm", []).append(rel(np.cross(Bs, nb)))
            # e il CONTROLLO che isola la RIFLESSIONE: stesso conto SENZA `refl`
            Br = np.zeros((n, 3))
            np.add.at(Br, ii, nb_vic[jj] * wl[:, None])
            np.add.at(Br, jj, nb_vic[ii] * wl[:, None])
            REG.setdefault("corr_norefl", []).append(rel(np.cross(Br, nb)))
            if S.TW_SPINORE and len(self.tw) >= len(mask):
                _twh = np.asarray(self.tw, float)[mask] / (2.0 * max(S.PHI_CRIT, 1e-9))
                _axis = np.where(cl[:, None] > 0, np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
                _otw = np.zeros((n, 3)); _degt = np.zeros(n)
                np.add.at(_otw, ii, _axis * _twh[:, None]); np.add.at(_degt, ii, 1.0)
                np.add.at(_otw, jj, _axis * _twh[:, None]); np.add.at(_degt, jj, 1.0)
                REG["otw"].append(rel(_otw / np.maximum(_degt[:, None], 1.0)))
    except Exception as e:
        REG.setdefault("errori", []).append(str(e))
    return orig_ps(self, i, j, w, dt_n, *a, **k)


# Punto 3: vive dentro step(). Si ricostruisce con le stesse espressioni, dal ramo che gira davvero.
orig_step = S.Rete.step


def spia_step(self):
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
            tn = np.zeros(n); gr = np.zeros(n)
            np.add.at(tn, i, twn); np.add.at(tn, j, -twn)
            np.add.at(gr, i, 1.0); np.add.at(gr, j, 1.0)
            REG["twist"].append(rel(tn[:n] / np.maximum(gr[:n], 1.0)))
            # e il confronto: la stessa cosa SENZA la divisione (lo scambio nudo)
            REG.setdefault("twist_nudo", []).append(rel(tn[:n]))
    except Exception as e:
        REG.setdefault("errori", []).append("step: %s" % e)
    return orig_step(self)


S.Rete._passo_spinoriale = spia_ps
S.Rete.step = spia_step

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
S.Rete._passo_spinoriale = orig_ps
S.Rete.step = orig_step

print("\n--- LA TABELLA: |sum| / max|.| contro l'epsilon macchina (~1e-16) ---")
print("  %-24s %-10s %-14s %-14s %-24s" % ("oggetto", "invocaz.", "MEDIANA", "MAX", "verdetto"))


def stampa(chiave, eti, atteso_zero):
    v = [x for x in REG.get(chiave, []) if x is not None]
    if not v:
        print("  %-24s %-10s %-14s %-14s %-24s" % (eti, 0, "-", "-", "NON OSSERVATO"))
        return None
    med, mx = float(np.median(v)), float(np.max(v))
    if not atteso_zero:
        ver = "non e' uno scambio"
    else:
        ver = "EPSILON: nessun cricchetto" if mx < 1e-12 else "CRICCHETTO (ordine %.2g)" % med
    print("  %-24s %-10d %-14.3e %-14.3e %-24s" % (eti, len(v), med, mx, ver))
    return med


print("  -- punto 1 --")
stampa("B", "B (media di campo)", False)
c1 = stampa("correzione", "correzione = BxNB", True)
stampa("corr_nudo", "  B SENZA divisione", True)
stampa("corr_simm", "  B con den. d'ARCO", True)
stampa("corr_norefl", "  B nudo e SENZA refl", True)
print("  -- punto 2 --")
if TW:
    c2 = stampa("otw", "_otw/_degt (TW forzato)", False)
else:
    print("  %-24s %-10s %-14s %-14s %-24s" % ("_otw/_degt", "-", "-", "-", "LATENTE: TW_SPINORE=False"))
print("  -- punto 3 --")
c3 = stampa("twist", "twist_nodo/grado", True)
stampa("twist_nudo", "  (lo stesso, NUDO)", True)

if REG.get("errori"):
    print("\n  ⚠ ERRORI DELLA SONDA (%d): %s" % (len(REG["errori"]), REG["errori"][:2]))

print("\n" + "=" * 118)
print("""COME SI LEGGE -- le letture erano fissate PRIMA, per ciascun punto
  residuo all'EPSILON        -> non e' un cricchetto li'. Si dice e si passa oltre: «dimostrato in
                                forma» puo' essere sbagliato in ENTRAMBE le direzioni.
  residuo di ORDINE UNO      -> e' lo stesso difetto di Z25, e la cura e' quella: denominatore
                                d'ARCO e simmetrico, oppure NESSUNO.
  lo schema e' DIVERSO       -> si riporta senza forzare l'analogia.
E la riga 'NUDO' del punto 3 e' il controllo: se il nudo e' all'epsilon e il diviso no, allora il
difetto e' ESATTAMENTE la divisione, come in Z25.""")
