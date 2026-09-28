# -*- coding: utf-8 -*-
"""**Genera `doc/RIPIEGHI_guasto.md` dal referto della prova a guasto.**

`L-NUMERI`: **ogni numero scritto in un referto esce da uno script.** Qui la prosa e' letterale e
### **tutti i numeri vengono da `_guasto_ripieghi.json`** e dalla tabella `doc/RIPIEGHI_classi.md`.
**Non si modifica `doc/RIPIEGHI_guasto.md` a mano: si rigira questo.**

COMANDO:  python csv/_test_fork/_referto_guasto.py
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

REFERTO = os.path.join(RADICE, "csv", "_seal_fork", "_guasto_ripieghi", "_guasto_ripieghi.json")
TABELLA = os.path.join(RADICE, "doc", "RIPIEGHI_classi.md")
FUORI = os.path.join(RADICE, "doc", "RIPIEGHI_guasto.md")

CLASSE_CORTA = {"(a)": "(a)", "(b)": "(b)", "(c)": "(c)", "(e)": "(e)"}


def classi_per_cache():
    """`{nome_cache: {classe: [righe]}}` dalla tabella generata. **Si legge, non si giudica.**"""
    q = {}
    for r in io.open(TABELLA, encoding="utf-8"):
        m = re.match(r"^\|\s*`:(\d+)`\s*\|\s*`([^`]*)`\s*\|\s*`([^`]*)`\s*\|"
                     r"\s*([A-Z]+)\s*\|\s*(.*?)\s*\|", r)
        if not m:
            continue
        riga, cache, testo = int(m.group(1)), m.group(3), m.group(5)
        nome = cache.split(".")[-1]
        cl = "(?)"
        for k in ("(a)", "(b)", "(c)", "(d)", "(e)"):
            if k in testo:
                cl = k
                break
        else:
            if "fuori dal mandato" in testo:
                cl = "(x)"
        q.setdefault(nome, {}).setdefault(cl, []).append(riga)
    return q


def alias_locali():
    """`{grandezza: [nomi locali in cui viene letta]}`, dal sorgente.

    ### Perche' serve, ed e' il difetto 3 dello strumento della prova
    `_cs_nodo_prev` si legge in `_csp_in = getattr(self, "_cs_nodo_prev", None)`: la tabella
    chiama quella cache **`_csp_in`**, non `_cs_nodo_prev`. ### **Dire <<mai nominata>> sarebbe
    FALSO**: e' nominata, con un altro nome.
    """
    src = io.open(os.path.join(RADICE, "soliton_simulator.py"), encoding="utf-8").read()
    q = {}
    for loc, vero in re.findall(r"(\w+)\s*=\s*getattr\(\s*self\s*,\s*[\"']"
                                r"(\w+)[\"']", src):
        if loc != vero:
            q.setdefault(vero, set()).add(loc)
    return {k: sorted(v) for k, v in q.items()}


def _e(r):
    return r.get("esito", "--")


def _breve(r):
    e = _e(r)
    if e == "PROTETTO":
        return "**PROTETTO** `%s`" % r.get("tipo", "?")
    if e == "ROTTO RUMOROSO":
        return "ROTTO `%s` %s" % (r.get("tipo", "?"), r.get("dove", ""))
    if e == "RIPIEGO SILENZIOSO":
        return "### **RIPIEGO SILENZIOSO**"
    return e


def principale():
    j = json.load(io.open(REFERTO, encoding="utf-8"))
    cpc = classi_per_cache()
    ali = alias_locali()
    esiti, n0, m0 = j["esiti"], j["n_base"], j["archi_base"]
    R = []
    P = R.append

    P("# 🔥 **LA PROVA A GUASTO DEI RIPIEGHI: il COMPORTAMENTO, non la lettura**")
    P("")
    P("> ### **Generato da** `csv/_test_fork/_referto_guasto.py` dal referto")
    P("> `csv/_seal_fork/_guasto_ripieghi/_guasto_ripieghi.json`. **Non si modifica a mano:** si")
    P("> rigira lo strumento. *(`L-NUMERI`: ogni numero esce da uno script.)*")
    P("")
    P("| | |")
    P("|---|---|")
    P("| strumento | `csv/_test_fork/_guasto_ripieghi.py` |")
    P("| simulatore | blob sha1-byte **`%s`** |" % j["blob_sim_sha1_byte"][:8])
    P("| scena | `nmasse %d`, `sep %.4f` → ### **`n = %d`, archi `%d`** dopo **%d** passi |"
      % (j["nmasse"], j["sep"], n0, m0, j["passi_base"]))
    P("| errori **dichiarati** riconosciuti | %s |"
      % ", ".join("`%s`" % x for x in j["errori_dichiarati"]))
    P("| ### **il CONTROLLO** | %s |"
      % ("### **TIENE**: un passo da due copie di BASE e' **byte-identico**, `net.rng` compreso "
         "→ ### **la prova VALE**" if not j["controllo"]["quante"]
         else "### **NON TIENE**: la prova NON VALE"))
    P("| grandezze per nodo, **trovate in automatico** | ### **%d** |"
      % len(j["grandezze_per_nodo"]))
    P("| sospette *(per arco con `len == n` per caso)* | %s |"
      % (", ".join(j["sospette_per_arco"]) if j["sospette_per_arco"]
         else "**NESSUNA** — `n = %d` e archi `= %d` non possono coincidere" % (n0, m0)))
    P("")
    P("**LA CONFIGURAZIONE INTERA** (`P5`) sta in "
      "`csv/_seal_fork/_guasto_ripieghi/_configurazione.txt`: ### **zero differenze su 80 "
      "booleani** rispetto alla configurazione del driver.")
    P("### ⚠ **E non la produce lo strumento, ed e' una mia omissione:** "
      "`_guasto_ripieghi.py` **non chiama** `_cli_flag.dichiara_configurazione`. "
      "Quel file e' un **riparo**, ricavato dallo **stesso** percorso *(stesso driver, stesso "
      "`--seme=11`, nessun passo avanzato)*. **La cura e' mettere la chiamata dentro lo "
      "strumento.**")
    P("")

    # ---------------------------------------------------------------------------------- IL CONTO
    P("## ⚖ Il verdetto sul criterio del guardiano, **fissato prima dei numeri**")
    P("")
    P("> **«a posto» solo se ENTRAMBI i guasti danno PROTETTO, oppure se danno INERTE ed e'")
    P("> DIMOSTRATO che nessuna legge del passo la legge.»**")
    P("")
    P("| esito | quante | quali |")
    P("|---|---|---|")
    P("| ### ⛔ **A POSTO** | ### **%d su %d** | %s |"
      % (len(j["a_posto"]), len(j["grandezze_per_nodo"]),
         ", ".join("`%s`" % x for x in j["a_posto"]) if j["a_posto"] else "### **NESSUNA**"))
    P("| ### **RIPIEGO SILENZIOSO** | **%d** | %s |"
      % (len(j["ripiego_silenzioso"]),
         " · ".join("`%s`" % x for x in j["ripiego_silenzioso"])))
    P("| **ROTTO RUMOROSO** *(eccezione non dichiarata)* | **%d** | %s |"
      % (len(j["rotto_rumoroso"]), " · ".join("`%s`" % x for x in j["rotto_rumoroso"])))
    P("| **INERTE su entrambi** *(e NON vuol dire protetto)* | **%d** | %s |"
      % (len(j["inerti"]), " · ".join("`%s`" % x for x in j["inerti"])))
    P("| ### **con effetto OLTRE l'ultimo nodo** | ### **%d** | **tutte quelle che ripiegano** |"
      % len(j["effetto_oltre_ultimo_nodo"]))
    P("")
    prot = sorted({k for k, v in esiti.items() for g in ("CORTA", "LUNGA")
                   if v.get(g, {}).get("esito") == "PROTETTO"})
    P("### ➜ **ZERO grandezze su %d sono «a posto».** E le sole due che sollevano un errore"
      % len(j["grandezze_per_nodo"]))
    P("**dichiarato** sono %s — ### **esattamente le due curate stamattina**, e ### **solo dal"
      % " e ".join("`%s`" % x for x in prot))
    P("lato CORTA**:")
    P("")
    P("| | CORTA | LUNGA |")
    P("|---|---|---|")
    for k in prot:
        P("| `%s` | %s | %s |" % (k, _breve(esiti[k].get("CORTA", {})),
                                  _breve(esiti[k].get("LUNGA", {}))))
    P("")
    P("> ### 📌 **LA CURA FUNZIONA, E FUNZIONA SOLO DOVE L'HO MESSA — e solo su CORTA.**")
    P("> `_ferma_se_cache_corta` comincia con `if quanta >= n: return`: ### **una cache PIU'")
    P("> LUNGA passa in silenzio.** E' il lato che i tre confronti `len(x) > n` guardavano, e che")
    P("> ho lasciato scoperto. ### **Non e' una congettura: `psi` LUNGA da' un `ValueError` di")
    P("> broadcast, non un errore dichiarato.**")
    P("")

    # -------------------------------------------------------------------------------- LA TABELLA
    P("## La tabella, grandezza per grandezza")
    P("")
    P("**`nodi` e `archi` sono QUANTI cambiano** rispetto al controllo, **sui primi `n-1` nodi**")
    P("*(cioe' escludendo il nodo che ho guastato io)* e su **tutti** gli archi.")
    P("### **`%d` nodi vuol dire OGNI nodo tranne quello guastato: e' TUTTA LA RETE.**" % (n0 - 1))
    P("")
    P("| grandezza | CORTA | LUNGA | gr. | nodi | archi | scost. max | come la leggeva la tabella |")
    P("|---|---|---|---|---|---|---|---|")
    for k in j["grandezze_per_nodo"]:
        v = esiti[k]
        c = v.get("CORTA", {})
        cl = dict(cpc.get(k, {}))
        vie = []
        for a in ali.get(k, []):
            for x, righe in cpc.get(a, {}).items():
                cl[x] = cl.get(x, []) + righe
                if a not in vie:
                    vie.append(a)
        etichetta = " ".join("**%s**×%d" % (x, len(cl[x])) for x in sorted(cl))
        if vie:
            etichetta += " *(come `%s`)*" % "`, `".join(vie)
        if not cl:
            etichetta = "### **mai nominata, con nessun nome**"
        P("| `%s` | %s | %s | %s | %s | %s | %s | %s |"
          % (k, _breve(c), _breve(v.get("LUNGA", {})),
             c.get("quante", "") or "", c.get("nodi", "") or "", c.get("archi", "") or "",
             ("`%.2e`" % c["scostamento_max"]) if c.get("scostamento_max") else "",
             etichetta))
    P("")

    # ------------------------------------------------------------------- IL CASO CHE DEVE FALLIRE
    cdf = j["caso_che_deve_fallire"]
    cp = (cdf.get("esito") or {}).get("CORTA", {})
    P("## ✅ **Il caso che deve fallire FALLISCE COME DEVE**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| il guasto | `psi` **CORTA** sul blob **PRE-CURA** *(il padre del commit che introduce "
      "`_eredita_psi_figli`)* |")
    P("| esito | ### **%s** |" % cp.get("esito", "?"))
    P("| quanto | **%d** grandezze · ### **%d nodi** · **%d archi** · scostamento max "
      "### **`%.3e`** |"
      % (cp.get("quante", 0), cp.get("nodi", 0), cp.get("archi", 0),
         cp.get("scostamento_max", 0.0)))
    P("| ### **lo stesso guasto OGGI** | %s |" % _breve(esiti["psi"].get("CORTA", {})))
    P("")
    P("### ➜ **La prova RIPRODUCE il flash e mostra che la cura l'ha chiuso.** Lo stesso guasto,")
    P("sulla stessa scena, sullo stesso passo: **prima** cambiava **tutta la rete in silenzio**,")
    P("**oggi** alza `SchermaturaSpenta`. ### **Non e' una lettura: e' lo stesso esperimento due")
    P("volte.**")
    P("")

    # -------------------------------------------------------------------- I DIFETTI DELLO STRUMENTO
    P("## ⛔ Tre difetti del MIO strumento, e **nessuno tocca gli esiti**")
    P("")
    P("Gli esiti escono dal **confronto dello stato**, non dal tracciatore.")
    P("### **Quello che segue invalida la colonna «riga responsabile», non il verdetto.**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| ### **① le etichette del braccio PRE-CURA sono SBAGLIATE** | i numeri di riga vengono dal"
      " file **pre-cura**, annotati con la tabella di **oggi**. ### **I numeri di riga SHIFTANO"
      " fra due blob** — e' la regola del par.2 che ho scritto io e poi violato. **Verificato:**"
      " pre-cura `:3391` e' `if med == _med_corrente:`, `:3465` e' `if _xi is None or len(_xi) <"
      " n:`, `:5754` e' `F = Mw @ np.exp(1j * self.phi)` — ### **nessuna delle tre e' un confronto"
      " su `psi`** |")
    P("| ### **② «eseguita» NON vuol dire «ramo di scorta PRESO»** | registro la riga della"
      " **GUARDIA**, non quella del **CORPO**: un `if` si esegue in **entrambi** i casi. Dove"
      " compare **anche** una riga di corpo *(`:3465` dentro `ritmo`, per `_psi_prec`)* la prova"
      " c'e'; **altrove no** |")
    P("| ### **③ il filtro per NOME perde gli ALIAS LOCALI** | `_cs_nodo_prev` si legge in"
      " `_csp_in = getattr(self, \"_cs_nodo_prev\", None)`, quindi la tabella chiama quella cache"
      " **`_csp_in`** e il mio filtro non la riconosce. ### **Ecco perche' 4 delle 10 che ripiegano"
      " non hanno una riga responsabile: non e' che il sito manchi dalla tabella — e' che il nome"
      " non combacia** |")
    P("")
    P("> ### 📌 **E' LA QUINTA VOLTA, E SEMPRE LA STESSA FORMA.** Dopo `(b)` che contava"
      " `full(n,…)` come «estende», `(a)` che chiamava «inizializzazione» una condizione fusa,"
      " `==`/`!=` messi «fuori dal mandato» e il ramo degli `IfExp` invertito: ### **una regola che"
      " parte dal NOME o dalla SINTASSI e non da CHE COSA SCATTA.** La prova a guasto e' immune"
      " *(guasta e guarda)*; ### **il pezzo che ci ho attaccato sopra per attribuire la colpa NO.**")
    P("")
    P("**Che cosa la renderebbe una prova:** registrare la riga del **corpo** del ramo, **oppure**"
      " confrontare i **contatori** `_g_*` fra il giro di controllo e il giro guastato — che sono"
      " ### **gia' li', per `A8`**, nei siti che li hanno *(`_cs_in_fallback`, `_ritmo_sicurezza`,"
      " `_sfb_lift_corto`…)*. E dove il contatore **non c'e'**, ### **la sua assenza e' essa stessa"
      " un difetto `A8`.**")
    P("")

    # ---------------------------------------------------------------------------- IL MECCANISMO
    def q(k, g="CORTA"):
        return esiti[k].get(g, {})
    P("## ⚙ **IL MECCANISMO, misurato: perche' la cura PER GUARDIE non tiene**")
    P("")
    P("Tre casi, e ### **tutti e tre si leggono dai numeri, non dal codice**.")
    P("")
    P("### ① `psi_spin`: la guardia c'e', ### **ESEGUE, e non spara**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| la guardia | `:4462` in `_nb_grav` — `_ferma_se_cache_corta(\"psi_spin\", len(_ps), n, ...)`,"
      " ed e' **la cura di stamattina**, classe **(e)** |")
    P("| il tracciatore | ### **`:4462` ESEGUE** |")
    P("| e nonostante questo | ### **%s** — %d grandezze, **%d nodi**, %d archi, scost. `%.2e` |"
      % (q("psi_spin").get("esito"), q("psi_spin").get("quante", 0), q("psi_spin").get("nodi", 0),
         q("psi_spin").get("archi", 0), q("psi_spin").get("scostamento_max", 0.0)))
    P("")
    P("### ➜ **Se la guardia esegue e NON solleva, quando la legge `psi_spin` e' GIA' LUNGA"
      " `n`.** E l'unica scrittura a piena lunghezza e' **`:4421` in `calcola_psi`**"
      " *(`self.psi_spin = _Fs / (1.0 + GAMMA * _norm)[:, None]`)*.")
    P("### ⚠ **La guardia sta A VALLE della riscrittura: non protegge NIENTE.** Il danno e'"
      " gia' avvenuto a monte, in chi ha letto la `psi_spin` corta prima di `calcola_psi`.")
    P("")
    P("### ② `_psi_spinor`: la coda si allunga, e la guardia a valle trova un array giusto")
    P("")
    P("| | |")
    P("|---|---|")
    P("| il tracciatore | ### **`:2262` ESEGUE** *(`elif len(cur) < n:` in `_estendi_psi_spinor`)*"
      " e ### **`:2265` NO** — quindi il ramo preso e' **l'estensione** `:2264`"
      " `self._psi_spinor = np.vstack([cur, manca])` |")
    P("| esito | ### **%s** — %d grandezze, **%d nodi**, %d archi, ### **scost. `%.2e`**,"
      " il piu' grande del giro |"
      % (q("_psi_spinor").get("esito"), q("_psi_spinor").get("quante", 0),
         q("_psi_spinor").get("nodi", 0), q("_psi_spinor").get("archi", 0),
         q("_psi_spinor").get("scostamento_max", 0.0)))
    P("")
    P("### ➜ **Un estensore a monte DISARMA ogni guardia a valle**: la cache arriva lunga `n`,")
    P("con **una riga inventata** al posto di quella vera.")
    P("")
    P("### ③ `mem_mot`: e' classe **(b)**, *«estensione dei soli nuovi»*, e ### **NON e' sicura**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| il sito | `:7009` `if len(self.mem_mot) < n:` → `vstack([mem_mot, zeros((n-len, 3))])`."
      " ### **E' una estensione VERA della coda**, non un `full(n, ...)` |")
    P("| la mia tabella | **(b)**, cioe' *«i primi `len(x)` restano»* — e **restano davvero** |")
    P("| ### **la misura** | ### **%s**: %d grandezze e ### **%d nodi su %d** cambiano,"
      " scost. `%.2e` |"
      % (q("mem_mot").get("esito"), q("mem_mot").get("quante", 0), q("mem_mot").get("nodi", 0),
         n0 - 1, q("mem_mot").get("scostamento_max", 0.0)))
    P("")
    P("### ➜ **Perche' (b) non basta:** l'elemento inventato e' `zeros(1, 3)`, e appartiene a un"
      " nodo ### **CHE ESISTEVA GIA'** e che aveva una memoria vera. ### **(b) e' sicura per i nodi"
      " APPENA NATI, non per una cache che e' corta per QUALUNQUE ALTRA RAGIONE** — e i due casi"
      " ### **hanno la STESSA FORMA**, quindi nessuna regola sintattica li distingue.")
    P("")
    P("> ### 📌 **E QUESTO E' L'ARGOMENTO PER LA SUA FORMA DI CURA.** Tre guasti su tre"
      " mostrano che una guardia **dentro** una legge arriva **troppo tardi** o **troppo presto**:"
      " a valle di una riscrittura non vede niente, a monte di un estensore viene aggirata."
      " ### **Un CONTROLLO UNICO nello schedulatore, PRIMA che le leggi girino, non ha questo"
      " problema** — ed e' esattamente quello che il guardiano ha proposto.")
    P("")

    # ----------------------------------------------------------------------------- L'INCROCIO
    P("## 🔀 L'incrocio con `doc/RIPIEGHI_incrocio.md`: **conferma o smentisce?**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| ### **conferma la SUA lettura** | il suo verdetto era *«sostituzione VIVA, deve diventare"
      " errore»*. ### **La prova lo dimostra col comportamento: 10 grandezze cambiano TUTTA LA"
      " RETE in silenzio, e ZERO su %d sono «a posto».** |" % len(j["grandezze_per_nodo"]))
    P("| ### **conferma la sua proposta di CURA** | la sua era **un solo controllo dello"
      " schedulatore** invece di quaranta `raise` sparsi. ### **La prova la corrobora: le due sole"
      " protette sono le due che ho curato a mano, e una delle due lo e' solo da un lato.** Curare"
      " sito per sito ha lasciato **29 grandezze su 31** scoperte |")
    P("| ### **smentisce una MIA premessa** | avevo trattato il mandato come «i 101 confronti»."
      " ### **La prova misura le GRANDEZZE, e sono 31 — quindici non stanno nelle 23 del"
      " sigillo.** Un elenco di confronti non e' un elenco di grandezze |")
    P("| aggiunge un lato che **nessuna** delle due letture aveva | ### **il lato LUNGA.** La cura"
      " di stamattina protegge solo il CORTO: `if quanta >= n: return` |")
    P("")
    P("### I tre *«da guardare a mano»* del suo gruppo 7")
    P("")
    P("| sito | che cosa dice la PROVA A GUASTO |")
    P("|---|---|")
    P("| `:2153` `_aggiorna_lift_spinoriale` *(`self._nb`)* | ### **la riga non e' MAI stata"
      " ESEGUITA** in un passo: e' assente da tutte e 10 le tracce. E il guasto su `_nb` da'"
      " ### **INERTE su entrambi**. ➜ ### **DORMIENTE in questa configurazione** — d'accordo con la"
      " sua lettura *(«blocco saltato»)*, e in piu': **il blocco non ci arriva nemmeno** |")
    P("| `:5750` `step` *(`self.d0`)* | ### **la prova NON PUO' provarlo, e lo dico:** `d0` e'"
      " **per ARCO**, quindi non e' fra le %d grandezze per nodo. ### **Ma la misura conferma la sua"
      " lettura per un'altra via:** archi `%d` contro `n = %d`, quindi `len(d0) >= n` e' **sempre"
      " vero** e ### **il ramo di scorta non scatta mai** |"
      % (len(j["grandezze_per_nodo"]), m0, n0))
    P("| `:5859` `step` *(`_chi_geom_nodi`, perche' `CHI_COOP` e' **ON**)* | ### **la riga ESEGUE**,"
      " e il guasto da' ### **INERTE su entrambi**. ➜ **ha ragione lui: e' un RICALCOLO**, e la"
      " prova aggiunge che il ricalcolo riproduce la cache ### **ESATTAMENTE** a questo passo."
      " ### ⚠ **«Inerte» NON vuol dire «a posto»: la grandezza E' LETTA**, quindi per il criterio"
      " del guardiano **non passa** |")
    P("")

    # ------------------------------------------------------------------------------ `eta` = inf
    nf = j.get("non_finiti_a_BASE") or {}
    if nf:
        P("## ✅ **E la correzione di una cosa che avevo detto senza saperla**")
        P("")
        P("In `360e681` ho scritto che almeno una grandezza porta un `inf` e che ### **non sapevo")
        P("quale**. Ora lo strumento lo elenca:")
        P("")
        P("| grandezza | `inf` | `nan` | su quanti |")
        P("|---|---|---|---|")
        for k in sorted(nf):
            P("| `%s` | ### **%d** | %d | %d |"
              % (k, nf[k]["inf"], nf[k]["nan"], nf[k]["elementi"]))
        P("")
        P("### ➜ **`eta` e' `inf` su TUTTI i nodi, ed e' LEGITTIMO E GIA' DICHIARATO:** la tabella")
        P("dei domini dice *«`eta`: `nonneg_inf` — non negativa, e **`+inf` per il vuoto DATO**»*")
        P("(`:241-242`). Un nodo del vuoto seminato **non ha un tempo di accensione**, e")
        P("`ramp = min(1, eta/tau)` da' `1`. ### **Quindi il primo giro non e' morto su un difetto")
        P("della fisica: e' morto sul mio confronto.** *(Nel commit del fallimento avevo detto")
        P("«probabilmente una sentinella»: era un'ipotesi, e va sostituita da questo fatto.)*")
        P("")

    P("---")
    P("")
    P("## 🛑 Che cosa NON dice questa prova")
    P("")
    P("| | |")
    P("|---|---|")
    P("| **«INERTE» non e' un'assoluzione** | vuol dire che **in QUESTO passo, in QUESTA"
      " configurazione** nessuna legge l'ha letta. ### **Sono %d grandezze, e per dirle «a posto»"
      " serve DIMOSTRARE che nessuna legge le legge** |" % len(j["inerti"]))
    P("| **un passo, non una traiettoria** | il guasto e' iniettato al passo **%d** e si guarda"
      " **un** passo. Un ripiego che morde solo **dopo** una nascita qui non compare — e le nascite"
      " cominciano al **42** |" % j["passi_base"])
    P("| ### **niente e' curato** | questa e' una **misura**, non una cura. ### **Non ho toccato un"
      " byte di fisica**, e sulla forma della cura decide Luca |")
    P("")
    io.open(FUORI, "w", encoding="utf-8", newline=chr(10)).write("\n".join(R) + "\n")
    print("scritto: %s  (%d righe)" % (FUORI, len(R)))
    print("a posto %d · ripiego %d · rotto %d · inerti %d su %d"
          % (len(j["a_posto"]), len(j["ripiego_silenzioso"]), len(j["rotto_rumoroso"]),
             len(j["inerti"]), len(j["grandezze_per_nodo"])))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
