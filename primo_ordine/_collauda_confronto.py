# -*- coding: utf-8 -*-
"""IL CONFRONTO TABELLA / BANCO, **ESEGUIBILE** — cosi' non si rifa' a mano.

> ### ⛔ **Il mandato:** *«Un collaudo ESEGUIBILE che renda il confronto non ripetibile a
> mano: costruisce lo stato iniziale con le funzioni del banco su una scena piccola e
> confronta `dtype`, forma e dove-vive con i tipi dichiarati in tabella.»*

### ⭐ **E LA COSA CHE LO RENDE UN CONFRONTO E NON UN'OPINIONE:** lo stato di riferimento
**lo costruisce il BANCO**, girando le sue funzioni — `camminata.stato_casuale`,
`vuoto3.vuoto_fondo`, `vuoto3.lambda_nodo`, `nonlineare2.elicita_nodo`. ### **Non lo
descrivo: lo FACCIO PRODURRE.**

### ⛔ **IL BANCO NON SI TOCCA: SI IMPORTA.** `[[BANCO-CONGELATO]]` vieta di modificarlo e
di farci girare corse nuove; **leggerlo e chiamare le sue funzioni su una scena di `6`
nodi non e' una corsa**, ed e' l'unico modo di avere **il fatto** invece della **mia
parola**.

### 📌 **E IL PRESIDIO CHE RENDE QUESTO CONFRONTO UN IMPEDIMENTO e' `P-E10`**, in
`csv/_presidi_era2.py`: una variabile in tabella **senza la sua riga** fa **rifiutare il
commit**. ### ⚠ **E l'ID sta QUI nel docstring e non in un commento accanto alla riga,
perche' `P-RIF` me l'ha rifiutato: un riferimento che una macchina deve seguire NON PUO'
VIVERE NELLA PROSA DI UN COMMENTO.**

### ⚠ **E I CASI CHE DEVONO FALLIRE SONO IL PUNTO:** il mandato ne nomina uno —
*«`phi` dichiarato reale contro il banco complesso»* — e ### **quello e' esattamente il
disallineamento che e' sfuggito tre volte.** Se il collaudo non lo prendesse, non
servirebbe a niente.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(RADICE, "proto_camminata"))

import _presidio                                              # noqa: E402

OK = [0, 0]
CONFRONTO = os.path.join(RADICE, "doc", "CONFRONTO_tabella_banco.md")
ESITI = ("COINCIDE", "ERRORE DI TRASCRIZIONE", "CONFLITTO", "MANCANTE", "NUOVA",
         "ORFANA")


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


# =====================================================================================
#   CHE COSA IL BANCO PRODUCE DAVVERO -- girando le SUE funzioni
# =====================================================================================
def stato_del_banco(nn):
    """### Lo stato iniziale **COSTRUITO DAL BANCO**, su una scena di `nn` nodi.

    ### ⛔ **Non e' una mia riproduzione:** sono **le sue funzioni**, chiamate.
    """
    import camminata as CM
    import nonlineare2 as N2
    import geometria as GE
    import scena as SC
    import vuoto3 as V3
    # ### ⛔ **`regolare` COSTRUISCE GIA- la scena**, e chiamare `costruisci`
    # ### sopra di lei era un errore mio: il collaudo me l-ha detto al primo giro,
    # ### ### **perche- il banco NON si e- potuto chiamare** invece di dare un numero
    # ### plausibile.
    # ### ⭐ **E `regolare` e- il CONTROLLO del banco:** un circolante, quindi
    # ### ### **tutti i gradi uguali** -- e per il confronto dei TIPI va benissimo,
    # ### perche- i tipi ### **non dipendono dalla scena.**
    sc = SC.regolare(nn)
    # ### ⛔ **`versori` torna UN ARRAY, non il `geo`**: il dizionario con `n` e `U`
    # ### lo costruisce ### **`scena_identita`** -- e il collaudo me l-ha detto con un
    # ### `AttributeError`, non con un numero sbagliato.
    # ### ⭐ **E `scena_identita` e- la scelta GIUSTA qui:** `U = I` su ogni arco,
    # ### cioe- ### **nessun campo** -- e per confrontare i TIPI serve il caso in cui
    # ### ### **non c-e- niente che possa spiegare una differenza.**
    geo = GE.scena_identita(sc)
    psi = CM.stato_casuale(sc, 11)
    phi = V3.vuoto_fondo(sc, V3.LAMBDA0, 11)
    return {
        "psi_h": psi,
        "phi_h": phi,
        "Lambda": V3.lambda_nodo(phi, sc),
        "h_int": N2.elicita_nodo(psi, sc, geo),
        # ### ⭐⭐ **`rho` E- ENTRATA IN TABELLA IL `2026-10-15`, E IL BANCO CE L-HA
        # ### GIA-:** `camminata.rho_nodo` e- ### **la stessa formula riga per riga**
        # ### *(`np.add.at(out, nodo, somma |psi|^2 sulle bande)`)*. ### ✅ **Quindi
        # ### l-esito e- `COINCIDE` e non `NUOVA`**, e questa riga ### **la fa
        # ### CONFRONTARE davvero** invece di farla passare per <<nuova>>.
        # ### ⚠ **Non e- una soglia aggiustata: e- la funzione del banco CHIAMATA**,
        # ### che e- cio- che il docstring di questo modulo promette.
        "rho": CM.rho_nodo(psi, sc),
    }, sc


# ### ⛔ **LA MAPPA TIPO -> (`dtype`, numero di colonne, dove vive), DICHIARATA.** ### Non
# ### si deduce da `stato.nuovo`, e il motivo e- che ### **cosi- il confronto e- fra DUE
# ### fonti**: la tabella da una parte, il banco dall-altra. ### **Dedurla dal generato
# ### vorrebbe dire confrontare il generato con se stesso.**
ATTESO = {
    "complesso_c2_estremita": ("complex128", 2, "estremita"),
    "complesso_estremita": ("complex128", 1, "estremita"),
    "complesso_c2_nodo": ("complex128", 2, "nodo"),
    "reale_nodo": ("float64", 1, "nodo"),
}


def tabella():
    """### Le variabili della tabella: `(nome, tipo)`. ### **Dalla FONTE, non dal
    generato.**"""
    import yaml
    d = yaml.safe_load(io.open(os.path.join(_QUI, "leggi", "leggi.yaml"),
                               encoding="utf-8").read()) or {}
    return [(v["nome"], v["tipo"]) for v in (d.get("variabili") or [])]


def righe_del_confronto():
    """### Le righe del documento del confronto: `nome -> esito`.

    ### ⛔ **Si legge il DOCUMENTO**, perche' e' quello che `P-E10` pretende: se il
    collaudo leggesse la tabella per sapere gli esiti, ### **non controllerebbe il
    documento.**
    """
    if not os.path.exists(CONFRONTO):
        return {}
    t = io.open(CONFRONTO, encoding="utf-8").read()
    fuori = {}
    for riga in t.split(chr(10)):
        if not riga.startswith("|"):
            continue
        for nome, _tipo in tabella():
            if ("`%s`" % nome) not in riga:
                continue
            for e in ESITI:
                if e in riga:
                    # ### il PRIMO esito che compare nella riga, e le righe sono
                    # ### ### **una per variabile**: il presidio lo pretende
                    fuori.setdefault(nome, e)
                    break
    return fuori


def confronta(nome, tipo, v, sc):
    """### `[]` oppure gli scarti fra ### **il tipo dichiarato** e ### **cio' che il
    banco produce.**"""
    err = []
    att = ATTESO.get(tipo)
    if att is None:
        return ["il tipo `%s` non sta nella mappa dichiarata di questo collaudo: un tipo"
                " nuovo si aggiunge QUI, cosi' il confronto non lo salta in silenzio"
                % tipo]
    dt, col, dove = att
    if str(v.dtype) != dt:
        err.append("`%s`: la tabella dichiara `%s` cioe' `%s`, e il banco produce `%s`"
                   % (nome, tipo, dt, v.dtype))
    cc = 1 if v.ndim == 1 else int(v.shape[1])
    if cc != col:
        err.append("`%s`: la tabella dichiara `%d` componenti e il banco ne produce `%d`"
                   % (nome, col, cc))
    atteso_righe = sc["n"] if dove == "nodo" else 2 * sc["m"]
    if int(v.shape[0]) != int(atteso_righe):
        err.append("`%s`: vive su `%s` (%d righe attese) e il banco ne produce %d"
                   % (nome, dove, atteso_righe, v.shape[0]))
    return err


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL CONFRONTO TABELLA / BANCO, ESEGUIBILE")
    print("=" * 100)
    nn = 6
    try:
        st, sc = stato_del_banco(nn)
    except Exception as e:                                    # noqa: BLE001
        print("  ### IL BANCO NON SI E' POTUTO CHIAMARE: %s" % e)
        print("  ### Senza il banco questo collaudo NON HA UN RIFERIMENTO, e un"
              " confronto senza riferimento e' un'opinione.")
        return 1
    print("  ### il riferimento lo ha prodotto IL BANCO: scena di %d nodi, %d archi"
          % (sc["n"], sc["m"]))
    print()
    esito("il collaudo ha MATERIA: il banco ha prodotto %d variabili" % len(st),
          len(st) >= 4 and all(v.size > 0 for v in st.values()),
          "### con zero variabili ogni confronto passerebbe PER VACUITA-")

    # ============================================ (1) IL CONFRONTO, variabile per variabile
    var = tabella()
    esito("### e la tabella dichiara %d variabili" % len(var), len(var) >= 4,
          "### %s" % ", ".join(n for n, _ in var))
    for nome, tipo in var:
        v = st.get(nome)
        if v is None:
            # ### ⭐ **IL BANCO NON LA HA, e NON e- un errore: e- il verso `(b)`.** La
            # ### variabile deve essere ### **dichiarata `NUOVA` col punto della carta**,
            # ### e il presidio dell-era `2` lo pretende -- qui si verifica ### **che la
            # ### riga ci sia.** *(Il suo ID sta nel DOCSTRING del modulo: un
            # ### riferimento che una macchina deve seguire non vive nella prosa di un
            # ### commento.)*
            e = righe_del_confronto().get(nome)
            esito("### `%s`: il banco NON la ha ⟹ la riga dice `NUOVA`" % nome,
                  e in ("NUOVA", "ORFANA"),
                  "### la riga dice `%s`: senza riga, `P-E10` rifiuta il commit" % e)
            continue
        err = confronta(nome, tipo, v, sc)
        esito("### `%s` (`%s`) coincide col banco: `dtype`, componenti, dove vive"
              % (nome, tipo), not err,
              "### %s, %s" % (v.dtype, v.shape) if not err else "### " + err[0][:70])

    # ============================================ (2) OGNI VARIABILE HA LA SUA RIGA
    print()
    righe = righe_del_confronto()
    senza = [n for n, _ in var if n not in righe]
    esito("### (2) OGNI variabile della tabella ha la sua riga nel confronto",
          not senza, "### %d su %d: %s" % (len(righe), len(var),
                                           "manca " + ", ".join(senza) if senza
                                           else "nessuna manca"))

    # ============================================ (3) I CASI CHE DEVONO FALLIRE
    print()
    # ### ⛔ **IL CASO CHE IL MANDATO NOMINA: `phi` dichiarato REALE contro il banco
    # ### COMPLESSO.** ### ⭐ **E- il disallineamento che e- sfuggito TRE VOLTE**, e se
    # ### questo braccio non lo prendesse il collaudo ### **non servirebbe a niente.**
    err = confronta("phi_h", "reale_nodo", st["phi_h"], sc)
    esito("### (3) DEVE fallire: `phi_h` dichiarato REALE contro il banco COMPLESSO",
          any("complex128" in x and "float64" in x for x in err),
          "### %s" % (err[0][:72] if err else "### NON ha visto niente"))
    # ### e il DOVE sbagliato: `psi_h` dichiarato sul NODO
    err = confronta("psi_h", "complesso_c2_nodo", st["psi_h"], sc)
    esito("### DEVE fallire: `psi_h` dichiarato sul NODO invece che sull'estremita'",
          any("vive su" in x for x in err),
          "### %s" % (err[0][:72] if err else "### NON ha visto niente"))
    # ### e le COMPONENTI sbagliate: `phi_h` come `C^2`
    err = confronta("phi_h", "complesso_c2_estremita", st["phi_h"], sc)
    esito("### DEVE fallire: `phi_h` dichiarato `C^2` invece che scalare",
          any("componenti" in x for x in err),
          "### %s" % (err[0][:72] if err else "### NON ha visto niente"))
    # ### e un TIPO che la mappa non conosce: ### **non si salta in silenzio**
    err = confronta("phi_h", "un_tipo_inventato", st["phi_h"], sc)
    esito("### DEVE fallire: un tipo che la mappa NON conosce, invece di saltarlo",
          any("non sta nella mappa" in x for x in err),
          "### un tipo nuovo che passasse in silenzio sarebbe il buco di domani")
    # ### ✅ **E IL VERSO OPPOSTO: il tipo GIUSTO non alza** -- senza questo braccio, i
    # ### quattro di sopra passerebbero anche se `confronta` dicesse SEMPRE errore.
    esito("### e il verso OPPOSTO: il tipo GIUSTO di `phi_h` NON alza",
          not confronta("phi_h", "complesso_estremita", st["phi_h"], sc),
          "### senza questo, i quattro di sopra passerebbero anche se `confronta`"
          " dicesse SEMPRE errore")

    # ============================================ (4) I CONTEGGI DEL DOCUMENTO
    print()
    t = io.open(CONFRONTO, encoding="utf-8").read() if os.path.exists(CONFRONTO) else ""
    esito("### (4) il documento del confronto ESISTE e porta i CONTEGGI in testa",
          "I CONTEGGI, PER ESITO" in t,
          "### %d caratteri: senza i conteggi in testa, chi legge deve contare a mano"
          % len(t))
    esito("### e cita le prove PER NOME DI FUNZIONE, non per riga",
          ".py:" not in t,
          "### i numeri di riga sono di blob vecchi e SONO SHIFTATI (par.2)")

    print("=" * 100)
    print("IL CONFRONTO TABELLA / BANCO: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
