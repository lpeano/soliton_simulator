# -*- coding: utf-8 -*-
"""`D27` e `D25` SENZA RUN: le COMPONENTI del grafo e il TEMPO che non scorre, dagli snapshot.

⚠ SOLA LETTURA su snapshot gia' scritti. Nessuna fisica, nessun run, nessuna cura.
  Puo' girare mentre `G4` e' in corso.

PERCHE' SI PUO' FARE SENZA RIGIOCARE: gli snapshot contengono gia' **`i`**, **`j`** *(il grafo)* e
  **`_r_corrente`** *(il ritmo per nodo, cioe' `dt_n = DT*r`)*. **Verificato dal disco prima di
  stimare il costo**, non supposto.

`D27` -- IL GRAFO IN QUATTRO COMPONENTI *(`Z65`)*. Per ogni archivio e ogni snapshot:
  quante **componenti**, quanti **nodi e archi** in ciascuna, **come si distribuiscono le
  regioni** *(vuoto / massa / nato)*, e **la mediana di `d0` e di `d` per componente** -- cioe'
  **se la crescita di `d0` e' la stessa in tutte**.
  **E LA DOMANDA DI LUCA: le tre masse stanno in componenti diverse?**

`D25` -- IL TEMPO CHE NON SCORRE *(`Z46`)*. Dalla distribuzione di **`_r_corrente`**:
  quanti nodi hanno un ritmo **trascurabile**, e **quanta parte del tempo proprio totale**
  portano. **Il confronto e' col nodo MEDIANO, non con una soglia scelta.**

⚠ NESSUNA CONSEGUENZA SULLE TRE PROVE E' SCRITTA COME RISPOSTA: solo come **DOMANDA**.
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "COMPONENTI_E_TEMPO.md")
ARCHIVI = [("G1/G3 riferimento (`_val600`)", "_val600"),
           ("G3 senza gravita' (`_g3_senza_bifase`)", "_g3_senza_bifase"),
           ("G4 riferimento (`_g4_riferimento`)", "_g4_riferimento"),
           ("G4 senza memoria del moto (`_g4_senza_memmoto`)", "_g4_senza_memmoto")]
N_VUOTO, N0_SEMINA = 900, 2391


def componenti(ii, jj, n):
    """Union-find: la componente di ogni nodo. Zero dipendenze esterne."""
    p = np.arange(n, dtype=np.int64)

    def radice(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    for a, b in zip(np.asarray(ii, dtype=np.int64), np.asarray(jj, dtype=np.int64)):
        if a >= n or b >= n:
            continue
        ra, rb = radice(a), radice(b)
        if ra != rb:
            p[ra] = rb
    et = np.array([radice(x) for x in range(n)], dtype=np.int64)
    _u, inv = np.unique(et, return_inverse=True)
    return inv, len(_u)


def collaudo(W):
    """`P1-sexies`: le componenti su grafi a risposta NOTA, e il caso che DEVE fallire."""
    W("COLLAUDO (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 96 + "\n")
    e = []
    # A: due triangoli SEPARATI -> 2 componenti
    ii = np.array([0, 1, 2, 3, 4, 5]); jj = np.array([1, 2, 0, 4, 5, 3])
    c, k = componenti(ii, jj, 6)
    ok1 = (k == 2) and (len(set(c[:3])) == 1) and (len(set(c[3:])) == 1) and (c[0] != c[3])
    W("K1 due triangoli SEPARATI -> atteso 2 componenti, ottenuto %d -> %s\n"
      % (k, "OK" if ok1 else "*** SBAGLIA ***"))
    e.append(ok1)

    # B: IL CASO CHE DEVE FALLIRE -- un solo arco in piu' li UNISCE: deve dare 1
    ii2 = np.concatenate([ii, [2]]); jj2 = np.concatenate([jj, [3]])
    c2, k2 = componenti(ii2, jj2, 6)
    ok2 = (k2 == 1)
    W("K2 IL CASO CHE DEVE FALLIRE: UN SOLO arco in piu' li unisce -> atteso 1, ottenuto %d\n"
      % k2)
    W("     -> %s\n" % ("OK: il criterio VEDE la connessione"
                        if ok2 else "*** direbbe 2 su un grafo CONNESSO ***"))
    e.append(ok2)

    # C: nodi ISOLATI -> ognuno la sua componente
    c3, k3 = componenti(np.array([0]), np.array([1]), 5)
    ok3 = (k3 == 4)
    W("K3 un arco e tre nodi ISOLATI su 5 -> atteso 4 componenti, ottenuto %d -> %s\n"
      % (k3, "OK" if ok3 else "*** i nodi isolati spariscono ***"))
    e.append(ok3)

    ok = all(e)
    W("-" * 96 + "\n")
    W("  -> %s\n\n" % ("i criteri PASSANO: si misura" if ok else "*** NON PASSANO ***"))
    return ok


def regione(k):
    return np.where(k < N_VUOTO, 0, np.where(k < N0_SEMINA, 1, 2))


def main():
    W_ = sys.stdout.write
    if not collaudo(W_):
        return 1
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# `D27` e `D25` — LE COMPONENTI e IL TEMPO, **senza nessun run**\n\n")
    W("> **SOLA LETTURA** su snapshot gia' scritti: `i`, `j` e `_r_corrente` ci sono gia'.\n")
    W("> Generato da `csv/_test_fork/_componenti_e_tempo.py`. **Nessuna cura, nessuna fisica.**\n\n")

    for eti, dirn in ARCHIVI:
        d = os.path.join(RADICE, "csv", "_test_fork", dirn)
        files = sorted(glob.glob(os.path.join(d, "scena_*.pkl.gz")))
        W("## %s\n\n" % eti)
        if not files:
            W("*(nessuno snapshot: l'archivio non c'e' ancora)*\n\n")
            continue
        W("| passo | comp. | la piu' grande: nodi / archi | le altre | masse in comp. diverse? |\n")
        W("|--:|--:|---|---|---|\n")
        ultimo = None
        for p in files:
            with gzip.open(p, "rb") as f:
                a = pickle.load(f)["attrs"]
            ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
            n = len(np.asarray(a["psi"]))
            passo = int(a.get("_db_step", -1))
            c, k = componenti(ii, jj, n)
            cnt = np.bincount(c, minlength=k)
            ordine = np.argsort(cnt)[::-1]
            m = (ii < n) & (jj < n)
            arch = np.bincount(c[ii[m]], minlength=k)
            # le masse: gli indici [N_VUOTO, N0_SEMINA) divisi in TRE parti uguali.
            # ⚠ E' un'ASSUNZIONE sulla semina, ed e' DICHIARATA: tre masse uguali, in ordine.
            tagli = np.linspace(N_VUOTO, N0_SEMINA, 4).astype(int)
            comp_masse = []
            for t in range(3):
                idx = np.arange(tagli[t], min(tagli[t + 1], n))
                comp_masse.append(int(np.bincount(c[idx], minlength=k).argmax())
                                  if len(idx) else -1)
            diverse = len(set(comp_masse)) > 1
            altre = ", ".join("%d/%d" % (cnt[x], arch[x]) for x in ordine[1:5])
            W("| %d | **%d** | %d / %d | %s | %s |\n"
              % (passo, k, cnt[ordine[0]], arch[ordine[0]], altre or "—",
                 "**SI', %s**" % comp_masse if diverse else "no, tutte in `%d`" % comp_masse[0]))
            ultimo = (a, c, k, cnt, arch, ordine, passo, n)
        W("\n")
        if ultimo is None:
            continue
        a, c, k, cnt, arch, ordine, passo, n = ultimo
        ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
        d0 = np.asarray(a["d0"], float); dd = np.asarray(a["d"], float)
        m = (ii < n) & (jj < n)
        ca = c[ii[m]]
        W("**All'ultimo snapshot (passo %d): `med d0` e `med d` PER COMPONENTE**, "
          "e la composizione per regione.\n\n" % passo)
        W("| comp. | nodi | archi | vuoto | massa | nato | `med d0` | `med d` | `med d/d0` |\n")
        W("|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
        reg = regione(np.arange(n))
        for x in ordine[:6]:
            sel = (ca == x)
            nodi = (c == x)
            if not np.any(sel):
                W("| %d | %d | 0 | %d | %d | %d | — | — | — |\n"
                  % (x, cnt[x], int(np.sum(nodi & (reg == 0))),
                     int(np.sum(nodi & (reg == 1))), int(np.sum(nodi & (reg == 2)))))
                continue
            W("| %d | %d | %d | %d | %d | %d | `%.4f` | `%.4f` | `%.4f` |\n"
              % (x, cnt[x], int(np.sum(sel)),
                 int(np.sum(nodi & (reg == 0))), int(np.sum(nodi & (reg == 1))),
                 int(np.sum(nodi & (reg == 2))),
                 float(np.median(d0[m][sel])), float(np.median(dd[m][sel])),
                 float(np.median(dd[m][sel] / np.maximum(d0[m][sel], 1e-300)))))
        W("\n")

    # ---------------------------------------------------------------- D25
    W("## `D25` — IL TEMPO CHE NON SCORRE: la distribuzione di `_r_corrente`\n\n")
    W("> `dt_n = DT * r` e' **il tic dei processi locali** *(`CLAUDE.md` par.9)*. Un nodo con `r`\n")
    W("> trascurabile **non integra**: le leggi che vivono in `dt_n` non lo toccano.\n")
    W("> **Il confronto e' col nodo MEDIANO, non con una soglia scelta.**\n\n")
    W("| archivio | passo | nodi | `med r` | `r/med` < 0.01 | < 0.1 | quota del tempo nei fermi |\n")
    W("|---|--:|--:|--:|--:|--:|--:|\n")
    for eti, dirn in ARCHIVI:
        d = os.path.join(RADICE, "csv", "_test_fork", dirn)
        files = sorted(glob.glob(os.path.join(d, "scena_*.pkl.gz")))
        for p in files[-1:]:
            with gzip.open(p, "rb") as f:
                a = pickle.load(f)["attrs"]
            r = a.get("_r_corrente")
            if r is None:
                W("| %s | — | — | **`_r_corrente` ASSENTE** | | | |\n" % eti)
                continue
            r = np.asarray(r, float)
            r = r[np.isfinite(r)]
            med = float(np.median(r)) if r.size else float("nan")
            q1 = float(np.mean(r < 0.01 * med)) if med else float("nan")
            q2 = float(np.mean(r < 0.1 * med)) if med else float("nan")
            fermi = r < 0.1 * med
            quota = float(np.sum(r[fermi]) / np.sum(r)) if np.sum(r) else float("nan")
            W("| %s | %d | %d | `%.4e` | `%.4f` | `%.4f` | `%.6f` |\n"
              % (eti, int(a.get("_db_step", -1)), r.size, med, q1, q2, quota))
    W("\n")
    W("## ⚠ COSA LA MISURA HA DETTO, **prima** delle domande\n\n")
    W("**Le due premesse vanno verificate PRIMA di trarne conseguenze** *(par.9-bis: ogni\n")
    W("numero porta la sua epoca)*. Le tabelle qui sopra dicono **quante componenti** e **quanti\n")
    W("nodi fermi** ci sono DAVVERO negli archivi di QUESTA epoca. **Dove il numero di componenti\n")
    W("e' `1`, la premessa di `D27` NON REGGE**, e le domande `1` e `2` restano aperte **solo per\n")
    W("gli archivi in cui piu' componenti ci sono davvero.**\n\n")
    W("## ⚠ LE CONSEGUENZE SULLE TRE PROVE: **DOMANDE, non risposte**\n\n")
    W("1. **Se il grafo e' in piu' componenti, che cosa significa «distanza fra due masse»\n")
    W("   nella PROVA 1?** Un cammino minimo fra componenti diverse **non esiste**. Si misura\n")
    W("   dentro una componente? Si dichiara infinita? **La domanda non ha oggi una risposta.**\n")
    W("2. **La PROVA 2 chiede la pendenza contro la distanza.** Se le separazioni appartengono a\n")
    W("   componenti diverse, **su quale asse si mette il punto?**\n")
    W("3. **Se il `93 %` dei nodi non integra**, la PROVA 3 *(tutti i corpi cadono uguale)*\n")
    W("   **sta confrontando corpi che evolvono, o corpi fermi?**\n")
    W("\n**Nessuna di queste e' una cura, e nessuna e' una risposta.** Vanno al `CHK3`.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read()[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
