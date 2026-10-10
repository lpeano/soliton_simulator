# -*- coding: utf-8 -*-
"""PUNTO `6` DELLA TERZA PARTE — **UN SOLO COMANDO, E I TEMPI.**

> ### ⛔ **Il mandato, alla lettera:** *«**I TEMPI:** budget dichiarato per il
> `pre-commit`, suite completa in CI; **un solo comando**, `primo_ordine/collauda.py`,
> esegue tutti i collaudi e **stampa i tempi**. Oltre il budget → segnale»*.

### ⭐ **E <<OLTRE IL BUDGET → SEGNALE>> E' LA PARTE CHE CONTA, non il budget.** Un budget
che ### **FERMA** sarebbe un presidio sul tempo di una macchina — e il tempo di una
macchina ### **non è una proprietà del repo**: cambia col PC, col carico, col disco.
### ⛔ **Fermare su quello vorrebbe dire rifiutare un commit perché il computer era
occupato.** ### ✅ **Un SEGNALE invece dice una cosa vera: <<questo `pre-commit` sta
diventando una ragione per dare `--no-verify`>>** — ed è il difetto che `A9` descrive,
### **arrivato dal lato del tempo.**

### 📌 **IL BUDGET E' DICHIARATO E NON SCELTO:** `120` secondi, ### **che è il valore che
questo repo ha già misurato come soglia** — i collaudi lenti *(la catena, il referto
dell'infrastruttura)* ### **lo superano, e per quello vivono SOLO nella CI.** ### **Non
l'ho tarato io: era già la riga di divisione fra `VELOCI` e `LENTI`.**

### ⚠ **E I TEMPI NON SONO UN NUMERO DEL REPO: sono una MISURA DI QUESTA MACCHINA.** Il
referto li stampa ### **con la piattaforma accanto**, perché ### **un tempo senza la
macchina che l'ha prodotto non si può confrontare con niente.**

### ⛔ **I DIECI CHE MANCAVANO, trovati il `2026-10-10` col censimento.** Dieci
collaudi giravano ### **nel `pre-commit` E in CI**, e ### **non stavano in `COLLAUDI`.**

### ⭐ **E conta perche- il guardiano USA QUESTO COMANDO per dire se il repo e-
verde:** su un clone pulito ha letto ### **`17` su `19`** e ha concluso che fallivano
### **DUE** collaudi -- mentre in CI era rosso ### **anche `P-MOD`**, che da qui
### **non si vedeva.** ### ⚠ **Un comando che si chiama <<LA SUITE COMPLETA>> e che
ne copre `19` su `29` e- un FALSO-UNO: il suo verde NON vuol dire che la CI e- verde.**

### ✅ **E aggiungerli ha trovato SUBITO altro rosso: `P-RIF`**, perche- la frase
che stai leggendo ### **l-avevo scritta in un COMMENTO** -- e un ID in un commento di
`primo_ordine/` e- esattamente cio- che `P-RIF` vieta. ### **Il presidio ha morso il
commit che lo rendeva visibile.**
"""
import io
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))

NL = chr(10)
PRESIDIO = "P-TEMPI"

# ### ⛔ **IL BUDGET, in secondi.** ### **Non e- scelto: e- la riga di divisione fra
# ### `VELOCI` e `LENTI` che `csv/_replay_registri.py` ha gia-** -- e quella nasce da una
# ### misura, non da un gusto.
BUDGET = 120.0

# ### ⚠ **I COLLAUDI, DICHIARATI UNO A UNO.** ### **Non si scoprono con un `glob`:**
# ### un `glob` prenderebbe ### **anche un file nuovo che nessuno ha ancora guardato**, e
# ### ### **un collaudo che nessuno ha deciso di far girare non e- una garanzia.**
#   `(nome, comando, dove)`  --  `dove`: `pre-commit` oppure `solo-CI`
COLLAUDI = (
    # ------------------------------------------------------------------ `primo_ordine/`
    ("il grafo valido", "primo_ordine/_collauda_grafo.py", "pre-commit"),
    ("il determinismo", "primo_ordine/_collauda_determinismo.py", "pre-commit"),
    ("le simmetrie e le conservazioni", "primo_ordine/_collauda_simmetrie.py",
     "pre-commit"),
    # ### ⚠ **Il collaudo e- uscito da `schema.py` il `2026-10-10`**, perche-
    # ### quel file era a `736` righe e ### **oltre il tetto SI DIVIDE.**
    ("lo schema della tabella", "primo_ordine/leggi/_collauda_schema.py",
     "pre-commit"),
    ("il generatore", "primo_ordine/_collauda_genera.py", "pre-commit"),
    ("lo schema della configurazione", "primo_ordine/config/schema_config.py",
     "pre-commit"),
    ("`@rif` byte-inerte", "primo_ordine/_rif.py", "pre-commit"),
    ("il modello di sigillo", "primo_ordine/sigilli/_modello.py", "pre-commit"),
    # ### ⭐ **E LA CATENA STA NEL `pre-commit`, PERCHE- L-HO MISURATA: `2.55` s.**
    # ### ⛔ **Era classificata LENTA** -- <<oltre i `120` secondi>> -- e
    # ### ### **quel numero era di un-altra cosa**: i lenti veri sono ### **i generatori
    # ### di referto** *(`45.99` e `28.33` s)*.
    # ### ⚠ **Questo e- il punto in cui un comando che STAMPA I TEMPI ha pagato: la
    # ### classificazione era asserita, non misurata.**
    ("la catena", "primo_ordine/_collauda_passo.py", "pre-commit"),
    # ### \u26d4 **E LA GUIDA SI ESEGUE**: nasce una legge di prova nella tabella VERA,
    # ### si genera, e si rimette tutto verificando lo ### **sha1.**
    ("la GUIDA, eseguita", "primo_ordine/_collauda_guida.py", "pre-commit"),
    # ### ⚠ **I LENTI VERI, e stanno SOLO in CI**: non perche- superino il budget da
    # ### soli, ma perche- ### **lo superano SOMMATI a tutto il resto.**
    # ### ⛔ **TOLTO il `2026-10-10`, e l-ha trovato IL MIO PRESIDIO su un clone
    # ### pulito:** `csv/_referto_seconda_parte.py` ### **GENERA UN REPERTO**, e farlo
    # ### girare qui ### **lo RIGENERAVA** -- gli toglieva la riga `CONGELATO` e poi
    # ### ### **il presidio della forma, che gira DOPO, lo vedeva mancare.**
    # ### ⭐ **Cioe-: il comando unico faceva <<ENTRAMBE>>**, la cosa che il mandato
    # ### di Luca VIETA, ### **e l-ho commessa io nello stesso giro in cui l-ho vietata.**
    # ### ✅ **E i collaudi che quel generatore chiamava sono TUTTI dichiarati qui
    # ### uno per uno** *(sono i dieci + i tre del censimento)*: ### **non si perde
    # ### copertura, si perde una RIGENERAZIONE.**
    ("il referto dell-infrastruttura (LENTO)", "csv/_referto_infrastruttura_era2.py",
     "solo-CI"),
    # ------------------------------------------------------------------ `csv/`
    ("la barriera dei hook", "csv/_barriera.py --collaudo", "pre-commit"),
    ("`P-ALB` l-albero delle scelte", "csv/_albero_era2.py --collaudo", "pre-commit"),
    ("`P-ID` un id che nasce", "csv/_id_nuovo.py --collaudo", "pre-commit"),
    ("`P-T2` il replay dei registri", "csv/_replay_registri.py --collaudo", "pre-commit"),
    ("l-arbitro fra le due vie", "csv/_registri_indice.py --collaudo", "pre-commit"),
    ("i presidi dell-indice", "csv/_presidio_indice.py --collaudo", "pre-commit"),
    ("`P-REG` le regole di gestione", "csv/_collauda_regole.py", "pre-commit"),
    # ------------------------------------------------- I DIECI CHE MANCAVANO
    # ### ⛔ **Perche- mancavano, e perche- conta: sta nel DOCSTRING del modulo** --
    # ### ### **e sta la- perche- un ID in un commento di `primo_ordine/` e- vietato**,
    # ### e il presidio dei riferimenti me lo ha detto ### **per la terza volta.**
    ("`P-E1`..`P-E5` i presidi dell-era 2", "csv/_presidi_era2.py --collaudo",
     "pre-commit"),
    ("`P-M1` il documento dei metodi", "csv/_metodi_era2.py --collaudo", "pre-commit"),
    ("`P-C1` i controlli nell-indice", "csv/_controlli_nell_indice.py --collaudo",
     "pre-commit"),
    ("`P-T1` il testo non si interpreta", "csv/_testo_e_metadati.py --collaudo",
     "pre-commit"),
    ("`P-R1` ogni ramo e- dichiarato", "csv/_rami_era2.py --collaudo", "pre-commit"),
    ("`P-T3` le citazioni strutturate", "csv/_citazioni_strutturate.py --collaudo",
     "pre-commit"),
    ("`P-RIF` un ID nel codice e- un costrutto", "csv/_rif_nel_codice.py --collaudo",
     "pre-commit"),
    ("`P-ES1` un solo esecutore", "csv/_un_solo_esecutore.py --collaudo", "pre-commit"),
    ("`P-MOD` la modularita-", "csv/_modularita_era2.py --collaudo", "pre-commit"),
    ("`P-AB` i confronti e i dati", "csv/_confronti_e_dati.py --collaudo", "pre-commit"),
    # ------------------------------------- E I TRE CHE IL CENSIMENTO HA TROVATO
    # ### ✅ **Questi non li ho messi a mano: li ha trovati `censimento()`**,
    # ### ### **e il nome non diceva che erano collaudi.** `_rinomina.py` lo e-
    # ### perche- ### **la lista del referto della seconda parte lo dichiara tale.**
    ("i presidi dell-indice, nei due versi", "csv/_collaudo_presidi_indice.py",
     "pre-commit"),
    ("i controlli della migrazione", "csv/_controlli_indice_v2.py", "pre-commit"),
    ("il rinominamento, sul piano", "csv/_rinomina.py", "pre-commit"),
    ("la FORMA dei testi generati", "csv/_forma_referti.py --collaudo",
     "pre-commit"),
    # ### ⚠ **`solo-CI` per il TEMPO, non per importanza:** i controlli sullo stage
    # ### costano `46.5` s, e nel `pre-commit` gira ### **il solo modo rapido.**
    ("i controlli sullo STAGE e non sul disco", "csv/_stage.py --collaudo", "solo-CI"),
    # ### ⛔ **LA PULIZIA DELLE TEMPORANEE** *(decisione di Luca, 2026-10-10)*: il
    # ### disco pieno l-hanno causato ### **11 cloni lasciati nel `%TEMP%`**, e
    # ### ### **24 cartelle che `rmtree` non riusciva a cancellare in silenzio.**
    # ### ✅ **Costa meno di un secondo**, quindi sta nel `pre-commit`.
    ("la pulizia delle temporanee", "csv/_pulizia.py --collaudo", "pre-commit"),
    # ### ⭐ **IL BANCO DELLA CAMMINATA** *(mandato di Luca, 2026-10-10)*: e-
    # ### ### **il primo codice di fisica dell-era 2**, e il suo collaudo porta
    # ### ### **il braccio 0** -- la simmetria di coniugazione di carica, AL BIT.
    # ### ⚠ **Sta nel `pre-commit` perche- costa pochi secondi**, e il
    # ### ### **determinismo fra due processi** e- la parte piu- lenta.
    ("il banco della camminata", "proto_camminata/_collauda_banco.py", "pre-commit"),
    # ### ⭐ **IL BANCO `v2`: SPIN LEGATO AL MOTO** *(decisione di Luca,
    # ### 2026-10-10)*. ### **Porta il braccio `0` in DUE PEZZI** -- `C` commuta al bit
    # ### nella scena identita-, e manda la camminata ### **nell-ANTI-camminata** quando
    # ### c-e- un campo `U(1)` -- e ### **DUE bracci che DEVONO fallire**: la fase pari, e
    # ### il gauge puro ### **coi versori non ruotati.**
    # ### ⚠ **Costa `0.90` s misurati**, quindi sta nel `pre-commit`.
    ("il banco della camminata v2", "proto_camminata/_collauda_banco2.py", "pre-commit"),
    # ### ⭐ **IL BANCO `v3`: IL VUOTO E LA SATURAZIONE** *(decisione di Luca,
    # ### 2026-10-11)*. ### **Il primo braccio e- la REGRESSIONE**: con la non linearita-
    # ### spenta il `v3` coincide ### **AL BIT** col `v2` -- cioe- ### **non lo invalida.**
    # ### ⚠ **Costa `0.93` s misurati.**
    ("il banco della camminata v3", "proto_camminata/_collauda_banco3.py", "pre-commit"),
    # ### ⚠ **E `csv/_verifica_clone.py` NON STA QUI, DI PROPOSITO:** fa un clone e
    # ### ### **ci fa girare QUESTA suite** -- metterlo fra i collaudi vorrebbe dire
    # ### ### **una ricorsione senza fondo.** Si lancia a mano, ed e- il punto 3 del
    # ### mandato.
)


# ### ⛔ **LE FONTI DEL CENSIMENTO: dove un collaudo PUO- girare senza stare qui.**
# ### ⚠ **IL DIFETTO che questo chiude, visto il `2026-10-10`:** la lista era
# ### ### **a mano**, e ### **DIECI collaudi giravano in CI e nel `pre-commit` senza
# ### esserci.** ### ⭐ **Aggiungerli non basta: la prossima volta ne mancherebbe un
# ### altro.** ### ✅ **Quindi il comando SI CONTA**, e ### **se manca qualcosa ESCE
# ### NON ZERO** -- il suo verde vuol dire ### **<<ho girato tutto cio- che gira>>**, non
# ### ### **<<ho girato la mia lista>>.**
FONTI = (".github/workflows/era2.yml", ".githooks/pre-commit",
         "csv/_referto_seconda_parte.py")


def _normale(s):
    """`python csv/x.py --collaudo` -> `csv/x.py --collaudo`, e via i prefissi del hook."""
    s = s.strip().strip('"')
    s = s.replace('"$(git rev-parse --show-toplevel)/', "").replace('"', "")
    s = s.replace("$R/", "")
    if s.startswith("python "):
        s = s[7:]
    pezzi = s.split()
    if not pezzi:
        return ""
    via = pezzi[0].replace(os.sep, "/")
    coda = " --collaudo" if "--collaudo" in pezzi else ""
    return via + coda


def _e_un_collaudo(via):
    """### Un collaudo si riconosce dal NOME o dal `--collaudo`, non a gusto."""
    b = os.path.basename(via.split()[0])
    return (via.endswith("--collaudo") or b.startswith("_collaud")
            or b.startswith("collaud") or "collaudo" in b
            or b.startswith("_controlli"))


def censimento():
    """### `[]` se ogni collaudo che gira altrove e- ### **dichiarato qui.**

    ### ⛔ **E le FONTI sono tre file del repo**, non una scansione cieca: il workflow
    della CI, il `pre-commit`, e ### **la lista `VELOCI`+`LENTI` del referto della seconda
    parte** -- che e- ### **essa stessa una dichiarazione di collaudi.**
    """
    import re
    dich = set()
    for _n, cmd, _d in COLLAUDI:
        dich.add(_normale(cmd))
    fuori, err = set(), []
    for rel in FONTI:
        p = os.path.join(RADICE, rel)
        if not os.path.exists(p):
            err.append("### la fonte del censimento `%s` NON ESISTE: il censimento "
                       "sarebbe un FALSO-UNO" % rel)
            continue
        testo = io.open(p, encoding="utf-8", errors="replace").read()
        # ### ⭐ **LA LISTA DEL REFERTO E- ESSA STESSA UNA DICHIARAZIONE:**
        # ### li- ogni comando ### **E-** un collaudo, anche se il nome non lo
        # ### dice *(`_rinomina.py`)*. ### **Nel workflow e nel hook, invece,
        # ### girano anche i GENERATORI**, e li- serve il riconoscimento dal
        # ### nome o dal `--collaudo`.
        tutto = rel.startswith("csv/_referto_")
        for m in re.finditer(r'python[^\n"\']*?((?:csv|primo_ordine)/[\w/]+\.py)'
                             r'((?:\s+--?[\w-]+)*)', testo):
            c = _normale("python " + m.group(1) + (m.group(2) or ""))
            if c and (tutto or _e_un_collaudo(c)):
                fuori.add(c)
    # ### ⚠ **IL RUNNER NON CENSISCE SE STESSO:** sarebbe una ricorsione, e
    # ### ### **un comando che si conta fra i propri collaudi direbbe sempre di esserci.**
    fuori.discard("primo_ordine/collauda.py")
    fuori.discard("primo_ordine/collauda.py --collaudo")
    # ### ⚠ **E IL FALSO POSITIVO VA TOLTO, non ammesso a mano:** nel workflow
    # ### molti strumenti girano DUE volte -- ### **la forma GENERATORE** *(senza
    # ### `--collaudo`, che SCRIVE)* e ### **la forma COLLAUDO**. ### **La prima
    # ### non e- un collaudo**, e se la seconda e- dichiarata ### **e- coperta.**
    manca = [c for c in sorted(fuori - dich)
             if (c + " --collaudo") not in dich]
    for c in manca:
        err.append("### `%s` GIRA (in CI, nel `pre-commit` o nel referto) e NON e- "
                   "dichiarato in `COLLAUDI`: il comando unico direbbe VERDE senza "
                   "averlo girato" % c)
    if not fuori:
        err.append("### IL CENSIMENTO NON HA TROVATO NESSUN COLLAUDO nelle fonti: "
                   "sarebbe un FALSO-ZERO, e il verde non vorrebbe dire niente")
    return err


def _sporchi():
    """### I file che `git` vede ### **cambiati adesso**, come insieme di percorsi."""
    r = subprocess.run(["git", "status", "--porcelain"], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    fuori = set()
    for riga in (r.stdout or "").split(NL):
        if len(riga) > 3:
            fuori.add(riga[3:].strip().strip('"'))
    return fuori


def gira(cmd):
    """### `(secondi, codice, uscita)`. ### **Il tempo lo misura `perf_counter`**, non `time`.

    ### \u26d4 **E L-USCITA SI TIENE** *(decisione di Luca, 2026-10-10)*: prima
    `capture_output=True` la prendeva e ### **nessuno la leggeva**, quindi un collaudo
    rosso diceva ### **soltanto <<codice 1>>.** ### \u26a0 **Cosi- un rosso d-AMBIENTE
    *(il disco pieno)* e un rosso da DIFETTO erano INDISTINGUIBILI**, e la diagnosi e-
    costata ### **tre corse da tre minuti.**
    """
    pezzi = cmd.split()
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable] + pezzi, cwd=RADICE, capture_output=True)
    uscita = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace")
    return time.perf_counter() - t0, r.returncode, uscita


def macchina():
    """La macchina, ### **perche- un tempo senza la macchina non si confronta.**"""
    import platform
    return "%s %s, python %s" % (platform.system(), platform.machine(),
                                 sys.version.split()[0])


def collaudo_censimento():
    """### I DUE VERSI del censimento. ### **Senza il verso che DEVE fallire, un
    censimento che non trova niente direbbe <<tutto a posto>>.**"""
    global COLLAUDI, FONTI
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL CENSIMENTO -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: il censimento TACE", censimento() == [],
          "%d collaudi dichiarati, %d fonti" % (len(COLLAUDI), len(FONTI)))
    # ### \u26d4 **IL VERSO CHE DEVE FALLIRE: si toglie un collaudo dalla lista**, e il
    # ### censimento ### **deve accorgersene.**
    salva = COLLAUDI
    try:
        COLLAUDI = tuple(x for x in salva
                         if "_modularita_era2.py" not in x[1])
        e = censimento()
        esito("### DEVE scattare: togliendo `P-MOD` dalla lista",
              any("_modularita_era2.py" in x for x in e),
              "### e- il difetto vero del 2026-10-10: DIECI collaudi giravano fuori")
        COLLAUDI = ()
        e2 = censimento()
        esito("### DEVE scattare: lista VUOTA, tutto risulta fuori",
              len(e2) >= 10, "%d mancanti: ### se fosse 0 il censimento sarebbe CIECO"
              % len(e2))
    finally:
        COLLAUDI = salva
    # ### \u26a0 **E IL FALSO-ZERO: se le FONTI non si leggono, il censimento tace per
    # ### VACUITA-** -- e un verde per vacuita- e- ### **peggio di un rosso.**
    sf = FONTI
    try:
        FONTI = ("csv/_non_esiste_proprio.py",)
        e3 = censimento()
        esito("### DEVE scattare: una FONTE che non esiste",
              any("NON ESISTE" in x for x in e3) and any("FALSO-ZERO" in x for x in e3),
              "### un censimento che non trova NIENTE non e- un censimento pulito")
    finally:
        FONTI = sf
    esito("NON deve scattare: rimesso tutto, il censimento TACE di nuovo",
          censimento() == [], "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DEL CENSIMENTO: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    # ### ⛔ **IL PRESIDIO DELL-ENCODING, e questa e- LA NONA VOLTA.** `CLAUDE.md`
    # ### par. `7` dice *<<ogni script di sigillo o di misura comincia con
    # ### `_presidio.avvia(__file__)`>>*, e dice anche ### **<<e- successo OTTO volte>>**.
    # ### ⚠ **Questo comando NON lo chiamava**, e si e- visto SOLO su un clone
    # ### pulito, quando il braccio dell-albero sporco ha provato a stampare un `⛔`:
    # ### ### **`UnicodeEncodeError`, codec `cp1252`.** ### ⭐ **Il presidio non
    # ### serviva finche- questo file stampava solo ASCII: il primo carattere non-ASCII
    # ### su un ramo che scatta L-HA FATTO CADERE.**
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo_censimento()
    solo_veloci = "--solo-veloci" in argv
    scelti = [x for x in COLLAUDI if not solo_veloci or x[2] == "pre-commit"]
    # ### \u26d4 **IL CENSIMENTO PRIMA DI TUTTO, e nel CODICE D-USCITA:** se un collaudo
    # ### gira altrove e non e- dichiarato qui, ### **questo comando NON PUO- dire
    # ### <<tutto verde>>** -- direbbe verde su cio- che non ha girato.
    fuori_lista = censimento()
    # ### \u26d4 **L-ALBERO PRIMA, perche- la suite deve lasciarlo COME L-HA TROVATO.**
    # ### \u26a0 **Richiesta di Luca, 2026-10-10:** *<<ogni collaudo deve lasciare
    # ### l-albero come l-ha trovato. Braccio: dopo la suite, `git status` VUOTO>>*.
    # ### \u2b50 **E un albero sporco dopo la suite NON e- un fastidio: e- una
    # ### DIAGNOSI** -- vuol dire che ### **un file generato COMMITTATO e- SCADUTO**, e
    # ### che il commit che l-ha cambiato ### **non ha portato il suo generato.**
    # ### \u2705 **Quindi si misura, si DICE QUALE, e si RIMETTE A POSTO** -- ma
    # ### ### **solo cio- che la suite ha sporcato LEI**, non cio- che era gia- sporco:
    # ### rimettere a posto il lavoro di qualcun altro sarebbe ### **peggio del
    # ### difetto.**
    _prima = _sporchi()
    print("=" * 100)
    print("TUTTI I COLLAUDI, CON I TEMPI   (punto 6)")
    print("=" * 100)
    print("  la macchina: %s" % macchina())
    print("  il budget del `pre-commit`: %.0f s   ### e oltre il budget e- un SEGNALE, "
          "non un rifiuto" % BUDGET)
    print()
    print("  %-38s %-10s %9s  %s" % ("il collaudo", "dove", "secondi", "esito"))
    print("  " + "-" * 94)
    tot = {"pre-commit": 0.0, "solo-CI": 0.0}
    rotti = []
    for nome, cmd, dove in scelti:
        s, rc, uscita = gira(cmd)
        tot[dove] += s
        if rc != 0:
            rotti.append((nome, cmd, rc, uscita))
        print("  %-38s %-10s %9.2f  %s"
              % (nome, dove, s, "ok" if rc == 0 else "### FALLISCE (codice %d)" % rc))
    print("  " + "-" * 94)
    print("  %-38s %-10s %9.2f" % ("IL TOTALE del `pre-commit`", "", tot["pre-commit"]))
    if not solo_veloci:
        print("  %-38s %-10s %9.2f" % ("piu- i LENTI, solo in CI", "", tot["solo-CI"]))
        print("  %-38s %-10s %9.2f" % ("IN TUTTO", "", sum(tot.values())))
    print()
    # ------------------------------------------------------------------ il VERDETTO
    if rotti:
        print("  ### %d COLLAUDI FALLISCONO:" % len(rotti))
        for nome, cmd, rc, uscita in rotti:
            print("     %-38s `%s` -> codice %d" % (nome, cmd, rc))
            # ### \u2705 **E SI STAMPA LA CODA DELLA SUA USCITA**, perche- ### **<<codice
            # ### 1>> non e- una diagnosi.** ### \u26a0 **Venti righe, non tutto:** un
            # ### collaudo che stampa 400 righe ### **seppellirebbe gli altri.**
            coda = [x for x in uscita.split(NL) if x.strip()][-20:]
            for riga in coda:
                print("        | %s" % riga[:160])
            if not coda:
                print("        | ### e NON HA SCRITTO NIENTE, che e- un difetto a se-")
    else:
        print("  ### TUTTI I COLLAUDI PASSANO: %d su %d" % (len(scelti), len(scelti)))
    if tot["pre-commit"] > BUDGET:
        print()
        print("  ### ⚠ SEGNALE: il `pre-commit` costa %.1f s, oltre il budget di "
              "%.0f s." % (tot["pre-commit"], BUDGET))
        print("  ### Non e- un rifiuto, ed e- una scelta: il tempo di una macchina NON E-")
        print("  ### una proprieta- del repo, e fermare su quello vorrebbe dire rifiutare")
        print("  ### un commit perche- il computer era occupato.")
        print("  ### MA UN `pre-commit` COSI- E- UNA RAGIONE PER DARE `--no-verify`, ed e-")
        print("  ### il difetto di `A9` arrivato dal lato del tempo: un presidio che si")
        print("  ### spegne perche- costa troppo NON E- UN PRESIDIO.")
    else:
        print("  ### il `pre-commit` sta nel budget: %.1f s su %.0f s (%.0f%%)"
              % (tot["pre-commit"], BUDGET, 100.0 * tot["pre-commit"] / BUDGET))
    print("=" * 100)
    _sporcati = sorted(_sporchi() - _prima)
    if _sporcati:
        print()
        print("  ### ⛔ LA SUITE HA SPORCATO %d FILE, e un collaudo deve lasciare "
              "l-albero come l-ha trovato:" % len(_sporcati))
        for f in _sporcati[:8]:
            print("     %s" % f)
        print("  ### Vuol dire che un file GENERATO e COMMITTATO e- SCADUTO: il commit")
        print("  ### che ha cambiato cio- che quel file racconta NON HA PORTATO IL SUO")
        print("  ### GENERATO. ### I byte si RIMETTONO A POSTO adesso, e il difetto RESTA")
        print("  ### SCRITTO QUI: rimetterli a posto in silenzio sarebbe nasconderlo.")
        for f in _sporcati:
            subprocess.run(["git", "checkout", "--", f], cwd=RADICE,
                           capture_output=True)
        print("  ### byte RIMESSI A POSTO: %d file" % len(_sporcati))
    if fuori_lista:
        print()
        print("  ### ⛔ IL CENSIMENTO TROVA %d COLLAUDI CHE GIRANO E NON SONO "
              "DICHIARATI:" % len(fuori_lista))
        for e in fuori_lista[:8]:
            print("     %s" % e)
        print("  ### Finche- sono fuori, IL VERDE DI QUESTO COMANDO NON VUOL DIRE CHE LA")
        print("  ### CI E- VERDE -- ed e- esattamente cio- che e- successo il 2026-10-10.")
    print("=" * 100)
    # ### ⛔ **IL CODICE D-USCITA GUARDA I COLLAUDI E IL CENSIMENTO, NON I TEMPI:**
    # ### il budget ### **segnala** e ### **non rifiuta**, ed e- scritto sopra.
    return 1 if (rotti or fuori_lista or _sporcati) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
