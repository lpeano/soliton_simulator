r"""**PARTECIPAZIONI MULTIPLE** — un nodo può appartenere a più masse, e l'opacità è il **MAX**.

*(Osservazione e regola di Luca, 2026-09-27.)*

## LA REGOLA

```
w_k = MAX sulle masse m  di  max(0, cos(phi_k - phibar_m(t)))
```

**Le due alternative sono state SCARTATE da Luca, e il perché sta qui perché non ci si torni:**

| forma | scartata perché |
|---|---|
| **media armonica** | **è dominata dal peso MINIMO** *(un nodo quasi ortogonale a una sola massa la trascinerebbe a zero)* e **non è definita con pesi nulli** |
| **somma limitata a 1** | **non ora: è una scelta di TEORIA**, non di misura — e una scelta di teoria non si prende dentro uno strumento |

**Il `max(0, ...)` interno resta quello già dichiarato:** `cos = -1` è **antifase**, e il codice del
simulatore dice che *«proietta CONTRO»* — quindi quel nodo **non fa parte di «dove la massa è
densa»**. **Il `MAX` esterno è la partecipazione: un nodo è opaco quanto la massa a cui
appartiene di più.**

## ⚠ **IN QUESTA SCENA LA REGOLA NON CAMBIA NULLA — e lo si DICHIARA misurandolo**

Le tre regioni sono **disgiunte** e nessun nodo partecipa a più di una massa, quindi il `MAX` su un
solo termine **è quel termine**. **Ma «non cambia nulla» va MISURATO**, non dedotto: se i nodi con
più di una partecipazione fossero `> 0`, **ci si ferma**.

    python csv/_test_fork/_partecipazioni.py

ASCII puro.
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: legge le coorti e i `misura.json` di un run che ha gia' dichiarato la propria
#   configurazione intera nel proprio referto. Non carica il simulatore, non costruisce scene.

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
STATI = os.path.join(DEST, "stati")
SEMI = [11, 12, 13, 14]
R = []


def P(s=""):
    print(s)
    R.append(s)


def peso_max(phi, regioni, bar):
    """**LA REGOLA**: `w_k = MAX_m max(0, cos(phi_k - phibar_m))`, su tutte le masse.

    `regioni` è `{massa: indici}`, `bar` è `{massa: phibar_m}`. I nodi che non partecipano a
    nessuna massa restano a **`0`**, ed è la definizione: **non partecipano**.
    """
    n = len(phi)
    w = np.zeros(n)
    for k, idx in regioni.items():
        idx = np.asarray(idx, int)
        idx = idx[idx < n]
        if not len(idx) or k not in bar:
            continue
        w[idx] = np.maximum(w[idx], np.maximum(0.0, np.cos(phi[idx] - bar[k])))
    return w


def principale():
    P("=" * 104)
    P("PARTECIPAZIONI MULTIPLE -- la regola del MAX, e la verifica che qui non cambi nulla")
    P("=" * 104)
    P("  w_k = MAX sulle masse m di max(0, cos(phi_k - phibar_m(t)))")
    P("  Scartate da Luca: la MEDIA ARMONICA (dominata dal peso minimo, non definita con pesi")
    P("  nulli) e la SOMMA LIMITATA A 1 (non ora: e' una scelta di TEORIA, non di misura).")
    P()
    P("-" * 104)
    P("LA VERIFICA: quanti nodi partecipano a PIU' DI UNA massa?   (atteso: 0)")
    P("-" * 104)
    P("  seme | nodi in 1 massa | in 2 | in 3 | totale nodi di massa | sovrapposizione")
    tot_multi = 0
    geo = []
    for s in SEMI:
        p = os.path.join(STATI, "coorti_seme%d.npz" % s)
        if not os.path.exists(p):
            P("  %4d | ** manca %s **" % (s, os.path.basename(p)))
            tot_multi += 1
            continue
        z = np.load(p, allow_pickle=False)
        masse = sorted(k for k in z.files if k.startswith("massa_"))
        tutti = np.concatenate([np.asarray(z[k], int) for k in masse])
        u, c = np.unique(tutti, return_counts=True)
        n1 = int(np.sum(c == 1))
        n2 = int(np.sum(c == 2))
        n3 = int(np.sum(c >= 3))
        tot_multi += n2 + n3
        P("  %4d | %15d | %4d | %4d | %20d | %s"
          % (s, n1, n2, n3, len(tutti), "NESSUNA" if (n2 + n3) == 0 else "** C'E' **"))
        geo.append((s, len(masse), len(u)))
    P()
    if tot_multi:
        P("  ** MI FERMO: %d nodi partecipano a piu' di una massa. **" % tot_multi)
        P("  La regola del MAX allora NON e' inerte, e prima di usarla va detto di quanto cambia")
        P("  i numeri gia' scritti -- non si applica in silenzio una regola che muove un risultato.")
        return False
    P("  ✅ ZERO nodi con piu' di una partecipazione, su tutti e 4 i semi.")
    P("  QUINDI IN QUESTA SCENA LA REGOLA DEL MAX E' INERTE: il massimo su un solo termine non")
    P("  nullo E' quel termine. Dichiarato e MISURATO, non dedotto.")

    # ------------------------------------------------------------------ la disgiunzione: perche'
    P()
    P("-" * 104)
    P("E LA DISGIUNZIONE NON E' UN CASO: E' PER COSTRUZIONE, e il margine si calcola")
    P("-" * 104)
    d = json.load(io.open(os.path.join(DEST, "seme_11", "misura.json"), encoding="utf-8"))
    sep = float(d["sep"])
    r = float(d["r_regione"])
    lato = sep * np.sqrt(3.0)          # i tre centri sono i vertici di un triangolo equilatero
    P("  la scena mette i centri a `sep` dall'origine, a 120 gradi: il LATO del triangolo e'")
    P("  sep*sqrt(3) = %.4f, e il raggio di ogni regione e' r_regione = %.4f." % (lato, r))
    P("  Due dischi di raggio r sono disgiunti se 2r < lato:  2r = %.4f  <  %.4f   ->  %s"
      % (2 * r, lato, "DISGIUNTI" if 2 * r < lato else "** SI TOCCANO **"))
    P("  IL VARCO fra due regioni vale lato - 2r = %.4f" % (lato - 2 * r))
    P("  ⚠ E NON E' UN NUMERO QUALUNQUE: la scena costruisce `r = 0.5*(sep*sqrt(3) - R_CONN)`,")
    P("    quindi il varco e' `R_CONN` ESATTAMENTE -- il raggio con cui il vuoto si allaccia.")
    P("    La disgiunzione e' VOLUTA, e il margine e' UNA CONNESSIONE di larghezza.")

    # ------------------------------------------------------------------ riduzione al limite
    P()
    P("-" * 104)
    P("RIDUZIONE AL LIMITE: col `MAX` e senza, lo STESSO numero (regioni disgiunte)")
    P("-" * 104)
    z = np.load(os.path.join(STATI, "coorti_seme11.npz"), allow_pickle=False)
    reg = {k: np.asarray(z[k], int) for k in sorted(z.files) if k.startswith("massa_")}
    st = os.path.join(STATI, "stato_seme11_passo000000.npz")
    zs = np.load(st, allow_pickle=False)
    phi = np.asarray(zs["phi"], float)
    n = int(zs["n"])
    bar = {k: float(np.angle(np.mean(np.exp(1j * phi[np.asarray(v, int)[np.asarray(v, int) < n]]))))
           for k, v in reg.items()}
    w_max = peso_max(phi[:n], reg, bar)
    w_uno = np.zeros(n)
    for k, idx in reg.items():
        idx = np.asarray(idx, int)
        idx = idx[idx < n]
        w_uno[idx] = np.maximum(0.0, np.cos(phi[idx] - bar[k]))     # una massa alla volta
    dif = float(np.max(np.abs(w_max - w_uno)))
    P("  max |w_MAX - w_una_massa| = %.3e   su %d nodi   ->  %s"
      % (dif, n, "IDENTICI" if dif == 0.0 else "** DIVERSI **"))
    P("  (con regioni disgiunte le due forme DEVONO coincidere: se non coincidessero, la")
    P("   disgiunzione non sarebbe quella che la misura sopra dice.)")
    P("=" * 104)
    return dif == 0.0


if __name__ == "__main__":
    ok = principale()
    io.open(os.path.join(DEST, "PARTECIPAZIONI.txt"), "w",
            encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    raise SystemExit(0 if ok else 1)
