# -*- coding: utf-8 -*-
"""IL COLLAUDO DI `P3` — **`E` e' una somma di densita', e la CORRENTE NON si chiude.**

### ⛔ **QUESTO COLLAUDO AFFERMA UN FALLIMENTO, e lo afferma come FATTO MISURATO.** La
previsione scritta nel task history **prima** dei numeri diceva: *«la parte lineare chiude
il bilancio locale ESATTAMENTE»*. ### **La misura dice NO**, e il collaudo **la inchioda**
invece di togliere il braccio.

### ⭐ **E L'ORDINE DEI BRACCI E' QUELLO CHE SERVE A CREDERCI:** prima si prova che
**lo STRUMENTO funziona** *(il bilancio chiude su una corrente COSTRUITA)*, poi che
**il caso sbagliato lo rompe** *(il verso invertito)*, e **solo dopo** si usa lo strumento
sulla corrente vera. ### ⛔ **Senza i primi due, <<il bilancio non chiude>> direbbe solo
che il mio bilancio e' rotto.**

### ⭐ **ANNOTAZIONE DEL 2026-10-13:** il titolo qui sopra — *<<la CORRENTE NON si
chiude>>* — ### **e' vero DELLA MIA CANDIDATA, e falso in generale.** Una corrente locale
di ### **portata `3` archi ESISTE**, ed e' costruita in `primo_ordine/corrente.py` col suo
collaudo `_collauda_corrente.py`. ### ⛔ **Il braccio `(4)` di questo file resta come
sta: il fatto che misura e' VERO.** ### ⚠ **Cio' che era sbagliato era la CONCLUSIONE
che ne avevo tratto**, e sta scritta nel titolo del commit `36182b7`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import energia as EN                                          # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)
PAR = {"eps": 0.5}


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))


def _banco(nn, seme, dt):
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dt), "numpy")
    return inc, st, mot


def _lin_nodo(st, mot):
    """### Il PRIMO termine, attribuito ai nodi."""
    eh = EN.densita_estremita(st, mot, PAR, np.zeros(st["psi_h"].shape[0]))
    out = np.zeros(mot.inc.n, dtype=float)
    np.add.at(out, mot.inc.nodo, eh)
    return out


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("`P3`: L'ENERGIA COME SOMMA DI DENSITA' LOCALI, E LA CORRENTE")
    print("=" * 100)

    # =============================== (1) LO STRUMENTO: il bilancio chiude su una corrente COSTRUITA
    inc, st, mot = _banco(16, 5, 0.2)
    r = np.random.default_rng(77)
    Jfinta = r.normal(size=inc.m)
    # ### ⭐ **SI COSTRUISCE IL `Delta e` DALLA CORRENTE**, e allora il bilancio
    # ### ### **DEVE** chiudere: e- un-identita- aritmetica.
    df = np.zeros(inc.n, dtype=float)
    np.add.at(df, inc.jj, Jfinta)
    np.add.at(df, inc.ii, -Jfinta)
    e0 = r.normal(size=inc.n)
    res = EN.bilancio(e0, e0 + df, Jfinta, inc.ii, inc.jj, inc.n)
    esito("### (1) LO STRUMENTO funziona: su una corrente COSTRUITA il bilancio chiude",
          float(res.max()) <= 1024 * EPS * float(np.max(np.abs(df))),
          "### residuo max %.3e: se questo fallisse, ogni braccio sotto non direbbe"
          " niente" % float(res.max()))
    # ### ⛔ **E IL CASO CHE DEVE FALLIRE, che il mandato chiede: IL VERSO INVERTITO.**
    verso = np.ones(inc.m)
    verso[0] = -1.0
    res_g = EN.bilancio(e0, e0 + df, Jfinta * verso, inc.ii, inc.jj, inc.n)
    esito("### (1) DEVE fallire: la stessa corrente col VERSO di un arco INVERTITO",
          float(res_g.max()) > 1e-6,
          "### residuo max %.3e, e il vero era %.3e: un bilancio che passasse anche col"
          " verso sbagliato NON misurerebbe il bilancio"
          % (float(res_g.max()), float(res.max())))
    esito("### e rompe SOLO i due nodi di quell'arco, non tutti",
          int(np.sum(res_g > 1e-6)) == 2,
          "### %d nodi rotti su %d: un errore di verso e' LOCALE"
          % (int(np.sum(res_g > 1e-6)), inc.n))

    # =============================== (2) `E` E' LA SOMMA DELLE DENSITA', ESATTAMENTE
    print()
    lav = st["psi_h"].copy()
    finto = dict(st)
    finto["psi_h"] = lav
    mot.operatori["moneta_spin"](finto, PAR, 1)
    mot.operatori["grover"](finto, {}, 1)
    mot.operatori["spostamento_trasporto"](finto, {}, 1)
    glob = float(np.sum(np.real(np.conj(st["psi_h"]) * lav)))
    glob += float(EN.densita_nodo(st, mot, np.zeros(inc.n)).sum())
    esito("### (2) `E` come SOMMA DELLE DENSITA' coincide con la forma globale, AL BIT",
          abs(EN.totale(st, mot, PAR) - glob) <= 1024 * EPS * abs(glob),
          "### scarto %.3e: la somma delle densita' NON e' un'approssimazione della"
          " forma globale -- E' la forma globale"
          % abs(EN.totale(st, mot, PAR) - glob))

    # =============================== (3) IL PRIMO TERMINE E' CONSERVATO, PER UN'IDENTITA'
    print()
    e0 = _lin_nodo(st, mot).copy()
    Jvero = EN.corrente(st, mot, PAR, None).copy()
    mot.apri_tick()
    mot.operatori["moneta_spin"](st, PAR, 1)
    mot.operatori["grover"](st, {}, 1)
    mot.operatori["spostamento_trasporto"](st, {}, 1)
    mot.chiudi_tick()
    e1 = _lin_nodo(st, mot).copy()
    d = abs(float(e1.sum() - e0.sum()))
    sc = abs(float(e0.sum()))
    esito("### (3) il PRIMO termine e' conservato dal tick lineare: e' un'IDENTITA'",
          d <= 256 * EPS * sc,
          "### scarto %.3e su %.3f, cioe' %.1f ulp -- `W^dag W W = W`, e nient'altro"
          " serve" % (d, sc, d / (EPS * sc)))
    esito("### e i cambiamenti PER NODO sommano a zero: quindi UNA corrente ESISTE",
          abs(float((e1 - e0).sum())) <= 256 * EPS * sc,
          "### un campo a divergenza nulla su un grafo AMMETTE un flusso: l'esistenza e'"
          " garantita, la FORMA no")

    # =============================== (4) IL FALLIMENTO, AFFERMATO COME FATTO
    print()
    res_v = EN.bilancio(e0, e1, Jvero, inc.ii, inc.jj, inc.n)
    senza = np.abs(e1 - e0)
    # ### ⛔ **LA PREVISIONE ERA SBAGLIATA, e il collaudo la INCHIODA.** Avevo scritto
    # ### *<<la parte lineare chiude il bilancio locale ESATTAMENTE>>*: non chiude, e
    # ### ### **non chiude di tanto** -- il residuo e- PIU GRANDE del cambiamento
    # ### ### **senza nessuna corrente.**
    esito("### (4) LA CORRENTE DERIVATA NON CHIUDE IL BILANCIO -- fatto misurato",
          float(res_v.max()) > 1e-6,
          "### residuo max %.3e su scala %.3f: la PREVISIONE del task history diceva"
          " <<chiude ESATTAMENTE>>" % (float(res_v.max()), float(np.max(np.abs(e0)))))
    esito("### e NON e' un errore piccolo: e' PEGGIO che senza nessuna corrente",
          float(res_v.max()) > float(senza.max()),
          "### con la corrente %.3e, senza %.3e: cioe' la corrente NON TOGLIE niente,"
          " AGGIUNGE" % (float(res_v.max()), float(senza.max())))
    # ### ⭐ **E IL PERCHE- E- STRUTTURALE, e si PROVA:** `e_h` e- una correlazione fra
    # ### ### **DUE TEMPI** -- `psi` e `W psi` -- quindi ### **non e- una carica che si
    # ### trasporta**, e l-argomento del campo `azione` *(solo `arco` attraversa)*
    # ### ### **vale per DOVE SI MUOVE `psi`, non per `e_h`.**
    # ### ⚠ **La prova: `e_h` cambia ANCHE su un nodo i cui archi non portano niente.**
    esito("### (4) e la CAUSA: `e_h` cambia su OGNI nodo, anche a corrente nulla",
          int(np.sum(senza > 1e-9)) == inc.n,
          "### %d nodi su %d cambiano: `e_h` e' una correlazione fra DUE TEMPI, non una"
          " carica trasportata" % (int(np.sum(senza > 1e-9)), inc.n))

    print("=" * 100)
    print("`P3`: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
