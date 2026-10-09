# -*- coding: utf-8 -*-
"""FASE 2: LE 184 VOCI *CHIUSE* SENZA DOMINIO — **ricevono SOLO dominio ed era.**

### ⛔ **Lo stato NON si tocca:** sono chiuse, e restano chiuse.

| | |
|---|--:|
| da una ### **regola**: fonte `doc/RAMIFICAZIONI.md` e classe `FRONTE` o `MISURA` — il documento dei ### **rami di ricerca sul sistema** | `102` |
| ### **lette una per una** | `82` |

### ⚠ **E L'<<EPOCA>> NON E' L'ERA, e queste voci me l'hanno insegnato:** `65` di loro portano
`[EPOCA 1]`, `11` `[EPOCA 3]`, `3` `[EPOCA 2]`. ### **Le epoche `1`-`2`-`3` sono FASI DI
LAVORO sul simulatore del SECONDO ordine**, mentre l'era `2` dello schema e' ### **la
riscrittura al primo ordine** — che e' la ### **lista `L2` di Luca**, non un marcatore nel
testo. ### ➜ **Avevo sbagliato su `4` voci** *(`Z87` `Z90` `Z91` `Z92`)*, corrette.

Gira con:  python csv/_fase2_chiuse.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"
PER_LOTTO = 50
M, F, I, DOC = "METODO", "FISICA", "INFRASTRUTTURA", "DOCUMENTAZIONE"

LETTE = {
    # ---------------------------------------- METODO: la validita' di una misura
    "B2": (M, "i SIGILLI NON RI-GIRABILI: e' la ri-eseguibilita' di una prova"),
    "CBIS-CRITERIO-VACUO": (M, "<<ed e' un FALSO-UNO>>: un verdetto garantito da qualcosa che "
                               "non parla del merito"),
    "CTRL-RISCELTA": (M, "<<i punti di controllo si RISCEGLIEVANO a ogni checkpoint>>: il "
                         "controllo non era un controllo"),
    "FINESTRA-DEL-PICCO": (M, "<<prima di usare 'non esplode'...>>: e' la FINESTRA di una "
                              "misura"),
    "FINESTRA-NON-DICHIARATA": (M, "<<TROVATO DAL PRESIDIO 3-bis AL SUO PRIMO GIRO>>: una "
                                   "finestra non dichiarata"),
    "MASSA-ID-FISSO": (M, "<<la versione a lignaggio fisso di MASSA-ID>>: l'identita' che "
                          "rende confrontabile una misura"),
    "OSSERVABILE-P1": (M, "<<NON ESISTE UNO STRUMENTO...>>: manca il mezzo per misurare"),
    "PESO-MAX": (M, "<<In questa scena e' INERTE, e lo dice una misura>>: e' la regola di "
                    "lettura di un'osservabile"),
    "SIM-PRIMA-STANTIO": (M, "la COPIA <<prima>> era STANTIA: la provenienza di un confronto"),
    "T4-TAUTOLOGICO": (M, "<<i valori sono costruiti per aritmetica>>: un collaudo "
                          "TAUTOLOGICO non prova niente"),
    "VELENO-ARCHI-KEEP": (M, "e' la sonda del VELENO: una prova sullo strumento"),
    "VELENO-AUTORINFRESCO": (M, "e' la sonda del VELENO, e <<NON LO DECIDO IO>>"),
    "C5-INVARIANTI": (M, "<<INVARIANTI -- 42 domini, due livelli>>: e' il presidio degli "
                         "invarianti"),
    "P1BIS-DELTA": (M, "<<P1-bis VERIFICA LA PRESENZA DI...>>: parla di un presidio"),
    # ---------------------------------------- INFRASTRUTTURA
    "A5-PANNELLO": (I, "<<il PANNELLO FEDELE (interpolazione di psi accanto a "
                       "campo_spaziale)>>: e' il RENDERING"),
    "B10": (I, "<<--override-blob e la COPIA del driver>>: strumenti e file"),
    "B8": (I, "<<IL BLOCCO DEL RUN A 6000 AL PASSO 2700>>: una corsa che si ferma"),
    "LUNGA-BATTITO-CADUTA": (I, "<<LA CORSA DELLA MISURA LUNGA E' CADUTA>>: l'esecuzione"),
    "LETTORI-INDICE": (I, "sono i LETTORI DELL'INDICE: strumenti"),
    "HASHSEED-RIPROD": (I, "<<l'ordine di iterazione di qualche insieme, che dipende "
                           "dall'hash randomizzato>>: e' il CODICE a non essere "
                           "deterministico"),
    "MITOSI-NON-DIVISA": (I, "<<spezzare mitosi() in una voce STRUTTURALE e una di STATO "
                             "restando BYTE-IDENTICA e' internamente incompatibile>>: e' la "
                             "struttura del codice"),
    "CURA2-STRUTTURALE": (I, "<<i rami `else` di TEMPO_UNICO_MITOSI>>: struttura del codice"),
    "ARCH-PAVIMENTI": (I, "<<i pavimenti MORTI escono dal simulatore>>: codice archiviato"),
    "ARCH-SYNC": (I, "<<SYNC_UPDATE e i suoi rami parziali escono>>: codice archiviato"),
    "DRIVER-SCENA-II": (I, "<<IL DRIVER NON SA FARE LA...>>: e' il driver"),
    "SCHED-T1": (I, "e' la tappa `T1` dello SCHEDULATORE DEL PASSO: architettura del codice"),
    "SCHED-T2-TIPI": (I, "<<ogni voce di `_PASSO_REG...`>>: architettura del codice"),
    "SCHED-T2-VALIDA": (I, "<<esegui_pa...>>: architettura del codice"),
    "NASCITA-PUNTO-UNICO": (I, "<<PRIMA i posti che scrivevano le grandezze>>: i SITI nel "
                               "codice"),
    "ETC-C1-CONFINE": (I, "<<_smp_apri() diventa IDEMPOTENTE>>: una funzione del codice"),
    "ARCH-LCONSERVA": (I, "<<strada (b) per l'incoerenza di tipo...>>: l'archiviazione"),
    # ---------------------------------------- DOCUMENTAZIONE
    "RIORDINO-NOMI-H": (DOC, "<<il prefisso `H-` e' sui NOMI VECCHI e non sui nomi "
                             "semantici>>: sono NOMI"),
    "RIORDINO-POSTO2": (DOC, "<<IL POSTO 2 HA 11 REGOLE E IL TETTO E' 10>>: e' un documento "
                             "di regole"),
    "ETICHETTA-A13": (DOC, "<<l'etichetta sbagliata `A13` dove la regola e' `A3-DISEGNO`>>: "
                           "un'etichetta sbagliata"),
    "REGIME-COMMENTI": (DOC, "sono i COMMENTI del regime: un testo"),
    "KAPPA-TW-COMMENTO": (DOC, "e' un COMMENTO su `kappa_tw`, letto dal codice"),
    "CHI-BASC-DESCRIZIONE": (DOC, "e' la DESCRIZIONE di `chi_basc`, che diceva una cosa "
                                  "falsa"),
    # ---------------------------------------- FISICA
    "A1-TREVIE": (F, "<<la catena a TRE VIE di `step`>>: l'ordine delle leggi"),
    "A2-ANELLO": (F, "<<l'anello `A6` di Z70 -- periodo 2>>: una retroazione fra leggi"),
    "A3-CHIRALE": (F, "<<la carica chirale non si conserva>>: una conservazione"),
    "A6-PERCCHI": (F, "<<`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE>>: una variabile di "
                      "stato"),
    "B1": (F, "<<`pos` nella fisica: l'ultimo SFONDO>>"),
    "B3": (F, "<<i rami di `memoria_hebbiana_moto`>>: una legge"),
    "B4": (F, "<<i `np.zeros` | tutto il simulatore | sono 116>>: l'inizializzazione dello "
              "STATO (`A7b`)"),
    "B5": (F, "<<theta / l'aliasing del settore di spin>>"),
    "COER-4PI": (F, "<<la coerenza della massa e' |<e^{i phi}>|, e non e' una convenzione>>"),
    "COPPIA-RAMP": (F, "<<PERCHE' LA COPPIA NON PORTA `ramp`?>>"),
    "D02": (F, "<<`pozzo_grafo` calcola `L` da `self.pos` -- IL DISEGNO>>"),
    "POZZO-D": (F, "<<la cura di D02: nel pozzo del grafo `L` viene da `self.d`>>"),
    "D09": (F, "<<`chi_basc` BLOCCA la mitosi e DIMEZZA l'olonomia netta>>"),
    "D11": (F, "<<`d` scende DIECI VOLTE sotto LAM mentre SCALA_MIN e' acceso>>"),
    "D16": (F, "<<SCALA_MIN frenava OGNI scrittura separatamente>>"),
    "D17": (F, "<<`peq` diventava NEGATIVO e il pavimento NE RIBALTAVA...>>"),
    "D18": (F, "<<COES_ADIM leggeva ISTANTI MISTI e il suo tetto era GLOBALE>>"),
    "D19": (F, "<<OTTO grandezze che la semina legge erano INERTI SUL VUOTO>>"),
    "D22": (F, "<<Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B)>>"),
    "D27": (F, "<<Il grafo e' in QUATTRO COMPONENTI che non si toccano mai>>"),
    "D32": (F, "<<I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE>>"),
    "D34": (F, "<<Il wrap 'a 4pi' di `ritmo()`>>"),
    "D37": (F, "<<CHIAVE DUPLICATA NEI DOMINI: 'cs_nodo_prev'...>>"),
    "U2": (F, "<<la mitosi mette figli SOTTO la scala di Planck>>"),
    "S10": (F, "<<Il tetto 1.414213 di `r` viene da un ramo di `ritmo()` che NON GIRA>>"),
    "RAMPA-1": (F, "la RAMPA, chiusa con la strada (3), decisione di Luca"),
    "SCENA-1": (F, "<<SEMINA_LAM...>>, chiusa con la strada (1), decisione di Luca"),
    "INERZIA-1(C)": (F, "<<CURATA e SIGILLATA 3/6: GIUSTA e INSUFFICIENTE>>: la legge "
                        "dell'inerzia"),
    "POTENZE-1": (F, "<<CHIUSA con la CURA A (rho_s/W^2)>>: una forma di legge"),
    "RIPIEGO-1": (F, "un RIPIEGO nella dinamica, aperto e chiuso lo stesso giorno"),
    "RIPIEGHI-ZERO": (F, "<<l'obiettivo e' ZERO ripieghi>>: la dinamica"),
    "NODI-1": (F, "<<PERCHE' E' CADUTA>>: una tesi sulla fisica, RITIRATA da Luca"),
    "OKN-ASSERT": (F, "<<UN `getattr(..., default)` CHE DECIDE AL POSTO...>>: un default che "
                      "decide la fisica (`A8`)"),
    "MAX-NODI-FERMA": (F, "<<i tre siti che la leggono CAMBIANO LA FISICA IN SILENZIO: e' la "
                          "forma di `A8`>>"),
    "PSI-FLASH": (F, "<<|psi| salta di un fattore 1.62 nei passi con na...>>"),
    "MITOSI-SOGLIA-GRAD": (F, "<<la soglia cri...>> della mitosi: una soglia dentro una "
                              "legge"),
    "PEQ-MEDIANA-ISTANTE": (F, "la MEDIANA e l'ISTANTE di `peq`: una statistica dentro una "
                               "legge"),
    "CHI-TORS-ZERO-FALSO": (F, "<<la misura del 0.3 a zero>>: la chiralita' e la torsione"),
    "ETC-PASSO": (F, "<<il passo diventa SINCRONO: tutte e cinque le leggi leggono la "
                     "fotografia>>: cambia COME le leggi leggono lo stato"),
    "SCUOT-INNESCO": (F, "<<col vuoto SPENTO in 72 passi NON HA NESSUNA NASCITA>>"),
    "SOGLIA-NON-MODULATA": (F, "<<la soglia vale 9.424778 con MIN = MEDIANA = MAX su TUTTI i "
                               "471575 archi, cioe' 3 pi ESATTO>>"),
    "TW-DIVISIONE-INCOGNITA": (F, "`tw` alla DIVISIONE: una memoria d'arco alla nascita"),
    "COMPONENTI:D1": (F, "<<`cs_nodo_prev` esteso alla...>>: un criterio di promozione a "
                         "fisica di default"),
    "COMPONENTI:D2": (F, "<<`psi_spin_prec` esteso alla...>>: idem"),
    "COMPONENTI:Y0-Y10": (F, "i criteri `Y0`-`Y10` di promozione a fisica di default"),
}
# ### ⛔ **le METODO, le INFRASTRUTTURA e le DOCUMENTAZIONE valgono in ENTRAMBE le ere**; la
# ### FISICA di queste voci e' quella del SECONDO ordine, quindi era `1`.
ERA = {M: "ENTRAMBE", I: "ENTRAMBE", DOC: "ENTRAMBE", F: "1"}
# ### ⚠ **MA tre INFRASTRUTTURA sono legate a codice che l'era 2 TOGLIE**, e lo dico:
ERA_UNO = ("ARCH-PAVIMENTI", "ARCH-SYNC", "CURA2-STRUTTURALE", "DRIVER-SCENA-II",
           "SCHED-T1", "SCHED-T2-TIPI", "SCHED-T2-VALIDA", "NASCITA-PUNTO-UNICO",
           "ETC-C1-CONFINE", "ARCH-LCONSERVA", "A5-PANNELLO", "MITOSI-NON-DIVISA",
           "REGIME-COMMENTI", "KAPPA-TW-COMMENTO", "CHI-BASC-DESCRIZIONE")


def cit(s, q=80):
    return " ".join((s or "").split())[:q]


def main():
    os.makedirs(LOTTI, exist_ok=True)
    voci = {v["id"]: v for v in (json.loads(r) for r in
                                 io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
                                 if r.strip())}
    res = [v for v in voci.values() if v["stato"] == "CHIUSA"
           and v["dominio"] == "DA_CLASSIFICARE"]
    lotto, manca = [], []
    for v in sorted(res, key=lambda x: x["id"]):
        i = v["id"]
        t = (v["descrizione"] or "") + " " + v["titolo"]
        ep = [x for x in ("[EPOCA 1", "[EPOCA 2", "[EPOCA 3") if x in t]
        if v["fonte"].startswith("doc/RAMIFICAZIONI") and v["classe"] in ("FRONTE", "MISURA"):
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"dominio": F, "era": "1"}, "meta": {},
                          "motivo": ("(regola) la fonte e' `doc/RAMIFICAZIONI.md`, il "
                                     "documento dei RAMI DI RICERCA SUL SISTEMA, e la classe "
                                     "e' `%s`: e' FISICA. L'era e' 1 perche' %s. Il testo "
                                     "dice <<%s>>"
                                     % (v["classe"],
                                        ("porta `%s`, e le EPOCHE sono fasi di lavoro sul "
                                         "SECONDO ordine" % ep[0]) if ep else
                                        "misura il simulatore del secondo ordine",
                                        cit(t)))})
            continue
        if i in LETTE:
            dom, perche = LETTE[i]
            era = "1" if (dom == F or i in ERA_UNO) else ERA[dom]
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"dominio": dom, "era": era}, "meta": {},
                          "motivo": ("(letta) `%s` -> %s, era %s: %s"
                                     % (i, dom, era, perche))})
            continue
        manca.append(i)
    assert not manca, "CHIUSE non classificate: %s" % manca
    nomi = []
    for k in range(0, len(lotto), PER_LOTTO):
        p = os.path.join(LOTTI, "chiuse_%02d.jsonl" % (k // PER_LOTTO + 1))
        io.open(p, "w", encoding="utf-8", newline=NL).write(
            NL.join(json.dumps(x, ensure_ascii=False) for x in lotto[k:k + PER_LOTTO]) + NL)
        nomi.append((os.path.relpath(p, RADICE).replace(chr(92), "/"),
                     len(lotto[k:k + PER_LOTTO])))
    c = {}
    for x in lotto:
        c[x["campi"]["dominio"]] = c.get(x["campi"]["dominio"], 0) + 1
    print("=" * 96)
    print("LE %d VOCI CHIUSE SENZA DOMINIO" % len(lotto))
    print("=" * 96)
    for k in sorted(c, key=lambda x: -c[x]):
        print("  %-16s %3d" % (k, c[k]))
    for p, q in nomi:
        print("  %-44s %d voci" % (p, q))
    return 0


if __name__ == "__main__":
    sys.exit(main())
