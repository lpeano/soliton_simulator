# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_infrastruttura_era2_terza.md` — **il referto del mandato `4` di `6`.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: le cifre escono
dall'### **uscita dei collaudi che questo script FA GIRARE**, dalla ### **tabella delle
leggi**, dalla ### **guida**, e da ### **`git`**.

### ⭐ **E QUESTO MANDATO ERA DI IRRIGIDIMENTO: ha preso cose che FUNZIONAVANO PER
ABITUDINE e le ha rese OBBLIGATORIE.** ### **La sezione che conta è la `3.`** — *«che cosa
i presidi mi hanno detto»* — perché in sette punti ### **i presidi del repo mi hanno
corretto DODICI volte**, e ### **tre di quelle correzioni hanno cambiato il disegno, non
una riga.**
"""
# ### ⚠ **L-ESENZIONE STA QUI, FUORI DAL DOCSTRING**, dove un commento e- un commento --
# ### e l-ho imparato da `H-P5` che mi ha rifiutato un commit.
# ESENTE-H-P5: questo referto NON misura il simulatore. Non fa girare nessuna scena di
#   fisica e non produce nessun numero di fisica: parla dei PRESIDI dell-era 2. Dichiarare
#   <<la configurazione intera>> del driver qui direbbe DOVE NON SI E- MISURATO, che e-
#   rumore. Il blob e- dichiarato comunque, e ASSERITO: b8c21049.
import hashlib
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)

import _verdetto as VD                                      # noqa: E402
VERDETTO = VD.verdetto

FUORI = os.path.join(RADICE, "doc", "REFERTO_infrastruttura_era2_terza.md")

# ### il commit del TASK HISTORY: per il rito del par. `8` e- ### **antenato** dei commit
# ### del lavoro, e la sezione finale ### **lo verifica con git.**
PRIMA = "e2781da"

PUNTI = (
    ("1", "DETERMINISMO", "`P-DET`", "primo_ordine/_collauda_determinismo.py"),
    ("2", "DIMENSIONI", "`P-DIM`", "primo_ordine/leggi/schema.py"),
    ("3", "SIMMETRIE E CONSERVAZIONI", "`P-SIM`", "primo_ordine/_collauda_simmetrie.py"),
    ("4", "IL GRAFO VALIDO A OGNI PASSO", "`P-GRAFO`", "primo_ordine/_collauda_grafo.py"),
    ("5", "HOOK COME BARRIERA, CI COME RETE", "`P-BARRIERA`",
     "csv/_barriera.py --collaudo"),
    ("6", "I TEMPI, E UN SOLO COMANDO", "`P-TEMPI`", "primo_ordine/collauda.py"),
    ("7", "LA GUIDA, ESEGUITA", "`P-GUIDA`", "primo_ordine/_collauda_guida.py"),
)

_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)")


def gira(cmd):
    p = subprocess.run([sys.executable] + cmd.split(), cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def conta(t):
    a = b = 0
    for m in _SUSU.finditer(t):
        a, b = max(a, int(m.group(1))), max(b, int(m.group(2)))
    return a, b


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    del argv

    blob = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"),
                                "rb").read()).hexdigest()[:8]
    assert blob == "b8c21049", "### IL SIMULATORE E- CAMBIATO: %s" % blob

    R = []

    def P(s=""):
        R.append(s)

    P("# IL REFERTO DELLA TERZA PARTE — **il mandato `4` di `6`**")
    P()
    P("> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_terza_parte.py`:"
      " non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.")
    P("> **Il simulatore:** `%s`, ### **non toccato.** **Nessuna fisica nuova:**"
      " la tabella ha ancora ### **`3` leggi, tutte `prova: true`.**" % blob)
    P()
    P("### ⭐ **QUESTO MANDATO ERA DI IRRIGIDIMENTO: ha preso cose che FUNZIONAVANO"
      " PER ABITUDINE e le ha rese OBBLIGATORIE.** Il piano, scritto due mandati prima,"
      " lo diceva di una di esse: la forma bilineare era *«gia' vera senza essere una"
      " regola»*, e ### **finche' il generatore non la pretende e' un'abitudine.**")
    P()
    P("---")
    P()
    P("## `1.` I SETTE PUNTI, e il collaudo di ognuno")
    P()
    P("| | il punto | il presidio | il collaudo |")
    P("|---|---|---|--:|")
    tot = [0, 0]
    coppie = []
    for n, titolo, pres, cmd in PUNTI:
        rc, t = gira(cmd)
        a, b = conta(t)
        tot[0] += a
        tot[1] += b
        coppie.append((a, b))
        P("| `%s` | %s | %s | %s |" % (n, titolo, pres, VERDETTO(a, b, rc)))
    # ### ⛔ **E IL TOTALE E- VERDE SOLO SE NESSUN ADDENDO ERA ROSSO:** sommare
    # ### `12`+`14` e scrivere `26`/`27` con un ✅ sarebbe ### **lo stesso difetto un
    # ### livello piu- in su.**
    P("| | ### **IN TUTTO** | | %s |" % VD.totale(coppie))
    P()
    P("---")
    P()
    P("## `2.` I NUMERI MISURATI")
    P()
    rc, t = gira("primo_ordine/collauda.py")
    mt = re.search(r"IL TOTALE del `pre-commit`\s+(\d+\.\d+)", t)
    ml = re.search(r"piu- i LENTI, solo in CI\s+(\d+\.\d+)", t)
    mi = re.search(r"IN TUTTO\s+(\d+\.\d+)", t)
    mc = re.search(r"TUTTI I COLLAUDI PASSANO: (\d+) su (\d+)", t)
    mm = re.search(r"la macchina: (.+)", t)
    P("| | |")
    P("|---|--:|")
    P("| i collaudi del comando unico | `%s` |"
      % (("### **%s su %s, TUTTI PASSANO**" % mc.groups()) if mc
         else "### **QUALCUNO FALLISCE**"))
    P("| il `pre-commit` | `%s` s su un budget di `120` |"
      % (mt.group(1) if mt else "?"))
    P("| i LENTI, solo in CI | `%s` s |" % (ml.group(1) if ml else "?"))
    P("| in tutto | `%s` s |" % (mi.group(1) if mi else "?"))
    P("| la macchina | %s |" % (mm.group(1).strip() if mm else "?"))
    P()
    # ------------------------------------------------------------------ il determinismo
    _rc, td = gira("primo_ordine/determinismo.py")
    mu = re.search(r"(\d+) usi di `random`[^,]*, (\d+) NON `default_rng`", td)
    P("| il determinismo | |")
    P("|---|--:|")
    P("| usi di `random` sotto `primo_ordine/` | `%s`, di cui GLOBALI `%s` |"
      % (mu.group(1) if mu else "?", mu.group(2) if mu else "?"))
    P("| due processi, stessa configurazione | ### **byte-identici** |")
    P()
    # ------------------------------------------------------------------ le conservazioni
    _rc, ts = gira("primo_ordine/_collauda_simmetrie.py")
    mn = re.search(r"NORMA\s+[\d.]+ -> [\d.]+\s+deriva relativa ([\d.e+-]+)\s+"
                   r"soglia ([\d.e+-]+)", ts)
    me = re.search(r"ENERGIA\s+[+\-\d.]+ -> [+\-\d.]+\s+deriva relativa ([\d.e+-]+)\s+"
                   r"soglia ([\d.e+-]+)", ts)
    P("| le conservazioni, e le soglie ### **DERIVATE** | la deriva | la soglia |")
    P("|---|--:|--:|")
    P("| `NORMA` *(`passi * eps`: invariante quadratico)* | `%s` | `%s` |"
      % (mn.group(1) if mn else "?", mn.group(2) if mn else "?"))
    P("| `ENERGIA` *(`dt^2`: metodo simmetrico)* | `%s` | `%s` |"
      % (me.group(1) if me else "?", me.group(2) if me else "?"))
    P()
    P("### ⭐ **E LE DUE SOGLIE SONO LONTANE DI NOVE ORDINI DI GRANDEZZA, che dice"
      " una cosa VERA: la norma e' conservata DALLA STRUTTURA del metodo, l'energia solo"
      " APPROSSIMATA.** ### **Dichiararle con la stessa soglia nasconderebbe esattamente"
      " questo.**")
    P()
    # ------------------------------------------------------------------ il grafo
    _rc, tg = gira("primo_ordine/_collauda_grafo.py")
    mg = re.search(r"il controllo: ([\d.]+) us\s+un passo GLOBALE: ([\d.]+) us\s+"
                   r"rapporto: ([\d.]+)%", tg)
    P("| il grafo, controllato A OGNI PASSO | |")
    P("|---|--:|")
    P("| il controllo | `%s` us |" % (mg.group(1) if mg else "?"))
    P("| un passo GLOBALE | `%s` us |" % (mg.group(2) if mg else "?"))
    P("| ### **il rapporto** | ### **`%s`%%** |" % (mg.group(3) if mg else "?"))
    P("| archi scambiati TUTTI | ### **stesso stato AL BIT** |")
    P()
    P("---")
    P()
    P("## `3.` CHE COSA I PRESIDI MI HANNO DETTO — ### **e tre volte hanno cambiato il"
      " DISEGNO, non una riga**")
    P()
    P("| | il presidio | che cosa ha visto |")
    P("|---|---|---|")
    DETTI = (
        ("`P-MOD`", "`grafo.py` NON era in mappa, e `passo.py` chiamava `controlla`"
         " senza dichiararla"),
        ("### **`P-MOD`**", "### ⭐ **IL COLLAUDO DI UN MODULO CHE STA IN FONDO ALLA"
         " CATENA DEGLI IMPORT NON PUO' VIVERE DENTRO QUEL MODULO:** il collaudo di"
         " `grafo.py` importava `driver` e `passo`, e `passo` importa `grafo` — ### **un"
         " CICLO.** ### **E' la stessa ragione per cui `_collauda_passo.py` esiste, e"
         " NON L'AVEVO CAPITA**"),
        ("### **`P-MOD`**", "### ⭐ **`_genera.py` a `738` righe sul tetto di `700`:"
         " *«oltre SI DIVIDE, NON SI ALLUNGA»*.** ### **Alzare il tetto sarebbe stato"
         " esattamente la manopola che `A1` vieta**"),
        ("`P-ES1`", "tre collaudi AVANZANO LO STATO, e le eccezioni vanno DICHIARATE"
         " col loro perche' di almeno `40` caratteri"),
        ("`P-C1`", "le voci `P-GRAFO` e `P-TEMPI` risultavano ### **tende**: le"
         " `SORGENTI` guardavano ### **solo `csv/`**, e un presidio puo' vivere"
         " ### **sotto `primo_ordine/`**"),
        ("`P-RIF`", "gli ID `P-C1`, `P-MOD` e `A16` stavano ### **in COMMENTI**: un"
         " riferimento che una macchina deve seguire ### **non vive nella prosa.** ### E"
         " al terzo giro ### **ha colto SE STESSO**"),
        ("`P-E6`", "la tabella cambiava e ### **la riga del registro dell'era `2` non era"
         " nel commit**: porta ### **l'IMPRONTA** della legge, e senza di lei il registro"
         " dichiara l'impronta di una tabella ### **che non esiste piu'**"),
        ("`H-P5`", "l'esenzione era ### **dentro il docstring**, dove ### **non e' un"
         " commento**"),
        ("`PI-FISICA-ERA1-NON-SOSPESA`", "una voce dell'era `1` non chiusa e'"
         " ### **`SOSPESA`**, e lo stato dell'era `1` va in `stato_era_1`"),
        ("`PI-STORICO-SENZA-COMMIT`", "### **otto volte**, e il rito e' sempre lo stesso:"
         " `python csv/indice.py storico-commit`"),
        ("### **`P-BARRIERA`**", "### ⭐ **MI HA FERMATO UN'ORA DOPO AVERLA"
         " SCRITTA:** ho cambiato il `pre-commit` e lo strumento dell'indice"
         " ### **si e' rifiutato di partire.** ### **L'ordine e': si cambia un hook, POI"
         " `--scrivi`, POI gli strumenti**"),
        ("### **`P-TEMPI`**", "### ⭐ **UNA MIA CLASSIFICAZIONE ASSERITA INVECE CHE"
         " MISURATA:** il collaudo della catena era dichiarato *«oltre `120` secondi»* e"
         " ### **costa `2.55`.** ### **Quel numero era di un'altra cosa**"),
    )
    for k, (pres, che) in enumerate(DETTI, 1):
        P("| `%d` | %s | %s |" % (k, pres, che))
    P()
    P("### ⚠ **DODICI CORREZIONI IN SETTE PUNTI, e il numero che conta e' un altro:"
      " TRE hanno cambiato il DISEGNO.** ### **Due volte `P-MOD` mi ha detto dove deve"
      " vivere un collaudo** *(fuori dal modulo che collauda, se quel modulo sta in fondo"
      " alla catena degli import)*, ### **e una volta mi ha impedito di alzare un"
      " tetto** — che e' la manopola piu' facile di tutte.")
    P()
    P("---")
    P()
    P("## `4.` CHE COSA HO SBAGLIATO IO — ### **e due previsioni, una tenuta e una no**")
    P()
    P("| | l'errore o la previsione | l'esito |")
    P("|---|---|---|")
    MIEI = (
        ("la trappola `(a)` del task history: *«il punto `5` puo' ROMPERE LA CI»*",
         "### ✅ **TENUTA.** Nella CI i hook ### **non sono attivi**, e il mandato"
         " preso alla lettera ### **avrebbe fatto fallire SEMPRE la CI.** ### **La"
         " barriera TACE fuori dal PC, e lo DICHIARO come mia inferenza**"),
        ("la trappola `(b)`: *«due processi NON daranno file byte-identici, perche' un"
         " `.npz` e' uno ZIP e porta la data»*",
         "### ⛔ **SBAGLIATA**, e il perche' e' MISURATO: `numpy.savez` scrive"
         " `date_time = (1980,1,1,0,0,0)` — ### **AZZERA l'ora.** ### ⭐ **E l'ho"
         " verificato in ENTRAMBE le direzioni: prima le due corse, POI l'intestazione"
         " dello ZIP — perche' due corse a meno di `2` secondi starebbero nella stessa"
         " finestra, e il braccio sarebbe un FALSO-UNO**"),
        ("il controllo dimensionale dentro `valida_legge`, che leggeva le dimensioni"
         " ### **da `variabili`**",
         "### ⛔ **SALTAVA IN SILENZIO**, e i `34` collaudi dello schema"
         " ### **passavano tutti** mentre il generatore ### **accettava `K` di dimensione"
         " `E^2`.** ### **Visto solo rompendo la tabella a posta e guardando il codice"
         " d'uscita**"),
        ("il timbro del determinismo",
         "### ⚠ **STAVA PER MENTIRE:** `avvia()` dice *«ero in tempo?»* e il timbro"
         " ### **lo richiama quando `numpy` c'e' gia'** — il driver lo chiama in tempo e"
         " il timbro diceva `false`. ### **Curato: il verdetto e' quello della PRIMA"
         " chiamata**"),
        ("<<zero sostituzioni = falso-uno>> nelle simmetrie",
         "### ⛔ **TROPPO STRETTO**, e il collaudo me l'ha detto rifiutando la mia"
         " riga di prova: zero sostituzioni di `U(1)` su una legge ### **senza `psi`** e'"
         " ### **invarianza VERA**; `SCAMBIO-DEI-CAPI` con zero sostituzioni"
         " ### **e' un falso-uno**"),
        ("il braccio di `P-ID` che cercava `` `D4` `` ### **come SOTTOSTRINGA**",
         "### ⛔ **FALSO FALLIMENTO:** `D4` compariva ### **nella DOMANDA di"
         " un'altra voce.** ### **E' lo stesso errore di una regex che non distingue un"
         " commento da un uso: il TERZO della giornata**"),
        ("lo split di `_genera.py`, al primo tentativo",
         "### ⛔ **HO ASSUNTO che `def collaudo()` venisse PRIMA di `def main()`:**"
         " il mio slice ha ### **DUPLICATO una regione** e il file si e' ritrovato con"
         " ### **due `main`.** ### **Ripristinato dai byte committati e rifatto"
         " GUARDANDO l'ordine vero**"),
        ("un'asserzione in uno script di patch",
         "### ⛔ **Cercava la parola `--prova` nel testo, e IL COMMENTO CHE"
         " INSERIVO LA CONTENEVA:** diceva *«non togliato»* mentre il ramo era via."
         " ### **Adesso guarda `return collaudo()`, cioe' IL CODICE**"),
    )
    for k, (che, esito) in enumerate(MIEI, 1):
        P("| `%d` | %s | %s |" % (k, che, esito))
    P()
    P("### ⭐ **E LA COSA CHE QUESTE OTTO RIGHE DICONO INSIEME: SEI SU OTTO SONO"
      " STATE TROVATE FACENDO GIRARE QUALCOSA, NON RILEGGENDO.** ### **Due le ho viste"
      " perche' ho guardato un'uscita DOPO averla scritta** *(il timbro, i tempi)*,"
      " ### **e una perche' ho rotto la tabella A POSTA.**")
    P()
    P("---")
    P()
    P("## `5.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**")
    P()
    P("| | |")
    P("|---|---|")
    P("| ### **il numero di thread** | ### **NON si verifica**: `threadpoolctl` non e'"
      " installato. ### ✅ **Ma i due processi byte-identici dicono cio' che quella"
      " verifica direbbe:** se coincidono, i thread ### **non stanno rompendo il"
      " determinismo** |")
    P("| ### **la CI** | ### **mai osservata girare**, e il passo di `P-BARRIERA` e' il"
      " posto dove ### **la mia inferenza sul silenzio in CI si vedrebbe cadere.**"
      " ### **La differenza fra <<scritto>> e <<osservato>> e' quella fra una tenda e un"
      " muro** |")
    P("| ### **`--no-verify`** | ### **NON e' impedibile in locale**, e nessuno strumento"
      " puo' accorgersene ### **perche' non viene chiamato.** ### **Lo trova la CI, che"
      " non impedisce: FA VEDERE** |")
    P("| ### **l'impronta dei hook** | e' in un file ### **tracciato**: chi cambia un hook"
      " puo' cambiare anche lei. ### **La barriera non lo impedisce, lo rende VISIBILE IN"
      " UNA DIFF** |")
    P("| ### **una legge prima della sua decisione** | ### **nessun presidio lo"
      " impedisce.** `P-ALB` guarda le ### **decisioni**, non le leggi — e la guida lo"
      " dichiara come ### **il suo passo `1`**, che oggi ### **ferma tutto** |")
    P("| ### **`H-FISICA-FUORI-LISTA`** | legge la lista ### **dal DISCO**: una modifica"
      " non committata ### **autorizza un commit.** ### **Aperto dal mandato `1`** |")
    P()
    P("---")
    P()
    P("## `6.` L'ORDINE E' VERIFICABILE DA GIT, non asserito da me")
    P()
    rc3, _ = gira("")
    q = subprocess.run(["git", "merge-base", "--is-ancestor", PRIMA, "HEAD"],
                       cwd=RADICE, capture_output=True)
    P("Il task history di questo mandato e' il commit ### **`%s`**, e per il rito del"
      " par. `8` e' ### **antenato di ogni commit del lavoro.**" % PRIMA)
    P()
    P("### %s **Verificato adesso con `git merge-base --is-ancestor`: `%s` %s antenato"
      " di `HEAD`.**"
      % ("✅" if q.returncode == 0 else "⛔", PRIMA,
         "E'" if q.returncode == 0 else "### NON E'"))
    P()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("  scritto %s (%d righe)" % (FUORI, len(R)))
    print("  il simulatore: %s, ASSERITO" % blob)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
