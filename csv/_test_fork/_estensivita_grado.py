# -*- coding: utf-8 -*-
"""L'ESTENSIVITA' E' UN DIFETTO? La speculazione di Luca su Z30, messa alla prova.

Progettazione in doc/TASK_HISTORY/2026-09-18_estensivita-omega-grado.md (committato PRIMA).

PASSO 0  ri-verificare LA CATENA dal sorgente: il feedback passa per l'inerzia, o per M_PH?
PASSO 1  LA PREMESSA DI LUCA: `grado` e' un proxy della densita' locale?
PASSO 2  LA COMPENSAZIONE ESISTE? `inerzia` cresce col grado?
PASSO 3  LA MISURA CHIESTA: `|phivel|` e `|omega_s|` contro il grado, PRIMA e DOPO la cura.

⚠ DUE OSSERVABILI, NON UNA, E VIVONO IN CATENE DIVERSE:
    `phivel`   e' la catena in cui il feedback ENTRA        (coppia / M_PH, massa UNIFORME)
    `omega_s`  e' la catena dell'INERZIA                     (correzione / inerzia, per nodo)
  Chiamarle entrambe «omega» e sceglierne una sarebbe un errore di popolazione travestito.

⚠ E SI RIPORTA SULLE DUE MODE (g=2 e g>=100), MAI CON UN FIT: la distribuzione dei gradi e'
  BIMODALE (Z27: 19.85 % a grado 2, 65.57 % a grado >= 100), e un fit su due popolazioni distinte
  e' esattamente l'errore gia' fatto una volta.

Le varianti PRIMA/DOPO si ottengono sostituendo il metodo per la durata della misura: nessuna legge
del file e' toccata.
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

S.TAU_A = float(_ARGV[_ARGV.index("--tau-a") + 1]) if "--tau-a" in _ARGV else 2.0
PASSI = int(_ARGV[_ARGV.index("--passi") + 1]) if "--passi" in _ARGV else 60

print("=" * 118)
print("L'ESTENSIVITA' E' UN DIFETTO?  [TAU_A=%s, %d passi, seme 5]" % (S.TAU_A, PASSI))
print("=" * 118)

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
RIGHE = src.splitlines()


def riga(fr):
    for k, l in enumerate(RIGHE, 1):
        if fr in l.split("#")[0]:
            return k
    return -1


# ---------------------------------------------------------------- PASSO 0
print("\n--- PASSO 0: LA CATENA. Il feedback passa per l'INERZIA o per M_PH? ---")
p = [("if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK", "il gate del feedback"),
     ("coppia += _fb", "il feedback entra in `coppia`"),
     ("coppia = coppia + twist_nodo[:self.n]", "e anche twist_nodo (Z27)"),
     ("delta_phivel = dt_n_s * (coppia - G_PH", "`coppia` -> delta_phivel / M_PH"),
     ("M_PH     =", "M_PH, il divisore di QUELLA catena"),
     ("omega_new = omega_src + dtn_c", "l'UNICA /inerzia: divide `correzione`, non `coppia`")]
for fr, eti in p:
    print("   :%-6d %-44s %s" % (riga(fr), eti, fr[:46]))
print("  M_PH = %s   -> %s" % (S.M_PH, "COSTANTE GLOBALE: nessuna inerzia a valle del feedback"
                               if np.isscalar(S.M_PH) else "?"))
print("""
  ESITO PASSO 0: la lettura committata in a15716c REGGE. Due catene separate:
    feedback + twist_nodo  ->  `coppia`  ->  / M_PH (uniforme)  ->  phivel      [settore FASE]
    correzione = B x nb    ->  / inerzia (per nodo)             ->  omega_s     [settore SPIN]
  Quindi la 'doppia compensazione' NON puo' avvenire sul canale del feedback: a valle c'e' una
  COSTANTE. Resta aperta la via INDIRETTA (phivel -> phi -> psi -> rho -> inerzia), mai misurata.""")

# ---------------------------------------------------------------- la scena, con le due varianti
orig_fb = S.Rete._feedback_spinoriale_archi
orig_tw = None


def fabbrica_fb(nudo):
    def m(self, i, j, w):
        out = np.zeros(self.n)
        self._spin_feedback_last = 0.0
        if not S.SPIN_FEEDBACK or len(self._spinor_lift) < self.n:
            return out
        mask = (i < self.n) & (j < self.n)
        if not mask.any():
            return out
        ii, jj, ww = i[mask], j[mask], w[mask]
        ov = np.sum(np.conj(self._spinor_lift[ii]) * self._spinor_lift[jj], axis=1)
        f = ww * np.imag(ov)
        if nudo:
            np.add.at(out, ii, -f); np.add.at(out, jj, f)
        else:                                        # la forma PRE-CURA
            g = np.zeros(self.n)
            np.add.at(g, ii, ww); np.add.at(g, jj, ww)
            np.add.at(out, ii, -f / np.maximum(g[ii], 1e-9))
            np.add.at(out, jj, f / np.maximum(g[jj], 1e-9))
        self._spin_feedback_last = float(np.mean(np.abs(f))) if len(f) else 0.0
        return out
    return m


def gira(nudo):
    """nudo=True -> lo stato CABLATO oggi; nudo=False -> la forma PRE-CURA."""
    S.Rete._feedback_spinoriale_archi = fabbrica_fb(nudo)
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
    for _ in range(PASSI):
        S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    S.Rete._feedback_spinoriale_archi = orig_fb
    return r


def stato(r):
    """Le grandezze per nodo, TUTTE allo STESSO istante e sulla STESSA popolazione (A3c)."""
    n = r.n
    i = np.asarray(r.i); j = np.asarray(r.j)
    g = np.zeros(n)
    m = (i < n) & (j < n)
    np.add.at(g, i[m], 1.0); np.add.at(g, j[m], 1.0)
    d = dict(n=n, grado=g)
    d["phivel"] = np.abs(np.asarray(r.phivel, float)[:n])
    om = np.asarray(r.omega_s, float)
    d["omega_s"] = np.linalg.norm(om[:n], axis=1) if om.ndim == 2 else np.abs(om[:n])
    try:
        d["rho"] = np.asarray(r._rho_sorgente(), float)[:n]
    except Exception:
        d["rho"] = None
    peq = np.asarray(getattr(r, "peq", []), float)
    if len(peq) == len(i) and m.any():
        sp = np.bincount(i[m], peq[m], minlength=n) + np.bincount(j[m], peq[m], minlength=n)
        d["peq_nodo"] = sp / np.maximum(g, 1.0)
    else:
        d["peq_nodo"] = None
    return d


def per_mode(v, g):
    """Le DUE MODE separate: mai un fit, mai una media fra popolazioni distinte."""
    a = v[g == 2]; b = v[g >= 100]
    ma = float(np.median(a)) if len(a) > 3 else float("nan")
    mb = float(np.median(b)) if len(b) > 3 else float("nan")
    return ma, mb, (mb / ma if ma > 0 else float("nan")), len(a), len(b)


print("\n--- giro POST-CURA (nudo, lo stato cablato) e giro PRE-CURA (/grado) ---")
POST = stato(gira(True))
PRE = stato(gira(False))
print("  nodi: POST %d   PRE %d   (traiettorie diverse: i confronti di AMPIEZZA fra i due non hanno barra)"
      % (POST["n"], PRE["n"]))

# ---------------------------------------------------------------- PASSO 1
print("\n--- PASSO 1: la premessa di Luca -- `grado` e' un proxy della DENSITA' locale? ---")
for eti, D in (("POST", POST), ("PRE", PRE)):
    g = D["grado"]
    for nome in ("rho", "peq_nodo"):
        v = D[nome]
        if v is None:
            print("  %-5s grado vs %-9s : ASSENTE" % (eti, nome)); continue
        ok = np.isfinite(v) & np.isfinite(g) & (g > 0)
        c = float(np.corrcoef(g[ok], v[ok])[0, 1]) if ok.sum() > 10 and np.std(v[ok]) > 0 else float("nan")
        a, b, rap, na, nb = per_mode(v, g)
        print("  %-5s grado vs %-9s : corr %+.4f   mediana a g=2 %.5g (n=%d)  a g>=100 %.5g (n=%d)  rapporto %.4g"
              % (eti, nome, c, a, na, b, nb, rap))
print("  (su un grafo costruito per PROSSIMITA' una correlazione positiva e' ATTESA: il valore")
print("   informativo e' QUANTO, e se il rapporto fra le due mode e' grande o vicino a 1)")

# ---------------------------------------------------------------- PASSO 2
print("\n--- PASSO 2: la compensazione ESISTE? `inerzia` cresce col grado? ---")
print("  inerzia = max( (rho_sorgente / peq_nodo) * (d_nodo/cs_nodo)^2 , 1e-6 )")
for eti, D in (("POST", POST), ("PRE", PRE)):
    if D["rho"] is None or D["peq_nodo"] is None:
        print("  %-5s NON RICOSTRUIBILE" % eti); continue
    contrasto = D["rho"] / np.maximum(D["peq_nodo"], 1e-300)
    g = D["grado"]
    ok = np.isfinite(contrasto) & (g > 0)
    c = float(np.corrcoef(g[ok], contrasto[ok])[0, 1]) if ok.sum() > 10 and np.std(contrasto[ok]) > 0 else float("nan")
    a, b, rap, na, nb = per_mode(contrasto, g)
    print("  %-5s contrasto rho/peq vs grado : corr %+.4f   g=2 %.5g   g>=100 %.5g   rapporto %.4g"
          % (eti, c, a, b, rap))
print("""  ⚠ NB: si riporta il CONTRASTO `rho/peq`, non l'inerzia piena: il fattore `(d/cs)^2` e' una
     LOCALE di _passo_spinoriale e il simulatore non lo espone. Ricostruirlo qui sarebbe una
     RI-IMPLEMENTAZIONE, e chiamarlo 'inerzia' sarebbe un fallback silenzioso (P5). Il contrasto e'
     il fattore che l'argomento di Luca chiama in causa ('rho/peq alto'), quindi e' quello giusto.""")

# ---------------------------------------------------------------- PASSO 3
print("\n--- PASSO 3: LA MISURA CHIESTA -- omega contro il grado, PRIMA e DOPO ---")
print("  ⚠ DUE osservabili in DUE catene: `phivel` e' dove il feedback ENTRA; `omega_s` e' la catena")
print("    dell'inerzia, dove entra solo INDIRETTAMENTE.\n")
print("  %-10s %-9s %-13s %-13s %-11s %-11s" %
      ("osservab.", "variante", "g = 2", "g >= 100", "rapporto", "corr(grado)"))
for nome in ("phivel", "omega_s"):
    for eti, D in (("PRE", PRE), ("POST", POST)):
        v = D[nome]; g = D["grado"]
        ok = np.isfinite(v) & (g > 0)
        c = float(np.corrcoef(g[ok], v[ok])[0, 1]) if ok.sum() > 10 and np.std(v[ok]) > 0 else float("nan")
        a, b, rap, na, nb = per_mode(v, g)
        print("  %-10s %-9s %-13.5g %-13.5g %-11.4g %+.4f" % (nome, eti, a, b, rap, c))
    print()

print("=" * 118)
print("""COME SI LEGGE -- le tre letture erano fissate PRIMA (task history, commit 75a15bc)
  |omega| PIATTO col grado DOPO  -> l'estensivita' e' compensata a valle: la speculazione REGGE, e
                                    `nudo` e' giustificato da una MISURA, non solo da A1.
  CRESCE dopo, era piatto prima  -> la cura ha introdotto un BIAS DI GRADO nell'osservabile: e' un
                                    costo reale, e va messo accanto al guadagno.
  Cresceva ANCHE PRIMA           -> il bias PRECEDE la cura: il denominatore non e' cio' che lo
                                    decide. Sarebbe il risultato piu' interessante.
E le due mode NON si mediano: se danno verdetti opposti si riportano separate.""")
