# -*- coding: utf-8 -*-
"""`M4` — LA MISURA DELLE PLAQUETTE *(l'opzione `P` di Luca)*, in **SOLA LETTURA**.

*(Mandato di Luca del 2026-10-06, integrazione. ### **Criteri fissati PRIMA della corsa.**
Il mandato dice: «questa misura NON sceglie un'opzione. Riporta i numeri e l'unica
affermazione permessa e' descrittiva.» ### **Lo strumento non scrive raccomandazioni.**)*

### 📌 **PERCHE' GIRA SULLA STESSA CORSA DI `M1`-`M3`, e lo DICHIARO**

Il mandato dice *«uno strumento SEPARATO, committato prima della sua corsa, che gira DOPO la
corsa `M1`-`M3` ### **(o sulla stessa, se lo strumento non e' ancora stato committato: in
quel caso dichiaralo)**»*. ### ✔ **Lo strumento di `M1`-`M3` NON era ancora committato
quando l'integrazione e' arrivata**, quindi `M4` entra ### **nella stessa corsa**: un file
separato, un osservatore separato, un json separato, ### **una corsa sola.**

### LA PLAQUETTE: **un triangolo con tutti e tre gli archi presenti**

**L'enumerazione, e perche' e' corretta UNA VOLTA SOLA per triangolo:** si scorre il nodo
`u`, si prendono i suoi vicini ### **di indice MAGGIORE**, e per ogni coppia `(v, w)` con
`v < w` si chiede se `(v, w)` e' un arco. ### **Cosi' ogni triangolo si trova ESATTAMENTE
una volta, quando `u` e' il suo vertice MINIMO.** *(Misurato al passo `1`: `5534011`
plaquette, `1.46 s`; e il conto indipendente `somma su archi dei vicini comuni / 6` da' lo
### **stesso numero**.)*

### ⛔ **IL SEGNO DI UNA PLAQUETTE E' ARBITRARIO, IL PRODOTTO COL VERSORE NO**

| | |
|---|---|
| scambio due vertici | la circolazione ### **cambia segno** |
| e la normale | ### **cambia segno anche lei** |
| ### ✔ **quindi `(Σ tw) · n̂`** | ### **NON cambia: il PRODOTTO e' invariante, ciascun fattore da solo NO** |

> ### ⛔ **PER QUESTO `(b)` MISURA IL MODULO `|Σ tw|`** *(il segno, da solo, non vuol dire
> niente)* ### **e `(c)` misura il VETTORE.** ### **E `R_k` resta un ASSE, non un verso:
> l'invarianza non regala il segno.**

### LA CIRCOLAZIONE, **con la convenzione degli archi del simulatore**

Tutti gli archi hanno ### **`i < j`** *(misurato: `471564` su `471564`)*, quindi per il
triangolo `u < v < w` il cammino `u -> v -> w -> u` da':

### ⛔ **ANNOTAZIONE DEL 2026-10-07: LA FRASE QUI SOPRA E' SMENTITA, e resta scritta
### perche' il codice qui sotto NON la usa piu'.** *(par.8: si annota, non si riscrive)*
  ### **La misura `471564 su 471564` era fatta ai passi `0`, `1` e `2`, cioe' PRIMA della
  prima nascita (`216`)**, e ### **ogni nascita produce ESATTAMENTE UN arco con `i > j`**
  -- alla mitosi il nodo nuovo `m` ha l'indice ### **piu' alto**, quindi `m-b` e'
  memorizzato al rovescio *(e lo Schwinger fa lo stesso con `k-bb`)*.
  ### ⛔ **E' COSTATA LA CORSA DEL PASSO `229`** *(2026-10-06)*, e la cura e' il
  `verso(e, da)` di `circolazione`: ### **il segno si LEGGE dall'arco** invece di essere
  dedotto da una convenzione, e ### **si riduce alla forma qui sotto SOLO quando la
  convenzione vale.**
  ### ⚠ **Resta qui come TRAPPOLA DOCUMENTATA:** chi leggesse questa formula e la
  riscrivesse <<semplificata>> rifarebbe l'errore. ### **La forma vera e' nel codice, non
  qui.**

```
circ = tw[(u,v)] + tw[(v,w)] - tw[(u,w)]
```

### ⛔ **IL `tw` DEVE ESSERE IL `tw` DEL PASSO, e la normale la POSIZIONE del passo**

`n̂ = (pos_v − pos_u) x (pos_w − pos_u)`, ### **normalizzato.** I triangoli
### **degeneri** *(tre nodi allineati, `|cross|` sotto `EPS_NORMALE`)* ### **si CONTANO e
si ESCLUDONO**: un versore indefinito messo a zero sarebbe ### **un FALSO-ZERO** nella
coerenza.

### LE CINQUE VOCI, coi criteri del mandato

* **`(a)`** il numero di plaquette per nodo, per classe, ### **e il tempo di calcolo**;
* **`(b)`** `|Σ tw|` sulle plaquette, per classe;
* **`(c)`** `R_k` e la ### **COERENZA `|Σ v| / Σ |v|`**, da `0` *(disordine)* a `1`
  *(tutte le plaquette ruotano attorno allo stesso asse)*;
* **`(d)`** il ### **coseno fra `R_k` e l'asse di Bloch `_nb`**, per classe. ### **Il caso
  nullo e' ANALITICO, non simulato:** fra due assi indipendenti in `3D` il coseno e'
  ### **UNIFORME su `[-1, 1]`**, quindi media `0` e ### **frazione con `|cos| > 0.5` pari a
  `0.5`.** ### **Se e' distribuito come il caso, `P2` non lega niente.**
* **`(e)`** l'### **angolo di cui `R_k` ruota fra due passi**, per classe, contro la
  ### **frequenza di cambio di `perc_geom`** *(il riferimento di oggi)*.
"""
import contextlib
import io
import json
import os
import sys
import time

import numpy as np
import scipy.sparse as sp

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _misura_verso as MV                       # noqa: E402
import _mitosi_zero_dove as _MZD                 # noqa: E402
import _mitosi_soglia_grad as _MSG               # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_misura_plaquette")
# ### IL BLOCCO DELL'ENUMERAZIONE: si svuota ogni `BLOCCO` triple, cosi' la memoria resta
#   limitata anche con `5.5` milioni di plaquette. ### **Non e' una manopola di fisica:
#   e' la taglia di un buffer, e il risultato non ne dipende.**
BLOCCO = 400000
# ### IL PASSO DI SOTTOCAMPIONE per i quantili sulle plaquette: un PRIMO fisso, dichiarato.
#   ### **Deterministico: nessun RNG, quindi nessun seme da dichiarare.**
PASSO_CAMPIONE = 29
EPS_NORMALE = 1e-12


def _coerenza(R, somma_mod):
    """`|Σ v| / Σ |v|`. ### **`None` dove non c'e' nessuna plaquette**, mai `0`."""
    nR = np.linalg.norm(R, axis=1)
    fuori = np.full(len(R), np.nan)
    m = somma_mod > 0
    fuori[m] = nR[m] / somma_mod[m]
    return fuori


def _per_classe_nan(val, cl, nomi=_MZD.CLASSI):
    """Come `per_classe`, ma i `NaN` ### **si CONTANO e si ESCLUDONO**, non si azzerano."""
    val = np.asarray(val, float)
    fuori = {}
    for k, nome in enumerate(nomi):
        m = (cl == k)
        v = val[m]
        buoni = v[~np.isnan(v)]
        fuori[nome] = {"n": int(v.size), "n_non_definiti": int(np.sum(np.isnan(v))),
                       "mediana": (float(np.median(buoni)) if buoni.size else None),
                       "media": (float(np.mean(buoni)) if buoni.size else None),
                       "q25": (float(np.percentile(buoni, 25)) if buoni.size else None),
                       "q75": (float(np.percentile(buoni, 75)) if buoni.size else None),
                       "min": (float(np.min(buoni)) if buoni.size else None),
                       "max": (float(np.max(buoni)) if buoni.size else None)}
    return fuori


class Plaquette(object):
    """### **LEGGE SOLTANTO.** L'enumerazione non chiama nulla del simulatore che scriva."""

    nome = "plaquette"

    def __init__(self):
        self.g = None
        self.geo = None
        self.misure = {}
        self.pesanti = {}
        self.avvisi = []

    def prepara(self, S, net):
        self.g = _MZD.Misura(S.DT, 0.0)
        self.geo = self.g.prepara(S, net)
        return self.geo

    def classe_nodi(self, net):
        u, _c = self.g._u(net, np.arange(net.n))
        return _MZD.classe(u, self.g.u_bordo)

    # ---------------------------------------------------------------- l'enumerazione
    def enumera(self, net):
        """Le plaquette, ### **a blocchi**, accumulando direttamente sui nodi.

        ### **Nessuna lista globale di triple:** la memoria resta al blocco, e con
        `5.5` milioni di triangoli una lista intera costerebbe centinaia di `MB`.
        """
        n = int(net.n)
        ii = np.asarray(net.i, np.int64); jj = np.asarray(net.j, np.int64)
        # ### ⛔ **I CAPPI SI CONTANO PRIMA DI TOGLIERLI, e il collaudo mi ha costretto
        #   a questo:** avevo messo una guardia che si fermava su `i == j`, ed era un
        #   ### **RAMO MORTO** -- il filtro qui sotto li toglie ### **prima**, quindi la
        #   guardia non poteva scattare mai. ### **`A8`: un ramo silenzioso non e' un
        #   ramo.** ### ✔ **Ora si CONTANO e si DICHIARANO**, ed e' la stessa esclusione
        #   che fa il simulatore in `_base_cicli_topologici` *(`if a < n and b < n and
        #   a != b`)*: ### **un'esclusione TACIUTA e' un insabbiamento, una DICHIARATA
        #   non lo e'.**
        cappi = int(np.sum(ii == jj))
        m = (ii < n) & (jj < n) & (ii != jj)
        ii, jj = ii[m], jj[m]
        tw = np.asarray(net.tw, float)[m]
        pos = np.asarray(net.pos, float)[:n]
        # ### `c0` PER ARCO: `cos(phi0_i - phi0_j)`, la memoria CONGELATA dei legami.
        _ph0 = np.asarray(net.phi0, float)[:n]
        c0_arco = np.cos(_ph0[ii] - _ph0[jj])
        # ### ⛔ **QUI C'ERA UN'ASSUNZIONE, E LA CORSA DEL 2026-10-06 L'HA FATTA SALTARE
        #   AL PASSO `229`:** lo strumento pretendeva `i < j` su TUTTI gli archi, e si
        #   fermava. ### ✔ **La guardia ha fatto il suo lavoro** -- ha trovato `9` archi
        #   fuori convenzione invece di produrre nove circolazioni sbagliate in silenzio
        #   -- ### ⛔ **ma l'assunzione era MIA, e andava TOLTA invece che difesa.**
        #   ### ✔ **LA CURA NON AGGIUNGE NIENTE** *(`9-ter`)*: la chiave diventa
        #   ### **CANONICA `(min, max)`** e il segno della circolazione diventa
        #   ### **ESPLICITO**, quindi ### **non c'e' piu' niente da assumere.**
        #   ### ⛔ **E NON RESTA NESSUN RIFIUTO QUI:** i cappi -- che la chiave canonica
        #   non distinguerebbe -- sono ### **gia' esclusi dal filtro sopra**, e il loro
        #   numero si ### **DICHIARA** nell'esito.
        fuori_convenzione = int(np.sum(ii > jj))
        A = sp.csr_matrix((np.ones(ii.size * 2, np.int8),
                           (np.concatenate([ii, jj]), np.concatenate([jj, ii]))),
                          shape=(n, n))
        A.data[:] = 1
        A.sort_indices()
        # ### ⛔ **`A.indices` DI SCIPY E' `int32`, E QUESTO HA PRODOTTO UN DIFETTO
        #   SILENZIOSO:** con NumPy 2 uno scalare Python e' ### **debole**, quindi
        #   `indices_int32 * BASE_CHIAVE` ### **resta `int32` e TRABOCCA**
        #   *(`12802 * 2097152 ~ 2.7e10` contro `2^31`)*. ### **Le chiavi si avvolgevano e
        #   il 97% dei triangoli spariva: `138313` invece di `5534011`, senza un errore.**
        #   ### **Non l'ha trovato un ragionamento: l'ha trovato il CONFRONTO con un conto
        #   indipendente**, che per questo e' entrato nello strumento qui sotto.
        indptr, indices = A.indptr, A.indices.astype(np.int64)
        if (int(n) + 1) * int(MV.BASE_CHIAVE) >= 2 ** 62:
            raise SystemExit("[FERMO] `n = %d` e' troppo grande per la base delle chiavi: "
                             "il prodotto traboccherebbe." % n)
        chiavi = np.minimum(ii, jj) * MV.BASE_CHIAVE + np.maximum(ii, jj)
        ordine = np.argsort(chiavi, kind="stable")
        ch_o, idx_o = chiavi[ordine], ordine

        def arco(a, b):
            """L'indice d'arco della coppia `(a, b)` con `a < b`, per chiave
            ### **CANONICA**. ### **`-1` se non esiste.**"""
            k = a * MV.BASE_CHIAVE + b
            p = np.searchsorted(ch_o, k)
            p = np.minimum(p, max(ch_o.size - 1, 0))
            ok = ch_o[p] == k
            fuori = np.full(k.size, -1, np.int64)
            fuori[ok] = idx_o[p[ok]]
            return fuori

        def verso(e, da):
            """`+1` se l'arco `e` e' memorizzato ### **`da -> ...`**, `-1` se al contrario.

            ### ✔ **E' TUTTA LA CURA:** il segno di `tw` in una circolazione
            ### **non si deduce da una convenzione, si LEGGE da come l'arco e'
            memorizzato.**
            """
            return np.where(ii[e] == da, 1.0, -1.0)

        R = np.zeros((n, 3))
        conta = np.zeros(n, np.int64)
        somma_mod = np.zeros(n)
        # ### ⛔ **DUE DENOMINATORI, E IL COLLAUDO MI HA COSTRETTO A SEPARARLI.** Un nodo
        #   le cui plaquette sono ### **tutte DEGENERI** ha `somma_mod > 0` ma `R = 0`:
        #   la coerenza `|ΣR|/Σ|v|` leggerebbe ### **`0`, cioe' <<disordine totale>>**,
        #   mentre la verita' e' ### **<<non definita>>** -- nessuna normale utilizzabile.
        #   ### **E' esattamente la famiglia di `CHI-TORS-ZERO-FALSO`:** uno zero che vuol
        #   dire <<non misurato>>. ### **Quindi la coerenza ha il SUO denominatore**, sulle
        #   sole plaquette non degeneri, e il suo conteggio.
        conta_ok = np.zeros(n, np.int64)
        somma_mod_ok = np.zeros(n)
        max_mod = np.zeros(n)
        # ### ⭐ **`M5(c)`, seconda parte: LE PLAQUETTE FRUSTRATE.** Una plaquette e'
        #   FRUSTRATA se il prodotto dei tre `c0 = cos(phi0_i - phi0_j)` e' NEGATIVO:
        #   ### **non esiste un assegnamento di fasi che soddisfi tutti e tre i legami.**
        #   ### ⚠ **E `c0` e' CONGELATO** *(`PHI0-CONGELATA`)*, quindi questa
        #   frustrazione ### **non si scioglie mai**: e' disordine IMMUTABILE, e il conto
        #   dice quanto.
        frustrate = np.zeros(n, np.int64)
        con_c0 = np.zeros(n, np.int64)
        degeneri = 0
        tot = 0
        camp_mod, camp_cls_v = [], []
        tri = {}
        bu, bv, bw = [], [], []
        quanti = 0

        def svuota():
            nonlocal bu, bv, bw, quanti, degeneri, tot, camp_mod
            nonlocal camp_cls_v, conta, somma_mod, conta_ok, somma_mod_ok
            nonlocal frustrate, con_c0
            if not bu:
                return
            tu = np.concatenate(bu); tv = np.concatenate(bv); tw_ = np.concatenate(bw)
            bu, bv, bw, quanti = [], [], [], 0
            e_uv = arco(tu, tv); e_vw = arco(tv, tw_); e_uw = arco(tu, tw_)
            buono = (e_uv >= 0) & (e_vw >= 0) & (e_uw >= 0)
            if not np.all(buono):
                # ### non dovrebbe capitare: l'enumerazione CHIEDE che l'arco esista.
                self.avvisi.append("enumera: %d triple senza i tre archi: ESCLUSE."
                                   % int(np.sum(~buono)))
                tu, tv, tw_ = tu[buono], tv[buono], tw_[buono]
                e_uv, e_vw, e_uw = e_uv[buono], e_vw[buono], e_uw[buono]
            # ### LA CIRCOLAZIONE sul cammino `u -> v -> w -> u`, ### **col segno di
            #   ogni tratto LETTO dall'arco** invece che dedotto da una convenzione.
            #   ### ✔ **SI RIDUCE ALLA FORMA VECCHIA quando tutti gli archi sono `i<j`:**
            #   i primi due versi valgono `+1` e il terzo `-1`, cioe'
            #   `tw[uv] + tw[vw] - tw[uw]`. ### **La riduzione al limite si vede, ed e'
            #   nel collaudo.**
            circ = (verso(e_uv, tu) * tw[e_uv] + verso(e_vw, tv) * tw[e_vw]
                    + verso(e_uw, tw_) * tw[e_uw])
            cr = np.cross(pos[tv] - pos[tu], pos[tw_] - pos[tu])
            nn = np.linalg.norm(cr, axis=1)
            ok = nn > EPS_NORMALE
            degeneri += int(np.sum(~ok))
            tot += int(circ.size)
            am = np.abs(circ)
            # --- il sottocampione per i quantili: STRIDE fisso, nessun RNG
            camp_mod.append(am[::PASSO_CAMPIONE])
            camp_cls_v.append(tu[::PASSO_CAMPIONE])
            # --- gli accumuli per NODO: ogni plaquette conta sui suoi TRE vertici
            vt = np.concatenate([tu, tv, tw_])
            conta += np.bincount(vt, minlength=n).astype(np.int64)
            # ### LA FRUSTRAZIONE: il prodotto dei tre `c0`. ### **Negativo = frustrata.**
            _pr = c0_arco[e_uv] * c0_arco[e_vw] * c0_arco[e_uw]
            _fr = (_pr < 0.0)
            con_c0 += np.bincount(vt, minlength=n).astype(np.int64)
            if np.any(_fr):
                frustrate += np.bincount(
                    np.concatenate([tu[_fr], tv[_fr], tw_[_fr]]),
                    minlength=n).astype(np.int64)
            somma_mod += np.bincount(vt, weights=np.concatenate([am, am, am]),
                                     minlength=n)
            np.maximum.at(max_mod, vt, np.concatenate([am, am, am]))
            if np.any(ok):
                vv = (circ[ok] / nn[ok])[:, None] * cr[ok]       # (Σtw) * n̂
                vt3 = np.concatenate([tu[ok], tv[ok], tw_[ok]])
                am_ok = np.abs(circ[ok])
                conta_ok += np.bincount(vt3, minlength=n).astype(np.int64)
                somma_mod_ok += np.bincount(
                    vt3, weights=np.tile(am_ok, 3), minlength=n)
                for c in range(3):
                    R[:, c] += np.bincount(vt3, weights=np.tile(vv[:, c], 3),
                                           minlength=n)

        t0 = time.time()
        for u in range(n):
            nb = indices[indptr[u]:indptr[u + 1]]
            hi = nb[nb > u]
            if hi.dtype != np.int64:
                raise SystemExit("[FERMO] i vicini non sono `int64` (%s): le chiavi "
                                 "TRABOCCHEREBBERO in silenzio." % hi.dtype)
            q = hi.size
            if q < 2:
                continue
            if q not in tri:
                tri[q] = np.triu_indices(q, 1)
            pv, pw = tri[q]
            v = hi[pv]; w = hi[pw]
            k = v * MV.BASE_CHIAVE + w
            p = np.searchsorted(ch_o, k)
            p = np.minimum(p, max(ch_o.size - 1, 0))
            ok = ch_o[p] == k
            if not np.any(ok):
                continue
            bu.append(np.full(int(np.sum(ok)), u, np.int64))
            bv.append(v[ok]); bw.append(w[ok])
            quanti += int(np.sum(ok))
            if quanti >= BLOCCO:
                svuota()
        svuota()
        secondi = time.time() - t0
        # ### ✔ **IL CONTROLLO INDIPENDENTE, e NON e' prudenza: ha trovato il difetto.**
        #   Per ogni arco `(u,v)` il numero di ### **vicini comuni** e' il numero di
        #   triangoli che passano per quell'arco; sommato sugli archi ORIENTATI, ogni
        #   triangolo si conta ### **sei volte** *(tre archi x due direzioni)*. ### **E' un
        #   conto che NON passa da nessuna chiave**, quindi non condivide nessun difetto
        #   con l'enumerazione. ### **Se i due numeri non coincidono, lo strumento SI
        #   FERMA.**
        t1 = time.time()
        atteso = 0
        for s0 in range(0, n, 400):
            bl = A[s0:s0 + 400]
            atteso += int((bl @ A).multiply(bl).sum())
        atteso //= 6
        secondi_controllo = time.time() - t1
        if atteso != tot:
            raise SystemExit(
                "[FERMO] l'enumerazione trova %d plaquette, il conto INDIPENDENTE %d. "
                "### Due conti della stessa cosa non si scelgono: si riconciliano."
                % (tot, atteso))
        camp_mod = (np.concatenate(camp_mod) if camp_mod else np.zeros(0))
        camp_cls_v = (np.concatenate(camp_cls_v) if camp_cls_v else np.zeros(0, np.int64))
        return {"n": n, "tot": tot, "degeneri": degeneri, "secondi": secondi,
                "archi_i_maggiore_j": fuori_convenzione, "cappi_esclusi": cappi,
                "frustrate": frustrate, "con_c0": con_c0,
                "controllo_indipendente": atteso,
                "secondi_controllo": secondi_controllo,
                "R": R, "conta": conta, "somma_mod": somma_mod, "max_mod": max_mod,
                "conta_ok": conta_ok, "somma_mod_ok": somma_mod_ok,
                "camp_mod": camp_mod, "camp_v": camp_cls_v}

    # ---------------------------------------------------------------- il giro
    def osserva(self, S, net, k, pesante):
        if not pesante:
            return
        cl = self.classe_nodi(net)
        d = self.enumera(net)
        n = d["n"]
        conta = d["conta"]; R = d["R"]
        # --- `(a)` quante plaquette per nodo, per classe
        a = MV.per_classe(conta.astype(float), cl)
        # --- `(b)` `|Σ tw|` per nodo (media sulle sue plaquette), per classe
        media_mod = np.full(n, np.nan)
        mm = conta > 0
        media_mod[mm] = d["somma_mod"][mm] / conta[mm]
        # --- `(c)` la coerenza
        # ### LA COERENZA SULLE SOLE PLAQUETTE NON DEGENERI, col suo denominatore.
        coe = _coerenza(R, np.where(d["conta_ok"] > 0, d["somma_mod_ok"], 0.0))
        nR = np.linalg.norm(R, axis=1)
        # --- `(d)` il coseno con l'asse di Bloch
        nb = np.asarray(getattr(net, "_nb", np.zeros((n, 3))), float)[:n]
        cos = np.full(n, np.nan)
        den = nR * np.linalg.norm(nb, axis=1)
        md = den > EPS_NORMALE
        cos[md] = np.sum(R[md] * nb[md], axis=1) / den[md]
        # ### ⛔ **IL CASO NULLO E' ANALITICO:** fra due assi indipendenti in `3D` il coseno
        #   e' UNIFORME su `[-1,1]`. ### **Quindi media `0`, `|cos| > 0.5` nella META' dei
        #   casi.** Si riportano entrambi, accanto al misurato.
        oltre = np.full(n, np.nan)
        oltre[md] = (np.abs(cos[md]) > 0.5).astype(float)
        fuori = {
            "passo": k, "n": n,
            "a_plaquette_totali": d["tot"], "a_degeneri": d["degeneri"],
            "a_secondi": round(d["secondi"], 2),
            "a_controllo_indipendente": d["controllo_indipendente"],
            "a_archi_i_maggiore_j": d["archi_i_maggiore_j"],
            "a_cappi_esclusi": d["cappi_esclusi"],
            # ### `M5(c)`: la quota di plaquette FRUSTRATE per nodo, per classe.
            #   ### ⚠ **`NaN` dove il nodo non ha plaquette**, non `0`.
            "c_frustrate_per_classe": _per_classe_nan(
                np.where(d["con_c0"] > 0,
                         d["frustrate"] / np.maximum(d["con_c0"], 1), np.nan), cl),
            "c_frustrate_totali": int(np.sum(d["frustrate"]) // 3),
            "c_plaquette_con_c0": int(np.sum(d["con_c0"]) // 3),
            "a_secondi_controllo": round(d["secondi_controllo"], 2),
            "a_per_nodo_per_classe": a,
            "a_nodi_senza_plaquette": int(np.sum(conta == 0)),
            "a_nodi_senza_plaquette_non_degenere": int(np.sum(d["conta_ok"] == 0)),
            "b_modulo_medio_per_nodo_per_classe": _per_classe_nan(media_mod, cl),
            "b_campione": {
                "passo_campione": PASSO_CAMPIONE, "n": int(d["camp_mod"].size),
                "quantili": ([float(x) for x in np.percentile(
                    d["camp_mod"], [5, 25, 50, 75, 95])] if d["camp_mod"].size else None),
                "max": (float(np.max(d["camp_mod"])) if d["camp_mod"].size else None)},
            "c_coerenza_per_classe": _per_classe_nan(coe, cl),
            "c_modulo_R_per_classe": _per_classe_nan(np.where(conta > 0, nR, np.nan), cl),
            "d_cos_con_nb_per_classe": _per_classe_nan(cos, cl),
            "d_frazione_oltre_mezzo_per_classe": _per_classe_nan(oltre, cl),
            "d_caso_nullo": {"media_attesa": 0.0, "frazione_oltre_mezzo_attesa": 0.5,
                             "legge": "coseno fra due assi indipendenti in 3D: UNIFORME su [-1,1]"},
        }
        self.pesanti[k] = {"fuori": fuori, "R": R, "conta": conta, "cl": cl,
                           "perc_geom": np.asarray(net.perc_geom, float)[:n].copy()}

    def chiudi(self):
        """`(e)` la stabilita': l'angolo fra `R_k(t-1)` e `R_k(t)`."""
        for k in MV.PASSI_MISURA:
            d = self.pesanti.get(k)
            p = self.pesanti.get(k - 1)
            if d is None:
                continue
            f = dict(d["fuori"])
            if p is None:
                f["e_stabilita"] = None
            else:
                nc = min(len(d["R"]), len(p["R"]))
                A = d["R"][:nc]; B = p["R"][:nc]
                na = np.linalg.norm(A, axis=1); nb_ = np.linalg.norm(B, axis=1)
                ang = np.full(nc, np.nan)
                m = (na > EPS_NORMALE) & (nb_ > EPS_NORMALE)
                # ### `clip` SOLO per l'errore di macchina: il coseno di due versori puo'
                #   uscire di `1e-16` da `[-1,1]`. ### **Non e' un tetto di fisica.**
                cc = np.clip(np.sum(A[m] * B[m], axis=1) / (na[m] * nb_[m]), -1.0, 1.0)
                ang[m] = np.degrees(np.arccos(cc))
                cl = d["cl"][:nc]
                cg = (d["perc_geom"][:nc] != p["perc_geom"][:nc]).astype(float)
                f["e_stabilita"] = {
                    "passo_precedente": k - 1, "nodi_confrontabili": int(nc),
                    "nodi_senza_R": int(np.sum(~m)),
                    "angolo_gradi_per_classe": _per_classe_nan(ang, cl),
                    "riferimento_perc_geom_frazione_cambiata_per_classe":
                        _per_classe_nan(cg, cl),
                    "riferimento_perc_geom_frazione_cambiata":
                        float(np.mean(cg)) if nc else None}
            self.misure[k] = f

    def esito(self):
        self.chiudi()
        return {"geometria": self.geo,
                "misure": {str(k): v for k, v in sorted(self.misure.items())},
                "passi_misura": list(MV.PASSI_MISURA),
                "passi_pesanti": list(MV.PASSI_PESANTI),
                "blocco": BLOCCO, "passo_campione": PASSO_CAMPIONE,
                "eps_normale": EPS_NORMALE,
                "gira_sulla_stessa_corsa_di_M1_M3": True,
                "avvisi": self.avvisi}


def _scrivi(d):
    for p in (FUORI, MV.FUORI):
        if not os.path.isdir(p):
            os.makedirs(p)
    io.open(os.path.join(FUORI, "plaquette.json"), "w", encoding="utf-8").write(
        json.dumps({k: v for k, v in d.items() if k != "verso"}, indent=1, default=str))
    # ### I DUE OSSERVATORI, DUE FILE: `M1`-`M3` resta nel suo json, con le sue chiavi.
    io.open(os.path.join(MV.FUORI, "verso.json"), "w", encoding="utf-8").write(
        json.dumps({k: v for k, v in d.items() if k != "plaquette"}, indent=1, default=str))
    io.open(os.path.join(FUORI, "plaquette.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)


def collaudo():
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))

    # --- l'invarianza del prodotto `(Σtw) · n̂`, che e' il cuore di `(c)`
    rng = np.random.default_rng(11)
    pu, pv, pw = rng.normal(size=3), rng.normal(size=3), rng.normal(size=3)
    t_uv, t_vw, t_uw = 0.7, -1.3, 0.4
    c1 = t_uv + t_vw - t_uw                       # u -> v -> w -> u
    n1 = np.cross(pv - pu, pw - pu)
    # scambio `v` e `w`: il cammino diventa `u -> w -> v -> u`
    c2 = t_uw - t_vw - t_uv
    n2 = np.cross(pw - pu, pv - pu)
    prova("invarianza: ### la circolazione cambia SEGNO scambiando due vertici",
          abs(c2 + c1) < 1e-12)
    prova("invarianza: ### e la normale cambia segno anche lei",
          np.allclose(n2, -n1))
    prova("invarianza: ### quindi il PRODOTTO (Σtw)·n̂ NON cambia",
          np.allclose(c1 * n1 / np.linalg.norm(n1), c2 * n2 / np.linalg.norm(n2)))
    prova("invarianza: ### DEVE FALLIRE -- il SEGNO della circolazione da solo NON e' invariante",
          not abs(c1 - c2) < 1e-12)

    # --- la coerenza
    v = np.array([[1.0, 0, 0], [1.0, 0, 0], [1.0, 0, 0]])
    prova("coerenza: ### tre vettori CONCORDI danno 1",
          abs(_coerenza(v.sum(axis=0)[None, :], np.array([3.0]))[0] - 1.0) < 1e-12)
    prova("coerenza: ### due OPPOSTI danno 0",
          abs(_coerenza(np.zeros((1, 3)), np.array([2.0]))[0]) < 1e-12)
    prova("coerenza: ### e senza plaquette da `NaN`, non 0",
          np.isnan(_coerenza(np.zeros((1, 3)), np.array([0.0]))[0]))

    # --- `_per_classe_nan`: i NaN si CONTANO
    pc = _per_classe_nan(np.array([1.0, np.nan, 5.0]), np.array([0, 0, 2]))
    prova("per_classe_nan: ### MATERIA ha 2 nodi di cui 1 non definito, mediana 1.0",
          pc["MATERIA"]["n"] == 2 and pc["MATERIA"]["n_non_definiti"] == 1
          and pc["MATERIA"]["mediana"] == 1.0)
    prova("per_classe_nan: ### una classe tutta NaN da mediana `None`, non 0",
          _per_classe_nan(np.array([np.nan]), np.array([0]))["MATERIA"]["mediana"] is None)

    # --- l'enumerazione, su un grafo COSTRUITO A MANO con triangoli NOTI
    class Rete(object):
        pass

    # due triangoli che condividono l'arco (1,2): {0,1,2} e {1,2,3}
    r = Rete()
    r.n = 5
    coppie = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]
    r.i = np.array([a for a, b in coppie]); r.j = np.array([b for a, b in coppie])
    r.tw = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    r.pos = np.array([[0.0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [9, 9, 9]])
    r._nb = np.tile(np.array([[0.0, 0, 1.0]]), (5, 1))
    r.perc_geom = np.zeros(5)
    # ### `phi0` SERVE a `M5(c)`: sul `net` vero c'e' SEMPRE, quindi NESSUN ripiego (`A8`).
    r.phi0 = np.zeros(5)
    pl = Plaquette()
    d = pl.enumera(r)
    prova("enumera: ### trova DUE triangoli, non uno e non sei", d["tot"] == 2)
    prova("enumera: ### il nodo 4 non sta in nessun triangolo", d["conta"][4] == 0)
    prova("enumera: ### gli archi (1,2) stanno in DUE triangoli -> conta 2 sui nodi 1 e 2",
          d["conta"][1] == 2 and d["conta"][2] == 2)
    prova("enumera: ### e i nodi 0 e 3 in uno solo",
          d["conta"][0] == 1 and d["conta"][3] == 1)
    # la circolazione del triangolo {0,1,2}: tw(0,1) + tw(1,2) - tw(0,2) = 1 + 3 - 2 = 2
    prova("enumera: ### la circolazione di {0,1,2} e' 1 + 3 - 2 = 2 (dal nodo 0)",
          abs(d["somma_mod"][0] - 2.0) < 1e-12)
    # {1,2,3}: tw(1,2) + tw(2,3) - tw(1,3) = 3 + 5 - 4 = 4
    prova("enumera: ### e quella di {1,2,3} e' 3 + 5 - 4 = 4 (dal nodo 3)",
          abs(d["somma_mod"][3] - 4.0) < 1e-12)
    prova("enumera: ### i due triangoli sono PIANI (z=0), quindi NON degeneri",
          d["degeneri"] == 0)

    # --- i triangoli DEGENERI si contano e si escludono
    r2 = Rete()
    r2.n = 3
    r2.i = np.array([0, 0, 1]); r2.j = np.array([1, 2, 2])
    r2.tw = np.array([1.0, 2.0, 3.0])
    r2.pos = np.array([[0.0, 0, 0], [1, 0, 0], [2, 0, 0]])   # ALLINEATI
    r2._nb = np.tile(np.array([[0.0, 0, 1.0]]), (3, 1))
    r2.perc_geom = np.zeros(3)
    r2.phi0 = np.zeros(3)
    d2 = Plaquette().enumera(r2)
    prova("degeneri: ### un triangolo di tre nodi ALLINEATI si trova...", d2["tot"] == 1)
    prova("degeneri: ### ...e si CONTA come degenere", d2["degeneri"] == 1)
    prova("degeneri: ### e NON contribuisce a `R` (niente versore inventato)",
          np.allclose(d2["R"], 0.0))
    # ### ⛔ **IL CASO CHE HA TROVATO UN DIFETTO NEL CODICE, non nella prova:** col
    #   denominatore di TUTTE le plaquette la coerenza di un nodo solo-degenere valeva
    #   ### **`0`**, cioe' <<disordine totale>>, invece di ### **<<non definita>>.**
    prova("degeneri: ### col denominatore di TUTTE le plaquette la coerenza darebbe 0 (il difetto)",
          abs(_coerenza(d2["R"], d2["somma_mod"])[0]) < 1e-12)
    prova("degeneri: ### col denominatore delle sole NON degeneri da' `NaN`, ed e' la cura",
          np.isnan(_coerenza(
              d2["R"], np.where(d2["conta_ok"] > 0, d2["somma_mod_ok"], 0.0))[0]))
    prova("degeneri: ### e `conta_ok` e' ZERO li', mentre `conta` e' UNO",
          d2["conta_ok"][0] == 0 and d2["conta"][0] == 1)

    # --- ### ⛔ **LA PROVA VECCHIA DICEVA <<un arco con `i > j` FERMA lo strumento>>, E
    #   LA CORSA DEL 2026-10-06 HA MOSTRATO CHE QUELLO ERA IL DIFETTO, non la cura:**
    #   al passo `229` c'erano `9` archi fuori convenzione, uno per nascita, e lo
    #   strumento si fermava. ### ✔ **Adesso NON deve fermarsi, e deve dare LA STESSA
    #   CIRCOLAZIONE.**
    #   ### ⚠ **E LA PROVA GIUSTA RIBALTA DUE COSE INSIEME:** `(i,j)` ### **e il segno di
    #   `tw`**, perche' `tw` e' una 1-forma ORIENTATA e ### **quella e' la STESSA forma
    #   scritta al rovescio.** Ribaltare solo `(i,j)` descriverebbe uno stato DIVERSO.
    rr = Rete()
    rr.n = 5
    rr.i = r.i.copy(); rr.j = r.j.copy(); rr.tw = r.tw.copy()
    rr.pos = r.pos.copy(); rr._nb = r._nb.copy(); rr.perc_geom = r.perc_geom.copy()
    rr.phi0 = r.phi0.copy()
    k_inv = 1                                  # l'arco `(0,2)`, che sta nel triangolo
    rr.i[k_inv], rr.j[k_inv] = r.j[k_inv], r.i[k_inv]
    rr.tw[k_inv] = -r.tw[k_inv]
    di = Plaquette().enumera(rr)
    prova("orientamento: ### un arco scritto al ROVESCIO non ferma piu' lo strumento",
          di["tot"] == 2)
    prova("orientamento: ### e lo DICHIARA: un arco con `i > j`",
          di["archi_i_maggiore_j"] == 1 and d["archi_i_maggiore_j"] == 0)
    prova("orientamento: ### la circolazione di {0,1,2} e' LA STESSA (2.0)",
          abs(di["somma_mod"][0] - 2.0) < 1e-12)
    prova("orientamento: ### e quella di {1,2,3} pure (4.0)",
          abs(di["somma_mod"][3] - 4.0) < 1e-12)
    prova("orientamento: ### e `R` e' identico, non solo il modulo",
          np.allclose(di["R"], d["R"]))
    # ### ✔ **E LA FORMA VECCHIA SBAGLIEREBBE, e si fa vedere invece di affermarlo:**
    #   `tw[uv] + tw[vw] - tw[uw]` sull'arco ribaltato da' `1 + 3 - (-2) = 6`, non `2`.
    vecchia = rr.tw[0] + rr.tw[2] - rr.tw[k_inv]
    prova("orientamento: ### DEVE FALLIRE -- la formula VECCHIA darebbe 6.0 invece di 2.0",
          abs(vecchia - 6.0) < 1e-12 and abs(vecchia - 2.0) > 1.0)
    # --- ### ⛔ **IL CAPPIO: avevo messo una GUARDIA e il collaudo l'ha trovata MORTA.**
    #   Il filtro `(ii != jj)` sta ### **PRIMA**, quindi `np.any(ii == jj)` non poteva
    #   essere vero ### **mai**. ### **`A8`: un ramo silenzioso non e' un ramo.**
    #   ### ✔ **Ora i cappi si CONTANO e si DICHIARANO**, come fa il simulatore stesso.
    r3 = Rete()
    r3.n = 4
    # un CAPPIO sul nodo 1, piu' il triangolo {0,1,2}
    r3.i = np.array([1, 0, 0, 1]); r3.j = np.array([1, 1, 2, 2])
    r3.tw = np.array([9.0, 1.0, 2.0, 3.0])
    r3.pos = np.array([[0.0, 0, 0], [1, 0, 0], [0, 1, 0], [5, 5, 5]])
    r3._nb = np.tile(np.array([[0.0, 0, 1.0]]), (4, 1))
    r3.perc_geom = np.zeros(4)
    r3.phi0 = np.zeros(4)
    d3 = Plaquette().enumera(r3)
    prova("cappio: ### si CONTA, e non ferma lo strumento", d3["cappi_esclusi"] == 1)
    prova("cappio: ### ed e' ESCLUSO dall'enumerazione: resta UN triangolo", d3["tot"] == 1)
    prova("cappio: ### e NON entra nella circolazione: 1 + 3 - 2 = 2, non 11",
          abs(d3["somma_mod"][0] - 2.0) < 1e-12)
    prova("cappio: ### DEVE FALLIRE -- se il cappio entrasse, il modulo NON sarebbe 2.0",
          abs(d3["somma_mod"][0] - 11.0) > 1.0)

    # ### ⛔ **IL CASO CHE AVREBBE COLTO IL DIFETTO DEL TRABOCCAMENTO**, e che non avevo:
    #   un prodotto `int32 * BASE_CHIAVE` ### **si avvolge in silenzio.**
    v32 = np.array([12802], np.int32)
    prova("traboccamento: ### `int32 * BASE_CHIAVE` TRABOCCA (e' il difetto, in una riga)",
          int(v32 * MV.BASE_CHIAVE) != 12802 * MV.BASE_CHIAVE)
    prova("traboccamento: ### e in `int64` no (e' la cura)",
          int(v32.astype(np.int64) * MV.BASE_CHIAVE) == 12802 * MV.BASE_CHIAVE)
    prova("traboccamento: ### il conto INDIPENDENTE coincide sul grafo a due triangoli",
          d["controllo_indipendente"] == d["tot"] == 2)

    # --- il blocco non cambia il risultato
    glob = BLOCCO
    try:
        globals()["BLOCCO"] = 1
        d3 = Plaquette().enumera(r)
    finally:
        globals()["BLOCCO"] = glob
    prova("blocco: ### con BLOCCO = 1 il risultato e' IDENTICO (e' un buffer, non una legge)",
          d3["tot"] == d["tot"] and np.allclose(d3["R"], d["R"])
          and np.array_equal(d3["conta"], d["conta"]))

    # --- ⭐ `M5(c)`: LE PLAQUETTE FRUSTRATE, su un caso COSTRUITO A MANO.
    #     Con `phi0 = 0` tutti i `c0` valgono `1`: ### **zero frustrazione.**
    #     Con `phi0 = [0, 2, 4]` i tre coseni sono `cos(-2)`, `cos(-4)`, `cos(-2)`, cioe'
    #     ### **TRE negativi**, e il prodotto e' ### **negativo**: FRUSTRATA.
    rf = Rete()
    rf.n = 5
    rf.i = r.i.copy(); rf.j = r.j.copy(); rf.tw = r.tw.copy()
    rf.pos = r.pos.copy(); rf._nb = r._nb.copy(); rf.perc_geom = r.perc_geom.copy()
    rf.phi0 = np.zeros(5)
    d0 = Plaquette().enumera(rf)
    prova("frustrate: ### con `phi0 = 0` i tre `c0` valgono 1 e la frustrazione e' ZERO",
          int(np.sum(d0["frustrate"])) == 0 and d0["tot"] == 2)
    rf.phi0 = np.array([0.0, 2.0, 4.0, 0.0, 0.0])
    d1 = Plaquette().enumera(rf)
    prova("frustrate: ### con `phi0 = [0, 2, 4]` il prodotto dei tre coseni e' NEGATIVO",
          float(np.cos(-2.0) * np.cos(-4.0) * np.cos(-2.0)) < 0.0)
    prova("frustrate: ### e il triangolo {0,1,2} risulta FRUSTRATO (nodo 0 conta 1)",
          int(d1["frustrate"][0]) == 1)
    prova("frustrate: ### DEVE FALLIRE -- con `phi0 = 0` lo stesso nodo contava ZERO",
          int(d0["frustrate"][0]) == 0)
    prova("frustrate: ### e `con_c0` conta TUTTE le plaquette del nodo, non solo le frustrate",
          int(d1["con_c0"][0]) == int(d1["conta"][0]))

    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    return 0 if all(esiti) else 1


def main(argv):
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _misura_plaquette.py")
        riga("=")
        return collaudo()
    passi = MV.PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    riga("=")
    stampa("M1-M4 -- IL VERSO E LE PLAQUETTE: %d passi, UN braccio, SOLA LETTURA" % passi)
    stampa("  ### M4 gira sulla STESSA corsa di M1-M3, e il motivo e' nel docstring.")
    riga("=")
    e = MV.corsa("msg_plaq", passi, [MV.Verso(), Plaquette()], _scrivi)
    io.open(os.path.join(FUORI, "plaquette.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return e


if __name__ == "__main__":
    sys.exit(main(sys.argv))
