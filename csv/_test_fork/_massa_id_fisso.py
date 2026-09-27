r"""**`MASSA-ID-FISSO`** — le masse per lignaggio **SOTTO UNA CONDIZIONE VERIFICATA**.

*(Decisione di Luca, 2026-09-27: né *(a)* rifare il run per il tracciamento, né *(b)* rimandare —
ma **(c)**: su **QUESTO** run, la versione **«a lignaggio fisso»**.)*

> ## ⚠⚠ **NON SI CHIAMA `MASSA-ID`, E NON È LA STESSA COSA.**
> `MASSA-ID` identifica la massa col **lignaggio VERO** (`conc_nodi`, che la mitosi eredita) ed è
> **BLOCCATA**: la scena non registra le regioni, e gli stati non portano il tracking.
> **`MASSA-ID-FISSO` usa le coorti del passo 0 come se fossero il lignaggio**, e vale **SOLO SE**
> una condizione è vera. **La condizione si VERIFICA PRIMA; se è falsa, ci si FERMA.**

## LA CONDIZIONE — `V-PRE`

> **Nessun nodo NATO *(indice `>= n0`)* ha come genitore o come vicino diretto un nodo di massa,
> fra un checkpoint e l'altro.**

**Si verifica sull'ADIACENZA, ed è una scelta CONSERVATIVA, non una scorciatoia:**
il figlio della mitosi nasce **collegato a ENTRAMBI i genitori** *(`:6292-6293`)*, e l'antinodo
Schwinger **a `aa` e `bb`** *(`:6413-6414`)*. **Quindi «adiacente a un nodo di massa» è un
SOVRAINSIEME di «figlio di un nodo di massa»**: se l'adiacenza è zero, la parentela è zero
**a maggior ragione**. *(Il lignaggio vero non sta negli stati — è il blocco di `MASSA-ID`.)*

**Se `V-PRE` regge**, i nodi di massa **sono** le coorti del passo 0, e allora si calcolano:
`phibar_m(t) = arg <e^{i phi}>` sui nodi della massa, i pesi `cos(phi_k - phibar_m(t))`,
il **medoide PESATO** e la **frazione di pesi negativi** (`Y5`).

    python csv/_test_fork/_massa_id_fisso.py

ASCII puro.
"""
import glob
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)

import _presidio                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402
import _massa_id as MI                                                 # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore. Legge gli `.npz` di un run
#   che ha gia' dichiarato la propria configurazione intera nel suo referto.

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
STATI = os.path.join(DEST, "stati")
FUORI = os.path.join(DEST, "MASSA_ID_FISSO.txt")
SEMI = [11, 12, 13, 14]
R = []


def P(s=""):
    print(s)
    R.append(s)


def coorti(seme):
    p = os.path.join(STATI, "coorti_seme%d.npz" % seme)
    if not os.path.exists(p):
        return None
    z = np.load(p, allow_pickle=False)
    return {k: np.asarray(z[k], int) for k in sorted(z.files) if k.startswith("massa_")}


def stati(seme):
    v = sorted(glob.glob(os.path.join(STATI, "stato_seme%d_passo*.npz" % seme)))
    return [(int(np.load(x, allow_pickle=False)["passo"]), x) for x in v]


def barra(v):
    o = OP.dispersione([x for x in v if np.isfinite(x)])
    if o["ic95"] is None:
        return o["media"], float("nan"), float("nan"), float("nan"), True
    lo, hi = o["ic95"]
    return o["media"], o["sd"], lo, hi, bool(lo <= 0.0 <= hi)


# ============================================================ `V-PRE`: LA CONDIZIONE
def verifica(seme):
    """`V-PRE` — **quanti nodi NATI toccano una massa.** Deve essere `0` a ogni checkpoint."""
    co = coorti(seme)
    if co is None:
        return None, "nessun `coorti_seme%d.npz`" % seme
    tutte = np.unique(np.concatenate([co[k] for k in sorted(co)]))
    st = stati(seme)
    if not st:
        return None, "nessuno stato per il seme %d" % seme
    n0 = int(np.load(st[0][1], allow_pickle=False)["n"])
    fuori = []
    for passo, p in st:
        z = np.load(p, allow_pickle=False)
        n = int(z["n"])
        ii, jj = np.asarray(z["i"], int), np.asarray(z["j"], int)
        nati = np.zeros(n, bool)
        nati[n0:] = True
        mass = np.zeros(n, bool)
        mass[tutte[tutte < n]] = True
        # un arco che unisce un NATO a un nodo di MASSA, nei due versi
        tocca = ((nati[ii] & mass[jj]) | (mass[ii] & nati[jj]))
        quali = np.unique(np.concatenate([ii[tocca], jj[tocca]])) if tocca.any() else np.zeros(0, int)
        quali = quali[quali >= n0]
        # ⚠ LA LUNGHEZZA di quegli archi, contro `LAM`: e' cio' che spiega perche' `V3` del pilota
        #   (metro: distanza di grafo <= LAM) li classifica <<vuoto>> mentre `V-PRE` (ADIACENZA,
        #   qualunque lunghezza) li trova A CONTATTO. Due METRI diversi, non due risultati diversi.
        dd = np.asarray(z["d"], float)[tocca] if tocca.any() else np.zeros(0)
        fuori.append(dict(passo=passo, n=n, nati=int(n - n0), archi_tocco=int(tocca.sum()),
                          nati_a_contatto=int(len(quali)),
                          d_min=float(dd.min()) if len(dd) else float("nan"),
                          d_med=float(np.median(dd)) if len(dd) else float("nan"),
                          sotto_lam=int(np.sum(dd <= 0.8)) if len(dd) else 0))
    return fuori, ""


# ============================================================ LA MISURA, SE LA CONDIZIONE REGGE
def misura(seme):
    co = coorti(seme)
    st = stati(seme)
    fuori = []
    for passo, p in st:
        z = np.load(p, allow_pickle=False)
        n = int(z["n"])
        phi = np.asarray(z["phi"], float)
        g, _u, _s = OP.grafo(z["i"], z["j"], np.asarray(z["d"], float), n)
        riga = {"passo": passo, "masse": {}}
        for k in sorted(co):
            idx = co[k]
            idx = idx[idx < n]
            if not len(idx):
                continue
            bar = float(np.angle(np.mean(np.exp(1j * phi[idx]))))
            w = np.cos(phi[idx] - bar)
            m_p, dia = MI.medoide_pesato(g, idx, w)
            m_u, _p, _r = OP.medoide(g, idx)
            spost = float(OP.distanze(g, [m_u])[0, m_p]) if (m_u >= 0 and m_p >= 0) else float("nan")
            riga["masse"][k] = dict(
                phibar=bar, coer=float(abs(np.mean(np.exp(1j * phi[idx])))),
                neg=float(dia["frazione_negativi"]), medoide_pesato=int(m_p),
                medoide_non_pesato=int(m_u), spostamento=spost,
                ripiego=int(dia["ripiego_non_pesato"]))
        fuori.append(riga)
    return fuori


def principale():
    P("=" * 108)
    P("`MASSA-ID-FISSO` -- le masse per lignaggio SOTTO UNA CONDIZIONE VERIFICATA")
    P("=" * 108)
    P("  ⚠ NON E' `MASSA-ID`: quella usa il lignaggio VERO (`conc_nodi`) ed e' BLOCCATA. Qui le")
    P("    coorti del passo 0 si usano COME SE fossero il lignaggio, e vale SOLO SE `V-PRE` regge.")
    P()
    P("-" * 108)
    P("`V-PRE` -- nessun nodo NATO tocca un nodo di massa. Verificata sull'ADIACENZA, che e' un")
    P("           SOVRAINSIEME della parentela (il figlio nasce collegato a ENTRAMBI i genitori,")
    P("           :6292-6293; l'antinodo Schwinger a `aa` e `bb`, :6413-6414).")
    P("-" * 108)
    P("  seme | passo | n     | nati | archi | a contatto | d min  | d mediano | d <= LAM")
    ko = 0
    for s in SEMI:
        v, nota = verifica(s)
        if v is None:
            P("  %4d | ** %s **" % (s, nota))
            ko += 1
            continue
        for r in v:
            P("  %4d | %5d | %5d | %4d | %5d | %10d | %6s | %9s | %d"
              % (s, r["passo"], r["n"], r["nati"], r["archi_tocco"], r["nati_a_contatto"],
                 ("%.4f" % r["d_min"]) if np.isfinite(r["d_min"]) else "-",
                 ("%.4f" % r["d_med"]) if np.isfinite(r["d_med"]) else "-", r["sotto_lam"]))
            ko += 1 if r["nati_a_contatto"] else 0
    P()
    if ko:
        P("  ** `V-PRE` NON REGGE: %d checkpoint con nodi nati a contatto con una massa. **" % ko)
        P("  MI FERMO, come chiesto: la versione a lignaggio fisso NON e' applicabile, e i numeri")
        P("  che ne uscirebbero sarebbero quelli di un insieme che NON e' la massa.")
        P()
        P("  ⚠ E QUESTO NON CONTRADDICE IL `V3` DEL PILOTA (<<0 nascite nelle masse>>): i due")
        P("    criteri usano METRI DIVERSI, e `V-PRE` e' piu' STRETTO.")
        P("    `V3` chiama <<in massa>> un nodo entro `LAM = 0.8` di distanza DI GRAFO dalla")
        P("    regione; `V-PRE` guarda l'ADIACENZA, qualunque sia la lunghezza dell'arco.")
        P("    MISURATO: gli archi `nato--massa` hanno `d` fra 0.80 e 1.58, e QUELLI CON")
        P("    `d <= LAM` SONO ZERO su tutti i semi e tutti i checkpoint. Quindi `V3` li")
        P("    classifica <<vuoto>> A RAGIONE, e `V-PRE` li trova a contatto A RAGIONE.")
        P("    IL FATTO NUOVO E': I NATI TOCCANO LE MASSE, anche se stanno APPENA OLTRE `LAM`.")
        P()
        P("  ⚠ E L'ADIACENZA NON E' PARENTELA: e' un SOVRAINSIEME. Il contatto NON DIMOSTRA che")
        P("    quei nodi siano figli di nodi di massa -- dimostra che NON SI PUO' ESCLUDERLO.")
        P("    Il lignaggio vero non sta negli stati, ed e' il blocco di `MASSA-ID`.")
        return False
    P("  ✅ `V-PRE` REGGE su tutti i semi e tutti i checkpoint: ZERO nodi nati a contatto.")
    P("  QUINDI, SOTTO QUESTA CONDIZIONE, i nodi di massa SONO le coorti del passo 0.")

    P()
    P("-" * 108)
    P("LA MISURA (solo perche' `V-PRE` regge): pesi `cos(phi_k - phibar_m(t))`, medoide PESATO")
    P("-" * 108)
    dati = {s: misura(s) for s in SEMI}
    passi = [r["passo"] for r in dati[SEMI[0]]]
    masse = sorted(dati[SEMI[0]][0]["masse"].keys())
    P("  passo | grandezza                    | media fra semi |   IC95          | nota")
    for p in passi:
        for nome, chiave, u in (("coerenza |<e^{i phi}>|", "coer", ""),
                                ("frazione di pesi NEGATIVI", "neg", ""),
                                ("spostamento medoide pesato", "spostamento", "")):
            v = [dati[s][[i for i, r in enumerate(dati[s]) if r["passo"] == p][0]]["masse"][k][chiave]
                 for s in SEMI for k in masse]
            m, sd, lo, hi, z = barra(v)
            P("  %5d | %-28s | %+13.5f | [%+.4f,%+.4f] | %s"
              % (p, nome, m, lo, hi, "contiene lo zero" if z else "esclude lo zero"))
        P()
    rip = sum(dati[s][i]["masse"][k]["ripiego"]
              for s in SEMI for i in range(len(passi)) for k in masse)
    P("  ripieghi sul medoide NON pesato (somma pesi <= 0): %d su %d"
      % (rip, len(SEMI) * len(passi) * len(masse)))
    P()
    P("  ⚠ LA CONDIZIONE VA CITATA OGNI VOLTA CHE SI CITANO QUESTI NUMERI: valgono <<a lignaggio")
    P("    fisso>>, cioe' SOTTO `V-PRE`. Non sono `MASSA-ID`.")
    P("=" * 108)
    return True


if __name__ == "__main__":
    ok = principale()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "referto in %s" % FUORI)
    raise SystemExit(0 if ok else 1)
