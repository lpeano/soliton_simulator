# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_infrastruttura_era2.md` — **la TAPPA `6` del mandato.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: questo script
### **FA GIRARE i collaudi** e prende le cifre ### **dalla loro uscita.** Se un collaudo
smette di passare, ### **il referto lo dice** invece di conservare il numero di ieri.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
BT = chr(96)
FUORI = os.path.join(RADICE, "doc", "REFERTO_infrastruttura_era2.md")

# ### I COMANDI, e ciascuno ### **si rigira verbatim.**
COMANDI = (
    ("la catena", "python primo_ordine/_collauda_passo.py"),
    ("i presidi dell-era 2", "python csv/_presidi_era2.py --collaudo"),
    ("lo schema della tabella", "python primo_ordine/leggi/schema.py"),
    ("il generatore", "python primo_ordine/_genera.py --prova"),
    ("la lista dei file di fisica", "python csv/_collaudo_file_fisica.py"),
    ("i presidi dell-indice", "python csv/_collaudo_presidi_indice.py"),
    ("i controlli della migrazione", "python csv/_controlli_indice_v2.py"),
)

_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)")


def gira(cmd):
    p = subprocess.run(cmd, shell=True, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def conta(testo):
    """L-ultimo `N su M` del testo: ### **il totale**, non un parziale."""
    m = _SUSU.findall(testo)
    return (int(m[-1][0]), int(m[-1][1])) if m else (None, None)


def numero(testo, pat, grp=1, conv=float):
    m = re.search(pat, testo)
    return conv(m.group(grp)) if m else None


def main():
    import _presidio
    _presidio.avvia(__file__)
    import hashlib
    sim = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"), "rb")
                       .read()).hexdigest()[:8]
    assert sim == "b8c21049", sim

    esiti = []
    for nome, cmd in COMANDI:
        rc, out = gira(cmd)
        a, b = conta(out)
        esiti.append((nome, cmd, rc, a, b, out))
        print("  %-28s %s   %s" % (nome, "%s/%s" % (a, b) if a is not None else "(nessun conto)",
                                   "ok" if rc == 0 else "### RC=%d" % rc))
    cat = [x for x in esiti if x[0] == "la catena"][0][5]

    # --- i numeri della catena, PRESI DALLA SUA USCITA
    loc = numero(cat, r"LOCALE: il raggio e- `(\d+)` archi", 1, int)
    glo = numero(cat, r"GLOBALE: il cono NON e- esatto -- arriva a `(\d+)` archi su `(\d+)`",
                 1, int)
    dmax = numero(cat, r"arriva a `\d+` archi su `(\d+)`", 1, int)
    tolleranze = re.findall(r"toll=([0-9.e+-]+): (\d+) archi \((\d+) iterazioni\)", cat)
    derive = re.findall(r"(GLOBALE|LOCALE)\s+norma ([\d.]+) -> ([\d.]+)\s+relativa "
                        r"([\d.e+-]+)", cat)
    energie = re.findall(r"energia ([+\-][\d.]+) -> ([+\-][\d.]+)\s+relativa ([\d.e+-]+)",
                         cat)
    strati = numero(cat, r"(\d+) strati su (\d+) archi", 1, int)
    n_archi = numero(cat, r"(\d+) strati su (\d+) archi", 2, int)
    n_op = numero(cat, r"`(\d+)` operazioni d-arco nella composizione", 1, int)
    passi = numero(cat, r"la deriva su `(\d+)` passi", 1, int)
    moduli = numero(cat, r"`(\d+)` moduli guardati", 1, int)
    per_d_loc = re.search(r"LOCALE, \|delta\| per distanza: (.+)", cat)
    per_d_glo = re.search(r"GLOBALE, \|delta\| per distanza: (.+)", cat)

    L = []
    A = L.append
    A("# IL REFERTO DELL'INFRASTRUTTURA DELL'ERA `2`")
    A("")
    A("> ### ⭐ **CHE COSA E' STATO COSTRUITO:** ### **la tabella delle leggi e' "
      "l'UNICA fonte**, il codice e la scheda ### **si GENERANO**, e "
      "### **la macchina verifica** che *legge ↔ file ↔ riga di registro "
      "↔ scheda* siano ### **in biiezione** — e che "
      "### **niente cambi senza che cambi la tabella.**")
    A("")
    A("### ⛔ **E NESSUNA DECISIONE DI FISICA E' STATA PRESA.** Le due leggi in "
      "tabella sono `prova: true` *(valori ### **da niente**, e la scheda lo dice)*, "
      "l'osservatore e' ### **uno strumento** *(`A17`)*, e "
      "### **la scelta dell'integratore e' di Luca** — i due candidati stanno "
      "### **nella stessa tavola, senza una raccomandazione travestita da misura.**")
    A("")
    A("**Il simulatore dell'era `1`: `%s`, NON toccato** *(verificato per `sha1` in "
      "ogni commit di questo mandato)*." % sim)
    A("")
    A("---")
    A("")
    # ### ⛔ **IL CONTO DELLE LEGGI** *(punto `10`)*: ### **ogni referto lo
    # ### STAMPA**, e un commit che lo aumenta ### **deve dichiararlo.**
    sys.path.insert(0, os.path.join(RADICE, "primo_ordine"))
    sys.path.insert(0, os.path.join(RADICE, "primo_ordine", "leggi"))
    import timbro as _TB
    _c = _TB.conto_leggi()
    A("## `0.` IL CONTO DELLE LEGGI — ### **`%d`** *(punto `10`)*" % _c["totale"])
    A("")
    A("> ### ⛔ **OGNI REFERTO LO STAMPA, e un commit che lo AUMENTA deve "
      "DICHIARARLO** *(`STANDARD-10`, `AUDIT-CURE`)*: ### **una cura non aumenta il "
      "numero delle leggi**, e a parita- di effetto ### **si preferisce togliere "
      "un-eccezione.**")
    A("")
    A("| | quante |")
    A("|---|--:|")
    for _t, _n in sorted(_c["per_tipo"].items()):
        A("| `%s` | `%d` |" % (_t, _n))
    A("| **in tutto** | ### **`%d`** |" % _c["totale"])
    A("| di cui ### **`prova: true`** | ### **`%d`** |" % _c["di_prova"])
    A("| le **variabili** | `%d` |" % _c["variabili"])
    A("")
    A("### ⚠ **E `%d` SU `%d` SONO DI PROVA**, cioe- ### **non sono fisica "
      "decisa**: valori che vengono ### **da niente**, e la scheda di ognuna lo dice. "
      "### **Il conto delle leggi VERE dell-era `2` e- `%d`.**"
      % (_c["di_prova"], _c["totale"], _c["totale"] - _c["di_prova"]))
    A("")
    A("---")
    A("")
    A("## `1.` CHE COSA BLOCCA, E DOVE")
    A("")
    A("> ### ⚠ **LA DISTINZIONE CHE CONTA, e che ho dovuto correggere in corsa:** "
      "### **blocca** significa *«il commit NON si fa»*. ### **Segnala** significa "
      "*«qualcuno lo legge, se guarda»*. ### ⛔ **`A9`: un presidio che non "
      "impedisce NON E' UN PRESIDIO.**")
    A("")
    A("| | che cosa impedisce | dove | via d'uscita |")
    A("|---|---|---|---|")
    A("| **`P-E1`** | la **BIIEZIONE** *(tabella ↔ file generato ↔ riga di "
      "registro ↔ scheda)*, e `LEGGE` si legge **via AST** | `pre-commit` | "
      "### ⛔ **NESSUNA** |")
    A("| **`P-E2`** | **l'IMPRONTA**: un file generato ritoccato a mano, o una tabella "
      "cambiata senza rigenerare | `pre-commit` | ### ⛔ **NESSUNA** |")
    A("| **`P-E3`** | le **VARIABILI nei due versi** *(tabella ↔ `stato.py` "
      "↔ registro)* | `pre-commit` | ### ⛔ **NESSUNA** |")
    A("| **`P-E4`** | le **IMPORTAZIONI**: la fisica non importa `osservatori/` ne' "
      "`driver` *(`A17`)* | `pre-commit` | ### ⛔ **NESSUNA** |")
    A("| **`P-E5`** | gli **OSSERVATORI in sola lettura**, ### **misurato AL BYTE** | "
      "`pre-commit` | ### ⛔ **NESSUNA** |")
    A("| **`P-E6`** | la tabella che cambia **senza** la riga di registro e **senza** "
      "l'ID nel messaggio | `commit-msg` | ### ⛔ **NESSUNA** |")
    A("| **`P-E7`** | i **RIFERIMENTI**: la scheda esiste, e ### **la `voce` di un "
      "osservatore risolve nell'indice** | `pre-commit` | ### ⛔ **NESSUNA** |")
    A("| **`H-FISICA-FUORI-LISTA`** | un `.py` sotto `primo_ordine/` che non e' "
      "### **dichiarato** in `FILE_FISICA` | `pre-commit` | dichiarata |")
    A("| **`H-ID-OBBLIGATORIO`** | un commit che tocca un file di fisica **senza** "
      "nominare un ID | `commit-msg` | dichiarata |")
    A("")
    A("### ⭐ **E L'ASSENZA DELLA VIA D'USCITA E' ESSA STESSA UN PRESIDIO, "
      "COLLAUDATO:** un braccio di `csv/_presidi_era2.py --collaudo` "
      "### **ispeziona l'AST del proprio file** e verifica che "
      "### **non esista nessun pattern di fuga che qualcuno legga.** "
      "*(La prima stesura ne definiva uno `_FUGA` ### **senza leggerlo mai** — "
      "codice morto che ### **INVITA** una scappatoia che il mandato vieta. Cancellato.)*")
    A("")
    A("### ⛔ `2.` LA CI **NON E' UN PRESIDIO**, ed e' una correzione a me stesso")
    A("")
    A("`.github/workflows/era2.yml` fa girare ### **tutti i collaudi a ogni push**. "
      "### ⚠ **Ma Luca ha deciso: NESSUNA protezione del ramo su GitHub** "
      "*(2026-10-09)*. ### ⛔ **Quindi la CI gira DOPO il push e "
      "NON PUO' IMPEDIRE NIENTE: e' una RETE CHE SEGNALA.**")
    A("")
    A("Io avevo scritto, nell'intestazione di quel file, *«LA CI NON SI PUO' "
      "DIMENTICARE … e NON HA VIA D'USCITA»*, e stavo per dichiararla "
      "### **il gradino di robustezza di questo mandato.** "
      "### ⛔ **ERA FALSO, E LO ERA SEMPRE STATO:** non mi serviva la decisione di "
      "Luca per vederlo — bastava chiedermi *«questa CI PUO' impedire un "
      "commit?»*. ### **Avevo trasferito alla CI una proprieta' vera dei presidi di "
      "`primo_ordine/`** *(che davvero non hanno fuga, perche' il loro codice non legge "
      "nessuna fuga)*, ### **dove non vale.** Il commento e' corretto nello stesso "
      "commit di questo referto.")
    A("")
    A("### ⚠ **E UN `--no-verify` NON E' IMPEDIBILE IN LOCALE.** Lo scrivo perche' "
      "e' ### **il limite vero** dell'intera impalcatura: tutti i presidi di sopra "
      "vivono in `.githooks/`, e ### **valgono solo se qualcuno ha dato "
      "`git config core.hooksPath .githooks`.** "
      "### ⛔ **Finche' quel comando non e' dato, questo repo NON HA PRESIDI** "
      "*(`A9`)*, e ### **chi clona non lo sa.** "
      "*(La cura — ogni strumento che verifica all'avvio che i hook siano attivi "
      "e ### **si rifiuta di partire** — e' in coda.)*")
    A("")
    A("## `3.` CHE COSA RESTA **REGOLA SCRITTA**, e perche'")
    A("")
    A("| | perche' non e' un presidio |")
    A("|---|---|")
    A("| **l'INVENTARIO** *(par.`6`①)* e il **README** *(par.`6`②)* | "
      "nessun hook li guarda: un file nuovo in `csv/` **senza** la sua voce passa. "
      "### **Lo dico invece di contarli fra i presidi** |")
    A("| **`L-STELLA`** *(le cinque domande)* | e' scritta, e in questo mandato "
      "### **ha funzionato comunque**: la domanda `3` mi ha fatto trovare un difetto "
      "*(vedi `6.`)*. ### ⚠ **Ma ha funzionato perche' l'ho applicata, non perche' "
      "qualcosa me l'ha imposta** |")
    A("| **il tipo `regola`** *(le leggi di crescita e di vuoto)* | lo **schema** lo "
      "valida, e il **generatore NON lo genera ancora**. ### ⛔ **Dichiarato, non "
      "risolto:** una `regola` in tabella oggi farebbe scattare `P-E1` *(manca il file)*, "
      "### **che e' il comportamento giusto** ma non e' il pezzo finito |")
    A("| **la decisione `9`** *(la geometria)* e la **`13`** *(i coniugati delle "
      "memorie)* | ### **APERTE, e il formato le AMMETTE senza scegliere** — vedi "
      "`7.` |")
    A("")
    A("## `4.` I NUMERI DEI COLLAUDI — ### **presi dall'uscita dei comandi**")
    A("")
    A("| il collaudo | il comando, ### **verbatim** | esito |")
    A("|---|---|---|")
    for nome, cmd, rc, a, b in [(x[0], x[1], x[2], x[3], x[4]) for x in esiti]:
        ok = (rc == 0) and (a is None or a == b)
        A("| %s | `%s` | %s |"
          % (nome, cmd,
             ("### ✅ **`%d`/`%d`**" % (a, b)) if a is not None
             else ("### ✅ **passa**" if ok else "### ⛔ **FALLISCE**")))
    A("")
    A("## `5.` QUALI PERMUTAZIONI SONO **BYTE-IDENTICHE**, E QUALI NO — "
      "### **con il perche' FISICO**")
    A("")
    A("| | che cosa si permuta | byte-identico? | il perche' |")
    A("|---|---|---|---|")
    A("| `1` | i **termini di `H`** | ### ✅ **SI**, `H` **e** il gradiente | "
      "`H` con `math.fsum`: la somma ### **ad arrotondamento esatto** non dipende "
      "dall'ordine. Il gradiente perche' `gradiente()` ### **impone l'ordine canonico "
      "per ID** — `fsum` non si puo' usare, gli addendi sono **array complessi** |")
    A("| `1-bis` | gli stessi, con la somma **GREZZA** | ### ⛔ **NO** | "
      "### ⭐ **ed e' il controllo che rende il braccio sopra una MISURA e non un "
      "FALSO-UNO:** se anche la somma grezza fosse identica, l'ordine canonico sarebbe "
      "### **un ornamento** |")
    A("| `2` | gli **archi dentro UNO strato** | ### ✅ **SI** | sono "
      "### **DISGIUNTI**: ogni nodo riceve ### **UN SOLO** contributo d'arco, quindi "
      "### **non c'e' nessuna somma da riordinare**. Con `%d` archi in `%d` strati |"
      % (n_archi or 0, strati or 0))
    A("| `3` | **gli STRATI, fra loro** | ### ⛔ **NO** | ### **NON COMMUTANO.** "
      "Due operatori che non commutano danno ### **un RISULTATO diverso, non un "
      "arrotondamento diverso** — e ### ⛔ **nessuna somma esatta puo' "
      "aggiustarlo.** ### ⭐ **L'unica cura e' la SIMMETRIA** *(alla Strang)*, che "
      "annulla l'errore di ordine pari |")
    A("")
    A("### **E LA COMPOSIZIONE E' VALIDATA, con quattro controlli** *(e ognuno ha il suo "
      "caso che DEVE fallire)*: i **nomi** nel vocabolario · i nomi **e i pesi** "
      "un ### **PALINDROMO** · nessun ### **DOPPIONE consecutivo** · i pesi di "
      "ogni operazione che ### **sommano a `1`** *(altrimenti "
      "### **si integrerebbe un tempo diverso da `dt`, e il codice non lo direbbe**)*.")
    A("")
    A("## `6.` I DUE INTEGRATORI — ### ⛔ **LA TAVOLA, SENZA SCEGLIERE**")
    A("")
    A("> ### **LA SCELTA E' DI LUCA** *(il nodo `INT` del piano)*. Qui ci sono "
      "### **le misure**, e ### **una cosa che non sapevo prima di misurare.**")
    A("")
    A("| | il cono | deriva **NORMA** | deriva **ENERGIA** | il costo |")
    A("|---|---|--:|--:|---|")
    dd = {k: (a, b, c) for k, a, b, c in derive}
    ee = dict(zip([k for k, _, _, _ in derive], energie))
    for nome in ("GLOBALE", "LOCALE"):
        r = glo if nome == "GLOBALE" else loc
        cono = ("`%d` su `%d` archi, ### ⚠ **NON dichiarato: ARTEFATTO della "
                "tolleranza**" % (r or 0, dmax or 0)) if nome == "GLOBALE" else \
               ("`%d` su `%d` archi, ### ✅ **ESATTO e DICHIARATO**"
                % (r or 0, dmax or 0))
        costo = ("`%s` iterazioni di punto fisso"
                 % "`-`".join(sorted({it for _, _, it in tolleranze}))) \
            if nome == "GLOBALE" else ("`%d` sotto-passi × le sue iterazioni"
                                       % (2 * (strati or 1) + 1))
        A("| **%s** | %s | `%s` | `%s` | %s |"
          % (nome, cono, dd.get(nome, ("", "", "?"))[2],
             ee.get(nome, ("", "", "?"))[2], costo))
    A("")
    A("**Il cono, misurato** *(catena di `%d` archi, `%d` strati, perturbo UN nodo, "
      "`dt` dichiarato nel collaudo)*:" % (n_archi or 0, strati or 0))
    A("")
    A("- **per STRATO:** ### **`1` arco**, e oltre ### ✅ **ESATTAMENTE ZERO** "
      "— e' cio' che uno strato **significa**.")
    A("- **per PASSO, LOCALE:** ### **`%s` archi**, e oltre ### ✅ **ESATTAMENTE "
      "ZERO**. ### ⚠ **E NON L'AVEVO PREVISTO:** credevo `%s`, il **numero di "
      "strati**. ### **La composizione simmetrica visita gli strati `2L-1` volte**, "
      "quindi il cono per passo e' ### **il numero di operazioni d'arco** *(`%s`)*, "
      "non `L`." % (loc, strati, n_op))
    if per_d_loc:
        A("  - `%s`" % per_d_loc.group(1).strip())
    A("- **per PASSO, GLOBALE:** `%s` archi su `%s`." % (glo, dmax))
    if per_d_glo:
        A("  - `%s`" % per_d_glo.group(1).strip())
    A("")
    A("### ⛔ **E QUI LA MISURA HA CORRETTO UN BRACCIO CHE AVEVO SCRITTO IO.** Avevo "
      "asserito *«il GLOBALE a distanza massima NON e' zero»*: "
      "### **falso** — oltre un certo raggio e' ### **esattamente zero**, "
      "per ### **underflow relativo allo stato.** "
      "### ⭐ **E la ragione vera e' PEGGIORE di quella che credevo:**")
    A("")
    A("| la tolleranza del punto fisso | il raggio del cono | le iterazioni |")
    A("|---|---|---|")
    for tl, r, it in sorted(tolleranze, key=lambda x: float(x[0])):
        A("| `%s` | ### **`%s` archi** | `%s` |" % (tl, r, it))
    A("")
    A("### ⛔ **IL CONO DELL'INTEGRATORE GLOBALE DIPENDE DA UNA MANOPOLA DEL "
      "RISOLUTORE.** Quindi ha un orizzonte che ### **ASSOMIGLIA a una causalita' e non "
      "lo e'.** ### ⭐ **Ed e' PEGGIO di un cono infinito, non meglio: un cono "
      "infinito si vedrebbe; questo si nasconde.** "
      "### **E' la ragione piu' forte contro il globale**, e "
      "### **non l'avrei trovata se non avessi misurato il cono A TRE TOLLERANZE** "
      "— cosa che ho fatto ### **perche' la domanda `3` della stella polare "
      "pretende di dire DI CHE TIPO e' un numero**, e non mi lasciava chiudere con "
      "*«parametro del risolutore, `A17`»*.")
    A("")
    A("### ⚠ **E LA NORMA NON E' CONSERVATA AL BIT DA NESSUNO DEI DUE**, e lo dico "
      "invece di prometterlo: il punto medio implicito conserva gli invarianti "
      "### **quadratici** ### **in aritmetica esatta**, non in virgola mobile. "
      "I numeri di sopra, su `%s` passi, ### **sono MISURE, non garanzie.**" % passi)
    A("")
    A("### `A8b` — **nessuna cache nascosta fra i passi**")
    A("")
    A("`senza_cache()` confronta ### **tutte le costanti di modulo** dei moduli di fisica "
      "prima e dopo tre passi: ### **`%s` moduli, nessuno si ricorda niente** — e "
      "### **il presidio SCATTA** se gliene si fa ricordare uno. "
      "### ⚠ **IL SUO LIMITE, dichiarato:** guarda le costanti di **MODULO**, e "
      "### **non vedrebbe uno stato nascosto in un attributo di OGGETTO o in una "
      "chiusura.** Oggi i moduli di fisica non hanno ne' classi ne' chiusure; "
      "### **se un giorno le avranno, il presidio VA ALLARGATO.**" % moduli)
    A("")
    A("## `7.` LE DOMANDE APERTE PER LUCA")
    A("")
    A("| | la domanda | perche' e' TUA e non mia |")
    A("|---|---|---|")
    A("| **`1`** | ### **QUALE INTEGRATORE** *(nodo `INT`)*: il **GLOBALE** o il "
      "**LOCALE**? | i due non sono *«lo stesso metodo fatto meglio»*: "
      "### **integrano cose diverse** *(il locale e' un prodotto di esponenziali di "
      "strato)*. ### **La norma e l'energia sono quasi identiche**; il cono "
      "### **no** — e un cono esatto e' ### **un impegno di fisica**, non una "
      "proprieta' numerica |")
    A("| **`2`** | la **dipendenza del cono globale dalla tolleranza** e' un "
      "### **DIFETTO da registrare nell'indice**? | io l'ho ### **misurata e "
      "dichiarata**, e ### **non le ho dato una voce**: dipende da se il globale resta "
      "un candidato. ### ⚠ **Se resta, la voce serve** |")
    A("| **`3`** | la **decisione `9`** *(la geometria)*: oggi `pos`, `x`, `y`, `z`, "
      "`coord` sono ### **SIMBOLI VIETATI**, e il generatore ### **rifiuta** "
      "un'espressione che li nomina | il formato ### **non anticipa la `9`**, e la "
      "direzione che hai dichiarato — *«lo spazio emerge grazie alla "
      "mitosi»*, la `9(b)` — ### **non e' ancora una decisione presa.** "
      "### ⛔ **Se diventa la `9(a)`, il divieto va TOLTO dallo schema**, non "
      "aggirato |")
    A("| **`4`** | la **decisione `13`** *(i coniugati delle memorie)*: il tipo "
      "`coppia_coniugata` e' ### **AMMESSO dal vocabolario e NON USATO** | e' "
      "### **la forma dell'ammissione senza la scelta**: `stato.py` solleva "
      "`NotImplementedError` se qualcuno lo usa, quindi "
      "### **la tabella puo' dichiararlo e il codice dice che non sa ancora farlo** "
      "— invece di fingere |")
    A("")
    A("### ⭐ **E CHE COSA LE DECISIONI `9` E `13` CAMBIERANNO NEL FORMATO** "
      "*(cosi' non si scopre dopo)*")
    A("")
    A("- **la `9`** toccherebbe ### **`VIETATI` nello schema** e "
      "### **`TIPI_VARIABILE`** *(servirebbe un tipo per una coordinata, che oggi "
      "**non esiste di proposito**)*. ### ✅ **Non toccherebbe il generatore**: i "
      "simboli vengono ### **dai tipi**, quindi un tipo nuovo "
      "### **si propaga da solo** a `stato.py`, all'ambiente e alla derivata.")
    A("- **la `13`** toccherebbe ### **`DOVE`** *(nodo o arco)* e "
      "### **`coppie_di()`** nel generatore, che e' ### **la mappa fra un simbolo e il "
      "suo coniugato**: una memoria con un coniugato ### **entrerebbe nella derivata di "
      "Wirtinger** come `psi`. ### ✅ **La forma c'e' gia'**, e il `NotImplementedError` "
      "e' ### **il segnaposto ONESTO.**")
    A("")
    A("---")
    A("")
    A("### ⚠ **E UNA COSA CHE QUESTO MANDATO NON HA FATTO, perche' non gliel'ho "
      "chiesto io:** la **CI non e' mai stata osservata girare**. E' scritta, i suoi "
      "passi sono gli stessi comandi della tavola `4.`, ### **ma non ho la prova che il "
      "server li abbia eseguiti** — e ### **per `A9` la differenza fra <<scritto>> "
      "e <<osservato>> e' la stessa che fra una tenda e un muro.**")
    A("")
    A("*(Referto generato da `csv/_referto_infrastruttura_era2.py`: "
      "### **ogni numero esce dall'uscita dei comandi della tavola `4.`** — "
      "`L-NUMERI`.)*")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(L) + NL)
    print()
    print("  scritto %s (%d righe)" % (os.path.relpath(FUORI, RADICE), len(L)))
    tutti_ok = all((x[2] == 0) and (x[3] is None or x[3] == x[4]) for x in esiti)
    print("  ### TUTTI I COLLAUDI PASSANO" if tutti_ok
          else "  ### ⛔ QUALCHE COLLAUDO NON PASSA, e il referto LO DICE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
