r"""**GENERA `doc/LISTA_CHIUSA.md` DA TUTTE LE FONTI** \u2014 nessuna riga ricopiata a mano (`P1-ter`).

**Bozza per l'APPROVAZIONE di Luca** *(mandato globale `0c42925` parte 1; **rifatto il 2026-09-26**
su rilievo di Luca)*.

> ## \u274c\u274c **LA VERSIONE PRECEDENTE LEGGEVA UNA FONTE SOLA, ED E' `STANDARD 9`**
> Leggeva **la sola tabella dei difetti acclarati** di `doc/STATO_RUN.md` e **presentava il
> risultato come la lista**. **Non si deduce l'assenza da una ricerca parziale.**
> **E il difetto meccanico era piu' stupido del principio:** la tabella `IN CODA` e' **interrotta
> da un blocco di codice** a meta', e il parser \u2014 che raccoglieva **righe CONTIGUE** \u2014 si fermava
> **alla sesta riga di quarantatre'**. **Un elenco che perde righe non si denuncia da solo.**

**LE TRE REGOLE DI QUESTA VERSIONE:**

1. **SI LEGGONO TUTTE LE FONTI**, e il documento **dichiara quali e quante voci da ciascuna**.
2. **OGNI voce finisce in `LISTA` OPPURE in `FUORI LISTA` col MOTIVO PROPOSTO.** **Nessuna
   esclusione silenziosa: escludere e' una decisione di LUCA**, qui c'e' solo la proposta.
3. **CONTROLLO NEI DUE VERSI** (`P1-sexies`): un elenco di voci che **DEVONO** comparire, e una che
   **NON DEVE** *(il caso che deve fallire)*. **Se un controllo non passa, il documento NON SI
   SCRIVE** \u2014 perche' un presidio che avvisa e lascia passare non impedisce nulla (`A9`).

**COSA E' GENERATO E COSA E' GIUDIZIO MIO:**
- **dal file**: la voce, il suo testo, la sezione, la fonte;
- **giudizio mio**: la **FAMIGLIA** e il **MOTIVO di esclusione** \u2014 entrambi da **regole** scritte
  qui in testa (`REG_FAM`, `ESCLUSIONI`), **non voce per voce**: una correzione si fa in un posto
  solo.

**NESSUN RUN, nessun simulatore: legge documenti e ne scrive uno.**
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Trasforma documenti in un documento;
#   una «configurazione del driver» non esiste per questa operazione.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "LISTA_CHIUSA.md")
NL = chr(10)

# ============================================================ LE SETTE FAMIGLIE
FAMIGLIE = [
    ("A", "INERZIA E AVVIO",
     "l'inerzia spinoriale, il contrasto, `rho_s`, la rampa, cio' che decide come nasce un nodo"),
    ("B", "TEMPO UNICO",
     "un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, `r`, `tau_pp`, le medie d'arco"),
    ("C", "DOPPIA COPERTURA E CREAZIONE",
     "la fase su `2pi`/`4pi`, la torsione `tw`, la mitosi, Schwinger, cio' che si eredita"),
    ("D", "SOGLIE TARATE E SOTTO PLANCK",
     "`A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato, e ogni soglia in "
     "unita' assolute invece che in frazione del dominio"),
    ("E", "DISEGNO E STATISTICHE GLOBALI",
     "`A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno che entra nella fisica"),
    ("F", "FRENO E CONTRAZIONE",
     "`SCALA_MIN`, il freno a senso unico, la coesione, la repulsione, `d0`, `LAM`"),
    ("G", "ARRETRATO DEGLI STRUMENTI",
     "presidi, ancore, reperti, ripresa, il passo incompleto: **non e' fisica**, ed e' cio' che "
     "rende verificabile il resto"),
]

# ============================================================ LE FONTI E LE REGOLE DI SEZIONE
#   modo:  "righe"   ogni riga di tabella della sezione e' UNA voce
#          "elenco"  ogni voce di elenco (`- `, `1. `) e' UNA voce
#          "aggrega" l'intera tabella e' UNA voce, col conteggio
#          "fuori"   la sezione NON e' un registro di fronti: si dichiara col conteggio
REGOLE = [
 ("doc/STATO_RUN.md", [
  (r"SOSPESI", "righe", "lavori sospesi da Luca"),
  (r"IN CODA, e NON bloccano", "righe", "la coda delle voci aperte"),
  (r"^A\. .*ACQUISITO", "righe", "cure in codice e accese"),
  (r"^B\. .*DECISO DA LUCA", "righe", "decisioni non ancora in codice"),
  (r"^C\. .*APERTO", "righe", "fronti aperti, uno per riga"),
  (r"POI, NELL'ORDINE DEL MANDATO", "righe", "l'ordine del mandato"),
  (r"LA CODA UNICA", "righe", "la coda unica: l'ordine del lavoro"),
  (r"DIFETTI APERTI", "righe", "i difetti acclarati"),
  (r"CURE VERIFICATE", "righe", "le cure con sigillo"),
  (r"PRESIDIO STRUTTURALE", "righe", "presidio strutturale, non cura"),
  (r"PROVE DI SPEGNIMENTO", "righe", "prove di spegnimento"),
  (r"ESITO DI OGNI VOCE", "righe", "esito delle voci CODICE di RAMIFICAZIONI"),
  (r"SOSPETTI", "righe", "i sospetti, NON promossi"),
  (r"^A \u2014 LASCIATE", "righe", "voci lasciate a meta'"),
  (r"^B \u2014 APERTE DA PRIMA", "righe", "voci aperte da prima"),
  (r"^C \u2014 CHIUSE DALLA VERIFICA", "righe", "voci chiuse dalla verifica"),
  (r"LO STATO DELLE CURE", "fuori", "duplica `CURE VERIFICATE`, che e' la tabella vera"),
  (r"^I RAMI", "fuori", "rami git, non fronti"),
  (r"CANCELLAZIONI|Dentro il repository|Fuori dal repository|NON e' stato cancellato"
   r"|TABELLA DI CORRISPONDENZA", "fuori", "inventario di file e archivi, non fronti"),
 ]),
 ("doc/RAMIFICAZIONI.md", [
  (r"^A\. CHIUSE PER DIMOSTRAZIONE", "righe", "chiuse per dimostrazione"),
  (r"^B\. CHIUSE PER MISURA", "righe", "chiuse per misura, su settore aliasato"),
  (r"^C\. DIAGNOSI CHIUSE", "righe", "diagnosi chiuse"),
  (r"^D\.\d", "righe", "i fronti aperti, per struttura"),
  (r"^`?Z\d+`?", "aggrega", "un riscontro `Z`: una voce per riscontro"),
  (r"IL TEMPO DI VALUTAZIONE", "fuori", "tabella di analisi interna a un riscontro"),
 ]),
 ("doc/REGISTRO_FISICA.md", [
  (r"LE DOMANDE APERTE|COSA RESTA APERTO|LAVORO RESIDUO|COSA NON SO DERIVARE"
   r"|COSA NON SI SA DERIVARE|NON. COPRE|DA DECIDERE", "elenco",
   "cio' che una scheda dichiara APERTO o NON DERIVATO"),
  (r"LA VERIFICA|I CRITERI DELL|I CRITERI DEI TEST|I CRITERI DELLA PROVA|I CRITERI,"
   r"|LE PREVISIONI|COSA CAMBIA CON", "righe",
   "punti di verifica, criteri fissati prima, e i siti che una cura cambia"),
  (r"^LO STATO|LE TRE FORME A CONFRONTO|IL CONFRONTO", "righe",
   "lo stato dichiarato di una scheda, e i confronti fra forme candidate"),
  (r"I LIMITI|LE DIMENSIONI|LA CURA DECISA|IL DIFETTO|I DUE DIFETTI|CONTROESEMPIO", "righe",
   "i limiti classificati con `A11` e le dimensioni: **e' qui che vivono le soglie tarate**"),
  (r".", "fuori", "tabella INTERNA a una scheda (forma, dimensioni, limiti, misure): e' LA LEGGE, "
   "non un fronte"),
 ]),
 ("doc/INVENTARIO_passo_incompleto.md", [
  (r"LA TABELLA", "aggrega", "gli script che avanzano in modo INCOMPLETO"),
  (r"DUE SITI", "aggrega", "i siti nel simulatore stesso"),
  (r"E I FILE CHE VANNO BENE", "fuori", "file corretti: non sono un fronte"),
  (r"RIEPILOGO PER CLASSE", "fuori", "riepilogo della tabella sopra"),
 ]),
 ("doc/CONFIGURAZIONE_misure_2026-09-25.md", [
  (r"LA DISTANZA DALLA CONFIGURAZIONE DEL DRIVER", "righe",
   "le misure da RIFARE in configurazione del driver"),
  (r".", "fuori", "elenco degli strumenti e della loro configurazione, non dei fronti"),
 ]),
]

# ============================================================ LO STATO -> LISTA o FUORI LISTA
#   Ogni motivo e' una PROPOSTA: la decisione di escludere e' di Luca.
ESCLUSIONI = [
 (r"NON E' UN DIFETTO", "non e' un difetto"),
 (r"RITIRATA|RITIRATO", "ritirata, resta come storia"),
 (r"SOSPES", "sospesa per decisione di Luca"),
 (r"run base|programma lungo|PROGRAMMA LUNGO|dopo le tre prove|per dopo|\bdopo il `CHECKPOINT",
  "dopo il run base"),
 (r"DA RIFARE|ALIASAT", "chiusa per misura su settore aliasato: da RIFARE dopo il run base"),
 (r"\bCURAT[OA]\b|\bCHIUS[AO]\b|\bCHIUSE\b|\u2705|\bFATTE\b|\bFINIT[OA]\b"
  r"|CHIUSA PER DIMOSTRAZIONE|CHIUSA PER MISURA", "gia' curata o chiusa"),
]

# ⚠ `VALE SEMPRE` NON E' FRA LE ESCLUSIONI GENERICHE, E IL PERCHE' E' UN DIFETTO MISURATO:
#   in `RAMIFICAZIONI` significa **chiusa per dimostrazione**; in `STATO_RUN` (sezione
#   «APERTE DA PRIMA») significa **la voce vale ANCORA**, cioe' APERTA. **Le stesse due parole,
#   il significato opposto** -- e come esclusione generica aveva buttato fuori proprio `A3` e
#   `B5`, due delle voci che Luca cercava. Percio' la chiusura per dimostrazione o per misura
#   si riconosce dalla SEZIONE, qui sotto.
SEZ_FUORI = [
 (r"SOSPETTI", "sospetto, NON acclarato: si promuove con la prova"),
 (r"^A\. CHIUSE PER DIMOSTRAZIONE",
  "chiusa per DIMOSTRAZIONE: non si riapre (par.5-quater)"),
 (r"^B\. CHIUSE PER MISURA",
  "chiusa per MISURA su settore aliasato: da RIFARE dopo il run base"),
 (r"^C\. DIAGNOSI CHIUSE", "diagnosi chiusa"),
 (r"ACQUISITO", "cura ACQUISITA: in codice e accesa nei run"),
 (r"CURE VERIFICATE", "cura VERIFICATA, con sigillo"),
]
#   ...e NON si applica se la riga porta un marchio di APERTURA: una diagnosi «DA RIVERIFICARE»
#   resta un fronte.
APERTA = r"DA RIVERIFICARE|DA RIFARE|APERT|NON MISURAT|\U0001f7e5|\U0001f7e7"


# ============================================================ LA FAMIGLIA (giudizio mio, per regola)
REG_FAM = [
 # ⚠ L'ORDINE CONTA, ed e' stato CORRETTO: `G` era PRIMA e si prendeva tutto, perche' quasi ogni
 #   riga di fisica cita un sigillo o un blob. Ora `G` e' ULTIMA e le sue parole sono STRETTE:
 #   restano a `G` solo le voci il cui OGGETTO e' lo strumento, non la legge.
 (r"inerzia|contrasto|rho_s|\bramp\b|rampa|accension|\beta\b|omega|spinor|\bpeq\b|semina"
  r"|sorgente di campo", "A"),
 (r"freno|SCALA_MIN|smorza|\bd0\b|coesion|repulsion|dx/d|compression|\bLAM\b|_nasce"
  r"|archi|distanz", "F"),
 (r"fase|\bphi\b|\u03c6|2pi|4pi|2\u03c0|4\u03c0|torsion|\btw\b|mitosi|Schwinger|antifase|wrap"
  r"|SCALE-TW|copertura", "C"),
 (r"tempo|dt_n|dt_e|orologio|ritmo|tau_pp|foliazion|causal|\btau\b", "B"),
 (r"soglia|clip|pavimento|tetto|QMIN|tarat|unita' assolute|massa_critica|costant|limite", "D"),
 (r"median|global|disegno|\bpos\b|statistic|rilassa_disegno", "E"),
 (r"presidi|hook|ancor|inventario|passo incompleto|step\(\)|argv|\bCLI\b|P1-bis|\bP5\b"
  r"|\bP8\b|\bP9\b|ripres|reperto|non ri-girabile|non e. ri-girabile|sigillo MANCA"
  r"|arretrato", "G"),
]

# ============================================================ IL CONTROLLO NEI DUE VERSI (P1-sexies)
#   DEVONO comparire: le voci che LUCA ha elencato come mancanti dalla bozza precedente.
DEVONO = [
 ("SCALE-TW", r"SCALE-TW"),
 ("la soglia di torsione 3pi", r"3\u03c0|3pi"),
 ("B5 \u2014 theta / l'aliasing del settore di spin", r"\bB5\b"),
 ("cura 5 via CLI (CLI-1)", r"CLI-1"),
 ("chi comprime d0", r"chi comprime d0"),
 ("tasso di mitosi", r"tasso di mitosi"),
 ("|dx|/d = V8/V9, che decide il freno", r"`V8`"),
 ("D33", r"\bD33\b"),
 ("A3 \u2014 il disegno esce dalla dinamica", r"\bA3\b"),
 ("CURA 3", r"CURA 3"),
 ("PASSO-2", r"PASSO-2"),
 ("FRAG1", r"FRAG1"),
 ("M1", r"\bM1\b"),
 ("M2", r"\bM2\b"),
 ("i 24 script che avanzano con step() da solo", r"\b24\b"),
]
#   NON DEVE comparire: il caso che DEVE fallire. Se salta fuori, il controllo e' VACUO.
NON_DEVE = ("una voce inventata", r"VOCE-CHE-NON-ESISTE-NEI-REGISTRI")

SEP = re.compile(r"^\|[\s:\-|]+\|\s*$")
ELE = re.compile(r"^\s*(?:[-*\u2022]|\d+\.)\s+\S")


def pulisci(s):
    return re.sub(r"\s+", " ", s).strip()


def breve(s, n):
    s = pulisci(s).replace("|", "/")
    return s if len(s) <= n else s[:n - 1] + "\u2026"


def celle(riga):
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def etichetta(cc):
    """La prima cella che non sia un indice (`1`, `4-bis`, un simbolo cerchiato)."""
    for c in cc:
        t = pulisci(re.sub(r"[`*]", "", c))
        if not t:
            continue
        if re.fullmatch(r"[\d\W_\u2460-\u24ff\u2100-\u21ff\s\-bis]{1,9}", t):
            continue
        return t
    return pulisci(re.sub(r"[`*]", "", cc[0])) if cc else "?"


def sezioni(testo):
    """(titolo, righe) per ogni sezione delimitata da un'intestazione markdown."""
    fuori, tit, buf = [], "", []
    for r in testo.split(NL):
        if re.match(r"^#{1,6} ", r):
            fuori.append((tit, buf))
            tit = pulisci(re.sub(r"[`*>#]", "", r.lstrip("# ")))
            buf = []
        else:
            buf.append(r)
    fuori.append((tit, buf))
    return fuori


def righe_tabella(buf):
    """Le righe di tabella della sezione, SENZA intestazioni ne' separatori.

    Si prendono TUTTE le righe che cominciano con `|`, anche se un blocco di codice o della prosa
    interrompono la tabella a meta': e' esattamente il difetto della versione precedente.
    """
    fuori = []
    for k, r in enumerate(buf):
        if not r.startswith("|") or SEP.match(r):
            continue
        if k + 1 < len(buf) and SEP.match(buf[k + 1]):
            continue                      # riga d'intestazione
        fuori.append(r)
    return fuori


def elenco(buf):
    return [pulisci(r) for r in buf if ELE.match(r)]


# ============================================================ LA RACCOLTA
VOCI = []          # {fonte, sez, et, txt, mot_sez}
FUORI_SEZ = []     # (fonte, sezione, righe, motivo)
NON_CLASS = []     # sezioni con righe e senza regola: FERMANO il generatore
SALTATI = {}       # elenchi in prosa non estratti, per fonte

for fonte, regole in REGOLE:
    testo = io.open(os.path.join(RADICE, fonte), encoding="utf-8", newline="").read()
    for tit, buf in sezioni(testo):
        rr = righe_tabella(buf)
        ee = elenco(buf)
        modo = motivo = None
        for pat, m, mot in regole:
            if re.search(pat, tit):
                modo, motivo = m, mot
                break
        if modo is None:
            if rr:
                NON_CLASS.append((fonte, tit, len(rr)))
            continue
        if modo == "fuori":
            if rr:
                FUORI_SEZ.append((fonte, tit, len(rr), motivo))
            SALTATI[fonte] = SALTATI.get(fonte, 0) + len(ee)
        elif modo == "righe":
            for r in rr:
                cc = celle(r)
                VOCI.append({"fonte": fonte, "sez": tit, "et": etichetta(cc),
                             "txt": pulisci(r.strip("|")), "mot_sez": motivo,
                             "stato": pulisci(cc[0][:60] + " || " + cc[-1][:60])})
            SALTATI[fonte] = SALTATI.get(fonte, 0) + len(ee)
        elif modo == "elenco":
            for e in ee:
                VOCI.append({"fonte": fonte, "sez": tit,
                             "et": breve(re.sub(r"[`*]", "", e), 70), "txt": e,
                             "mot_sez": motivo})
        elif modo == "aggrega":
            if rr or ee:
                VOCI.append({"fonte": fonte, "sez": tit, "et": breve(tit, 70),
                             "txt": "%d righe. %s" % (len(rr), breve(rr[0] if rr else ee[0], 230)),
                             "mot_sez": motivo})

if NON_CLASS:
    print("*** FERMO: %d sezioni con righe di tabella e SENZA regola." % len(NON_CLASS))
    print("    Nessuna esclusione in silenzio: vanno classificate in REGOLE.")
    for f, t, n in NON_CLASS[:60]:
        print("    %-40s n=%-4d %s" % (f, n, t[:80]))
    sys.exit(2)

# ============================================================ LA CLASSIFICAZIONE
for v in VOCI:
    t = v["txt"]
    v["fuori"] = None
    _sf = None
    for pat, mot in SEZ_FUORI:
        # LA GUARDIA SUGLI ID: la tabella dei difetti e' SPEZZATA, e `D34`-`D38` cadono sotto
        #   l'intestazione di un'altra sezione. Escludere per SEZIONE senza questa guardia
        #   butterebbe fuori cinque difetti acclarati per la loro POSIZIONE nel file.
        if (re.search(pat, v["sez"]) and not re.search(APERTA, t)
                and not re.match(r"D\d\d", v["et"])):
            _sf = mot
            break
    if _sf:
        v["fuori"] = _sf
    elif re.search(r"I LIMITI|LE DIMENSIONI", v["sez"]) and "✅" in v.get("stato", ""):
        v["fuori"] = "limite dichiarato LEGITTIMO: esprime un vincolo fisico (`A11`)"
    elif (re.search(r"I LIMITI|LE DIMENSIONI|IL CONFRONTO|LE TRE FORME", v["sez"])
          and not re.search(r"❌|⚠|difett|incoerent|è il punto|A POSTERIORI", t)):
        # In queste sezioni una riga SENZA esito e' la LEGGE descritta, non un fronte: per esempio
        #   `| rho_s | adimensionale |`. Resta VISIBILE qui, col motivo, invece di gonfiare la lista.
        v["fuori"] = "riga DESCRITTIVA della legge, senza esito: non e' un fronte"
    else:
        # ⚠ LO STATO SI CERCA NELLA PRIMA E NELL'ULTIMA CELLA, non nella riga intera: nella riga
        #   intera un `\u2705` qualunque — il sigillo di un'altra voce, una prova citata — faceva
        #   dichiarare CHIUSA una voce APERTA. Misurato su `SCALE-TW`, che e' il caso di Luca.
        for pat, mot in ESCLUSIONI:
            if re.search(pat, v.get("stato", t)):
                v["fuori"] = mot
                break
    v["fam"] = "?"
    v["perche"] = ""
    for pat, k in REG_FAM:
        m = re.search(pat, t, re.I)
        if m:
            v["fam"] = k
            v["perche"] = m.group(0)
            break

LISTA = [v for v in VOCI if not v["fuori"]]
FUORI = [v for v in VOCI if v["fuori"]]
SENZA_FAM = [v for v in LISTA if v["fam"] == "?"]

# ============================================================ IL DOCUMENTO
R = []


def P(s=""):
    R.append(s)


P("# \U0001f4cb **LA LISTA CHIUSA \u2014 BOZZA PER L'APPROVAZIONE DI LUCA**")
P()
P("*(Mandato globale `0c42925` parte 1. **Generata** da `csv/_lista_chiusa.py`: nessuna riga e'")
P("ricopiata a mano, `P1-ter`. **RIFATTA il 2026-09-26** dopo il rilievo di Luca \u2014 la versione")
P("precedente leggeva **una fonte sola**, ed era `STANDARD 9`.)*")
P()
P("> ## \u26a0 **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.**")
P("> **Diventa la linea d'arrivo solo quando Luca la APPROVA**, e finche' non lo e' **non vale il")
P("> vincolo che vieta le indagini nuove**. **Nessuna voce e' esclusa in silenzio:** la sezione")
P("> `FUORI LISTA` porta **ogni** voce col **motivo PROPOSTO**, e **la decisione di escludere e'")
P("> di Luca.**")
P()
P("## LE FONTI LETTE, e quante voci da ciascuna")
P()
P("| fonte | voci estratte | in LISTA | FUORI LISTA | sezioni dichiarate FUORI PORTATA |")
P("|---|--:|--:|--:|--:|")
for fonte, _rg in REGOLE:
    vv = [v for v in VOCI if v["fonte"] == fonte]
    P("| `%s` | %d | %d | %d | %d |"
      % (fonte, len(vv), len([v for v in vv if not v["fuori"]]),
         len([v for v in vv if v["fuori"]]), len([x for x in FUORI_SEZ if x[0] == fonte])))
P("| **TOTALE** | **%d** | **%d** | **%d** | **%d** |"
  % (len(VOCI), len(LISTA), len(FUORI), len(FUORI_SEZ)))
P()
P("**LE FONTI SONO CINQUE E NON QUATTRO:** oltre alle quattro del mandato c'e'")
P("**`doc/CONFIGURAZIONE_misure_2026-09-25.md`**, che e' **l'unico posto** dove stanno le sei misure")
P("da rifare in configurazione del driver *(fra cui `chi comprime d0`)*. **L'ho aggiunta perche'")
P("altrimenti quelle voci non comparirebbero** \u2014 ed e' il difetto che questo rifacimento cura.")
P()
P("**COSA E' GENERATO E COSA E' GIUDIZIO MIO:**")
P()
P("| | |")
P("|---|---|")
P("| **dal file** | la voce, il suo testo, la sezione, la fonte |")
P("| **giudizio MIO** | la **FAMIGLIA** e il **MOTIVO di esclusione** \u2014 da **regole** scritte in "
  "testa allo script (`REG_FAM`, `ESCLUSIONI`), **non voce per voce**: una correzione si fa in un "
  "posto solo |")
P()
P("---")
P()
P("## LE SETTE FAMIGLIE")
P()
P("| | famiglia | cosa raccoglie | voci in lista |")
P("|---|---|---|--:|")
for k, nome, che in FAMIGLIE:
    P("| **%s** | **%s** | %s | %d |" % (k, nome, che, len([v for v in LISTA if v["fam"] == k])))
if SENZA_FAM:
    P("| **?** | **SENZA FAMIGLIA** | **nessuna regola ha deciso: le elenco invece di metterle in "
      "una famiglia a caso** | %d |" % len(SENZA_FAM))
P()
P("> **L'ORDINE FRA LE FAMIGLIE E' UNA PROPOSTA, e ha una ragione:** **`A`** prima, perche'")
P("> l'inerzia entra in **ogni** passo di **ogni** nodo e una misura fatta con l'inerzia sbagliata")
P("> va rifatta; **`G` non va per ultima: va IN PARALLELO**, perche' e' cio' che rende verificabile")
P("> il resto e **non produce numeri di fisica**. **Le altre cinque le ordina Luca.**")
P()
P("---")
P()

for k, nome, _che in FAMIGLIE + [("?", "SENZA FAMIGLIA \u2014 da assegnare a mano", "")]:
    vv = [v for v in LISTA if v["fam"] == k]
    if not vv and k == "?":
        continue
    P("## FAMIGLIA **%s** \u2014 %s   *(%d voc%s)*"
      % (k, nome, len(vv), "e" if len(vv) == 1 else "i"))
    P()
    if not vv:
        P("*(nessuna voce: se e' un errore di regola, si corregge in `REG_FAM`.)*")
        P()
        P("---")
        P()
        continue
    P("| voce | la riga, come sta nella fonte | famiglia decisa da | fonte \u2014 dove CADE nel file |")
    P("|---|---|---|---|")
    for v in sorted(vv, key=lambda x: (x["fonte"], x["sez"], x["et"])):
        P("| **%s** | %s | `%s` | `%s` \u2014 %s |"
          % (breve(v["et"], 58), breve(v["txt"], 420), v["perche"] or "\u2014",
             v["fonte"].replace("doc/", ""), breve(v["sez"], 40)))
    P()
    P("---")
    P()

P("## \U0001f4e4 **FUORI LISTA \u2014 %d voci, ciascuna col MOTIVO PROPOSTO**" % len(FUORI))
P()
P("> **Non sono escluse: sono PROPOSTE di esclusione.** **Decide Luca**, e finche' non decide")
P("> restano qui, leggibili, col motivo accanto.")
P()
_mot = {}
for v in FUORI:
    _mot.setdefault(v["fuori"], []).append(v)
for mot in sorted(_mot, key=lambda m: -len(_mot[m])):
    P("### motivo proposto: **%s**   *(%d voci)*" % (mot, len(_mot[mot])))
    P()
    P("| voce | la riga | fonte |")
    P("|---|---|---|")
    for v in sorted(_mot[mot], key=lambda x: (x["fonte"], x["et"])):
        P("| %s | %s | `%s` |"
          % (breve(v["et"], 80), breve(v["txt"], 200), v["fonte"].replace("doc/", "")))
    P()

P("### \u26a0 SEZIONI DICHIARATE **FUORI PORTATA** \u2014 %d, col conteggio delle righe" % len(FUORI_SEZ))
P()
P("**Non sono registri di fronti**, e la differenza conta: una tabella di dimensioni, di formule o")
P("di archivi non contiene voci da curare. **Le dichiaro col numero di righe** invece di tacerle.")
P()
P("| fonte | sezione | righe | perche' non e' un registro di fronti |")
P("|---|---|--:|---|")
for f, t, n, mot in sorted(FUORI_SEZ, key=lambda x: (x[0], -x[2])):
    P("| `%s` | %s | %d | %s |" % (f.replace("doc/", ""), breve(t, 58), n, mot))
P()
P("### \u26a0 E UN FATTO DEI FILE, che ho scoperto scrivendo questo: **UNA TABELLA PUO' ESSERE")
P("SPEZZATA FRA DUE INTESTAZIONI**")
P()
P("La tabella dei **difetti acclarati** di `STATO_RUN` **non e' contigua**: comincia sotto la sua")
P("intestazione e **riprende dopo altre due sezioni** *(`D34`-`D38` cadono sotto")
P("`PROVE DI SPEGNIMENTO`)*. Per questo la colonna dice **\u00abdove CADE nel file\u00bb** e non")
P("\u00aba quale registro appartiene\u00bb: **la voce e' presa, la sezione e' solo il suo posto fisico.**")
P("**E' la stessa forma del difetto che ha prodotto la bozza sbagliata** *(un registro che non e'")
P("un blocco continuo)*, vista dall'altro lato.")
P()
P("**E UN LIMITE DICHIARATO, perche' e' un silenzio che ho scelto io:** nelle sezioni **non**")
P("marcate `elenco`, gli **elenchi in prosa** non vengono estratti \u2014 sono %s."
  % ", ".join("**%d** righe in `%s`" % (n, f.replace("doc/", ""))
              for f, n in sorted(SALTATI.items()) if n))
P("**Un fronte che vive SOLO in un elenco in prosa di una sezione non dichiarata aperta, questo")
P("generatore NON lo vede.** *(E' della stessa famiglia del difetto che ha prodotto la bozza")
P("sbagliata: lo scrivo prima invece di scoprirlo dopo.)*")
P()
P("---")
P()
P("## \u2705 IL CONTROLLO NEI DUE VERSI *(`P1-sexies`)*")
P()
P("**Le voci che Luca ha elencato come mancanti dalla bozza precedente sono diventate il")
P("COLLAUDO**: se una di loro non compare **nella parte IN LISTA** \u2014 non basta il documento, non")
P("basta comparire fra le escluse \u2014 **il generatore NON SCRIVE IL FILE**.")
P("*(Un presidio che avvisa e lascia passare non impedisce nulla: `A9`.)*")
P()
P("| deve comparire | trovata? |")
P("|---|:--:|")

# ⚠ IL CONTROLLO GUARDA **LA PARTE IN LISTA**, non il documento intero: una voce che comparisse
#   solo fra le ESCLUSE passerebbe un controllo di sola presenza, ed e' proprio cio' che non deve
#   accadere. **Ho verificato PRIMA di stringere il criterio che tutte e quindici stanno in LISTA**
#   -- lo dico perche' l'ordine conta: stringere dopo un `FAIL` sarebbe `P1-sexies` violato.
_doc = NL.join(R)
_k = _doc.find("FUORI LISTA \u2014 ")
_corpo = _doc[:_k] if _k > 0 else _doc
mancano = [n for n, p in DEVONO if not re.search(p, _corpo)]
falso = re.search(NON_DEVE[1], _doc)
for n, p in DEVONO:
    P("| %s | %s |" % (n.replace("|", "\\|"), "\u2014 **MANCA**" if n in mancano else "\u2705"))
P("| **%s** \u2014 *il caso che DEVE fallire* | %s |"
  % (NON_DEVE[0], "\u274c TROVATA: il controllo e' VACUO" if falso else "\u2705 assente, come deve"))
P()
P("**Il caso che DEVE fallire e' il piu' importante:** se una voce inventata risultasse «trovata»,")
P("il controllo starebbe cercando in un testo che contiene tutto, e i quindici `PASS` sopra non")
P("varrebbero niente.")
P()
P("---")
P()
P("## LE QUATTRO STRADE PER UN DIFETTO NUOVO *(mandato, parte 2)*")
P()
P("```")
P("1. BLOCCA la voce in corso        -> si ferma e si dice")
P("2. INVALIDA la voce in corso      -> la voce torna aperta, la misura non si pubblica")
P("3. STESSA RADICE di una voce      -> entra in QUELLA famiglia, con la conferma di Luca")
P("4. altrimenti                     -> doc/LISTA_DOPO.md, e NON SI TOCCA")
P("```")
P()
P("> **E IL VINCOLO CHE CAMBIA IL MIO COMPORTAMENTO:** finche' la lista e' attiva **non si aprono")
P("> indagini nuove** \u2014 inventari, controlli a tappeto, sonde esplorative \u2014 **se non servono a una")
P("> voce**.")
P()
P("## LA LINEA D'ARRIVO *(mandato, parte 4)*")
P()
P("```")
P("lista VUOTA  ->  BASE: scena (ii)(a), configurazione del driver con TUTTE le cure,")
P("                 4 semi, 600 passi, passo pieno, P5 attivo, referto elencato")
P("             ->  tag  base-epoca-4")
P("             ->  PROVA 1 sulla base, criteri scritti PRIMA")
P("                 (la prima delle tre prove di doc/IPOTESI_gravita_a_spinta.md:")
P("                  IL BERSAGLIO DEL PROGETTO)")
P("```")
P()
P("**E ogni giorno, in `doc/STATO_RUN.md`:** quante **chiuse**, **aperte**, **nuove**, e in quale")
P("strada. **La lista deve ACCORCIARSI: se in un giorno cresce, lo si scrive IN TESTA.**")
P()
P("---")
P()
P("## COSA QUESTA BOZZA *NON* DICE")
P()
P("- **non dice che le voci aperte siano %d e non una di piu'**: dice che **%d voci delle CINQUE"
  % (len(LISTA), len(LISTA)))
P("  fonti lette** non portano uno stato di chiusura. **Un fronte che non e' in nessuna delle")
P("  cinque fonti non lo vede nessuno**, e questo generatore meno degli altri.")
P("- **non dice che le famiglie siano le giuste**: sono le sette proposte nel mandato, che dice")
P("  **di correggerle se i dati dicono altro, dichiarandolo**.")
P("- **non contiene la DIMENSIONE di ciascuna voce**, che il mandato chiede: stimarla richiede di")
P("  leggere il codice di ognuna, ed e' **lavoro, non generazione**. **Manca, e lo dico.**")
P("- **non e' ordinata per DIPENDENZE dentro la famiglia**: le dipendenze **non stanno in un campo**")
P("  di nessuna fonte, quindi ricavarle sarebbe un giudizio mio riga per riga. **Secondo punto che")
P("  manca.**")
P("- **la stessa voce puo' comparire DUE VOLTE**, se e' registrata in due fonti *(per esempio in")
P("  `STATO_RUN` e in `RAMIFICAZIONI`)*. **Non le ho unificate:** unificare per somiglianza di testo")
P("  produrrebbe **fusioni sbagliate**, e un doppione visibile e' meno dannoso di una voce persa.")
P("- **lo STATO lo decide una regex sul testo della riga**, non un campo strutturato: una voce che")
P("  dice \u00abcurata la meta'\u00bb finisce fra le chiuse. **Percio' `FUORI LISTA` e' STAMPATA PER INTERO**")
P("  e non riassunta: e' la' che un errore di classificazione si vede.")

T = NL.join(R) + NL

if mancano or falso:
    print("*** FERMO: il documento NON e' stato scritto.")
    for n in mancano:
        print("    MANCA la voce che DEVE comparire: %s" % n)
    if falso:
        print("    IL CASO CHE DEVE FALLIRE E' STATO TROVATO: il controllo e' VACUO.")
    sys.exit(3)

io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print("scritto %s" % DEST)
print("  voci %d   LISTA %d   FUORI LISTA %d   sezioni fuori portata %d   senza famiglia %d"
      % (len(VOCI), len(LISTA), len(FUORI), len(FUORI_SEZ), len(SENZA_FAM)))
for fonte, _rg in REGOLE:
    print("  %-46s %4d voci" % (fonte, len([v for v in VOCI if v["fonte"] == fonte])))
