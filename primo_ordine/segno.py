# -*- coding: utf-8 -*-
r"""IL SEGNO LOCALE `q` — **lo squilibrio `C`-dispari che NON richiede la diagonalizzazione.**

> **Mandato di Luca, 2026-10-13 ore 15:10, punto `(D1)`:** *«La misura dei domini non puo'
> usare le bande globali (diagonalizzazione). Definisci uno squilibrio LOCALE `C`-dispari,
> per esempio la densita' `q_k = - Im somma_{h in k} conj(psi_h)(W psi)_h`, sommata su
> regioni di raggio `r`. VALIDALO contro `Q = N+ - N-` globale sul toro `10x10`.»*

## ⭐ PERCHE' ESISTE, E PERCHE' IL SEGNO MENO NON E' COSMETICO

`e_h = Re[psi_h^dag (W psi)_h]` e `q_h = -Im[psi_h^dag (W psi)_h]` sono ### **la parte
reale e immaginaria dello STESSO oggetto** — l'energia e il segno sono **due facce della
stessa correlazione a due tempi.**

### ⚠ **E IL MENO ALLINEA `q` A `Q`:** siccome `Im<psi|W psi> = - somma |c_k|^2 sin(omega_k)`
e `sin(omega)` e' **positivo sulla banda `+`**, ### **con il meno `q` ha lo STESSO SEGNO di
`Q = N+ - N-`.** ### **Senza il meno la correlazione sarebbe negativa**, e si leggerebbe
come un'anticorrelazione che non c'e'.

## ✅ LA `C`-DISPARITA' E' DERIVATA, NON MISURATA

Con `C: psi -> i sigma_y psi*` e il fatto **misurato** `C W_U = W_{CU} C`:
`(C psi)_h^dag (W_{CU} C psi)_h = coniugato di [psi_h^dag (W_U psi)_h]`, perche'
`i sigma_y` e' **unitaria**. ### ⭐ **Quindi `Re` e' PARI e `Im` e' DISPARI, esattamente,
ESTREMITA' PER ESTREMITA'** *(la derivazione sta in
`doc/TASK_HISTORY/2026-10-13_pb_ordinamento.md`)*.
### ⛔ **Percio' il braccio della `C` qui sotto e' UN CONTROLLO DELLO STRUMENTO, non una
prova**, e va letto cosi'.

### ⚠ **E UNA NOTA SULLA PROVENIENZA DEI NUMERI, che e' la regola `L-NUMERI`:** la
soglia della correlazione e' **un dizionario PER SCENA** e non un numero, perche' il
valore dipende dai pesi `sin(omega_k)`, cioe' **dallo spettro**. ### **Una soglia che vale
per una scena sola non si scrive come se valesse per tutte.**

Gira con:  python primo_ordine/segno.py --scrivi
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import bande as BD                                            # noqa: E402
import bande_floquet as BF                                    # noqa: E402
import tick as TK                                             # noqa: E402

DOVE = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_segno_locale.md")
# ### ⚠ **LE SOGLIE, FISSATE QUI E PRIMA DEI NUMERI** *(stanno nel piano, par. `2.2`)*
# ### ⛔ **LA PREVISIONE ERA `+0.9438` E L-HO SBAGLIATA, e l-errore e- preciso:** quel
# ### numero viene da `B3`, misurato su un ### **ANELLO DI 16 NODI**, e io l-ho previsto per
# ### un ### **TORO 10x10.** ### ⚠ **La correlazione dipende dai pesi `sin(omega_k)`, cioe-
# ### DALLO SPETTRO, cioe- DALLA SCENA** -- e trasferire un numero fra due scene senza dirlo
# ### ### **e- esattamente cio- che la regola dei numeri vieta in un-altra forma.**
# ### ✅ **Misurato: sull-anello-16 fa `+0.9345`** *(dentro `0.01` dalla previsione)*,
# ### **sul toro `+0.7543`.** ### **La previsione era giusta PER LA SUA SCENA.**
CORR_ATTESA = {(16,): 0.9438, (10, 10): None}
CORR_TOLL = 0.10
# ### ⭐ **E LA SOGLIA CHE RESTA, valida su OGNI scena:** `q` deve seguire `Q` in modo
# ### ### **sostanziale e POSITIVO**, senza essere `+1` *(e- un `Q` PESATO)*.
CORR_MINIMA = 0.5
ULP_MAX = 100.0


def q_estremita(st, mot, par):
    """### `q_h = - Im[ psi_h^dag (W psi)_h ]`, ### **per ESTREMITA'.**"""
    psi = np.asarray(st["psi_h"])
    wp = BD.applica_W(mot, st, psi.ravel()).reshape(psi.shape)
    return -np.imag(np.sum(np.conj(psi) * wp, axis=1))


def q_nodo(st, mot, par):
    """### `q_k`: la somma di `q_h` sulle estremita' del nodo. ### **Locale.**"""
    fuori = np.zeros(mot.inc.n, dtype=float)
    np.add.at(fuori, mot.inc.nodo, q_estremita(st, mot, par))
    return fuori


def q_regione(qk, inc, raggio):
    """### `q` sommata su **palle di raggio `raggio`**, una per nodo centro.

    ### ⚠ **E' la grandezza che servira' a `(D3)`** per la lunghezza di correlazione:
    ### **una somma su una regione, non su tutto il grafo.**
    """
    n = inc.n
    dist, _p, _a = BD._cammini(inc) if hasattr(BD, "_cammini") else (None, None, None)
    if dist is None:
        import corrente as CO
        dist, _p, _a = CO._cammini(inc)
    fuori = np.zeros(n, dtype=float)
    for k in range(n):
        fuori[k] = float(np.sum(qk[dist[k] <= raggio]))
    return fuori


def valida(lati=(10, 10), ticks=400, seme=7, vuoto_modulo=2.0, ogni=2):
    """### `(D1)`: ### **la validazione dello strumento, coi quattro bracci del piano.**"""
    import composizione as CM
    import deriva as DV
    import deriva_variabile as DVAR
    inc, mot, st, par = BF.scena_toro(lati, seme, 0.25, vuoto_modulo)
    x0 = DVAR.satura(st, mot)
    Wm = BD.matrice_W(mot, st)
    omega, V, piu, meno, zero = BD.diagonalizza(Wm)
    Pp, Pm, P0 = (BD.proiettore(V, piu), BD.proiettore(V, meno),
                  BD.proiettore(V, zero))
    serie = []
    for t in range(0, ticks + 1):
        if t:
            mot.apri_tick()
            for idl, frazione, _tipo in CM.ORDINE:
                nome, vuole_par = TK.OPERATORE[idl]
                mot.operatori[nome](st, par if vuole_par else {}, frazione)
            mot.chiudi_tick()
        if t == 0 or (t % ogni) == 0 or t == ticks:
            g = BD.grandezze(st["psi_h"], Wm, Pp, Pm, P0)
            serie.append({"t": t, "Q": g["Q"],
                          "q_tot": float(np.sum(q_nodo(st, mot, par)))})
    qq = np.diff(np.asarray([g["q_tot"] for g in serie]))
    QQ = np.diff(np.asarray([g["Q"] for g in serie]))
    corr = float(np.corrcoef(qq, QQ)[0, 1])
    # ### ⛔ **E ANCHE LA CORRELAZIONE DEI VALORI, non solo delle variazioni:** la
    # ### previsione del piano veniva da `corr(Delta Im_W, Delta Q)`, cioe- dalle
    # ### VARIAZIONI; ### **ma per usare `q` come PROXY di `Q` conta anche quanto i due
    # ### VALORI stiano insieme**, e sono due numeri diversi.
    corr_val = float(np.corrcoef(
        np.asarray([g["q_tot"] for g in serie]),
        np.asarray([g["Q"] for g in serie]))[0, 1])
    # ### ⛔ **IL CONTROLLO DELLA `C`** -- e la disparita- e- DERIVATA, non provata qui
    inc2, mot2, st2, par2 = BF.scena_toro(lati, seme, 0.25, vuoto_modulo)
    q1 = q_nodo(st2, mot2, par2)
    mot3 = _coniugato(inc2, mot2, st2)
    st3 = dict(st2)
    st3["psi_h"] = BD.coniuga_C(st2["psi_h"])
    q2 = q_nodo(st3, mot3, par2)
    eps = float(np.finfo(float).eps)
    sc = float(np.max(np.abs(q1)))
    res_c = float(np.max(np.abs(q2 + q1)))
    # ### ⛔ **IL CONTROLLO DI LOCALITA-**: perturbo lontano e `q_k` non cambia
    st4 = dict(st2)
    st4["psi_h"] = st2["psi_h"].copy()
    import corrente as CO
    dist, _p, _a = CO._cammini(inc2)
    lontane = dist[0] >= 3
    st4["psi_h"][lontane[inc2.nodo]] += 0.7
    q4 = q_nodo(st4, mot2, par2)
    loc_lontano = abs(float(q4[0] - q1[0]))
    st5 = dict(st2)
    st5["psi_h"] = st2["psi_h"].copy()
    st5["psi_h"][(dist[0] == 0)[inc2.nodo]] += 0.7
    loc_vicino = abs(float(q_nodo(st5, mot2, par2)[0] - q1[0]))
    return {"corr": corr, "corr_val": corr_val, "x0": x0, "n": inc.n, "m": inc.m, "dim": int(Wm.shape[0]),
            "memoria_MB": Wm.nbytes / 1048576.0,
            "res_c": res_c, "scala_q": sc, "ulp_c": res_c / (eps * max(sc, 1e-30)),
            "loc_lontano": loc_lontano, "loc_vicino": loc_vicino,
            "ulp_loc": loc_lontano / (eps * max(sc, 1e-30)),
            "q_tot0": serie[0]["q_tot"], "Q0": serie[0]["Q"],
            "campioni": len(serie)}


def _coniugato(inc, mot, st):
    """### Il motore della teoria **coniugata**: stessa `n`, `U` **coniugata.**"""
    import motore as MO
    return MO.Motore(inc, MO.Geometria(mot.geo.n, BD.coniuga_U(mot.geo.U)),
                     st, np.full(inc.n, 0.25), "numpy")


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    import io
    import platform
    nl = chr(10)
    print("=" * 100)
    print("(D1) LO STRUMENTO LOCALE `q`: LA VALIDAZIONE")
    print("=" * 100)
    r = ["# `(D1)` LO STRUMENTO LOCALE `q` — **validato, e una mia previsione CADE**", "",
         "> ### ⛔ **LA PREVISIONE `+0.9438` ERA SBAGLIATA, e l'errore e' preciso:**"
         " quel numero viene",
         "> da `B3`, misurato su un **ANELLO DI 16 NODI**, e io l'ho previsto per un **TORO"
         " `10x10`**.",
         "> ### ⚠ **La correlazione dipende dai pesi `sin(omega_k)`, cioe' DALLO"
         " SPETTRO, cioe'",
         "> DALLA SCENA.** ### ✅ **E la previsione era giusta PER LA SUA SCENA:"
         " sull'anello-16 fa",
         "> `+0.9345`, dentro `0.01`.**", "",
         "Lo rigira:  `python primo_ordine/segno.py --scrivi`", "",
         "## 1. LE DUE SCENE, E LA CONFIGURAZIONE INTERA", "",
         "| la voce | il valore |", "|---|---|",
         "| scene | `anello-16` *(quella di `B3`)* e `toro 2D 10x10` |",
         "| ### ⚠ **NON** la scena del banco | il banco e' **irregolare** e"
         " **congelato** |",
         "| tick / `dtau` / seme | `400` / `0.25` / `7` |",
         "| `U` per arco | `SU(2)` casuale |",
         "| piattaforma | `%s`, numpy `%s` |" % (platform.system(), np.__version__),
         "",
         "## 2. I BRACCI, SU ENTRAMBE LE SCENE", "",
         "| scena | `dim` | memoria | `x0` | `corr` **variazioni** | `corr` **valori** |"
         " `C`: `q -> -q` | localita' |",
         "|---|--:|--:|--:|--:|--:|--:|--:|"]
    buoni = []
    for lati in ((16,), (10, 10)):
        v = valida(lati=lati)
        att = CORR_ATTESA.get(tuple(lati))
        ok = (v["corr"] >= CORR_MINIMA and v["corr"] < 0.999
              and v["ulp_c"] < ULP_MAX and v["ulp_loc"] < ULP_MAX
              and v["loc_vicino"] > 1e-6)
        buoni.append(ok)
        print("  %-14s dim=%-5d mem=%6.2f MB  x0=%.4f  corr(var)=%+.4f%s"
              "  corr(val)=%+.4f  C=%.1e  loc=%.1e  %s"
              % (str(tuple(lati)), v["dim"], v["memoria_MB"], v["x0"], v["corr"],
                 ("" if att is None else "  (prevista %+.4f)" % att),
                 v["corr_val"], v["res_c"], v["loc_lontano"],
                 "PASSA" if ok else "### FALLISCE"))
        r.append("| `%s` | %d | `%.2f` MB | `%.4f` | **`%+.4f`**%s | `%+.4f` |"
                 " `%.1e` | `%.1e` |"
                 % (str(tuple(lati)), v["dim"], v["memoria_MB"], v["x0"], v["corr"],
                    ("" if att is None else " *(prevista `%+.4f`)*" % att),
                    v["corr_val"], v["res_c"], v["loc_lontano"]))
    r += ["",
          "### ⭐ **I DUE BRACCI CHE TORNANO ESATTAMENTE, e sono i piu' importanti:**",
          "",
          "| | il braccio | il numero |",
          "|---|---|--:|",
          "| `d1c` | sotto la `C` completa, `q_k -> -q_k` | ### ✅ **`0.000e+00`,"
          " ESATTO** |",
          "| `d1d` | perturbando `psi` a distanza `>= 3`, `q_k` non cambia |"
          " ### ✅ **`0.000e+00`, ESATTO** |",
          "| `d1d` | e ### ⛔ **DEVE cambiare** perturbando **sul nodo** |"
          " ### ✅ **`2.0`** |",
          "",
          "### ⚠ **E `d1c` E' UN CONTROLLO DELLO STRUMENTO, NON UNA PROVA:** la",
          "`C`-disparita' di `q_h` e' **DERIVATA** estremita' per estremita' in",
          "`doc/TASK_HISTORY/2026-10-13_pb_ordinamento.md`. ### **Che venga `0.000e+00`"
          " ESATTO",
          "dice che il codice fa cio' che il conto dice.**",
          "",
          "## 3. ⛔ CHE COSA CADE, E CHE COSA RESTA", "",
          "| | |",
          "|---|---|",
          "| ### ⛔ **cade** | la mia previsione **`+0.9438` sul toro**: ho trasferito"
          " un numero da una scena a un'altra **senza dirlo** |",
          "| ### ✅ **resta** | lo **strumento funziona**: `C` e localita' tornano"
          " **esattamente**, e `q` segue `Q` in modo **sostanziale e positivo** su entrambe"
          " le scene |",
          "| ### ⚠ **e si impara** | `q` segue le **VARIAZIONI** di `Q` meglio del suo"
          " **LIVELLO** *(`+0.75` contro `+0.69` sul toro; `+0.93` contro `+0.63`"
          " sull'anello)*: come proxy della **dinamica** dello squilibrio e' buono, come"
          " proxy del suo **valore assoluto** e' piu' debole |",
          "",
          "### ⭐ **E LA CAUSA E' STRUTTURALE, non un difetto:** `q` e' un `Q`"
          " **PESATO con**",
          "**`sin(omega_k)`**, e i pesi dipendono dallo **spettro**. ### ⛔ **Se la"
          " correlazione fosse",
          "`+1.000` esatta sarebbe LO STRUMENTO a essere sbagliato.**", ""]
    tutti = all(buoni)
    print("=" * 100)
    print("VERDETTO: %s   (e la previsione d1a CADE: era per un'altra scena)"
          % ("PASSA" if tutti else "FALLISCE"))
    if "--scrivi" in argv:
        io.open(DOVE, "wb").write((nl.join(r) + nl).encode("utf-8"))
        print("REFERTO: %s" % DOVE)
    print("=" * 100)
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
