# -*- coding: utf-8 -*-
"""Y5 RISCRITTO — il fallback dello sfondo dell'inerzia, misurato sul comportamento VERO.

PERCHE' IL VECCHIO E' SCADUTO (l'ottavo di questo giro):
  diceva *«il fallback cessa entro poche invocazioni e non torna»*, ed era vero SOLO perche' il
  neonato riceveva un peso spurio `~2e-4` — uno SFASAMENTO (`_pesi()` valutato su `eta` PRIMA
  dell'incremento, poi `calcola_psi()` lo RICALCOLAVA DOPO). Tolto lo sfasamento, i figli hanno
  `rho_sorgente = 0` al loro primo passo **sempre, per costruzione**, e il criterio vecchio legge
  quella CORREZIONE come un danno. `doc/REFERTO_sfasamento_eta.md`.

IL CRITERIO NUOVO risponde a TRE domande, e DEVE POTER FALLIRE:
  Y5a  il fallback scatta SOLO su nodi appena nati?  (grado 2 e eta minima)
  Y5b  nessun nodo MATURO cade nel fallback          (questo deve restare ZERO)
  Y5c  ogni nodo resta in fallback per UNA SOLA invocazione?
       <- e' la domanda che conta: un figlio deve USCIRE al passo successivo, quando eta > 0.
          Se resta dentro piu' a lungo, ALLORA c'e' un difetto, e sarebbe NUOVO.

COME PUO' FALLIRE, ed e' il punto: basta UN nodo maturo in fallback (Y5b), o UN figlio che ci resti
due invocazioni (Y5c). Nessuno dei due e' garantito dalla forma del codice.
ASCII PURO.
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
import importlib.util
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SIM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "soliton_simulator.py")
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


spec = importlib.util.spec_from_file_location("sim_y5", SIM)
M = importlib.util.module_from_spec(spec)
sys.modules["sim_y5"] = M
sys.argv = ["soliton_simulator.py"]
spec.loader.exec_module(M)
for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(M, _f, True)

TA = M.TAU_A
reg = []          # per invocazione: insieme dei nodi in fallback, col loro grado ed eta
n_storia = []
orig = M.Rete._passo_spinoriale
inv = {"k": 0}


def spia(self, i, j, w, dt_n, *a, **k):
    inv["k"] += 1
    n = self.n
    n_storia.append(n)
    rs = np.asarray(self._rho_sorgente(), float)[:n]
    ko = ~(np.isfinite(rs) & (rs > 0))
    if ko.any():
        grado = (np.bincount(self.i, minlength=n)[:n] +
                 np.bincount(self.j, minlength=n)[:n]) if len(self.i) else np.zeros(n)
        eta = np.asarray(getattr(self, "eta", np.zeros(n)), float)[:n]
        idx = np.where(ko)[0]
        reg.append({"inv": inv["k"], "n": n, "idx": idx.copy(),
                    "grado": grado[idx].copy(), "eta": eta[idx].copy(),
                    "eta_med_tutti": float(np.median(eta))})
    return orig(self, i, j, w, dt_n, *a, **k)


M.Rete._passo_spinoriale = spia

# scena del batch, riprodotta dal sorgente (~:5993-6014), non inventata
r = M.Rete(5)
r.semina(80)
for _ in range(6):
    M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = M.N_CRITICO() if callable(getattr(M, "N_CRITICO", None)) else 200
for kk in range(3):
    ang = 2 * np.pi * kk / 3
    r.nuova_massa(int(Nc * 0.6), raggio=M._size_video(kk, 0.8),
                  centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for kk in range(60):
    M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()

print("=" * 118)
print("Y5 RISCRITTO -- il fallback dello sfondo, sul comportamento VERO")
print("=" * 118)
print("  invocazioni osservate: %d   di cui col fallback: %d" % (inv["k"], len(reg)))

# gli indici dei nodi sono stabili? (i nuovi si aggiungono in coda; `keep` e' sugli ARCHI)
monotona = all(b >= a for a, b in zip(n_storia, n_storia[1:]))
verdetto("Y5.0 gli indici dei nodi sono STABILI (n monotono)", monotona,
         "n da %d a %d, mai decrescente: %s" % (n_storia[0], n_storia[-1], monotona))

# ------------------------------------------------------------------ SETUP escluso, e dichiarato
SETUP = 7   # le invocazioni del setup: semina(80) + riscaldamento + creazione delle tre masse
vivi = [x for x in reg if x["inv"] > SETUP]
print("\n  Le prime %d invocazioni sono il SETUP (semina + riscaldamento + creazione masse):" % SETUP)
print("  li' TUTTI i nodi sono nuovi e il campo non e' ancora calcolato. ESCLUSE, e dichiarato.")
print("  invocazioni col fallback DOPO il setup: %d" % len(vivi))

# ------------------------------------------------------------------ Y5a / Y5b
print("\n--- Y5a/Y5b: CHI cade nel fallback? ---")
if not vivi:
    print("  nessuna: il fallback non scatta oltre il setup.")
    verdetto("Y5a fallback solo su nodi appena nati", True, "nessun fallback oltre il setup")
    verdetto("Y5b nessun nodo MATURO nel fallback", True, "0")
else:
    g = np.concatenate([x["grado"] for x in vivi])
    e = np.concatenate([x["eta"] for x in vivi])
    em = np.median([x["eta_med_tutti"] for x in vivi])
    print("  nodi-invocazione in fallback : %d" % len(g))
    print("  GRADO  : min %g  mediana %g  max %g" % (g.min(), np.median(g), g.max()))
    print("  ETA    : min %.6g  mediana %.6g  max %.6g   (eta mediana di TUTTI: %.6g)"
          % (e.min(), np.median(e), e.max(), em))
    non_neo = int(np.sum(g != 2))
    maturi = int(np.sum(e > 0.5 * em))
    verdetto("Y5a fallback SOLO su nodi di grado 2 (firma mitosi)", non_neo == 0,
             "%d nodi-invocazione con grado != 2 (max grado %g)" % (non_neo, g.max()))
    verdetto("Y5b nessun nodo MATURO cade nel fallback  [deve restare 0]", maturi == 0,
             "%d nodi con eta > meta' della mediana (%.4g)" % (maturi, 0.5 * em))

# ------------------------------------------------------------------ Y5c
print("\n--- Y5c: per QUANTE invocazioni consecutive ciascun nodo resta in fallback? ---")
conta = {}
for x in vivi:
    for nid in x["idx"]:
        conta.setdefault(int(nid), []).append(x["inv"])
if not conta:
    verdetto("Y5c ogni nodo esce al passo successivo", True, "nessun nodo oltre il setup")
else:
    lung = {k: len(v) for k, v in conta.items()}
    peggio = max(lung.values())
    quanti_oltre = sum(1 for v in lung.values() if v > 1)
    dist = {}
    for v in lung.values():
        dist[v] = dist.get(v, 0) + 1
    print("  nodi distinti che cadono nel fallback: %d" % len(lung))
    print("  distribuzione (quante invocazioni ciascuno): %s"
          % ", ".join("%d inv -> %d nodi" % (k, dist[k]) for k in sorted(dist)))
    verdetto("Y5c ogni nodo resta in fallback UNA SOLA invocazione", peggio == 1,
             "peggiore: %d invocazioni; nodi con piu' di una: %d" % (peggio, quanti_oltre))
    if quanti_oltre:
        ese = [k for k, v in lung.items() if v > 1][:3]
        for k in ese:
            print("     es. nodo %d: invocazioni %s" % (k, conta[k]))

print("\n" + "=" * 118)
ok = sum(esiti)
print("Y5 RISCRITTO: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COME QUESTO CRITERIO PUO' FALLIRE -- ed e' la ragione per cui sostituisce il vecchio
  Y5b fallisce se UN SOLO nodo maturo cade nel fallback: nulla nella forma del codice lo impedisce,
      e sarebbe il segnale che il campo si annulla dove NON dovrebbe.
  Y5c fallisce se un figlio resta in fallback DUE invocazioni: significherebbe che `eta` non e'
      cresciuta, o che il campo non si e' acceso al passo dopo. Sarebbe un difetto NUOVO.
  Il vecchio Y5 invece misurava "quando cessa", che dipendeva dallo SFASAMENTO: era un criterio
  scritto sul difetto, non sulla legge.""")
