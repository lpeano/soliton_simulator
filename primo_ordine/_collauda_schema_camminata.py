# -*- coding: utf-8 -*-
r"""IL COLLAUDO DELLO SCHEMA DELLA CAMMINATA — **nei DUE VERSI, sempre.**

> ### ⛔ **Un braccio che prova solo che una cosa giusta PASSA non e' un collaudo:** prova
> che il presidio **non rifiuta il buono**, e **non dice niente** su cio' che deve
> rifiutare. ### **Qui ogni controllo nuovo ha il suo rovescio.**

### ⚠ **DUE COSE CHE QUESTO FILE HA IMPARATO DAI PRESIDI, e stanno QUI e non in un
commento perche' `P-RIF` ha ragione: un ID che una macchina deve seguire non vive nella
prosa di un commento** — o e' un costrutto, o e' documentazione.

* **l'import e' `import schema`, piatto e non relativo:** la mappa dei moduli dichiara la
  dipendenza col nome `schema`, e `P-MOD` pretende che **cio' che la mappa prevede sia
  cio' che il file importa** — *«una dipendenza dichiarata e non usata resta come un
  permesso che nessuno ha chiesto»*.
* **il primo caso di prova che avevo scritto era SBAGLIATO, e il presidio me l'ha preso:**
  usava `x` come argomento del generatore, e **`x` e' un nome di COORDINATA**, vietato da
  `A17`. Il generatore vero non ha `x`: e' `Lambda * G(h/Lambda)`, e le sue variabili sono
  **`h` e `Lambda`**, che sono grandezze del sistema.

Gira con:  python primo_ordine/_collauda_schema_camminata.py
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(_QUI, "leggi"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import schema as S                                            # noqa: E402


def _pezzo(**k):
    """Un `pezzo_unitario` VALIDO, da cui i bracci rompono UNA cosa per volta."""
    d = {"id": "PROVA-MONETA", "tipo": "pezzo_unitario", "prova": True,
         "scheda": "un pezzo di prova", "assiomi": ["A16"],
         "operatore": "moneta_spin", "azione": "estremita",
         "ambito": ["psi"], "parametri": {}, "simmetrie": []}
    d.update(k)
    return d


def _flusso(**k):
    d = {"id": "PROVA-FLUSSO", "tipo": "flusso", "prova": True,
         "scheda": "un flusso di prova", "assiomi": [],
         "generatore": "Lambda*(h/Lambda - atan(h/Lambda))", "esatto": True,
         "ambito": ["psi"], "parametri": {}, "simmetrie": [], "conserva": []}
    d.update(k)
    return d


VAR = {"psi": "complesso_c2_estremita", "phi": "reale_estremita",
       "h": "reale_estremita", "Lambda": "reale_nodo"}


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("LO SCHEMA DELLA CAMMINATA -- nei DUE VERSI")
    print("=" * 100)

    # ============================================== i TIPI nuovi esistono
    esito("### i due tipi di legge nuovi sono nel vocabolario",
          "pezzo_unitario" in S.TIPI and "flusso" in S.TIPI,
          "### %s" % list(S.TIPI))
    esito("### i due tipi di variabile delle ESTREMITA' esistono",
          "complesso_c2_estremita" in S.TIPI_VARIABILE
          and "reale_estremita" in S.TIPI_VARIABILE)
    esito("### e hanno un DOMINIO dichiarato (senza, nessuno li controlla)",
          S.DOMINI.get("complesso_c2_estremita") == "finito"
          and S.DOMINI.get("reale_estremita") == "finito")
    esito("### e `estremita` e' un TERZO posto, non un sinonimo di `arco`",
          S.DOVE.get("complesso_c2_estremita") == "estremita"
          and S.DOVE.get("reale_arco") == "arco",
          "### un arco ha DUE estremita': confonderli dimezza o raddoppia lo stato")

    # ============================================== `pezzo_unitario`: i DUE VERSI
    esito("### (1) un `pezzo_unitario` valido PASSA", not S.valida_legge(_pezzo(), VAR))
    esito("### (1-bis) un `operatore` FUORI vocabolario e' RIFIUTATO",
          bool(S.valida_legge(_pezzo(operatore="moneta_inventata"), VAR)),
          "### il vocabolario e' CHIUSO (posto `P4`)")
    esito("### (1-ter) un'`azione` FUORI vocabolario e' RIFIUTATA",
          bool(S.valida_legge(_pezzo(azione="dove_mi_pare"), VAR)))
    esito("### (1-quater) un `pezzo_unitario` con `espressione` e' RIFIUTATO",
          bool(S.valida_legge(_pezzo(espressione="psi_0"), VAR)),
          "### un unitario NON si scrive come espressione: ha un `operatore`")
    esito("### (1-quinquies) e senza `operatore` e' RIFIUTATO",
          bool(S.valida_legge({k: v for k, v in _pezzo().items()
                               if k != "operatore"}, VAR)))

    # ============================================== `flusso`: i DUE VERSI
    esito("### (2) un `flusso` valido PASSA", not S.valida_legge(_flusso(), VAR))
    esito("### (2-bis) un `flusso` SENZA generatore e' RIFIUTATO",
          bool(S.valida_legge(_flusso(generatore="   "), VAR)),
          "### il flusso e' DI QUALCOSA, e quel qualcosa va scritto")
    esito("### (2-ter) un `flusso` con `esatto` NON booleano e' RIFIUTATO",
          bool(S.valida_legge(_flusso(esatto="si'"), VAR)),
          "### non e' una promessa: e' una dichiarazione che un collaudo verifica")

    # ============================================== L'ORDINE: i DUE VERSI
    LEGGI = [_pezzo(id="PROVA-LINEARE", operatore="grover", azione="nodo"),
             _flusso(id="PROVA-ENNE"),
             {"id": "PROVA-TERMINE", "tipo": "termine_nodo", "prova": True,
              "scheda": "x", "assiomi": [], "espressione": "psi_0*psi_0c",
              "ambito": ["psi"], "parametri": {}, "simmetrie": [], "conserva": []}]
    # ### ⭐ **IL BRACCIO CHE VALE PIU' DI TUTTI: LO STESSO PEZZO DUE VOLTE.**
    strang = [{"legge": "PROVA-ENNE", "frazione": 0.5},
              {"legge": "PROVA-LINEARE", "frazione": 1},
              {"legge": "PROVA-ENNE", "frazione": 0.5}]
    esito("### (3) LA COMPOSIZIONE DI STRANG PASSA: lo stesso pezzo DUE VOLTE",
          not S.valida_ordine(strang, LEGGI),
          "### e' l'argomento che ha CHIUSO il posto `P2`")
    esito("### (3-bis) l'ordine ASSENTE e' RIFIUTATO",
          bool(S.valida_ordine(None, LEGGI)) and bool(S.valida_ordine([], LEGGI)),
          "### senza ordine il passo NON ESISTE: i pezzi si COMPONGONO")
    esito("### (3-ter) le frazioni che NON sommano a 1 sono RIFIUTATE",
          bool(S.valida_ordine([{"legge": "PROVA-ENNE", "frazione": 0.5},
                                {"legge": "PROVA-LINEARE", "frazione": 1},
                                {"legge": "PROVA-ENNE", "frazione": 0.4}], LEGGI)),
          "### 0.5 + 0.4 = 0.9 NON integra il passo intero: e' un PASSO SBAGLIATO")
    esito("### (3-quater) una legge che NON ESISTE e' RIFIUTATA",
          bool(S.valida_ordine([{"legge": "NON-CI-SONO", "frazione": 1}], LEGGI)))
    esito("### (3-quinquies) un `termine_*` nell'ordine e' RIFIUTATO",
          bool(S.valida_ordine([{"legge": "PROVA-TERMINE", "frazione": 1}], LEGGI)),
          "### un termine sta DENTRO un generatore, non nella composizione")
    esito("### (3-sexies) una `frazione` fuori da `(0, 1]` e' RIFIUTATA",
          bool(S.valida_ordine([{"legge": "PROVA-ENNE", "frazione": 0}], LEGGI))
          and bool(S.valida_ordine([{"legge": "PROVA-ENNE", "frazione": 1.5}], LEGGI)))
    esito("### (3-septies) una chiave NON prevista nell'elemento e' RIFIUTATA",
          bool(S.valida_ordine([{"legge": "PROVA-ENNE", "frazione": 1,
                                 "quando": "dopo"}], LEGGI)),
          "### il vocabolario e' CHIUSO anche dentro l'ordine")

    # ======================================= IL PRESIDIO SUI POSTI APERTI, tre versi
    # ### ⛔ **E- L-IMPEDIMENTO che la decisione di Luca pretende**, e <<accendere>>
    # ### ha un significato preciso: ### **stare nell-ORDINE.** Una legge in tabella e
    # ### ### **fuori** dall-ordine ### **esiste e non agisce.**
    APERTA = _flusso(id="PROVA-APERTA", posto="A4",
                     voce_decisione="DOMANDA-FINTA-APERTA")
    LEGGI2 = LEGGI + [APERTA]
    fuori_ordine = [{"legge": "PROVA-ENNE", "frazione": 1}]
    dentro = [{"legge": "PROVA-APERTA", "frazione": 1}]
    esito("### (5) un posto aperto FUORI dall'ordine PASSA",
          not S.valida_posti(fuori_ordine, LEGGI2),
          "### in tabella e fuori dall'ordine: ESISTE e NON AGISCE")
    esito("### (5-bis) e DENTRO l'ordine, con la voce NON decisa, e' RIFIUTATO",
          bool(S.valida_posti(dentro, LEGGI2)),
          "### accendere un posto aperto senza la sua decisione e' accenderlo di nascosto")
    esito("### (5-ter) e DENTRO l'ordine con la voce DECISA PASSA",
          not S.valida_posti(dentro, LEGGI2,
                             voci_decise=("DOMANDA-FINTA-APERTA",)),
          "### il braccio (5-bis) NON e' un falso-uno: scatta per la VOCE, non per l'id")
    esito("### (5-quater) e un posto DICHIARATO SENZA la sua voce e' RIFIUTATO",
          bool(S.valida_posti(dentro, LEGGI + [_flusso(id="PROVA-APERTA",
                                                       posto="A4")])),
          "### <<appartengo a un posto aperto>> senza dire QUALE decisione non basta")
    esito("### (5-quinquies) e il valore di comodo e' il piu' SEVERO",
          bool(S.valida_posti(dentro, LEGGI2)),
          "### chi chiama senza l'elenco ottiene NESSUNA decisa, non TUTTE")

    # ============================================== e i VIETATI valgono ancora
    esito("### (4) una POSIZIONE nell'`ambito` resta VIETATA anche sui tipi nuovi",
          bool(S.valida_legge(_flusso(generatore="pos_x*psi_0"), VAR)),
          "### `A17`: una posizione non entra nella fisica (decisione `9`)")

    print("=" * 100)
    print("LO SCHEMA DELLA CAMMINATA: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
