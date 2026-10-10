# -*- coding: utf-8 -*-
"""IL COLLAUDO DELLO SCHEMA DELLA TABELLA — **nei DUE VERSI, su righe costruite in
memoria.**

> ### ⛔ **PERCHE' STA IN UN FILE SUO, dal `2026-10-10`:** `schema.py` era arrivato a
> ### **`736` righe**, oltre il tetto di `700`, e `P-MOD` ha rifiutato il commit con la
> frase giusta — ### **«oltre SI DIVIDE, NON SI ALLUNGA».**

### ⭐ **E LA DIVISIONE NON E' A CASO: e' la stessa che `_genera.py` ha avuto.** Il
collaudo e' ### **la parte che cresce**, perche' ogni controllo nuovo porta
### **il suo caso che deve fallire** — e lo schema, che e' ### **la regola**, deve
restare leggibile.

### ⚠ **E IL TETTO NON SI ALZA.** Alzarlo sarebbe ### **spegnere il presidio dal lato
del numero**, che e' `A9` con un vestito diverso.

Gira con:  python primo_ordine/leggi/_collauda_schema.py
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(_QUI)), "csv"))

from schema import (                                         # noqa: E402
    RADICE, TIPI_VARIABILE, VIETATI, dimensioni_incoerenti,
    simboli_vietati, valida_legge, valida_variabile,
)

# =====================================================================================
#   IL COLLAUDO DELLO SCHEMA -- nei due versi, su righe costruite in memoria
# =====================================================================================

def collaudo():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    VAR = {"psi": "complesso_c2_nodo", "w": "reale_arco", "theta": "fase_arco",
           "rho": "reale_nodo", "qp": "coppia_coniugata"}

    def base(**kw):
        d = {"id": "PROVA-UNO", "tipo": "termine_nodo", "espressione": "rho**2",
             "ambito": ["rho"], "parametri": {}, "assiomi": [], "prova": True,
             "scheda": "una scheda",
             # ### ⚠ **`rho` NON E- `psi`**, quindi la sostituzione di `U(1)`
             # ### ### **non tocca nessun simbolo** -- ed e- ### **invariante
             # ### davvero**, non per vacuita-: la legge NON COINVOLGE LA FASE.
             "simmetrie": ["U1-FASE-GLOBALE"], "conserva": []}
        d.update(kw)
        return {k: v for k, v in d.items() if v is not None}

    print("=" * 100)
    print("IL COLLAUDO DELLO SCHEMA DELLA TABELLA -- nei DUE VERSI")
    print("=" * 100)
    esito("il caso SANO", valida_legge(base(), VAR) == [])
    esito("### id troppo corto (`AB`)", valida_legge(base(id="AB"), VAR) != [],
          "almeno 4 caratteri")
    esito("### `tipo` fuori vocabolario", valida_legge(base(tipo="PIPPO"), VAR) != [])
    esito("### una chiave NON prevista", valida_legge(base(zzz=1), VAR) != [],
          "il vocabolario e- CHIUSO")
    esito("### `scheda` vuota", valida_legge(base(scheda=" "), VAR) != [],
          "una legge senza scheda NON si genera")
    esito("### `prova` non booleano", valida_legge(base(prova="si"), VAR) != [])
    esito("### l-ambito nomina una variabile INESISTENTE",
          valida_legge(base(ambito=["non-esiste"]), VAR) != [])
    # ### ⛔ **IL CASO CHE IL MANDATO NOMINA: un termine di nodo che legge un vicino.**
    esito("### un `termine_nodo` con una variabile d-ARCO nell-ambito",
          any("NON VEDE I VICINI" in e
              for e in valida_legge(base(ambito=["w"]), VAR)),
          "una variabile d-ARCO collega due nodi: leggerla E- vedere il vicino")
    esito("NON deve scattare: un `termine_arco` con la STESSA variabile d-arco",
          valida_legge(base(tipo="termine_arco", ambito=["w"]), VAR) == [],
          "un termine d-arco PUO- leggere l-arco: e- il suo mestiere")
    # ### ⛔ **I PARAMETRI: `A1` pretende valore E ORIGINE.**
    esito("### un parametro SENZA `origine`",
          any("MANOPOLA" in e
              for e in valida_legge(base(parametri={"K": {"valore": 1.0}}), VAR)),
          "`A1`: la legge, NON il numero")
    esito("### un parametro senza `dimensione`",
          any("CHE COSA SIA" in e
              for e in valida_legge(base(parametri={"K": {
                  "valore": 1.0, "origine": "valore di prova"}}), VAR)),
          "### un numero senza dimensione e- un numero di cui non si sa CHE COSA SIA")
    esito("NON deve scattare: un parametro con `valore`, `origine` E `dimensione`",
          valida_legge(base(parametri={"K": {"valore": 1.0,
                                             "origine": "valore di prova",
                                             "dimensione": "E^1"}}), VAR) == [])
    # ### ⛔ **IL BILANCIO di una regola.**
    reg = {"id": "PROVA-REG", "tipo": "regola", "ingressi": [], "uscite": [],
           "bilancio": "", "assiomi": [], "prova": True, "scheda": "s"}
    esito("### una `regola` col `bilancio` VUOTO",
          any("DA QUALCHE PARTE" in e for e in valida_legge(reg, VAR)),
          "cio- che esce da `H` deve andare da qualche parte")
    # ### \u26d4 **DAL 2026-10-10 QUESTO E- IL CASO CHE DEVE FALLIRE**, e prima era
    # ### il caso SANO: ### **<<l-energia va nel vuoto>> e- IL NOME DI UN MECCANISMO**,
    # ### non una formula. ### \u2b50 **Il valore con cui lo schema provava che una
    # ### regola dichiarata PASSA e- diventato cio- che RIFIUTA.**
    reg_prosa = dict(reg, bilancio="l-energia va nel vuoto")
    esito("### DEVE scattare: un `bilancio` che e- PROSA e non una formula",
          any("NON SI LEGGE COME FORMULA" in x or "non sono ne- " in x
              for x in valida_legge(reg_prosa, VAR)),
          "### decisione di Luca, 2026-10-10: un bilancio e- una FORMULA che il "
          "generatore verifica")
    reg_pos = dict(reg, bilancio="rho - pos_x")
    esito("### DEVE scattare: un `bilancio` che nomina una POSIZIONE",
          any("VIETATI" in x for x in valida_legge(reg_pos, VAR)),
          "### `A17` vale per il bilancio come per un termine di `H`")
    reg_ramo = dict(reg, bilancio="Max(rho, 0) - rho")
    esito("### DEVE scattare: un `bilancio` con un RAMO vietato",
          any("VIETATI" in x for x in valida_legge(reg_ramo, VAR)),
          "### `A11`: un limite e- una LEGGE, non una toppa -- anche in un bilancio")
    reg2 = dict(reg, bilancio="rho - rho")
    esito("NON deve scattare: la stessa regola col bilancio dichiarato",
          valida_legge(reg2, VAR) == [])
    # ### ⛔ **L-OSSERVATORE dichiara la sua VOCE.**
    oss = {"id": "PROVA-OSS", "tipo": "osservatore", "espressione": "rho",
           "ambito": ["rho"], "voce": "", "assiomi": [], "prova": True, "scheda": "s",
           "dimensione": "E^0", "simmetrie": ["U1-FASE-GLOBALE"], "conserva": []}
    esito("### un `osservatore` senza `voce`",
          any("MISURA/CRITERIO" in e for e in valida_legge(oss, VAR)))
    esito("NON deve scattare: lo stesso osservatore con la `voce`",
          valida_legge(dict(oss, voce="Z999-PROVA"), VAR) == [])
    print()
    print("  (b) LE DUE DECISIONI APERTE: AMMESSE, NON SCELTE")
    # ### ⭐ **LA `coppia_coniugata` E- AMMESSA E NON USATA, e il braccio lo PROVA:** un tipo
    # ### che nessuno usa ### **non e- collaudato dall-uso**, solo dallo schema.
    esito("la `coppia_coniugata` e- NEL VOCABOLARIO (decisione `13`, aperta)",
          "coppia_coniugata" in TIPI_VARIABILE)
    esito("e lo schema ACCETTA una legge che la legge",
          valida_legge(base(ambito=["qp"]), VAR) == [],
          "AMMESSA, e NESSUNA legge della tabella la usa: non e- SCELTA")
    esito("### e `pos` NON e- un tipo di variabile (decisione `9`, aperta)",
          not any("pos" in k for k in TIPI_VARIABILE),
          "il formato NON PUO- esprimere una geometria, quindi non ne sceglie una")
    esito("### e un-espressione che nomina `pos` si RICONOSCE",
          simboli_vietati("K * pos_x + rho") == ["pos_x"],
          "`A17` per costruzione")
    esito("NON deve scattare: un-espressione che nomina `rho`",
          simboli_vietati("K * rho**2") == [])
    # ### ⚠ **E `x` dentro una parola NON conta:** `max`, `xi`, `index`.
    esito("NON deve scattare: `x` DENTRO una parola (`max`, `xi`, `index`)",
          simboli_vietati("max(xi) + index") == [],
          "i confini di parola: e- la quarta volta che una parola dentro un-altra inganna")
    print()
    print("  (c) IL VOCABOLARIO DELLE VARIABILI")
    esito("una variabile SANA",
          valida_variabile({"nome": "rho", "tipo": "reale_nodo", "voce": "V-X",
                            "scheda": "s", "dimensione": "E^1"}) == [])
    esito("### una variabile SENZA `dimensione`",
          any("`hbar = 1`" in e for e in valida_variabile(
              {"nome": "rho", "tipo": "reale_nodo", "voce": "V-X", "scheda": "s"})),
          "### e la dimensione sta SULLA VARIABILE, non sul tipo: due `reale_nodo` "
          "possono essere UN-ENERGIA E UN TEMPO")
    # ===================================================================================
    #   ### ⭐ **IL CONTROLLO DIMENSIONALE, provato DIRETTAMENTE** *(punto `2`)*
    # ===================================================================================
    # ### ⚠ **E si prova QUI e non attraverso `valida_legge`, per una ragione che
    # ### dichiaro:** `valida_legge` prende `variabili` in ### **DUE FORME** -- la tabella
    # ### vera gli passa ### **una lista di dizionari** *(che portano la `dimensione`)*,
    # ### questo collaudo gli passa ### **un dizionario `nome -> tipo`** *(che non la
    # ### porta)*. ### **Quindi il controllo dimensionale li- NON GIRA**, e provarlo
    # ### attraverso quella via ### **direbbe PASSA senza aver guardato niente.**
    # ### ✅ **`dimensioni_incoerenti` e- PURA: si prova su righe costruite a mano.**
    print()
    print("  (e) LE DIMENSIONI -- punto 2 della terza parte")
    DIM = {"psi": "E^0"}
    HOP = {"id": "PROVA-DIM", "tipo": "termine_arco",
           "espressione": "-K*(psi_i_0c*psi_j_0 + psi_j_0c*psi_i_0)",
           "parametri": {"K": {"dimensione": "E^1"}}}
    esito("NON deve scattare: un termine d-arco con `K` di dimensione `E^1`",
          dimensioni_incoerenti(HOP, DIM) == [],
          "### `psi` e- ADIMENSIONALE (`psi^dag psi` e- un CONTEGGIO), quindi `K` deve "
          "essere un-energia perche- il termine entri in `H`")
    esito("### DEVE scattare: lo stesso termine con `K` di dimensione `E^2`",
          any("NON E- UN TERMINE DI `H`" in e for e in dimensioni_incoerenti(
              dict(HOP, parametri={"K": {"dimensione": "E^2"}}), DIM)),
          "### `H` E- UN-ENERGIA: un termine che non lo e- non e- un termine di `H`")
    MIX = {"id": "PROVA-MIX", "tipo": "termine_nodo",
           "espressione": "K*psi_0c*psi_0 + g*psi_0c*psi_0*psi_1c*psi_1",
           "parametri": {"K": {"dimensione": "E^1"}, "g": {"dimensione": "E^2"}}}
    esito("### DEVE scattare: DUE ADDENDI di dimensione diversa",
          any("UN-ALTRA FISICA" in e for e in dimensioni_incoerenti(MIX, DIM)),
          "### sommare un-energia e un-energia al quadrato NON e- un errore di "
          "battitura: e- un-altra fisica")
    esito("NON deve scattare: gli stessi addendi con `g` di dimensione `E^1`",
          dimensioni_incoerenti(
              dict(MIX, parametri={"K": {"dimensione": "E^1"},
                                   "g": {"dimensione": "E^1"}}), DIM) == [],
          "### e- il braccio che dice che il controllo NON rifiuta OGNI somma")
    OSS = {"id": "PROVA-OSSD", "tipo": "osservatore", "espressione": "psi_0c*psi_0",
           "dimensione": "E^0", "parametri": {}}
    esito("NON deve scattare: un osservatore `E^0` che misura la NORMA",
          dimensioni_incoerenti(OSS, DIM) == [],
          "### pretendere `E^1` da ogni osservatore VIETEREBBE DI MISURARE LA NORMA, "
          "che e- la prima cosa che si misura")
    esito("### DEVE scattare: lo stesso osservatore che dichiara `E^1`",
          any("dichiara" in e for e in dimensioni_incoerenti(
              dict(OSS, dimensione="E^1"), DIM)),
          "### l-espressione da- `E^0`: una dichiarazione che non coincide e- PEGGIO di "
          "nessuna dichiarazione")
    esito("### DEVE scattare: un simbolo che non risale a nessuna variabile",
          any("non risale" in e for e in dimensioni_incoerenti(
              dict(HOP, espressione="-K*zeta_0c*zeta_0"), DIM)),
          "### non la indovino: un controllo che riempie i buchi da se- NON CONTROLLA "
          "NIENTE")
    esito("### una variabile col `tipo` fuori vocabolario",
          valida_variabile({"nome": "rho", "tipo": "PIPPO", "voce": "V-X",
                            "scheda": "s"}) != [])
    esito("### una variabile chiamata `pos`",
          any("A17" in e for e in valida_variabile({"nome": "pos",
                                                    "tipo": "reale_nodo",
                                                    "voce": "V-X", "scheda": "s"})))
    esito("### una variabile senza `voce`",
          valida_variabile({"nome": "rho", "tipo": "reale_nodo", "voce": "",
                            "scheda": "s"}) != [],
          "ogni variabile ha una voce in `doc/indice/variabili.jsonl` (`P-E3`)")
    print("=" * 100)
    print("IL COLLAUDO DELLO SCHEMA: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1

if __name__ == "__main__":
    sys.exit(collaudo())
