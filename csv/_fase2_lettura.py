# -*- coding: utf-8 -*-
"""FASE 2: LE VOCI LETTE UNA PER UNA — **la tavola, con il motivo che cita**.

### ⭐ **IL DISCRIMINE che ho usato per i criteri, e lo dichiaro:**

| se il criterio misura… | dominio |
|---|---|
| ### **una proprieta' del SISTEMA** *(`d ≥ LAM`, la mitosi viva, la deriva sotto rumore, il contrasto)* | ### **`FISICA`** |
| ### **una proprieta' dello STRUMENTO o della VERIFICA** *(byte-identita', un presidio che non deve scattare, <<dall'AST non da un grep>>, <<model-free>>, un controllo positivo)* | ### **`METODO`** |
| il ### **codice o i file** come oggetto *(una chiave duplicata in uno strumento)* | ### **`INFRASTRUTTURA`** |

### ⛔ **E' il criterio del mandato** *(«un criterio di sigillo e' METODO anche se il padre e'
FISICA: vince il CONTENUTO»)*, ### **applicato al contenuto di ciascuna.**

Gira con:  python csv/_fase2_lettura.py
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

# ### (dominio, era, perche') -- il `perche'` entra nel motivo accanto alla CITAZIONE
M = "METODO"
F = "FISICA"
I = "INFRASTRUTTURA"
DOC = "DOCUMENTAZIONE"
TAVOLA = {
    # ---------------------------------------- METODO: misurano la VERIFICA
    "REGISTRO_FISICA:A1": (M, "ENTRAMBE", "e' la BYTE-IDENTITA' di un braccio: misura lo "
                                          "STRUMENTO, non il sistema"),
    "REGISTRO_FISICA:A2": (M, "ENTRAMBE", "e' un controllo ESATTO al passo 1: verifica che la "
                                          "misura legga cio' che crede"),
    "REGISTRO_FISICA:A7": (M, "ENTRAMBE", "<<dall'AST, non da un grep>>: parla del METODO con "
                                          "cui si e' censito"),
    "REGISTRO_FISICA:C1": (M, "ENTRAMBE", "byte-identita' a flag spento: proprieta' dello "
                                          "strumento"),
    "REGISTRO_FISICA:E1c": (M, "ENTRAMBE", "<<DERIVATA dagli archi GIA'...>>: e' il criterio "
                                           "di un sigillo, non la legge"),
    "REGISTRO_FISICA:E2": (M, "ENTRAMBE", "<<NON MISURABILE, e si dichiara>>: e' una "
                                          "dichiarazione sul metodo"),
    "REGISTRO_FISICA:E4": (M, "ENTRAMBE", "e' un DIAGNOSTICO di controllo del braccio"),
    "REGISTRO_FISICA:REG-R": (M, "ENTRAMBE", "e' la regola del REGISTRO, cioe' come si tiene "
                                             "la documentazione delle leggi"),
    "REGISTRO_FISICA:S1": (M, "ENTRAMBE", "firma dei byte su tutti i campi: lo strumento"),
    "REGISTRO_FISICA:S4": (M, "ENTRAMBE", "<<il presidio non deve scattare>>: misura il "
                                          "PRESIDIO"),
    "REGISTRO_FISICA:T4": (M, "ENTRAMBE", "<<il controllo che rende T3 LEGGIBILE>>: e' un "
                                          "CONTROLLO POSITIVO, cioe' metodo puro"),
    "REGISTRO_FISICA:T5": (M, "ENTRAMBE", "byte-inerte, 206 campi identici: lo strumento"),
    "REGISTRO_FISICA:U2-5": (M, "ENTRAMBE", "<<MODEL-FREE: non confronta col mio conto>>: e' "
                                            "una proprieta' della MISURA"),
    # ---------------------------------------- INFRASTRUTTURA
    "REGISTRO_FISICA:D37": (I, "ENTRAMBE", "una CHIAVE DUPLICATA nei domini di uno strumento: "
                                           "e' il codice come oggetto"),
    # ---------------------------------------- FISICA: misurano il SISTEMA
    "REGISTRO_FISICA:A11": (F, "1", "un PAVIMENTO dentro una legge"),
    "REGISTRO_FISICA:A13": (F, "1", "<<sotto LAM non esiste niente, nemmeno una distanza>>: "
                                    "e' l'assioma applicato a una cura"),
    "REGISTRO_FISICA:A3": (F, "1", "il nodo nato da MITOSI e il suo tempo-luce: comportamento "
                                   "del sistema"),
    "REGISTRO_FISICA:C2": (F, "1", "la CAPIENZA della semina: una proprieta' di LAM e della "
                                   "sfera"),
    "REGISTRO_FISICA:C3": (F, "1", "la FRAZIONE DI IMPACCHETTAMENTO nella sfera interna"),
    "REGISTRO_FISICA:C4": (F, "1", "<<nessun rifiuto falso>> sotto la capienza misurata"),
    "REGISTRO_FISICA:D33": (F, "1", "la REPULSIONE e il suo segno oltre 3.5pi"),
    "REGISTRO_FISICA:D35": (F, "1", "<<l'antifase non e' un'antifase>>: la forma del campo"),
    "REGISTRO_FISICA:E1a": (F, "1", "<<la mitosi non muore>>: un fenomeno del sistema"),
    "REGISTRO_FISICA:E1b": (F, "1", "<<la mitosi non esplode>>: un fenomeno del sistema"),
    "REGISTRO_FISICA:E4-LAM": (F, "1", "<<LA LEGGE d = LAM SI VERIFICA SEMPRE>>, decisione di "
                                       "Luca"),
    "REGISTRO_FISICA:P1": (F, "1", "la somma dei pesi per nodo: una grandezza del sistema"),
    "REGISTRO_FISICA:P2": (F, "1", "il CONTRASTO fra massa e vuoto"),
    "REGISTRO_FISICA:P3": (F, "1", "Lambda, la scala del sistema"),
    "REGISTRO_FISICA:P3b": (F, "1", "l'AMPIEZZA dello scuotimento"),
    "REGISTRO_FISICA:P4": (F, "1", "il cs_floor DENTRO le masse"),
    "REGISTRO_FISICA:P5": (F, "1", "lambda_nodi, <<quasi COSTANTE, 0.74-0.76 LAM ovunque>>"),
    "REGISTRO_FISICA:S10": (F, "1", "<<le regioni restano coerenti>>: un fenomeno"),
    "REGISTRO_FISICA:S2": (F, "1", "<<e' A13 misurato direttamente>>: la distanza minima"),
    "REGISTRO_FISICA:S3": (F, "1", "sum(d < LAM) e sum(d == LAM): l'invariante delle "
                                   "lunghezze"),
    "REGISTRO_FISICA:S5": (F, "1", "<<un nodo isolato e' un nodo che ESCE DALLA FISICA>>"),
    "REGISTRO_FISICA:S6": (F, "1", "d == |pos_i - pos_j| per ogni arco: e' D02, cioe' se la "
                                   "lunghezza e' relazionale"),
    "REGISTRO_FISICA:S7": (F, "1", "<<la mitosi viva, il bilancio di d0 CHIUDE>>"),
    "REGISTRO_FISICA:S9": (F, "1", "l'intensita' dentro le regioni contro quella del vuoto"),
    "REGISTRO_FISICA:SCENA-1": (F, "1", "<<IL VUOTO DI DEFAULT E' LA SATURAZIONE>>, decisione "
                                        "di Luca"),
    "REGISTRO_FISICA:T2": (F, "1", "<<fa cio' che la geometria impone>>"),
    "REGISTRO_FISICA:T3": (F, "1", "<<un arco sotto LAM a flag SPENTI FERMA il run>>: "
                                   "l'invariante"),
    "REGISTRO_FISICA:U2": (F, "1", "<<U2 E' ATTIVA E FABBRICA LUNGHEZZA>>, decisione di Luca"),
    "REGISTRO_FISICA:U2a": (F, "1", "la LUNGHEZZA FABBRICATA da `_nasce`, sum(LAM - v)"),
    "REGISTRO_FISICA:U2b": (F, "1", "quanti archi sono stati TRONCATI"),
    "REGISTRO_FISICA:U2c": (F, "1", "la frazione di archi sotto 2 LAM"),
    "REGISTRO_FISICA:V1": (F, "1", "<<a, il passo tipico di rumore>>, il numero che decide la "
                                   "condizione a < LAM"),
    "REGISTRO_FISICA:V2": (F, "1", "la DERIVA di oggi sotto rumore simmetrico"),
    "REGISTRO_FISICA:V3": (F, "1", "la deriva della proposta: <<deve essere del secondo "
                                   "ordine>>"),
    "REGISTRO_FISICA:V4": (F, "1", "la deriva al confine d -> LAM"),
    "REGISTRO_FISICA:V5": (F, "1", "la deriva lontano: <<decade come 1/d>>"),
    "REGISTRO_FISICA:V7": (F, "1", "<<mai sotto LAM: una discesa enorme, dx = -100*d>>"),
    "REGISTRO_FISICA:V8": (F, "1", "<<il numero che decide fra piana e Ito>>: decide LA FORMA "
                                   "DELLA LEGGE"),
    "REGISTRO_FISICA:V9": (F, "1", "<<Ito comprime / Ito inverte il verso>>: la forma della "
                                   "legge"),
    "RITMO-FLAG-SENZA-OGGETTO": (F, "1", "il RITMO r = cs_nodo/CS_M, censito dal sorgente"),
    "RITMO-PAVIMENTO": (F, "1", "<<IL PAVIMENTO DEL RITMO MORDE: min(r) e' ESATTAMENTE il "
                                "pavimento>>"),
}

# ==========================================================================
#   IL SECONDO GIRO: le 57 che restavano (STATO_RUN, gli strumenti, i PROC/STRUM)
# ==========================================================================
TAVOLA.update({
    # ---------------------------------------- METODO: la validita' di una misura
    "AB-CONTROLLI": (M, "ENTRAMBE", "<<senza i punti di CONTROLLO la densificazione non si "
                                    "separa dall'attrazione>>: e' una misura che NON "
                                    "DISCRIMINA"),
    "ALLUNG-RELATIVO": (M, "ENTRAMBE", "<<due corpi RIGIDI danno un allungamento FINTO>>: e' "
                                       "un FALSO SEGNALE della misura"),
    "FOGLIO-NULLO": (M, "ENTRAMBE", "un valore che al passo 0 vale <<meta' e meta'>>: e' un "
                                    "FALSO ZERO da riconoscere"),
    "FORMA-N-VUOTO": (M, "ENTRAMBE", "la riga `n` del referto misura <<la taglia "
                                     "dell'insieme>>, non cio' che si crede"),
    "TRATTI-INTERNI": (M, "ENTRAMBE", "come si SCOMPONE una distanza in unita' assolute: e' "
                                      "il metodo della misura"),
    "V5-SOGLIA": (M, "ENTRAMBE", "<<il criterio V5 del pilota legge...>>: e' un CRITERIO di "
                                 "lettura"),
    "VELENO-ORIENTATO": (M, "ENTRAMBE", "e' la sonda del VELENO sotto lo scambio a<->b: una "
                                        "prova sullo strumento"),
    "CHK2": (M, "ENTRAMBE", "e' un CHECKPOINT della campagna di misura"),
    "CHK3": (M, "ENTRAMBE", "<<referto dei quattro esiti, ciascuno contro le sue letture "
                            "fissate>>: e' il metodo del referto"),
    "CHK3-D": (M, "ENTRAMBE", "la sezione <<I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE>>: "
                              "e' una regola del referto"),
    "E3": (M, "ENTRAMBE", "<<EPOCA 3 + RUN LUNGO -- tag, 3000 passi, leggere durante il "
                          "run>>: e' il PIANO di una campagna"),
    # ---------------------------------------- DOCUMENTAZIONE
    "REG-B": (DOC, "ENTRAMBE", "<<FASE B: le SCHEDE, a lotti, un commit per lotto>>: e' il "
                               "lavoro sulle SCHEDE del registro"),
    "REG-C": (DOC, "ENTRAMBE", "<<FASE C: LA STORIA di ogni legge, e le schede delle leggi "
                               "TOLTE>>: documentazione"),
    "SCHED-T3-REGOLE": (DOC, "ENTRAMBE", "<<il documento delle regole di composizione>>: e' "
                                         "un testo, non una legge"),
    # ---------------------------------------- INFRASTRUTTURA
    "RAMI-OFF-CURA2": (I, "1", "<<i rami a flag spento, archiviati COPIATI dal sorgente>>: "
                               "sono FILE di archivio"),
    "D32-CONTATORE": (I, "1", "<<i contatori `_rep_taupp_*` contano un clamp che NON ESISTE "
                              "PIU'>>: diagnostica scaduta nel codice"),
    "FRAG1": (I, "ENTRAMBE", "<<va in IndexError INVECE DI DICHIARARLO>>: e' la robustezza "
                             "del codice, non una legge"),
    # ---------------------------------------- FISICA, era 1
    "A2-DXD": (F, "1", "<<|dx|/d del freno-legge>>: la grandezza di una legge"),
    "A4-METRICHE": (F, "1", "<<le METRICHE DEL SETTORE CHIRALE>>: grandezze del sistema"),
    "B6": (F, "1", "<<le due cure OFF: COPPIA_RECIPROCA e GRAV_AMPIEZZA>>: due leggi spente"),
    "B9": (F, "1", "<<i 1455 nodi a 1e-13; la catena f -> x -> r che non riproduce r>>"),
    "CICLO-CHIUSURA-SEGNO": (F, "1", "il SEGNO nella chiusura di un ciclo: una legge"),
    "CRESCITA-DOPO-Z43": (F, "1", "la CRESCITA dopo il sigillo di Z43: un fenomeno misurato"),
    "D14": (F, "1", "<<median(|f|) fa TRE mestieri: e' anche il rompi-anello>>: una grandezza "
                    "dentro le leggi"),
    "E4-LAM": (F, "1", "<<LA LEGGE 'NESSUNA LUNGHEZZA SOTTO LAM' DEVE DIVENTARE...>>"),
    "FILI-CORTI": (F, "1", "<<i fili si accorciano SOLO FRA LE MASSE o OVUNQUE?>>: un "
                           "fenomeno"),
    "INERZIA-1": (F, "1", "<<LA LEGGE DELL'INERZIA CEDE A k = 2, ED E' UN DIFETTO "
                          "DIMOSTRATO>>"),
    "MASSA-CRITICA-LOCALE": (F, "1", "<<non voglio un valore calcolato...>>, direzione di "
                                     "Luca sulla massa critica"),
    "MASSA-MIGRA": (F, "1", "<<la massa segue i NODI o la COERENZA? E come cambia la sua "
                            "FORMA?>>"),
    "P-EQ-MEDIANA-ARCHI": (F, "1", "la MEDIANA sugli archi dentro `P_eq`: una statistica "
                                   "dentro una legge"),
    "PASSO-2": (F, "1", "<<UN AVANZAMENTO INCOMPLETO NEL SIMULATORE STESSO, for in "
                        "range(300)>>: tocca come il sistema avanza"),
    "PERC-TW-MORTA": (F, "1", "`perc_tw` e' STATO MORTO: una variabile del sistema che "
                              "nessuno legge"),
    "PHI-FUORI-DOMINIO": (F, "1", "`phi` fuori dal suo dominio: la fase del sistema"),
    "PROVA1-40-80": (F, "1", "<<l'osservabile A(t) = ...>> nel pilota: una misura del "
                             "sistema"),
    "RAMPA-2": (F, "1", "<<AL PASSO 0 TUTTI LEGGONO cs = CS_M>>: il transitorio della metrica"),
    "RINCULO-RIPETUTI": (F, "1", "<<il rinculo dei genitori>> nella nascita: una legge"),
    "RITMO-AVVIO-FREDDO": (F, "1", "il RITMO all'avvio freddo, misurato da TERMOSTATO-E-FRENO"),
    "S01": (F, "1", "<<Chi fa crescere d0: gli scrittori sommano -1.6e+03 e med d0 "
                    "RADDOPPIA>>"),
    "S02": (F, "1", "<<Il freno di SCALA_MIN e' il motore di d0>>"),
    "S03": (F, "1", "<<La memoria del moto fa scappare d0>>"),
    "S04": (F, "1", "<<La crescita e' NUCLEAZIONE, non stiramento>>"),
    "S05": (F, "1", "<<La compressione d/d0 < 1 e' un difetto e non una fase>>"),
    "S06": (F, "1", "<<Il muro dell'1 % dell'antifase e' causato da D35>>"),
    "S07": (F, "1", "<<dphi_arc = angle(exp(1j*Dphi)) COLLASSA a 2pi una differenza che vive "
                    "su...>>"),
    "S08": (F, "1", "<<Se phi non e' l'azimut del Bloch, CHE COS'E'?>>"),
    "S09": (F, "1", "<<IL TETTO DI r E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO>>"),
    "S09-MEDIANA": (F, "1", "<<la spinta S09 moltiplica per median(self.d0[mask]), una "
                            "statistica>>"),
    "S11": (F, "1", "<<r E' SATURO AL SUO TETTO PER UN TERZO DEI NODI, e la quota CRESCE>>"),
    "S12": (F, "1", "<<IL RILASSAMENTO DI rep DENTRO mitosi()>>"),
    "S13": (F, "1", "<<IL TEMPO D'ARCO DOVREBBE ESSERE min(ri, rj) INVECE DELLA MEDIA "
                    "ARITMETICA?>>"),
    "SOGLIA-MITOSI-3PI": (F, "1", "la SOGLIA della mitosi a 3pi: una soglia dentro una legge"),
    "TORS-SPINTA": (F, "1", "<<la spinta repulsiva di...>>: una legge"),
    "TORS-W8-AVVOLGIMENTO": (F, "1", "l'AVVOLGIMENTO della torsione, da una derivazione "
                                     "verificata"),
    "XI-RUMORE-E-STATO": (F, "1", "<<_xi_rumore e' un...>>: una variabile di stato del "
                                  "sistema"),
})
# ### ⛔ **LE DUE CHE NON CLASSIFICO, ed e' un esito legittimo** *(il mandato: «il dubbio»)*
DUBBIO = {
    "I1": ("FISICA", "<<IDEA DI LUCA, PER DOPO: costruire UNA massa, farla maturare, leggerne "
                     "la struttura>>. ### E' FISICA, ma <<per dopo>> non dice SE e' dell'era "
                     "2: non sta nelle AGENDA di Luca, e indovinarlo sarebbe inventare"),
    "B7": ("FISICA", "<<i reperti DA RIMISURARE sulla scena nuova | Z43, Z46, Z48-Z52>>: "
                     "### E' UN CONTENITORE di piu' reperti, e l'era dipende da CIASCUNO"),
}
# ### ⛔ **E LE DUE CHE CONTENGONO DUE COSE: non si forzano** *(il mandato: «la mescolanza»)*
DIVIDERE = {
    "M2": ("FISICA", "1", "<<LA MITOSI -- DUE DIFETTI DA ACCLARARE. (1) il figlio nasce nel "
                          "PUNTO MEDIO... (2)...>>: il testo stesso dice DUE",
           "PROPOSTA: dividere in <<il figlio nasce nel punto medio>> e il secondo difetto "
           "elencato, ciascuno con la sua misura"),
    "B6": ("FISICA", "1", "<<le DUE cure OFF: COPPIA_RECIPROCA e GRAV_AMPIEZZA>>: sono DUE "
                          "flag diversi in una voce",
           "PROPOSTA: dividere per flag -- una voce per COPPIA_RECIPROCA e una per "
           "GRAV_AMPIEZZA, perche' si accendono e si misurano SEPARATAMENTE"),
}

# ### LO STATO: fisica dell'era 1 non chiusa -> SOSPESA; metodo/infrastruttura/doc -> APERTA
STATO = {("FISICA", "1"): "SOSPESA", ("FISICA", "2"): "AGENDA"}


def cit(s, q=80):
    return " ".join((s or "").split())[:q]


def main():
    os.makedirs(LOTTI, exist_ok=True)
    voci = {v["id"]: v for v in (json.loads(r) for r in
                                 io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
                                 if r.strip())}
    lotto, manca = [], []
    for idv, (dom, era, perche) in sorted(TAVOLA.items()):
        v = voci.get(idv)
        if v is None:
            manca.append(idv)
            continue
        stato = STATO.get((dom, era), "APERTA")
        lotto.append({"id": idv, "quando": DATA,
                      "campi": {"dominio": dom, "era": era, "stato": stato},
                      "meta": {},
                      "motivo": ("(letta) %s -> %s, era %s: %s. Il testo dice <<%s>>"
                                 % (idv, dom, era, perche,
                                    cit(v["descrizione"] or v["titolo"])))})
    assert not manca, "ID non trovati: %s" % manca
    # ### IL DUBBIO: dominio sì, era e stato NO -- e il perche' sta in `motivo_dubbio`
    for idv, (dom, perche) in sorted(DUBBIO.items()):
        v = voci[idv]
        lotto.append({"id": idv, "quando": DATA,
                      "campi": {"dominio": dom, "era": "DA_CLASSIFICARE",
                                "stato": "DA_CLASSIFICARE"},
                      "meta": {"motivo_dubbio": perche[:300]},
                      "motivo": ("(dubbio) `%s`: il dominio e' %s, ma l'ERA NON si decide dal "
                                 "contenuto. %s" % (idv, dom, perche[:140]))})
    # ### LA MESCOLANZA: si classifica, ma si MARCA `da_dividere` con la proposta
    for idv, (dom, era, perche, prop) in sorted(DIVIDERE.items()):
        v = voci[idv]
        lotto = [x for x in lotto if x["id"] != idv]
        lotto.append({"id": idv, "quando": DATA,
                      "campi": {"dominio": dom, "era": era,
                                "stato": STATO.get((dom, era), "APERTA")},
                      "meta": {"da_dividere": True, "nota_guardiano": prop[:300]},
                      "motivo": ("(da dividere) `%s`: %s. %s -- LA DIVISIONE LA DECIDE LUCA"
                                 % (idv, perche[:150], prop[:120]))})
    nomi = []
    for k in range(0, len(lotto), PER_LOTTO):
        p = os.path.join(LOTTI, "lettura_%02d.jsonl" % (k // PER_LOTTO + 1))
        io.open(p, "w", encoding="utf-8", newline=NL).write(
            NL.join(json.dumps(x, ensure_ascii=False) for x in lotto[k:k + PER_LOTTO]) + NL)
        nomi.append((os.path.relpath(p, RADICE).replace(chr(92), "/"),
                     len(lotto[k:k + PER_LOTTO])))
    c = {}
    for x in lotto:
        c[x["campi"]["dominio"]] = c.get(x["campi"]["dominio"], 0) + 1
    print("=" * 96)
    print("LE VOCI LETTE UNA PER UNA: %d" % len(lotto))
    print("=" * 96)
    for k in sorted(c, key=lambda x: -c[x]):
        print("  %-16s %3d" % (k, c[k]))
    for p, q in nomi:
        print("  %-44s %d voci" % (p, q))
    return 0


if __name__ == "__main__":
    sys.exit(main())
