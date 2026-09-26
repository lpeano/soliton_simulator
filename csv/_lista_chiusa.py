r"""**GENERA `doc/LISTA_CHIUSA.md` DALLA CODA UNICA** — nessuna riga ricopiata a mano (`P1-ter`).

**Bozza per l'APPROVAZIONE di Luca** *(mandato globale `0c42925`, parte 1)*. Legge la tabella dei
**difetti acclarati** di `doc/STATO_RUN.md`, tiene **solo quelli APERTI o con la cura non ancora in
codice**, li assegna a una **famiglia** e li stampa **ordinati per famiglia e per dipendenza**.

**COSA FA A MANO E COSA NO, dichiarato:**
- **generati dal file:** l'ID, la riga del difetto, la prova, il campo `cura`, lo stato;
- **scelta MIA, quindi da correggere:** **la FAMIGLIA** e la **dimensione**. L'assegnazione e' un
  giudizio, non un dato: sta in `FAMIGLIA_DI` qui sotto, **una riga per ID**, cosi' Luca la legge e
  la cambia in un posto solo.

**NESSUN RUN, nessun simulatore: legge un file di testo e ne scrive un altro.**

ASCII puro.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Trasforma un documento in un altro
#   documento; una «configurazione del driver» non esiste per questa operazione.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SORGENTE = os.path.join(RADICE, "doc", "STATO_RUN.md")
DEST = os.path.join(RADICE, "doc", "LISTA_CHIUSA.md")
NL = chr(10)

# ---------------------------------------------------------------- le sette famiglie
FAMIGLIE = [
    ("A", "INERZIA E AVVIO",
     "l'inerzia spinoriale, il contrasto, la rampa, cio' che decide come nasce un nodo"),
    ("B", "TEMPO UNICO",
     "un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, e le medie d'arco"),
    ("C", "DOPPIA COPERTURA E CREAZIONE",
     "la fase su `2pi`/`4pi`, la mitosi, Schwinger, cio' che eredita"),
    ("D", "SOGLIE TARATE E SOTTO PLANCK",
     "`A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato, e ogni soglia in "
     "unita' assolute invece che in frazione del dominio"),
    ("E", "DISEGNO E STATISTICHE GLOBALI",
     "`A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno che entra nella fisica"),
    ("F", "FRENO E CONTRAZIONE",
     "`SCALA_MIN`, il freno a senso unico, la coesione, cio' che tiene o comprime le distanze"),
    ("G", "ARRETRATO DEGLI STRUMENTI",
     "presidi, ancore, reperti, ripresa: **non e' fisica**, ed e' cio' che rende il resto verificabile"),
]

# ---------------------------------------------------------------- l'assegnazione (GIUDIZIO MIO)
FAMIGLIA_DI = {
    "D01": "E", "D02": "E", "D03": "D", "D04": "B", "D05": "E", "D06": "D",
    "D07": "D", "D08": "E", "D09": "C", "D10": "C", "D11": "C", "D12": "B",
    "D13": "D", "D14": "E", "D15": "D", "D16": "A", "D17": "A", "D18": "C",
    "D19": "E", "D20": "D", "D21": "B", "D22": "C", "D23": "E", "D24": "F",
    "D25": "F", "D26": "F", "D27": "D", "D28": "E", "D29": "A", "D30": "F",
    "D31": "F", "D32": "F", "D33": "F", "D34": "C", "D35": "C", "D36": "D",
    "D37": "B", "D38": "F",
}

# ---------------------------------------------------------------- le voci NON-difetto in coda
CODA_ALTRO = [
    ("RIPRESA-ARGV", "G", "la ripresa si fida del BLOB, e il blob non certifica l'ARGV: un json con "
     "la configurazione sbagliata verrebbe RIPRESO", "2026-09-26"),
    ("REPERTI-IMMUTABILI", "G", "un file archiviato con un sigillo e citato da un referto non deve "
     "poter cambiare in silenzio (caso reale: `e062fdb`)", "2026-09-26"),
    ("P1BIS-DELTA", "G", "il hook di `P1-bis` verifica la PRESENZA di `RELAZIONE_PER_CLAUDE.md` fra "
     "i file staged, non il suo DELTA (caso `009d49a`)", "2026-09-25"),
    ("ANCORE-1", "G", "**43 sigilli** prendono «il codice di prima» da `HEAD` invece che dal "
     "PADRE del commit che ha introdotto il flag (`P8`)", "2026-09-25"),
    ("CONFIG-1", "G", "le misure (b)-(e) da rifare in configurazione del driver; (a) fatta", "2026-09-25"),
    ("CLI-1", "G", "i sigilli delle cure 4 e 5 da rifare **attraverso il CLI**, non impostando il modulo",
     "2026-09-25"),
    ("PRESIDI-RESTO", "G", "`P1`, `P2`, `P4`, `P6` non scritti, piu' l'**arretrato** dei file che non "
     "soddisfano `P3`/`P5`/`P7`", "2026-09-25"),
    ("P9", "G", "la copia diagnostica si genera al run e il **diff** deve essere verificato: oggi i "
     "due blob si stampano, **il diff non lo controlla nessuno** — `P9` e' META' fatto", "2026-09-25"),
    ("RAMPA-2", "A", "`_cs_nodo_prev` non e' inizializzata: la cache parte assente e il primo passo "
     "cade sul fallback", "2026-09-25"),
    ("RAMPA-2/c", "A", "la candidata di Luca: inizializzare valutando **la stessa legge** sullo stato "
     "iniziale", "2026-09-25"),
    ("OMEGA-ETA", "A", "il rapporto `|omega|` figlio/maturo **sale con l'eta'** (`1.05 -> 1.86` fra "
     "eta' 2 e 14): **da seguire nel run base, NON una cura** *(Luca)*", "2026-09-26"),
    ("COPPIA-RAMP", "A", "la coppia **non porta `ramp`** (`^0.15`, `^0.04`) mentre il peso d'arco porta "
     "`ramp_i*ramp_j`: **domanda aperta, non cura**", "2026-09-26"),
    ("INERZIA-1(C)", "A", "la cura per **conteggio** e' giusta e insufficiente; superata dalla **CURA A** "
     "(`rho_s/W^2`), che resta da **sigillare a 4 semi anche su `C2`**", "2026-09-25"),
]


def righe_difetti(testo):
    """Le righe della tabella dei difetti acclarati: `| **Dxx** | ... |`."""
    fuori = []
    for riga in testo.split(NL):
        m = re.match(r"^\|\s*\*\*(D\d\d)\*\*([^|]*)\|(.*)$", riga)
        if not m:
            continue
        marchio = m.group(2)          # `D34`/`D37` portano il loro stato DOPO l'id
        campi = [c.strip() for c in m.group(3).split("|")]
        while len(campi) < 4:
            campi.append("")
        fuori.append({"id": m.group(1), "difetto": campi[0], "prova": campi[1],
                      "cura": campi[2], "stato": campi[3] + " " + marchio})
    return fuori


def stato_corto(s):
    for k in ("NON E' UN DIFETTO", "CURATO", "CURA IN CODICE", "CURA DERIVATA", "APERTO"):
        if k in s:
            return k
    return "?"


def breve(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n - 1] + "…"


T = io.open(SORGENTE, encoding="utf-8", newline="").read()
D = righe_difetti(T)
assert len(D) >= 30, "trovati solo %d difetti: la tabella e' cambiata, NON tiro a indovinare" % len(D)

APERTI = [d for d in D if stato_corto(d["stato"]) in ("APERTO", "CURA DERIVATA")]
FUORI = [d for d in D if d not in APERTI]
MANCA = sorted(set(d["id"] for d in D) - set(FAMIGLIA_DI))
# il controllo INVERSO, e serve: un ID classificato che la tabella non contiene significa che ho
#   scritto una famiglia per un difetto che non esiste, o che la riga non si fa leggere.
FANTASMI = sorted(set(FAMIGLIA_DI) - set(d["id"] for d in D))

R = []


def P(s=""):
    R.append(s)


P("# \U0001f4cb **LA LISTA CHIUSA — BOZZA PER L'APPROVAZIONE DI LUCA**")
P()
P("*(Mandato globale `0c42925`, parte 1. **Generata** da `csv/_lista_chiusa.py` leggendo la tabella")
P("dei difetti acclarati di `doc/STATO_RUN.md`: **nessuna riga e' ricopiata a mano** (`P1-ter`).)*")
P()
P("> ## ⚠ **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.**")
P("> **Diventa la linea d'arrivo solo quando Luca la APPROVA.** Finche' non lo e', **non vale il")
P("> vincolo che vieta le indagini nuove**, e non si comincia a spuntarla.")
P()
P("**COSA E' GENERATO E COSA E' MIO GIUDIZIO, perche' la differenza conta:**")
P()
P("| | |")
P("|---|---|")
P("| **generato dal file** | l'`ID`, la riga del difetto, la prova, il campo `cura`, lo stato |")
P("| **giudizio MIO, da correggere** | **la FAMIGLIA** di ciascun difetto e la **dimensione**: "
  "stanno in `FAMIGLIA_DI` dentro lo script, **una riga per ID**, cosi' si cambiano in un posto solo |")
P()
P("```")
P("difetti acclarati in tabella      %3d" % len(D))
P("APERTI o con CURA DERIVATA        %3d   <- LA LISTA" % len(APERTI))
P("gia' CURATI / non-difetti         %3d   <- fuori, ma restano in tabella (non si cancellano)" % len(FUORI))
P("voci di coda non-difetto          %3d   <- strumenti, domande, misure da rifare" % len(CODA_ALTRO))
P("```")
P()
if FANTASMI:
    P("> ⚠ **CLASSIFICATI MA ASSENTI DALLA TABELLA, e lo dico perche' significa che una riga non")
    P("> si fa leggere o che ho inventato un ID:** %s." % ", ".join("`%s`" % f for f in FANTASMI))
    P()
if MANCA:
    P("> ⚠ **SENZA FAMIGLIA, e lo dico invece di metterli in una a caso:** %s."
      % ", ".join("`%s`" % m for m in MANCA))
    P()

P("---")
P()
P("## LE SETTE FAMIGLIE")
P()
P("| | famiglia | cosa raccoglie |")
P("|---|---|---|")
for k, nome, che in FAMIGLIE:
    P("| **%s** | **%s** | %s |" % (k, nome, che))
P()
P("> **L'ORDINE FRA LE FAMIGLIE E' UNA PROPOSTA, e ha una ragione:** **`A`** prima perche' l'inerzia")
P("> entra in **ogni** passo di **ogni** nodo, e una misura fatta con l'inerzia sbagliata va rifatta;")
P("> **`G`** per ultima **no**: va **in parallelo**, perche' e' cio' che rende verificabile tutto il")
P("> resto e **non produce numeri di fisica**. **Le altre cinque le ordina Luca.**")
P()
P("---")
P()

for k, nome, _che in FAMIGLIE:
    dd = [d for d in APERTI if FAMIGLIA_DI.get(d["id"]) == k]
    aa = [a for a in CODA_ALTRO if a[1] == k]
    P("## FAMIGLIA **%s** — %s   *(%d difett%s, %d voc%s di coda)*"
      % (k, nome, len(dd), "o" if len(dd) == 1 else "i", len(aa), "e" if len(aa) == 1 else "i"))
    P()
    if dd:
        P("| ID | il difetto | stato | cura proposta | prova |")
        P("|---|---|---|---|---|")
        for d in dd:
            P("| **%s** | %s | `%s` | %s | %s |"
              % (d["id"], breve(d["difetto"], 200), stato_corto(d["stato"]),
                 breve(d["cura"], 90) or "—", breve(d["prova"], 110) or "—"))
        P()
    if aa:
        P("**Voci di coda che NON sono difetti acclarati** *(strumenti, domande, misure da rifare)*:")
        P()
        P("| voce | dal | cosa |")
        P("|---|---|---|")
        for nm, _f, che, quando in aa:
            P("| **%s** | %s | %s |" % (nm, quando, che))
        P()
    if not dd and not aa:
        P("*(nessuna voce aperta assegnata a questa famiglia: se e' un errore di assegnazione, si")
        P("corregge in `FAMIGLIA_DI`.)*")
        P()
    P("---")
    P()

P("## ⚠ **I SOSPETTI RESTANO SEPARATI**")
P()
P("Nella coda unica di `doc/STATO_RUN.md` i **sospetti** (`Sxx`) hanno la loro sezione e **non")
P("entrano qui**: un sospetto si **promuove** con la prova (`PROMOSSO: Sxx -> Dyy`) e **solo allora**")
P("puo' entrare in una famiglia. **Metterli nella lista la renderebbe non finibile**, che e'")
P("esattamente cio' che la chiusura deve impedire.")
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
P("> indagini nuove** — inventari, controlli a tappeto, sonde esplorative — **se non servono a una")
P("> voce**. *(Nel solo 2026-09-25 ne avevo aperte cinque: audit di `eta`, audit di `rho_s`,")
P("> `ANCORE-1`, la tabella delle configurazioni, `P7`. Sono state utili, e da ora ciascuna ha")
P("> bisogno di una voce a cui servire.)*")
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
P("- **non dice che i difetti aperti siano %d e non uno di piu'**: dice che **%d righe della tabella"
  % (len(APERTI), len(APERTI)))
P("  portano lo stato `APERTO` o `CURA DERIVATA`**. Un difetto che esiste e **non e' in tabella**")
P("  non lo vede nessuno, e la tabella stessa e' stata **ricostruita dai file, non da memoria**.")
P("- **non dice che le famiglie siano le giuste**: sono le sette proposte dal guardiano nel mandato,")
P("  e il mandato dice **di correggerle se i dati dicono altro, dichiarandolo**.")
P("- **non contiene la DIMENSIONE di ciascuna voce**, che il mandato chiede: stimarla richiede di")
P("  leggere il codice di ognuna, ed e' **lavoro, non generazione**. **Manca, e lo dico** invece di")
P("  riempire una colonna con numeri inventati.")
P("- **non e' ordinata per DIPENDENZE dentro la famiglia**: l'ordine e' quello della tabella")
P("  *(decrescente per ID)*. Le dipendenze fra difetti **non sono registrate in un campo**, quindi")
P("  ricavarle sarebbe un giudizio mio riga per riga. **Secondo punto che manca.**")

t = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(t)
print("scritto %s   (%d difetti in lista, %d fuori, %d voci di coda)"
      % (DEST, len(APERTI), len(FUORI), len(CODA_ALTRO)))
if MANCA:
    print("SENZA FAMIGLIA: %s" % ", ".join(MANCA))
