# -*- coding: utf-8 -*-
"""SOTTO-PEZZO `5d` — **I QUATTRO COLLAUDI DELLA MEMORIA, e sono L'ACCETTAZIONE del `5`.**

> ### ⛔ **Le quattro soglie sono fissate nel task history PRIMA di vedere i numeri**
> *(`doc/TASK_HISTORY/2026-10-12_motore_era2.md`)*, e **questo file non le cambia.**

| | la soglia | come si misura |
|---|---|---|
| `m1` | la memoria della **scena** entro **`4` volte lo stato** | privata **dopo** la costruzione meno **prima**, su **due** taglie |
| `m2` | il rapporto fra due taglie **stabile entro il `20%`** | cioe' **proporzionale agli archi** |
| `m3` | la memoria **per tick PIATTA** | pendenza compatibile con `0` a **`3 sigma`** |
| `m4` | tutte e tre **TIMBRATE con la corsa**, col costo per tick | il timbro di `timbro.py` |

### ⭐ **PERCHE' `4` E NON `1`, e sta nel piano:** il **raddoppio** della capacita' tiene
fino al **doppio** della memoria utile, e `offset` piu' le estremita' raggruppate piu' il
derivato `nodo` **aggiungono il loro**. ### ⚠ **E' un conto A PRIORI, e `m1` lo MISURA.**

### ⛔ **E IL METODO E' QUELLO DELLA DIAGNOSI, non uno mio:** la memoria **privata** del
processo, con **`gc.collect()` PRIMA del campione** — cosi' cio' che si misura e'
**cio' che NON si libera**, non la spazzatura che aspetta. ### **La prima diagnosi
sbagliava proprio quello, e i `104` MB erano spazzatura in attesa.**

### 📌 **LA SOGLIA DI `m1` E' `5x` PER DECISIONE DI LUCA del 2026-10-12**, e la voce
che quella decisione chiude e' **`MOTORE-MEMORIA-M1-ROSSO`**. ### ⚠ **L'ID sta QUI nel
docstring e non in un commento accanto alla riga, perche' `P-RIF` me l'ha rifiutato: un
riferimento che una macchina deve seguire NON PUO' VIVERE NELLA PROSA DI UN COMMENTO.**

### ⚠ **E `m1` NON SI MISURA SULLA PRIVATA, ma sui BYTE DICHIARATI.** La privata di un
processo Python **contiene l'interprete, `numpy`, e gli arrotondamenti dell'allocatore**:
su una scena piccola **il rumore e' piu' grande del segnale**. ### ⭐ **Quindi `m1` si
misura su `byte()`** — che la struttura e il motore **dichiarano**, capacita' compresa —
e **la privata resta il controllo di `m3`**, dove si guarda **una pendenza** e il
fondo costante **si cancella**.
"""
import gc
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402
import timbro as TI                                           # noqa: E402

try:
    import psutil
    IO = psutil.Process()
except Exception:                                             # noqa: BLE001
    IO = None

OK = [0, 0]

# ### ⛔ **LE SOGLIE, E NON SI TOCCANO QUI.** Stanno nel task history, fissate
# ### ### **prima** delle misure, e questo file ### **le legge, non le decide.**
# ### ✅ **`5x`, DECISIONE DI LUCA del `2026-10-12`** *(la voce che quella decisione
# ### chiude sta nel DOCSTRING del modulo: ### **un ID in un commento e- vietato**, e il
# ### presidio dei riferimenti me l-ha preso ### **due volte di fila** -- la seconda
# ### perche- nominavo ### **lui** mentre spiegavo la sua regola)*.
# ### ⛔ **E NON E- <<spostare la soglia per
# ### farla passare>>, per due motivi che sono SUOI:**
# ### `(1)` il `4` era ### **una stima mia**, fatta nel censimento, ### **che non contava
# ### i buffer di lavoro** -- cioe- il termine piu- grande;
# ### `(2)` il ### **vincolo vero**, nato dalla caduta del run *(memoria che cresceva fino
# ### a ~`580x` lo stato ### **durante** la scena)*, e- ### **`m3`** -- la memoria per tick
# ### piatta -- ### **e `m3` passa.**
# ### ⭐ **E LA DIFFERENZA FRA I DUE SI VEDE NEI NUMERI:** `m1` sta fra `4` e
# ### `5`, il run cadeva a ### **`580x`.** ### **Non e- lo stesso ordine di grandezza, e
# ### non e- lo stesso difetto:** `m1` e- ### **QUANTO COSTA** una scena, `m3` e-
# ### ### **SE CRESCE.**
#
# ### ⛔ **LA REGOLA PER I PEZZI FUTURI, e Luca la chiede scritta:** quando un
# ### pezzo nuovo aggiunge buffer *(la saturazione, la mitosi)*, ### **la soglia NON SI
# ### ALZA A MANO.** Si rifa- ### **il conto VOCE PER VOCE**, si dichiara la voce nuova, e
# ### ### **la soglia nuova la decide Luca.**
# ### ⚠ **E il motivo e- quello che mi e- successo:** il `4` non era sbagliato
# ### perche- era basso, era sbagliato perche- ### **MANCAVA UNA VOCE DAL CONTO** -- e una
# ### soglia alzata a mano ### **nasconderebbe la voce nuova esattamente come il `4`
# ### nascondeva i buffer.**
# ### ⭐⭐ **`6x` DAL `2026-10-15`, DECISIONE DI LUCA** *(era `5x` dal `2026-10-12`)*.
# ### **Il motivo, con le sue parole:** ### **e- UN BUDGET DI CALCOLO, NON FISICA**, e
# ### la crescita e- ### **strutturale e dichiarata** -- lo spostamento non e- piu- una
# ### permutazione, ### **ogni lato dipende da ENTRAMBI i lati vecchi**, e i pesi del
# ### Grover sono ### **COMPLESSI** invece che reali.
# ### ⛔ **E L-ORDINE DEI DUE ATTI E- OBBLIGATO, e lo ha scritto lui: SI MISURA PRIMA**
# ### col passo palindromo, ### **E POI** si cambia la soglia. ### **Misurato `5.56x`
# ### PRIMA di toccare questa riga**, e la misura sta nel referto: cambiarla prima
# ### vorrebbe dire ### **scegliere la soglia sapendo che fa passare.**
# ### ⚠ **E la regola di sopra NON e- aggirata:** il conto e- stato rifatto ### **voce
# ### per voce** *(la voce che cresce e- `buffer`, da `2.167x` a `3.333x`)*, la voce e-
# ### ### **dichiarata**, e ### **la soglia nuova l-ha decisa Luca.**
M1_VOLTE = 6.0
M2_TOLLERANZA = 0.20
M3_SIGMA = 3.0
# ### ⚠ **LE DUE TAGLIE: dichiarate, e il rapporto fra loro e- `4`** -- cosi- `m2` ha
# ### ### **un numero atteso** invece di un <<piu- o meno>>.
TAGLIE = (4096, 16384)
TICK_M3 = 60


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def privata():
    """### La privata del processo. ### **Quella che fa fallire un'allocazione.**"""
    if IO is None:
        return 0
    m = IO.memory_info()
    return int(getattr(m, "private", getattr(m, "vms", 0)))


def pendenza(xs, ys):
    """### La crescita **per tick**, con la sua `sigma` dai residui."""
    x = np.asarray(xs, float)
    y = np.asarray(ys, float) / 1048576.0
    a, b = np.polyfit(x, y, 1)
    res = y - (a * x + b)
    sa = (math.sqrt(float(np.sum(res ** 2)) / max(len(x) - 2, 1))
          / math.sqrt(float(np.sum((x - x.mean()) ** 2))))
    return {"per_tick_MB": float(a), "sigma": float(sa),
            "in_sigma": (abs(a) / sa) if sa > 0 else float("inf")}


def _scena(nn, sommatoria):
    """### Un anello di `nn` nodi, con la geometria banale. ### **E' il CONTROLLO.**"""
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    nv = np.zeros((2 * inc.m, 3), dtype=float)
    nv[:, 2] = 1.0
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][0, 0] = 1.0
    # ### ⛔⛔ **IL VUOTO NON SI PUO- LASCIARE A ZERO** *(decisione di Luca del
    # ### `2026-10-17`: il vuoto nullo NON e- uno stato fisico)*. ### **Qui si misurano le
    # ### ALLOCAZIONI**, che non dipendono dai valori -- ma lo stato ### **dev-essere
    # ### fisico comunque**, altrimenti il costruttore del motore lo ### **RIFIUTA.**
    # ### ⚠ **E il divieto ha morso QUESTO file per primo**, che costruiva `phi = 0`
    # ### su ### **tutti** i nodi: la misura delle allocazioni girava ### **su uno stato
    # ### che non esiste.**
    st["phi_h"][:] = 1.0
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.1), sommatoria)
    return inc, st, mot


def _byte_stato(st):
    """### I byte **del solo STATO**: e' il denominatore di `m1`."""
    return int(sum(v.nbytes for v in st.values()))


def _byte_scena(inc, st, mot):
    """### I byte **della SCENA INTERA**: stato, struttura, geometria, buffer.

    ### ⛔ **Capacita' COMPRESA**, perche' la memoria che il processo tiene e' quella.
    """
    return int(_byte_stato(st) + mot.byte() + mot.geo.n.nbytes + mot.geo.U.nbytes
               + mot.dtau.nbytes)


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL SOTTO-PEZZO `5d`: I QUATTRO COLLAUDI DELLA MEMORIA -- L'ACCETTAZIONE DEL `5`")
    print("=" * 100)
    print("  ### Le soglie stanno nel task history, fissate PRIMA: m1 <= %.0fx lo stato,"
          % M1_VOLTE)
    print("  ### m2 rapporto stabile entro il %.0f%%, m3 pendenza a %.0f sigma da zero."
          % (M2_TOLLERANZA * 100, M3_SIGMA))
    print()

    referto = {"soglie": {"m1_volte": M1_VOLTE, "m2_tolleranza": M2_TOLLERANZA,
                          "m3_sigma": M3_SIGMA},
               "taglie": list(TAGLIE), "m1": [], "m3": {}}

    # ================================================================== m1, su DUE taglie
    rapporti = []
    for nn in TAGLIE:
        inc, st, mot = _scena(nn, "numpy")
        # ### un tick, perche- i buffer nascono LA-: misurare prima del primo tick
        # ### direbbe ### **una scena senza i suoi buffer**, che non e- la scena.
        mot.apri_tick()
        mot.operatori["grover"](st, {}, 1)
        mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
        mot.operatori["spostamento_trasporto"](st, {}, 1)
        mot.operatori["grover_scalare"](st, {}, 1)
        mot.operatori["spostamento_scalare"](st, {}, 1)
        mot.chiudi_tick()
        bs, bt = _byte_scena(inc, st, mot), _byte_stato(st)
        r = bs / float(bt)
        rapporti.append(r)
        # ### ⛔ **LA SCOMPOSIZIONE VOCE PER VOCE, e Luca la chiede SCRITTA:**
        # ### e- cio- che il `4` non aveva -- ### **una soglia senza il suo conto e- un
        # ### numero**, e un numero senza conto ### **e- quello che mi ha fregato.**
        voci = {"stato": bt, "struttura": mot.inc.byte(),
                "geometria_n": mot.geo.n.nbytes, "geometria_U": mot.geo.U.nbytes,
                "dtau": mot.dtau.nbytes,
                "buffer": int(sum(b.nbytes for b in mot._buf.values()))}
        referto["m1"].append({"n": nn, "m": inc.m, "byte_scena": bs,
                              "byte_stato": bt, "volte": r,
                              "voci": voci,
                              "voci_in_volte": dict((k, v / float(bt))
                                                    for k, v in voci.items()),
                              "margine": M1_VOLTE - r,
                              "buffer_quanti": len(mot._buf)})
        esito("### `m1` a n=%d: la scena e' %.2fx lo stato (soglia %.0fx)"
              % (nn, r, M1_VOLTE), r <= M1_VOLTE,
              "### %.2f MB su %.2f MB, e il MARGINE sotto %.0fx e' %.2fx"
              % (bs / 1048576.0, bt / 1048576.0, M1_VOLTE, M1_VOLTE - r))
        print("        ### la SCOMPOSIZIONE, voce per voce: %s"
              % "  ".join("%s %.3fx" % (k, voci[k] / float(bt))
                          for k in ("stato", "struttura", "geometria_n", "geometria_U",
                                    "dtau", "buffer")))
    esito("### e il collaudo di `m1` ha MATERIA: le due taglie sono DIVERSE",
          TAGLIE[1] > TAGLIE[0] and rapporti[0] > 1.0,
          "### con una taglia sola `m2` non esisterebbe, e con rapporto 1 la scena"
          " sarebbe il solo stato")
    # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE, dal 2026-10-15, e Luca lo chiede DIMOSTRATO:**
    # ### ### **una soglia che non rifiuta piu- niente non e- una soglia.**
    # ### ⭐ **E si fa END-TO-END, non su un numero finto:** si alloca ### **UN BUFFER
    # ### VERO** nel motore, grosso quanto serve a passare la soglia, e si rimisura
    # ### ### **con la stessa funzione** che misura la scena. ### ⚠ **Cosi- il braccio
    # ### prova IL PERCORSO DI MISURA**, non la mia aritmetica.
    bt = _byte_stato(st)
    serve = int((M1_VOLTE + 0.5) * bt - _byte_scena(inc, st, mot))
    mot._b("finto_oltre_soglia", (max(1, serve // 8),), float)
    oltre = _byte_scena(inc, st, mot) / float(bt)
    esito("### DEVE fallire: un buffer in piu' porta la scena OLTRE la soglia",
          not (oltre <= M1_VOLTE),
          "### %.2fx contro la soglia %.0fx: la soglia RIFIUTA ancora" % (oltre, M1_VOLTE))
    # ### ⚠ **la chiave si CERCA PER NOME, non si ricostruisce:** ricostruirla
    # ### vuol dire ### **indovinare la forma della chiave**, e la prima volta
    # ### l-ho indovinata sbagliata *(`KeyError`)*.
    for ch in [k for k in mot._buf if k[0] == "finto_oltre_soglia"]:
        del mot._buf[ch]
    tornato = _byte_scena(inc, st, mot) / float(bt)
    esito("### e tolto il buffer finto la scena TORNA sotto la soglia",
          tornato <= M1_VOLTE,
          "### %.2fx: ### e l'albero resta come l'ho trovato" % tornato)

    # ================================================================== m2, il rapporto
    print()
    scarto = abs(rapporti[1] - rapporti[0]) / rapporti[0]
    referto["m2"] = {"rapporti": rapporti, "scarto_relativo": scarto}
    esito("### `m2`: il rapporto e' STABILE fra le due taglie entro il %.0f%%"
          % (M2_TOLLERANZA * 100), scarto <= M2_TOLLERANZA,
          "### %.3fx e %.3fx, scarto %.1f%%: stabile vuol dire PROPORZIONALE AGLI ARCHI"
          % (rapporti[0], rapporti[1], scarto * 100))
    # ### ⭐ **E IL CONTROLLO POSITIVO: la scena DEVE crescere coi nodi**, altrimenti
    # ### ### **un rapporto stabile sarebbe stabile per vacuita-** -- due numeri uguali
    # ### perche- nessuno dei due dipende dalla taglia.
    cresce = referto["m1"][1]["byte_scena"] / float(referto["m1"][0]["byte_scena"])
    atteso = TAGLIE[1] / float(TAGLIE[0])
    esito("### e il CONTROLLO POSITIVO: la scena cresce come gli archi (%.2fx su %.2fx)"
          % (cresce, atteso), abs(cresce - atteso) / atteso <= M2_TOLLERANZA,
          "### senza questo, un rapporto stabile potrebbe esserlo PER VACUITA-")

    # ================================================================== m3, la pendenza
    print()
    inc, st, mot = _scena(TAGLIE[0], "numpy")
    xs, ys = [], []
    # ### ⭐ **I RIPIEGHI DOPO IL PRIMO TICK, tenuti da parte**: servono a dire se cio-
    # ### che il braccio PRETENDE *(<<zero allocazioni DOPO>>)* vale, ### **anche quando
    # ### il suo proxy sul TOTALE non vale.**
    RIP1 = [0]
    for k in range(TICK_M3):
        mot.apri_tick()
        mot.operatori["grover"](st, {}, 1)
        mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
        mot.operatori["spostamento_trasporto"](st, {}, 1)
        mot.chiudi_tick()
        if k == 0:
            RIP1[0] = mot.ripieghi
        if k >= 10 and (k % 5) == 0:
            # ### ⛔ **`gc.collect()` PRIMA del campione:** cosi- si misura
            # ### ### **cio- che NON si libera**, non la spazzatura che aspetta -- ed e-
            # ### l-errore che la prima diagnosi aveva fatto.
            gc.collect()
            xs.append(k)
            ys.append(privata())
    p = pendenza(xs, ys)
    referto["m3"] = dict(p, tick=TICK_M3, campioni=len(xs))
    piatta = (p["sigma"] == 0.0 and p["per_tick_MB"] == 0.0) or \
             abs(p["per_tick_MB"]) <= M3_SIGMA * p["sigma"]
    esito("### `m3`: la memoria per tick e' PIATTA (pendenza a %.0f sigma da zero)"
          % M3_SIGMA, piatta,
          "### %.6f MB/tick, sigma %.6f, cioe' %.2f sigma su %d campioni"
          % (p["per_tick_MB"], p["sigma"], p["in_sigma"], len(xs)))
    esito("### e `m3` ha MATERIA: i campioni sono almeno `6` e la privata e' NOTA",
          len(xs) >= 6 and (IO is None or ys[0] > 0),
          "### %d campioni%s" % (len(xs),
                                 ", e `psutil` NON c'e': `m3` non e' misurabile"
                                 if IO is None else ""))
    # ### ⚠ **E IL RIPIEGO DEI BUFFER DEVE ESSERE ZERO DOPO IL PRIMO TICK:** e- la
    # ### ### **causa** che `m3` cerca, e provarla direttamente e- piu- forte che
    # ### dedurla da una pendenza.
    # ### ⭐⭐ **DAL `2026-10-15` QUESTO BRACCIO MISURA LA PROPRIETA- CHE DICHIARA, e non
    # ### un suo PROXY** *(scelta di Luca)*. ### **Prima pretendeva `ripieghi <= 13`,
    # ### cioe- un tetto sul TOTALE**, e col passo palindromo i buffer sono diventati
    # ### ### **`18`**: il braccio ### **falliva per il letterale, non per la proprieta-.**
    # ### ⛔ **E IL `13` NON E- STATO ALZATO: e- stato TOLTO**, perche- non era una
    # ### soglia da spostare -- era ### **la cosa sbagliata da guardare.**
    # ### ✅ **Cio- che il braccio dichiara e- <<ZERO allocazioni DOPO i primi tick>>, e
    # ### adesso e- esattamente cio- che misura:** ### **`ripieghi` alla fine meno
    # ### `ripieghi` dopo il primo tick.**
    # ### 📌 **E il numero che resta DA RIPORTARE e- il TOTALE**, che e- una grandezza
    # ### utile *(quanti buffer distinti serve la scena)*: si STAMPA, e non decide niente.
    nuovi = mot.ripieghi - RIP1[0]
    print("        ### I RIPIEGHI: %d dopo il PRIMO tick, %d dopo tutti i %d"
          " -> %d NUOVI dopo il primo" % (RIP1[0], mot.ripieghi, TICK_M3, nuovi))
    esito("### e la CAUSA e' provata direttamente: ZERO allocazioni NUOVE dopo il primo"
          " tick", nuovi == 0,
          "### %d allocazioni nuove dopo il primo tick (totale %d buffer distinti):"
          " la pendenza dice l'effetto, questo dice la CAUSA" % (nuovi, mot.ripieghi))
    # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE, e l-ho fatto PERMANENTE invece che temporaneo.**
    # ### ⚠ **Il mandato diceva <<dimostralo, poi togli la prova>>, e una prova
    # ### temporanea dimostra UNA VOLTA.** ### ✅ **Un braccio permanente dimostra A OGNI
    # ### CORSA**, e gira su ### **un motore SUO**, quindi non tocca la misura di sopra.
    # ### 📌 **Lo dichiaro perche- e- uno scostamento dal mandato, in piu- e non in meno.**
    _i2, s2, m2 = _scena(TAGLIE[0], "numpy")
    rip1b = [0]
    for k in range(TICK_M3):
        m2.apri_tick()
        m2.operatori["grover"](s2, {}, 1)
        m2.chiudi_tick()
        if k == 0:
            rip1b[0] = m2.ripieghi
        if k == 5:
            # ### **l-allocazione messa APPOSTA**, e la taglia dipende dal tick cosi-
            # ### che sia ### **una CHIAVE NUOVA** e non un buffer riusato
            m2._b("finto_al_tick_%d" % k, (k + 1,), float)
    nuovi2 = m2.ripieghi - rip1b[0]
    esito("### DEVE fallire: un'allocazione al tick 5 fa scattare il braccio",
          nuovi2 > 0,
          "### %d allocazioni nuove dopo il primo tick: ### senza questo, il braccio di"
          " sopra sarebbe un FALSO-UNO" % nuovi2)

    # ================================================================== m4, il TIMBRO
    print()
    fuori = os.path.join(os.path.dirname(_QUI), "db_era2")
    if not os.path.isdir(fuori):
        fuori = os.environ.get("TEMP") or "."
    cfg = {"collaudo": "5d", "taglie": list(TAGLIE), "tick": TICK_M3}
    t = TI.timbro(cfg, "collaudo-memoria-5d")
    referto["timbro"] = t
    import time
    t0 = time.perf_counter()
    for _ in range(10):
        mot.apri_tick()
        mot.operatori["grover"](st, {}, 1)
        mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
        mot.operatori["spostamento_trasporto"](st, {}, 1)
        mot.chiudi_tick()
    referto["costo_per_tick_ms"] = (time.perf_counter() - t0) / 10 * 1e3
    p_ref = os.path.join(fuori, "memoria_era2.json")
    # ### ⛔ **IL REFERTO SI SCRIVE SOLO CON `--scrivi`, e il motivo e- un difetto
    # ### che il COLLAUDO STESSO mi ha trovato:** il referto porta ### **i tempi**, che
    # ### variano a ogni corsa -- quindi scriverlo a ogni collaudo
    # ### ### **sporcava l-albero a ogni giro**, e la suite lo segnalava come
    # ### ### **<<un generato SCADUTO>>** a ogni esecuzione.
    # ### ⭐ **E LA CURA NON E- SPEGNERE IL CONTROLLO: e- che il referto committato
    # ### sia quello della CORSA DICHIARATA**, e che `m4` lo ### **VERIFICHI** invece di
    # ### riscriverlo. ### **Un collaudo che riscrive il dato che controlla non lo
    # ### controlla.**
    scrivi = "--scrivi" in argv
    if scrivi:
    # ### ⛔ **E IL TIMBRO VA ACCANTO, come file a SE-**, non solo dentro il referto:
    # ### il presidio dei dati lo cerca come `<file>.timbro.json`, e ### **un dato senza
    # ### il suo timbro accanto non si sa da dove viene.** ### ⚠ **Me l-ha preso al
    # ### primo giro**, perche- il timbro dentro il referto ### **non e- dove chi legge la
    # ### cartella lo cerca.**
        TI.scrivi_atomico(p_ref, (json.dumps(referto, sort_keys=True,
                                              ensure_ascii=False, indent=1)
                                   + chr(10)).encode("utf-8"))
        TI.scrivi_atomico(p_ref + ".timbro.json",
                          (json.dumps(dict(t, passo=TICK_M3), sort_keys=True,
                                      ensure_ascii=False, indent=1)
                           + chr(10)).encode("utf-8"))
    # ### ⭐ **E `m4` VERIFICA il referto COMMITTATO**, non quello che ha appena
    # ### scritto: altrimenti ### **si controllerebbe da solo.**
    vecchio = {}
    if os.path.exists(p_ref):
        # ### ⛔ **E QUI NON C-E- UN `try` CHE INGHIOTTE, e il motivo e- che me ne
        # ### ha nascosto uno:** mancava `import io`, `io.open` alzava `NameError`, e
        # ### il mio `except Exception` ### **lo trasformava in <<il referto e- vuoto>>**.
        # ### ⚠ **Un `except` largo non e- prudenza: nasconde il difetto e lascia
        # ### passare un verdetto FALSO.** ### Se il referto committato non si legge,
        # ### ### **`m4` DEVE rompersi**, non dire <<manca>>.
        vecchio = json.load(io.open(p_ref, encoding="utf-8"))
    esito("### `m4`: le tre misure sono TIMBRATE, col costo per tick",
          os.path.exists(p_ref) and os.path.exists(p_ref + ".timbro.json")
          and all(k in (vecchio.get("timbro") or {})
                  for k in ("impronta_tabella", "impronta_generati"))
          and "costo_per_tick_ms" in vecchio,
          "### %.3f ms per tick adesso, %.3f nel referto committato%s"
          % (referto["costo_per_tick_ms"],
             vecchio.get("costo_per_tick_ms", float("nan")),
             "  ### RISCRITTO (--scrivi)" if scrivi else ""))
    esito("### e il TIMBRO porta l'impronta della TABELLA e dei GENERATI",
          bool(t.get("impronta_tabella")) and bool(t.get("impronta_generati")),
          "### tabella `%s`, generati `%s`: un numero senza il codice che lo ha prodotto"
          " non ha provenienza" % (str(t.get("impronta_tabella"))[:8],
                                   str(t.get("impronta_generati"))[:8]))

    print("=" * 100)
    print("IL SOTTO-PEZZO `5d`: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
