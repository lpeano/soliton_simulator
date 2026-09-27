r"""**UN BRACCIO del pilota della `PROVA 1`** — un seme, un processo (`STANDARD 1`).

*(criteri `V1`-`V6` di `doc/TASK_HISTORY/2026-09-27_pilota-prova1.md`, scritti **prima**.)*

**NON e' il run base.** Vedi la testa del task history: gli altri `SI` sono aperti.

**COME**, e ogni scelta e' quella che le regole impongono:

* **argv del DRIVER** (`_cli_flag.argv_del_driver`), scena `(ii)`(a), `POZZO_D` **acceso**
  *(e' il default del driver dal commit `aa64397`)*;
* avanzamento con **`_passo.passo_pieno`** (`H-P9`): **mai `net.step()` da solo**;
* **tutte le distanze LUNGO IL GRAFO pesate con `net.d`**, da `csv/_osservabile_p1.py`;
  **mai `pos`** — `A3-DISEGNO`;
* checkpoint `0, 40, 80, 120`;
* **le coppie di CONTROLLO sono FISSE**: scelte **una volta al passo 0** e poi **seguite**
  (`OP.controlli_fissi` + `OP.segui_controlli`). **La riscelta si tiene come DIAGNOSTICO**,
  perche' e' il difetto: `K5b` misura che porta l'osservabile a `~0` su un effetto vero del
  `-5 %`. *(`CTRL-RISCELTA`.)*

> ### ⚠ DUE PREMESSE DEL MANDATO **NON REGGONO**, e sono verificate dal sorgente
>
> **①** *«ridefinisci la regione dalla FASE, stesso criterio con cui la scena la costruisce»*:
> **quel criterio non esiste.** La scena costruisce la regione **da `pos`**
> (`idx = where(norm(pos - c) <= r)`) e **poi** le assegna la fase
> (`ph = _dphi()/2 + normal(0, 0.05)`). Il criterio di fase si **DERIVA** da cio' che la scena
> **scrive**: `|wrap(phi - _dphi()/2)| <= KAPPA * 0.05`. **`_dphi()/2` e `0.05` vengono dal
> codice; l'unica scelta e' `KAPPA`, e si CALIBRA al passo 0 dove la risposta e' NOTA.**
>
> **②** **LA FASE E' LA STESSA PER TUTTE E TRE LE REGIONI**, per decisione dichiarata di Luca
> *(commento `②❗` della scena: masse sfasate interferirebbero in modo distruttivo «dalla
> CONDIZIONE INIZIALE, non dalla dinamica»)*. **Quindi la fase NON PUO' separare le masse:**
> da' **un solo** insieme coerente. La separazione arriva dalla **CONTIGUITA' SUL GRAFO**
> *(componenti connesse del sottografo indotto)*, e l'assegnazione alla massa dalla
> **sovrapposizione massima** con la regione del passo 0. **E' dichiarato qui, non tacito.**

    python csv/_test_fork/_pilota_prova1_braccio.py --seme 11 --passi 120
    ...  --salva-stati            # gli stati del grafo ai checkpoint (LOCALI, `STATI-LOCALI`)
    ...  --salva-stati --ogni 2   # e i fotogrammi `pos`/`phi` ogni 2 passi (`VIDEO-SCENA`)

ASCII puro.
"""
import io
import json
import os
import sys

import numpy as np
from scipy.sparse.csgraph import connected_components, dijkstra

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402
import _passo                                                          # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

# ------------------------------------------------------------------ LE COSTANTI, TUTTE DICHIARATE
SIGMA_SCENA = 0.05      # la dispersione che LA SCENA scrive: non e' mia
KAPPA_PROVE = (2, 3, 4)  # i valori collaudati al passo 0, sulla risposta NOTA
TOLL_VARCO = 0.10       # «sul quasi-geodetica fra due masse»: entro il 10 % del cammino
MIN_COMPONENTE = 10     # una componente sotto 10 nodi non e' una massa: si conta a parte
MAX_QUANTILI = 1500     # oltre, le distanze interne si campionano (DETERMINISTICO, seme 0)


# ======================================================================= I MATTONI DI MISURA
def dmin(g, sorgenti):
    """La distanza di grafo dal PIU' VICINO fra `sorgenti`. Una Dijkstra, non `len(sorgenti)`."""
    s = np.asarray(sorted(set(int(x) for x in sorgenti)), int)
    if not len(s):
        return np.full(g.shape[0], np.inf)
    return dijkstra(g, directed=False, indices=s, min_only=True)


def wrap(x, dphi):
    """La distanza ANGOLARE sul dominio `[0, dphi)`: `phi` e `phi + dphi` sono lo STESSO punto."""
    y = np.mod(np.asarray(x, float), dphi)
    return np.minimum(y, dphi - y)


def regione_da_fase(net, dphi, kappa):
    """L'insieme COERENTE: `|wrap(phi - dphi/2)| <= kappa * SIGMA_SCENA`. **Uno solo, non tre.**"""
    return np.where(wrap(np.asarray(net.phi, float) - dphi / 2.0, dphi)
                    <= kappa * SIGMA_SCENA)[0]


def componenti_regione(g, idx, min_comp=MIN_COMPONENTE):
    """Le componenti CONNESSE del sottografo indotto su `idx`. **La contiguita' separa le masse.**"""
    idx = np.asarray(sorted(set(int(x) for x in idx)), int)
    if not len(idx):
        return [], 0
    nc, lab = connected_components(g[idx, :][:, idx], directed=False)
    fuori, scartati = [], 0
    for c in range(nc):
        m = idx[lab == c]
        if len(m) >= min_comp:
            fuori.append(m)
        else:
            scartati += len(m)
    fuori.sort(key=len, reverse=True)
    return fuori, scartati


def assegna_vicino(g, sel, dist, masse):
    """**`R-VICINO`** -- ogni nodo coerente va alla massa PIU' VICINA SUL GRAFO.

    Pareggi: la `k` MINORE. Regola dichiarata, non caso taciuto.

    WARN PERCHE' ESISTE UNA SECONDA REGOLA, e il collaudo al passo 0 l'ha IMPOSTA.
    `R-COMP` (le componenti connesse) **FALLISCE, MISURATO**: la contaminazione del vuoto
    **PONTA** le tre regioni in **UNA SOLA** componente da 1253 nodi, che finisce tutta su
    una massa e lascia le altre due a `n = 0`. Non e' una sorpresa da fuori: **la fase e'
    LA STESSA per tutte e tre** *(scelta dichiarata di Luca nella scena)*, quindi la fase
    **non le distingue**, e un ponte di ~200 nodi basta a fonderle.

    **E questa regola NON presuppone la risposta di `V5`:** l'etichetta dice **quale**
    massa; la MIGRAZIONE la misurano **sovrapposizione** e **spostamento del medoide**. Se
    la coerenza si spostasse di 5, quei nodi resterebbero etichettati con la massa
    d'origine e lo spostamento **lo direbbe**.
    """
    sel = np.asarray(sorted(set(int(x) for x in sel)), int)
    fuori = dict((k, np.array([], int)) for k in masse)
    if not len(sel) or not masse:
        return fuori, 0
    M = np.vstack([dist[k][sel] for k in masse])
    fin = np.isfinite(M).any(axis=0)
    lab = np.argmin(np.where(np.isfinite(M), M, np.inf), axis=0)
    for q, k in enumerate(masse):
        fuori[k] = np.asarray(sorted(sel[fin & (lab == q)]), int)
    return fuori, int(np.sum(~fin))


def assegna(comp, coorti0, masse):
    """Ogni componente va alla massa con cui si SOVRAPPONE PIU'. Regola dichiarata, non tacita.

    Una massa puo' restare senza componente *(e allora si dice)*; due componenti possono cadere
    sulla stessa massa *(e allora si UNISCONO, e si conta quante)*.
    """
    s0 = {k: set(int(x) for x in coorti0[k]) for k in masse}
    per_massa = {k: [] for k in masse}
    orfane = 0
    for m in comp:
        sm = set(int(x) for x in m)
        punteggi = [(len(sm & s0[k]), k) for k in masse]
        best, k = max(punteggi)
        if best == 0:
            orfane += len(m)
            continue
        per_massa[k].append(m)
    fuori = {}
    for k in masse:
        fuori[k] = (np.array(sorted(set(int(x) for c in per_massa[k] for x in c)), int)
                    if per_massa[k] else np.array([], int))
    return fuori, {k: len(per_massa[k]) for k in masse}, orfane


def precisione_richiamo(stimata, vera):
    """`(precisione, richiamo, F1)` di un insieme stimato contro la risposta NOTA del passo 0."""
    a, b = set(int(x) for x in stimata), set(int(x) for x in vera)
    if not a or not b:
        return 0.0, 0.0, 0.0
    tp = len(a & b)
    p, r = tp / len(a), tp / len(b)
    return p, r, (0.0 if p + r == 0 else 2 * p * r / (p + r))


def coerenza(phi_reg, dphi):
    """La coerenza della regione. **IL CRITERIO E' `coer_campo = |<e^{i phi}>|`.**

    * **`coer_campo = |<e^{i phi}>|`** — **IL CRITERIO.** E' la coerenza **come il campo la sente**,
      e non e' una convenzione: `Z118`/`Z120` misurano che **in 31 righe su 31** il campo legge
      `phi` da `exp`/`cos`/`sin`, dove `phi` e `phi + 2 pi` sono **lo stesso stato**.
    * **`coer_dominio = |<e^{i 2 pi phi / dphi}>|`** — **DIAGNOSTICO**: **crolla** quando i due
      fogli sono mescolati. La fisica del campo non li distingue; **la TORSIONE si'**.
    * **`foglio_0`, `foglio_1`** — **DIAGNOSTICO**: la frazione di nodi della regione per foglio,
      `floor(phi / 2 pi)` dentro il dominio `_dphi()`. Con `_dphi() = 2 pi` esiste **solo**
      `foglio_0`, e vale `1` per costruzione.

    *(Ritiro di Luca, 2026-09-27, di una propria correzione della stessa giornata.)*
    """
    p = np.asarray(phi_reg, float)
    if not len(p):
        return dict(coer_campo=float("nan"), coer_dominio=float("nan"),
                    foglio_0=float("nan"), foglio_1=float("nan"))
    fg = np.floor(np.mod(p, dphi) / (2.0 * np.pi)).astype(int)
    return dict(coer_campo=float(abs(np.mean(np.exp(1j * p)))),
                coer_dominio=float(abs(np.mean(np.exp(1j * 2.0 * np.pi * p / dphi)))),
                foglio_0=float(np.mean(fg == 0)),
                foglio_1=float(np.mean(fg == 1)))


def collaudo_coerenza(dphi=4.0 * np.pi):
    """**`K-FOGLIO`** — il caso a risposta NOTA: che cosa vede il CAMPO e che cosa vedono i FOGLI.

    **Il criterio `coer_campo` DEVE essere CIECO al foglio** *(e' il contenuto fisico di
    `Z118`/`Z120`: `exp(i(phi+2pi)) = exp(i phi)`)*; **il diagnostico `coer_dominio` DEVE
    accorgersene**. **E il caso che deve dare il valore OPPOSTO e' il piu' importante**
    (`P1-sexies`): se entrambi dessero `1`, il diagnostico non diagnosticherebbe nulla.
    """
    fuori = []
    meta = np.concatenate([np.full(500, dphi / 2.0), np.zeros(500)])
    c = coerenza(meta, dphi)
    fuori.append(("K-FOGLIO-a  meta' a 2pi, meta' a 0", c,
                  c["coer_campo"] > 0.999999,          # il CAMPO: un solo stato -> coerente
                  c["coer_dominio"] < 1e-12,           # i FOGLI: mescolati -> zero
                  abs(c["foglio_0"] - 0.5) < 1e-12))
    c = coerenza(np.full(1000, dphi / 2.0), dphi)
    fuori.append(("K-FOGLIO-b  tutti a 2pi (un foglio)", c,
                  c["coer_campo"] > 0.999999, c["coer_dominio"] > 0.999999,
                  c["foglio_1"] > 0.999999))
    c = coerenza(np.full(1000, 0.0), dphi)
    fuori.append(("K-FOGLIO-c  tutti a 0 (l'altro foglio)", c,
                  c["coer_campo"] > 0.999999, c["coer_dominio"] > 0.999999,
                  c["foglio_0"] > 0.999999))
    c = coerenza(np.random.default_rng(0).random(20000) * dphi, dphi)
    fuori.append(("K-FOGLIO-d  fasi CASUALI sul dominio", c,
                  c["coer_campo"] < 0.03, c["coer_dominio"] < 0.03,
                  abs(c["foglio_0"] - 0.5) < 0.02))
    return fuori


def stampa_collaudo_coerenza(P=print):
    """Stampa `K-FOGLIO` e restituisce quante righe passano su quattro."""
    P("=" * 104)
    P("`K-FOGLIO` -- IL CRITERIO E' CIECO AL FOGLIO, IL DIAGNOSTICO NO   (caso a risposta NOTA)")
    P("=" * 104)
    P("  Il criterio e' `coer_campo = |<e^{i phi}>|`: in 31 righe su 31 il campo legge `phi` da")
    P("  `exp`/`cos`/`sin` (`Z118`/`Z120`), quindi `phi` e `phi+2pi` SONO LO STESSO STATO.")
    P("")
    ok = 0
    for nome, c, a1, a2, a3 in collaudo_coerenza():
        buono = bool(a1 and a2 and a3)
        ok += 1 if buono else 0
        P("  %-37s coer_campo %.6f   coer_dominio %.6f   foglio_0 %.3f   %s"
          % (nome, c["coer_campo"], c["coer_dominio"], c["foglio_0"],
             "PASS" if buono else "** FAIL **"))
    P("")
    P("  LA RIGA CHE CONTA E' `K-FOGLIO-a`: meta' a 2pi e meta' a 0 danno `coer_campo = 1`")
    P("  -- perche' per il CAMPO sono lo stesso stato -- e `coer_dominio = 0`, perche' i due")
    P("  FOGLI sono mescolati. Se dessero lo stesso numero, il diagnostico sarebbe inutile.")
    P("")
    P("  %d/4" % ok)
    return ok


def forma(g, idx, phi, dphi, seme_camp=0):
    """`V6` — LA FORMA, sulle distanze di GRAFO: `n`, raggio, quantili interni, coerenza."""
    idx = np.asarray(sorted(set(int(x) for x in idx)), int)
    o = {"n": int(len(idx))}
    if len(idx) < 2:
        o.update(raggio=float("nan"), p10=float("nan"), p50=float("nan"), p90=float("nan"),
                 coer_campo=float("nan"), coer_dominio=float("nan"),
                 foglio_0=float("nan"), foglio_1=float("nan"), medoide=-1,
                 nota="regione con meno di 2 nodi")
        return o
    # LA COERENZA DELLA MASSA E' `coer_campo = |<e^{i phi}>|`, ed E' UN FATTO MISURATO NEL
    #   SIMULATORE, non una convenzione: il commento di `FASE_2PI` (`:1300`) porta `Z118`/`Z120`
    #   -- **in 31 righe su 31 il campo legge `phi` da `exp`/`cos`/`sin`**, e li'
    #   `exp(i(phi + 2 pi)) = exp(i phi)`. **Per la fisica del campo `phi` e `phi + 2 pi` SONO LO
    #   STESSO STATO**, e la doppia copertura vive nel **SEGNO** dello spinore (`_spinor_lift`,
    #   `sign(perc_chi)`) e nei **MEZZI ANGOLI** (`exp(-0.5i ...)`), **non in `phi`**.
    #   Quindi `|<e^{i phi}>|` **non confonde** due stati diversi: li identifica perche' la fisica
    #   li identifica.
    #
    #   WARN E I DUE DIAGNOSTICI SERVONO COMUNQUE, perche' `_dphi() = 4 pi` e quindi `phi` porta
    #   un'etichetta di FOGLIO che il campo non legge e **la TORSIONE distingue**:
    #     `coer_dominio` = |<e^{i 2pi phi/dphi}>|  DIAGNOSTICO: crolla se i fogli sono MESCOLATI
    #     `foglio_0`, `foglio_1`                   DIAGNOSTICO: la frazione di nodi della regione
    #                                              per foglio, `floor(phi / 2 pi)`
    #
    #   (RITIRO DI LUCA, 2026-09-27: la mattina aveva corretto il criterio in `coer_dominio`, e
    #    nel pomeriggio ha annullato la propria correzione citando `Z118`/`Z120`. Ho VERIFICATO
    #    la premessa dal sorgente prima di annullare. -> voce `COER-4PI`.)
    o.update(coerenza(np.asarray(phi, float)[idx], dphi))
    sub = g[idx, :][:, idx]
    camp = idx
    if len(idx) > MAX_QUANTILI:
        rng = np.random.default_rng(seme_camp)          # campionamento DETERMINISTICO
        pos_c = np.sort(rng.choice(len(idx), size=MAX_QUANTILI, replace=False))
        o["campionati"] = int(MAX_QUANTILI)
    else:
        pos_c = np.arange(len(idx))
    d = dijkstra(sub, directed=False, indices=pos_c)
    fin = np.isfinite(d)
    somma = np.where(fin, d, 0.0).sum(axis=1)
    somma[fin.sum(axis=1) < fin.sum(axis=1).max()] = np.inf
    kmed = int(np.argmin(somma))
    o["medoide"] = int(idx[pos_c[kmed]])
    riga = d[kmed]
    o["raggio"] = float(np.mean(riga[np.isfinite(riga)]))
    v = d[np.isfinite(d)]
    v = v[v > 0]
    if len(v):
        o["p10"], o["p50"], o["p90"] = [float(x) for x in np.percentile(v, [10, 50, 90])]
    else:
        o["p10"] = o["p50"] = o["p90"] = float("nan")
    o["raggiungibili"] = int(fin.sum(axis=1).max())
    del camp
    return o


# ======================================================================= LA SPIA DELLE NASCITE
class Spia(object):
    """`V3`/`V4` — **chi crea nodi, quanti, e le SCORCIATOIE di Schwinger.**

    **Come si separano mitosi e Schwinger SENZA toccare il simulatore:** dentro `mitosi()` i
    figli della mitosi sono appesi **prima** e gli antinodi Schwinger **dopo**
    (`k = self.n + arange(nc)`, `:6365`), e il simulatore conta gia' gli antinodi in
    `_g_nati_schwinger` (`:6396`). Quindi, in UNA chiamata:
        schwinger = [n1 - dsch, n1)        mitosi = [n0, n1 - dsch)
    **La scorciatoia** *(`A3-DISEGNO`)*: l'antinodo aggiunge il cammino `aa -> k -> bb` lungo
    `2*dd` **SENZA togliere** l'arco `(aa, bb)` (`:6413-6416`), quindi e' una scorciatoia **solo
    se `2*dd < d(aa,bb)`**. `aa` e `bb` si RILEGGONO dagli archi appesi, `d(aa,bb)` dallo stato
    di PRIMA della chiamata.
    """

    def __init__(self, S, net):
        self.S, self.net = S, net
        self.per_chiamata = {}
        self.nascite = []            # (passo, tipo, primo, ultimo+1)
        self.schw = dict(coppie=0, scorciatoie=0, arco_non_trovato=0, ambigui=0,
                         dd=[], d_arco=[])
        self.originali = {}

    def installa(self):
        for tipo, nome in _passo.ordine():
            if tipo != "metodo":
                continue
            self.originali[nome] = getattr(self.net, nome)
            self.per_chiamata[nome] = 0
            setattr(self.net, nome, self._avvolgi(nome))

    def _avvolgi(self, nome):
        orig = self.originali[nome]
        net = self.net

        def dentro(*A, **K):
            n0 = int(net.n)
            s0 = int(getattr(net, "_g_nati_schwinger", 0))
            if nome == "mitosi":
                pre = (np.asarray(net.i).copy(), np.asarray(net.j).copy(),
                       np.asarray(net.d, float).copy())
            r = orig(*A, **K)
            n1 = int(net.n)
            if n1 > n0:
                self.per_chiamata[nome] += (n1 - n0)
                dsch = int(getattr(net, "_g_nati_schwinger", 0)) - s0
                if nome == "mitosi" and dsch > 0:
                    self.nascite.append((self.passo, "mitosi", n0, n1 - dsch))
                    self.nascite.append((self.passo, "schwinger", n1 - dsch, n1))
                    self._scorciatoie(pre, dsch)
                else:
                    self.nascite.append((self.passo, nome, n0, n1))
            return r
        return dentro

    def _scorciatoie(self, pre, dsch):
        """Per ogni coppia Schwinger: `2*dd` contro il `d` dell'arco `(aa, bb)` di PRIMA."""
        net = self.net
        i_b, j_b, d_b = pre
        ii, jj = np.asarray(net.i, int), np.asarray(net.j, int)
        dd_arr = np.asarray(net.d, float)
        # gli ULTIMI 2*dsch archi sono `[aa -> k]` (primi dsch) e `[k -> bb]` (ultimi dsch)
        if len(ii) < 2 * dsch:
            self.schw["arco_non_trovato"] += dsch
            return
        aa = ii[-2 * dsch:-dsch]
        bb = jj[-dsch:]
        dd = dd_arr[-2 * dsch:-dsch]
        self.schw["coppie"] += int(dsch)
        for t in range(dsch):
            a, b, q = int(aa[t]), int(bb[t]), float(dd[t])
            m = ((i_b == a) & (j_b == b)) | ((i_b == b) & (j_b == a))
            cand = d_b[m]
            if not len(cand):
                self.schw["arco_non_trovato"] += 1
                continue
            if len(cand) > 1:
                self.schw["ambigui"] += 1
            d_arco = float(np.min(cand))     # il piu' CORTO: il confronto piu' SEVERO
            self.schw["dd"].append(q)
            self.schw["d_arco"].append(d_arco)
            if 2.0 * q < d_arco:
                self.schw["scorciatoie"] += 1


# ============================================== IL SALVATAGGIO (LOCALE, mai in git)
def _blob_sim():
    """Lo `sha1` dei BYTE GREZZI del simulatore: la convenzione dei presidi."""
    import hashlib
    with open(os.path.join(RADICE, "soliton_simulator.py"), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def cartella_stati():
    """`csv/_test_fork/_pilota_prova1/stati/` -- **in `.gitignore`** (`STATI-LOCALI`)."""
    d = os.path.join(_QUI, "_pilota_prova1", "stati")
    if not os.path.isdir(d):
        os.makedirs(d)
    return d


def salva_stato(net, seme, passo, blob):
    """LO STATO DEL GRAFO a un checkpoint: i soli campi che servono al CAMMINO e alla FASE.

    **Non e' uno snapshot del simulatore** *(quelli sono `.pkl` da ~18 MB)*: sono `i`, `j`,
    `d`, `phi`, `pos` e `n`. **Resta in LOCALE** e in git ne vanno `sha1`, percorso e comando.

    ⚠ **PURE-READ:** legge e basta. Non tocca `psi`, non tocca l'RNG, non avanza niente.
    """
    p = os.path.join(cartella_stati(), "stato_seme%d_passo%06d.npz" % (seme, passo))
    np.savez_compressed(
        p, i=np.asarray(net.i, np.int32), j=np.asarray(net.j, np.int32),
        d=np.asarray(net.d, np.float64), phi=np.asarray(net.phi, np.float64),
        pos=np.asarray(net.pos, np.float64), n=np.int64(net.n),
        passo=np.int64(passo), seme=np.int64(seme), blob=np.str_(blob))
    return p


def salva_fotogramma(net, seme, passo, blob, arco_max=24000):
    """IL FOTOGRAMMA per il video (`VIDEO-SCENA`). **Piccolo, e PURE-READ.**

    **Che cosa porta, e perche' ciascuna cosa:**

    * `pos`, `phi` -- il pannello di **destra**: `cos(phi - dphi/2)`, la coerenza con le masse;
    * `phi_g` *(per nodo)* e `dpozzo` *(per arco)* -- il pannello di **sinistra**, che e' **la
      vista di sempre del simulatore**: nodi `magma` su `phi_g`, archi `plasma` su `|dpozzo|`;
    * `ii`, `jj` -- gli estremi degli archi disegnati. **Il taglio a `24000` NON e' mio: e' quello
      della vista del simulatore** (`indici = flatnonzero(valid)[:24000]`), e riprodurlo e' l'unico
      modo di mostrare *la vista di sempre* invece di una diversa.

    ⚠ **PURE-READ, e su due punti non e' gratis:**

    1. **`Ivis` si legge dalla `psi` ESISTENTE**, senza chiamare `calcola_psi()`: ricalcolarla
       cambierebbe `self.psi`, che `step()` fotografa in `_psi_prec` al passo dopo -- e' il difetto
       che `MASSA-ID` ha trovato, e qui **non lo si rifa'**.
    2. **`pozzo_grafo` INCREMENTA due contatori** (`_pozzo_d_nonpos`, `_pozzo_d_tot`) nel ramo a
       flag acceso. Si **fotografano e si ripristinano**, cosi' il run riporta i SUOI numeri e non
       quelli gonfiati dal diagnostico.
    """
    n = int(net.n)
    Ivis = (np.abs(net.psi[:n]) ** 2
            if hasattr(net, "psi") and len(net.psi) >= n else np.zeros(n))
    # (2) fotografia dei contatori che `pozzo_grafo` tocca
    _c1 = getattr(net, "_pozzo_d_nonpos", None)
    _c2 = getattr(net, "_pozzo_d_tot", None)
    phi_g, _m, dpozzo_tutti = net.pozzo_grafo(Ivis)
    for _k, _v in (("_pozzo_d_nonpos", _c1), ("_pozzo_d_tot", _c2)):
        if _v is None:
            if hasattr(net, _k):
                delattr(net, _k)
        else:
            setattr(net, _k, _v)
    valid = ((net.i < n) & (net.j < n)) if len(net.i) else np.zeros(0, bool)
    # ⚠ CAMPIONE CASUALE A SEME FISSO, non i PRIMI per indice (`ARCHI-PRIMI`).
    #   `[:arco_max]` e' quello che fa la vista del simulatore (:7685), e MISURATO produce una
    #   distorsione TOTALE: il 100 % degli archi disegnati finisce in UN quadrante, baricentro
    #   (-4.392, -4.283) contro (0, 0) di tutti i nodi. L'indice d'arco correla con l'ordine di
    #   semina, che correla con la posizione.
    #   IL SEME E' FISSO (0) perche' due fotogrammi vicini devono mostrare GLI STESSI archi: un
    #   campione che cambia a ogni passo farebbe sfarfallare il disegno e sembrare dinamica
    #   cio' che e' rumore di campionamento.
    _v = np.flatnonzero(valid)
    if len(_v) > arco_max:
        indici = np.sort(np.random.default_rng(0).choice(_v, size=arco_max, replace=False))
    else:
        indici = _v
    na = len(indici)
    ii = np.asarray(net.i[indici], np.int32) if na else np.zeros(0, np.int32)
    jj = np.asarray(net.j[indici], np.int32) if na else np.zeros(0, np.int32)
    dpz = (np.abs(np.asarray(dpozzo_tutti, float)[:na]).astype(np.float32) if na
           else np.zeros(0, np.float32))
    p = os.path.join(cartella_stati(), "frame_seme%d_passo%06d.npz" % (seme, passo))
    np.savez_compressed(
        p, pos=np.asarray(net.pos[:n], np.float32), phi=np.asarray(net.phi[:n], np.float32),
        phi_g=np.asarray(phi_g, np.float32), dpozzo=dpz, ii=ii, jj=jj,
        n=np.int64(n), na=np.int64(na), passo=np.int64(passo), seme=np.int64(seme),
        dphi=np.float64(net._dphi()), blob=np.str_(blob))
    return p


# ======================================================================= UN CHECKPOINT
def checkpoint(S, net, coorti0, rr, dphi, kappa, spia, passo, LAM=0.8, calibra=False,
               stato=None):
    o = OP.misura(net, coorti0)                     # LO STRUMENTO UFFICIALE, pesi = `net.d`
    # `V1` -- I PUNTI DI CONTROLLO, **FISSI**: scelti UNA VOLTA al passo 0 e poi SEGUITI.
    #   `OP.controlli()` RISCEGLIE a ogni istante, e con la riscelta l'osservabile va a ZERO
    #   PER COSTRUZIONE (`K5b`: su un effetto vero del -5 % legge ~0 %). Si tiene ANCHE la
    #   riscelta, ma come DIAGNOSTICO: cosi' il difetto e' visibile nei dati del run stesso.
    #   *(`CTRL-RISCELTA`, difetto trovato da Luca il 2026-09-27.)*
    if stato is not None and "fissi" not in stato:
        stato["fissi"] = OP.controlli_fissi(o, coorti0, rr)
    fissi = (stato or {}).get("fissi") or OP.controlli_fissi(o, coorti0, rr)
    ctrl = OP.controlli(o, coorti0, rr)             # DIAGNOSTICO: la RISCELTA, che e' il difetto
    g = o["_g"]
    masse = o["masse"]
    # la distanza di grafo dalla regione del passo 0 di OGNI massa: serve a `R-VICINO`
    # (etichettare i nodi coerenti) E alle zone delle nascite. UNA Dijkstra per massa.
    dist = {k: dmin(g, coorti0[k]) for k in masse}
    fuori = {"passo": int(passo), "n": int(net.n), "archi": int(len(net.i)),
             "componenti_grafo": int(o["componenti"]),
             "coppie_passo0": dict((k, {"centro_centro": float(v["centro_centro"]),
                                        "insieme_insieme": float(v["insieme_insieme"])})
                                   for k, v in o["coppie"].items()),
             "centri_passo0": dict((k, int(v)) for k, v in o["centri"].items()),
             "controlli": {"trovati": int(ctrl.get("trovati", 0)),
                           "candidati_lontani": int(ctrl.get("candidati_lontani", 0)),
                           "metro_lontananza": float(ctrl.get("metro_lontananza", float("nan")))
                           if ctrl.get("metro_lontananza") is not None else float("nan"),
                           "coppie": dict((k, {"distanza": float(v["distanza"]),
                                               "bersaglio": float(v["bersaglio"]),
                                               "scarto_relativo": float(v["scarto_relativo"]),
                                               "entro_toll": bool(v["entro_toll"]),
                                               "nodo_a": int(v["nodo_a"]),
                                               "nodo_b": int(v["nodo_b"])})
                                          for k, v in ctrl.get("coppie", {}).items()),
                           "nota": ctrl.get("nota", ""),
                           "MARCHIO": "RISCELTA: diagnostico, NON l'osservabile (K5b)"}}

    # i controlli FISSI: la distanza fra GLI STESSI nodi. Le esclusioni si CONTANO.
    sel_coer = regione_da_fase(net, dphi, kappa)
    seg = OP.segui_controlli(o, fissi, dentro_coerenti=sel_coer)
    fuori["controlli_fissi"] = {
        "trovate": fissi.get("trovate", {}),
        "candidati_lontani": int(fissi.get("candidati_lontani", 0)),
        "metro_lontananza": float(fissi.get("metro_lontananza", float("nan"))),
        "quante_chieste": int(fissi.get("quante_chieste", 0)),
        "esclusi_dentro": int(seg["esclusi_dentro"]),
        "esclusi_componenti": int(seg["esclusi_componenti"]),
        "esclusi_inf": int(seg["esclusi_inf"]),
        "usate": int(seg["usate"]), "totali": int(seg["totali"]),
        "coppie": seg["coppie"]}

    # ---------------------------------------------------- `V5`: LA CALIBRAZIONE (solo al passo 0)
    if calibra:
        tab = []
        dcal = dist
        nreg = sum(len(coorti0[k]) for k in masse)
        nv = int(len(coorti0.get("vuoto", [])))
        tutte = [x for k in masse for x in coorti0[k]]
        for kp in KAPPA_PROVE:
            sel = regione_da_fase(net, dphi, kp)
            comp, scart = componenti_regione(g, sel)
            r_comp, quante, orf_c = assegna(comp, coorti0, masse)
            r_vic, orf_v = assegna_vicino(g, sel, dcal, masse)
            voce = {"kappa": int(kp), "selezionati": int(len(sel)),
                    "componenti": int(len(comp)), "scartati_piccoli": int(scart),
                    "orfani_comp": int(orf_c), "orfani_vicino": int(orf_v), "regole": {}}
            # LA CONTAMINAZIONE COL SUO VALORE PREVISTO: `2*kappa*sigma/dphi` del vuoto.
            # E' il valore SOTTO IPOTESI NULLA del criterio di fase: senza di esso
            # <<1514 selezionati>> non dice se il criterio funzioni.
            _p, rich, _f = precisione_richiamo(sel, tutte)
            voce["contaminanti_misurati"] = float(len(sel) - rich * nreg)
            voce["contaminanti_previsti"] = float(2.0 * kp * SIGMA_SCENA / dphi * nv)
            for nome, reg in (("R-COMP", r_comp), ("R-VICINO", r_vic)):
                v = {"per_massa": {}}
                pmin = rmin = 1.0
                for k in masse:
                    p, r, f1 = precisione_richiamo(reg[k], coorti0[k])
                    v["per_massa"][k] = {"n": int(len(reg[k])), "precisione": p,
                                         "richiamo": r, "f1": f1}
                    pmin, rmin = min(pmin, p), min(rmin, r)
                v["precisione_min"], v["richiamo_min"] = pmin, rmin
                v["f1_min"] = min(v["per_massa"][k]["f1"] for k in masse) if masse else 0.0
                v["masse_vuote"] = int(sum(1 for k in masse if len(reg[k]) == 0))
                voce["regole"][nome] = v
            tab.append(voce)
        fuori["calibrazione"] = tab

    # ------------------------------------------- `V5`: la regione DALLA FASE, al `kappa` fissato
    sel = sel_coer                 # gia' calcolata sopra per le esclusioni dei controlli
    comp, scart = componenti_regione(g, sel)
    reg, orfane = assegna_vicino(g, sel, dist, masse)     # `R-VICINO`: la regola che REGGE
    quante = dict((k, 1 if len(reg[k]) else 0) for k in masse)
    fuori["fase"] = {"kappa": int(kappa), "regola": "R-VICINO",
                     "selezionati": int(len(sel)), "componenti": int(len(comp)),
                     "scartati_piccoli": int(scart), "orfani": int(orfane), "per_massa": {}}
    for k in masse:
        s0 = set(int(x) for x in coorti0[k])
        sk = set(int(x) for x in reg[k])
        med0 = o["centri"][k]
        m1, _p, _r = medoide_di(g, reg[k])
        spost = float(dijkstra(g, directed=False, indices=[med0])[0, m1]) \
            if (med0 >= 0 and m1 >= 0) else float("nan")
        fuori["fase"]["per_massa"][k] = {
            "n": int(len(sk)), "componenti": int(quante[k]),
            "sovrapposizione": (len(sk & s0) / len(s0)) if s0 else float("nan"),
            "medoide_passo0": int(med0), "medoide_fase": int(m1),
            "spostamento_medoide": spost}

    # la distanza fra le masse SULLE REGIONI ATTUALI, per confrontarla con quella del passo 0
    fuori["coppie_fase"] = {}
    for x in range(len(masse)):
        for y in range(x + 1, len(masse)):
            ka, kb = masse[x], masse[y]
            ca = fuori["fase"]["per_massa"][ka]["medoide_fase"]
            cb = fuori["fase"]["per_massa"][kb]["medoide_fase"]
            dc = float(dijkstra(g, directed=False, indices=[ca])[0, cb]) \
                if (ca >= 0 and cb >= 0) else float("nan")
            fuori["coppie_fase"]["%s|%s" % (ka, kb)] = {
                "centro_centro": dc,
                "insieme_insieme": OP.fra_insiemi(g, reg[ka], reg[kb])
                if (len(reg[ka]) and len(reg[kb])) else float("nan")}

    # ------------------------------------------------------------------------ `V6`: LA FORMA
    fuori["forma_passo0"] = dict((k, forma(g, coorti0[k], net.phi, dphi)) for k in masse)
    fuori["forma_fase"] = dict((k, forma(g, reg[k], net.phi, dphi)) for k in masse)

    # ------------------------------------------- `V3`: DOVE SONO I NODI (e dove sono NATI)
    # WARN IL METRO DI <<DENTRO UNA MASSA>> E' `LAM`, NON `r_regione` -- e il collaudo al
    #   passo 0 ha denunciato l'altro: con `r_regione = 4.096` su distanze di GRAFO
    #   risultavano <<dentro una massa>> **7427 nodi su 12802 (58 %)** e il varco era
    #   **VUOTO**, cioe' il criterio non distingueva niente. `r_regione` e' un raggio su
    #   `pos`: trasportarlo sul grafo era un ERRORE DI UNITA'.
    #   `LAM` e' la scala minima del sistema (`A13`) ed e' la lunghezza d'arco piu' corta
    #   che esista: **un nodo entro UN arco minimo dalla regione ne sta sul BORDO.**
    #   Zero manopole.
    in_massa = {k: (dist[k] <= LAM) for k in masse}
    dentro_qualcuna = np.zeros(int(net.n), bool)
    for k in masse:
        dentro_qualcuna |= in_massa[k]
    varco = np.zeros(int(net.n), bool)
    for nome, v in o["coppie"].items():
        ka, kb = nome.split("|")
        D = v["insieme_insieme"]
        if not np.isfinite(D) or D <= 0:
            continue
        varco |= (~dentro_qualcuna) & np.isfinite(dist[ka]) & np.isfinite(dist[kb]) \
            & ((dist[ka] + dist[kb]) <= (1.0 + TOLL_VARCO) * D)
    zona = np.where(dentro_qualcuna, 0, np.where(varco, 1, 2))      # 0 massa, 1 varco, 2 vuoto
    fuori["zone_tutti"] = {"massa": int(np.sum(zona == 0)), "varco": int(np.sum(zona == 1)),
                           "vuoto": int(np.sum(zona == 2)), "metro_massa": float(LAM),
                           "toll_varco": float(TOLL_VARCO)}
    nasc = {"mitosi": [0, 0, 0], "schwinger": [0, 0, 0], "altro": [0, 0, 0]}
    for (pas, tipo, p0, p1) in spia.nascite:
        if pas > passo:
            continue
        t = tipo if tipo in ("mitosi", "schwinger") else "altro"
        idx = np.arange(p0, min(p1, int(net.n)))
        if not len(idx):
            continue
        for z in (0, 1, 2):
            nasc[t][z] += int(np.sum(zona[idx] == z))
    fuori["nascite_per_zona"] = {t: {"massa": v[0], "varco": v[1], "vuoto": v[2]}
                                 for t, v in nasc.items()}
    # I DATI GREZZI accanto alla classificazione, cosi' chi legge non e' obbligato a
    # fidarsi del metro (`A8`): la distanza dei NATI dalla massa piu' vicina.
    if masse:
        dtut = np.min(np.vstack([dist[k] for k in masse]), axis=0)
        nati = np.array(sorted(set(int(x) for (pa, ti, p0, p1) in spia.nascite
                                   if pa <= passo
                                   for x in range(p0, min(p1, int(net.n))))), int)
        if len(nati):
            v = dtut[nati]
            v = v[np.isfinite(v)]
            if len(v):
                fuori["nati_distanza_massa"] = dict(
                    n=int(len(v)),
                    p05=float(np.percentile(v, 5)), p50=float(np.percentile(v, 50)),
                    p95=float(np.percentile(v, 95)), minimo=float(np.min(v)))
    fuori["nascite_per_chiamata"] = dict(spia.per_chiamata)
    fuori["schwinger"] = {"coppie": spia.schw["coppie"],
                          "scorciatoie": spia.schw["scorciatoie"],
                          "arco_non_trovato": spia.schw["arco_non_trovato"],
                          "ambigui": spia.schw["ambigui"]}
    if spia.schw["dd"]:
        dd = np.asarray(spia.schw["dd"], float)
        da = np.asarray(spia.schw["d_arco"], float)
        fuori["schwinger"].update(
            dd_mediano=float(np.median(dd)), d_arco_mediano=float(np.median(da)),
            rapporto_mediano=float(np.median(2.0 * dd / np.maximum(da, 1e-300))),
            rapporto_min=float(np.min(2.0 * dd / np.maximum(da, 1e-300))))
    return fuori


def medoide_di(g, idx):
    return OP.medoide(g, idx)


# ======================================================================= IL BRACCIO
def principale(seme, passi, cps, out, salva=False, ogni=0):
    _S0, argv = _cli_flag.argv_del_driver(
        extra=["--seme=%d" % seme],
        dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_pilota")
    S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
    S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    dati = S.test["dati"]
    coorti0 = dict((k, np.asarray(v, int).copy()) for k, v in dati["coorti"].items())
    rr = float(dati["scena_ii"]["r_regione"])
    dphi = float(net._dphi())
    spia = Spia(S, net)
    spia.passo = 0
    spia.installa()

    # `VIDEO-SCENA` / `STATI-LOCALI`: il blob del simulatore accompagna ogni file salvato,
    # cosi' un `.npz` rimasto li' da un run vecchio si riconosce SENZA fidarsi della data.
    _blob = _blob_sim()
    fuori = {"seme": int(seme), "passi": int(passi), "checkpoint": list(cps),
             "salvataggio": bool(salva), "ogni": int(ogni), "blob_sim": _blob,
             "pozzo_d": bool(S.POZZO_D), "sep": float(S._NMASSE_VIDEO["sep"]),
             "r_regione": rr, "dphi": dphi, "LAM": float(S.LAM),
             "sigma_scena": SIGMA_SCENA, "n0": int(net.n),
             "coorti0": dict((k, int(len(v))) for k, v in coorti0.items()),
             "blocchi": []}

    LAM = float(S.LAM)
    stato = {}                     # ci vivono le coppie di controllo FISSE, scelte al passo 0
    b0 = checkpoint(S, net, coorti0, rr, dphi, KAPPA_PROVE[0], spia, 0,
                    LAM=LAM, calibra=True, stato=stato)
    # ⚠ LA REGOLA DI SCELTA DI `KAPPA` E' SCRITTA PRIMA DI GUARDARE: il piu' PICCOLO fra
    #   `KAPPA_PROVE` col richiamo >= 0.99 su OGNI massa; se nessuno ce l'ha, quello col
    #   `f1` minimo piu' alto, **e si dichiara che nessuno arrivava a 0.99**.
    tab = b0["calibrazione"]
    ok = [v for v in tab if v["regole"]["R-VICINO"]["richiamo_min"] >= 0.99]
    if ok:
        kappa = int(min(v["kappa"] for v in ok))
        regola = "il piu' piccolo `kappa` con richiamo >= 0.99 su ogni massa"
    else:
        kappa = int(max(tab, key=lambda v: v["regole"]["R-VICINO"]["f1_min"])["kappa"])
        regola = ("NESSUN `kappa` raggiunge richiamo 0.99: si prende il `f1` minimo piu' alto, "
                  "e il criterio di fase va letto come LIMITE")
    fuori["kappa"] = kappa
    fuori["kappa_regola"] = regola
    # il passo 0 si RIFA' col `kappa` scelto, cosi' il blocco 0 e i seguenti sono OMOGENEI
    fuori["blocchi"].append(
        checkpoint(S, net, coorti0, rr, dphi, kappa, spia, 0, LAM=LAM, calibra=True,
                   stato=stato))

    if salva:
        # le COORTI del passo 0: servono al BORDO del video (`V3`). Indici, non taglie.
        np.savez_compressed(
            os.path.join(cartella_stati(), "coorti_seme%d.npz" % seme),
            **dict((k, np.asarray(v, np.int32)) for k, v in coorti0.items()))
        fuori["stati"] = [salva_stato(net, seme, 0, _blob)]
        fuori["frames"] = ([salva_fotogramma(net, seme, 0, _blob)] if ogni else [])
    if hasattr(S, "passo_test"):
        S.passo_test()
    for p in range(1, int(passi) + 1):
        spia.passo = p
        _passo.passo_pieno(S, net)              # `H-P9`: mai `net.step()` da solo
        if salva and ogni and (p % ogni == 0):
            fuori["frames"].append(salva_fotogramma(net, seme, p, _blob))
        if salva and p in cps:
            fuori["stati"].append(salva_stato(net, seme, p, _blob))
        if p in cps:
            fuori["blocchi"].append(
                checkpoint(S, net, coorti0, rr, dphi, kappa, spia, p, LAM=LAM,
                           stato=stato))
    fuori["n_finale"] = int(net.n)
    io.open(out, "w", encoding="utf-8", newline=chr(10)).write(
        json.dumps(fuori, sort_keys=True, indent=1, default=float))
    print("OK seme %d  n %d -> %d  kappa %d  schwinger %d/%d scorciatoie"
          % (seme, fuori["n0"], fuori["n_finale"], kappa,
             spia.schw["scorciatoie"], spia.schw["coppie"]))


if __name__ == "__main__":
    A = sys.argv[1:]

    def opz(nome, dflt):
        return A[A.index(nome) + 1] if nome in A else dflt
    seme = int(opz("--seme", "11"))
    passi = int(opz("--passi", "120"))
    cps = sorted(set(int(x) for x in opz("--checkpoint", "0,40,80,120").split(",")))
    dest = os.path.join(_QUI, "_pilota_prova1", "seme_%d" % seme)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    principale(seme, passi, [c for c in cps if c > 0],
               opz("--out", os.path.join(dest, "misura.json")),
               salva=("--salva-stati" in A), ogni=int(opz("--ogni", "0")))
