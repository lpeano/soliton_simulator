# -*- coding: utf-8 -*-
"""**IL CONTRATTO DELL'ORDINE NELLA NASCITA — generato, non ricopiato** *(`L-NUMERI`)*.

**Passo 2 del `COMMIT 3` del riordino.** Il piano *(`doc/PIANO_riordino_mitosi.md`, parte (c))*
chiede che ### **l'ordine delle estrazioni e delle somme diventi PARTE DEL CONTRATTO, scritto
nella tabella delle regole di nascita.** Questo script ce lo scrive, ### **leggendolo dal referto
della misura** e non da una mia trascrizione.

## CHE COSA FA, in due cose

| | |
|---|---|
| **1** | aggiunge a `doc/REGOLE_nascita.tsv` una colonna ### **`ordine_pezzi`**, e per ogni riga ci mette ### **l'ordine dei pezzi della concatenazione MISURATA**, abbinata ### **PER ANCORA** |
| **2** | scrive `doc/CONTRATTO_nascita.md` con la parte ### **GLOBALE** del contratto: la **sequenza delle estrazioni**, la misura ### **IEEE-754**, e le **riduzioni** |

## ✅ **PERCHE' L'ABBINAMENTO E' PER ANCORA, e qui e' legittimo**

La misura da' `(funzione, grandezza, testo_della_riga)`; la tabella da' `(grandezza, evento,
ancora)`. ### **La funzione `mitosi` copre DUE eventi** *(divisione e Schwinger)*, quindi
`(funzione, grandezza)` **non basta** a scegliere la riga.
### ➜ **L'ANCORA invece e' un pezzo di TESTO della riga giusta**, ed e' ### **gia' verificata per
testo** da `_referto_ordine.py`. ### **Qui il testo E' la chiave dichiarata**, non una comodita':
e' la stessa ragione per cui l'ancora esiste.
### ⚠ **E se l'abbinamento non e' UNICO si DICHIARA, non si indovina:** `0` ancore trovate o
`>= 2` finiscono in una colonna che dice ### **esattamente quante**, e lo script ### **stampa il
conto** invece di scegliere.

## ⛔ **CIO' CHE QUESTO SCRIPT NON FA**

* ### **non tocca le prime SETTE colonne** della tabella, e lo **ASSERISCE**: `_referto_ordine.py`
  le legge per indice *(`c[0]`..`c[6]`)*, e cambiarle romperebbe un lettore;
* ### **non inventa un ordine:** se una riga non ha una concatenazione misurata, la colonna dice
  **perche'** — *(`(nessuna concatenazione nel perimetro misurato)`)*;
* ### **non decide se il commit 3 passera' il byte-identico:** scrive **l'ordine da rispettare.**

COMANDO:  python csv/_contratto_nascita.py [--prova]
ASCII puro nel codice.
"""
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
sys.path.insert(0, _QUI)
import _presidio  # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
TAB = chr(9)
REGOLE = os.path.join(RADICE, "doc", "REGOLE_nascita.tsv")
MISURA = os.path.join(RADICE, "csv", "_test_fork", "_ordine_estrazioni",
                      "_ordine_estrazioni.json")
FUORI = os.path.join(RADICE, "doc", "CONTRATTO_nascita.md")
COL7 = 7


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def principale():
    prova = "--prova" in sys.argv[1:]
    d = json.load(io.open(MISURA, encoding="utf-8"))
    if not d.get("vale"):
        raise SystemExit("** il referto della misura dice `vale: false`. NON scrivo un contratto "
                         "su una misura che non vale. **")
    conc = d["contratto_concatenazioni"]
    righe = io.open(REGOLE, encoding="utf-8").read().split(NL)
    testa = righe[0].split(TAB)
    if len(testa) < COL7:
        raise SystemExit("** la tabella ha %d colonne, attese almeno %d **" % (len(testa), COL7))
    gia = "ordine_pezzi" in testa
    fuori = []
    conti = {"uniche": 0, "zero": 0, "molte": 0}
    nuove = [TAB.join(testa[:COL7] + ["ordine_pezzi"])]
    for r in righe[1:]:
        if not r.strip():
            continue
        c = r.split(TAB)
        if len(c) < COL7:
            nuove.append(r)
            continue
        anc = c[4]
        # ⚠ L'ABBINAMENTO E' PER ANCORA, e il testo E' la chiave dichiarata (vedi il docstring).
        cand = [x for x in conc if anc and anc in x["testo"]]
        if len(cand) == 1:
            x = cand[0]
            val = "%s := %s" % (x["forma"], " | ".join(x["addendi_in_ordine"]))
            conti["uniche"] += 1
        elif not cand:
            val = "(nessuna concatenazione nel perimetro misurato)"
            conti["zero"] += 1
        else:
            val = "(ANCORA NON UNIVOCA: %d concatenazioni la contengono -- righe %s)" % (
                len(cand), ",".join(str(y["riga_oggi"]) for y in cand))
            conti["molte"] += 1
        nuove.append(TAB.join(c[:COL7] + [val]))
        fuori.append((c[0], c[2], val))

    # ### IL CONTROLLO CHE IMPEDISCE: le prime SETTE colonne non devono cambiare di un carattere.
    vecchie = [x for x in righe if x.strip()]
    if len(vecchie) != len(nuove):
        raise SystemExit("** righe %d -> %d: NON scrivo. **" % (len(vecchie), len(nuove)))
    for a, b in zip(vecchie[1:], nuove[1:]):
        if a.split(TAB)[:COL7] != b.split(TAB)[:COL7]:
            raise SystemExit("** le prime %d colonne sono cambiate su una riga. NON scrivo. **"
                             % COL7)

    print("=" * 100)
    print("IL CONTRATTO DELL'ORDINE NELLA NASCITA -- generato dal referto, non ricopiato")
    print("=" * 100)
    print("  referto della misura ... %s  (blob sim %s, strumento %s)"
          % (os.path.relpath(MISURA, RADICE).replace(chr(92), "/"),
             d["blob_sim_sha1_byte"][:8], d["blob_strumento"][:8]))
    print("  la tabella aveva gia' la colonna `ordine_pezzi`? %s" % ("SI" if gia else "NO"))
    print("  righe della tabella ....... %d" % (len(nuove) - 1))
    print("  abbinate per ANCORA, una sola concatenazione ... %d" % conti["uniche"])
    print("  senza concatenazione nel perimetro misurato .... %d" % conti["zero"])
    print("  ### con ANCORA NON UNIVOCA (dichiarate, non scelte) %d" % conti["molte"])
    print("")

    sq_s = d["sequenza_passo_senza_nascite"]
    sq_c = d["sequenza_passo_con_nascite"]
    ie = d["controllo_ieee754"]
    tutte = d["tutte_le_somme_del_perimetro"]
    doc = []

    def P(s=""):
        doc.append(s)

    P("# IL CONTRATTO DELL'ORDINE NELLA NASCITA")
    P("")
    P("> ### **GENERATO da `csv/_contratto_nascita.py` dal referto della misura. NON si modifica "
      "a mano** *(`L-NUMERI`)*.")
    P("> **Passo 2 del `COMMIT 3` del riordino** *(`doc/PIANO_riordino_mitosi.md`, parte (c))*.")
    P("> **Il referto:** `csv/_test_fork/_ordine_estrazioni/_ordine_estrazioni.json` "
      "*(strumento `%s`, simulatore `%s`)*." % (d["blob_strumento"][:8],
                                               d["blob_sim_sha1_byte"][:8]))
    P("")
    P("**Perche' esiste:** il piano dichiara il rischio -- *spostare le scritture della nascita in "
      "un punto solo puo' cambiare l'ORDINE DELLE ESTRAZIONI e delle SOMME, e il generatore e' "
      "UNO: chi pesca prima cambia cio' che pescano tutti*. ### **Questo documento dice qual e' "
      "l'ordine da RISPETTARE**; non dice che il commit 3 lo rispettera'.")
    P("")
    P("---")
    P("")
    P("## 1. LA SEQUENZA DELLE ESTRAZIONI, per PASSO -- e questa e' la parte stretta del contratto")
    P("")
    P("*(scena grande, seme %d, dal passo %d al %d; la VOCE si ricava dalla composizione IN USO, "
      "non dal nome cablato.)*" % (d["seme"], d["da"], d["fino"]))
    P("")
    P("### Un passo SENZA nascite -- **%d estrazioni** *(passo %s)*"
      % (len(sq_s or []), d["passo_senza_nascite"]))
    P("")
    P("| # | voce | metodo | elementi |")
    P("|--:|---|---|--:|")
    for k, x in enumerate(sq_s or [], 1):
        P("| %d | `%s` | `rng.%s` | %d |" % (k, x[0], x[1], x[2]))
    P("")
    P("### Un passo CON nascite -- **%d estrazioni** *(passo %s)*"
      % (len(sq_c or []), d["passo_con_nascite"]))
    P("")
    P("| # | voce | metodo | elementi | che cos'e' |")
    P("|--:|---|---|--:|---|")
    for k, x in enumerate(sq_c or [], 1):
        nota = ""
        if x[0] == "mitosi" and k == 3:
            nota = ("### **la DECISIONE** (`decidi_divisione`: `rng.random(len(avv))`), e pesca "
                    "**a OGNI passo**, anche quando non nasce niente -- gli elementi sono "
                    "**tutti gli archi**")
        elif x[0] == "mitosi" and k == 4:
            nota = ("### **lo SCHWINGER** (`estratto = rng.random(len(sel))`), e c'e' **solo nei "
                    "passi con nascite**: gli elementi sono gli archi SELEZIONATI")
        P("| %d | `%s` | `rng.%s` | %d | %s |" % (k, x[0], x[1], x[2], nota))
    P("")
    P("### ⚠ **E UN RAMO CHE NON PESCA, dichiarato perche' la sua ASSENZA e' parte del "
      "contratto**")
    P("`ANTIFASE_ADD` pescherebbe (`flip = rng.random(len(sel))`) ed e' ### **spento nella "
      "configurazione di riferimento**: nella finestra misurata ### **quell'estrazione non "
      "compare.** ### ➜ **Se un giorno si accendesse, la sequenza avrebbe CINQUE estrazioni e "
      "questo contratto non la coprirebbe.**")
    P("")
    P("## 2. LE ESTRAZIONI FUORI DAL PASSO -- **%d**, e si contano a parte"
      % d["fuori_dal_passo"]["estrazioni"])
    P("")
    P("| dove | metodo | chiamate | elementi |")
    P("|---|---|--:|--:|")
    for q in d["fuori_dal_passo"]["per_voce_e_metodo"]:
        P("| %s | `rng.%s` | %d | %d |" % (q["voce"], q["metodo"], q["chiamate"], q["elementi"]))
    P("")
    P("## 3. L'ORDINE DEGLI ADDENDI -- e la misura RESTRINGE il contratto invece di allargarlo")
    P("")
    P("| la proprieta' | misurata |")
    P("|---|---|")
    P("| `a + b` contro `b + a` *(DUE addendi)* | ### **byte-identici: %s** ⇒ l'ordine "
      "**NON** conta" % ie["due_addendi_commutativi"])
    P("| `(a+b)+c` contro `a+(b+c)` *(TRE addendi)* | ### **identici: %s** -- differenze "
      "### **%d su 200000** ⇒ l'ordine **CONTA**" % (ie["tre_addendi_associativi"],
                                                         ie["differenze_su_200000"]))
    P("")
    P("### ➜ **Quindi l'ordine degli addendi entra nel contratto DA TRE IN SU.** E nel "
      "perimetro della nascita:")
    P("")
    P("| | |")
    P("|---|--:|")
    P("| somme `+` nelle 5 funzioni, ### **qualunque bersaglio, LOCALI COMPRESE** | **%d** |"
      % tutte["totale"])
    for k in sorted(tutte["per_numero_di_addendi"], key=lambda z: int(z)):
        P("| con **%s** addendi | %d |" % (k, tutte["per_numero_di_addendi"][k]))
    P("| ### **con TRE o piu'** | ### **%d** |" % len(tutte["con_tre_o_piu"]))
    P("")
    if not tutte["con_tre_o_piu"]:
        P("### ✅ **ZERO con tre o piu' addendi, e questo CHIUDE un buco del mio strumento "
          "invece di nasconderlo:** il classificatore parte dalle scritture di `self.<nome>`, "
          "quindi ### **perde le somme che passano da una LOCALE** *(`pos_figlio = 0.5 * "
          "(pos[a] + pos[b])`)*. ### ➜ **Ma se NESSUNA somma del perimetro ha tre addendi, "
          "una somma persa in una locale NON PUO' CAMBIARE IL VERDETTO.** Il limite si chiude con "
          "una misura, non con una promessa.")
    else:
        P("### ⛔ **CI SONO somme con tre o piu' addendi: il loro ordine E' nel contratto.**")
        for q in tutte["con_tre_o_piu"]:
            P("* `%s` :%d -- %d addendi: `%s`" % (q["funzione"], q["riga_oggi"], q["quanti"],
                                                  q["testo"]))
    P("")
    P("## 4. LE RIDUZIONI -- **%d**, e li' l'associativita' morde davvero"
      % len(d["riduzioni_ordine_dipendenti"]))
    P("")
    P("### ⚠ **NON sono solo `np.add.at` e `np.bincount`** *(rilievo del guardiano, "
      "2026-10-02)*: ### **una `.mean()` in virgola mobile lo e' anche**, e la prima stesura del "
      "rilevatore ### **la perdeva.** Sono **accumulazioni su molti termini**, non somme scritte.")
    P("")
    P("| riga | funzione | scrive | forma | gate |")
    P("|--:|---|---|---|---|")
    for q in d["riduzioni_ordine_dipendenti"]:
        P("| `:%d` | `%s` | %s | `%s` | %s |"
          % (q["riga_oggi"], q["funzione"],
             ("### **`%s`**" % q["scrive"]) if (q["scrive"] and not
                                               q["scrive"].startswith("(locale)"))
             else ("*%s*" % q["scrive"] if q["scrive"] else "-"),
             q["forma"], (" AND ".join("`%s`" % x for x in q["gate"]) if q["gate"] else "-")))
    P("")
    P("### **I FLAG dei gate, dal RUNTIME:** %s"
      % "  ·  ".join("`%s = %r`" % (k, v)
                         for k, v in d["flag_dei_gate_dal_runtime"].items()))
    P("")
    cr = d["controllo_riduzioni"]
    P("### ✅ **QUALI riduzioni dipendano dall'ordine e' MISURATO, non dichiarato a parole**")
    P("")
    P("| | |")
    P("|---|---|")
    P("| MEDIA in virgola mobile | ### **dipende dall'ordine da `n = %s` IN SU** -- "
      "`%d` vettori DIVERSI per taglia: %s |"
      % (cr.get("soglia_misurata"), cr.get("giri_per_taglia", 0),
         ", ".join("`n=%s`: %d" % (k, cr["media_float_per_taglia"][k])
                   for k in sorted(cr["media_float_per_taglia"], key=lambda z: int(z)))))
    P("| MEDIA di **BOOLEANI** | **%d** su %d ⇒ ### **ESATTA**, l'ordine non conta "
      "*(e' il caso di `flip.mean()`)* |" % (cr["media_booleani"], cr.get("giri_per_taglia", 0)))
    P("| **MEDIANA** | **%d** su %d ⇒ l'ordine **non conta** |"
      % (cr["mediana_float"], cr.get("giri_per_taglia", 0)))
    P("| `norm(axis=1)` **per riga** | permutando le **RIGHE**, la norma di una riga cambia "
      "**%d** volte su 50 ⇒ l'ordine delle righe **non entra** |"
      % cr.get("norm_per_riga_cambia_permutando_le_righe", -1))
    P("")
    P("### ⛔ **E LA SOGLIA `n = %s` COINCIDE con la misura IEEE-754 del par. 3** *(due "
      "addendi commutativi al bit, TRE no)*: ### **le due misure si confermano a vicenda.**"
      % cr.get("soglia_misurata"))
    P("### ⚠ **E una versione precedente di questo referto diceva «inerte fino a 4, "
      "ordine-dipendente da ~8»: era un FALSO ZERO** -- usava **UN SOLO vettore per taglia**, "
      "e per `n = 3` e `n = 4` quel vettore dava `0` **per caso**. ### **La riga vecchia resta nel "
      "repo** *(par.8)*, e questa e' la correzione.")
    P("")
    vp = d.get("verdetto_ultima_prob_coppia", {})
    P("### ⭐ **LA REGOLA DEL CONTRATTO SU `ultima_prob_coppia`, DERIVATA dai numeri**")
    P("")
    P("> ### **`ultima_prob_coppia` e' inerte all'ordine SOLO SE `len(sel) <= %s`; da `%s` in su "
      "DIPENDE dall'ordine degli archi.**"
      % ((cr.get("soglia_misurata") or 0) - 1, cr.get("soglia_misurata")))
    P("")
    P("| | |")
    P("|---|---|")
    P("| la soglia **misurata** | `n = %s` |" % cr.get("soglia_misurata"))
    P("| le taglie **vere** di `len(sel)` nella finestra | %s |"
      % (", ".join("`%s`" % x for x in vp.get("taglie_len_sel", [])) or "*(nessun evento)*"))
    P("| ### **l'esito** | ### **%s** |" % vp.get("esito", "NON DETERMINABILE"))
    P("")
    if vp.get("esito", "").startswith("INERTE"):
        P("### ⚠ **E NON E' INERTE PER LEGGE: lo e' perche' la scena divide POCO.** Il "
          "margine e' di ### **pochi archi**: ### **un passo con `%s` divisioni la renderebbe "
          "ordine-dipendente SENZA che nessuna legge sia cambiata.** ### **E' la forma che `A8` "
          "chiama pericolosa:** *un'inerzia che dipende da un numero di oggi non e' un'inerzia, e' "
          "una coincidenza che vale finche' dura.*" % cr.get("soglia_misurata"))
    P("")
    P("## 4-bis. ⛔ **E IL SIGILLO NON CONFRONTA TRE DI QUESTE GRANDEZZE**")
    P("")
    P("La regola del braccio `B` *(letta da `csv/_seal_fork/_sig_controllo_unico.py`, "
      "`_contatori`)* confronta ### **DUE insiemi**: le grandezze di `REGISTRO_NOMI`, e i "
      "**contatori** = ogni attributo che ### **comincia con `_` ED E' UN INTERO.**")
    P("")
    P("| grandezza | nel registro? | contatore? | tipo a runtime | ### **confrontata?** |")
    P("|---|---|---|---|---|")
    for g, q in sorted(d.get("riduzioni_il_sigillo_le_confronta", {}).items()):
        P("| `%s` | %s | %s | `%s` | %s |"
          % (g, q["nel_registro"], q["contatore"], q["tipo_runtime"],
             "SI" if q["confrontata"] else "### **NO**"))
    P("")
    P("### ➜ **Quindi un cambio d'ordine su queste tre NON farebbe cadere il sigillo: ci "
      "passerebbe accanto IN SILENZIO.** ### **E' `A8` applicato al sigillo.**")
    P("### ⚠ **E `_g_peqn_mediana` e' il caso peggiore:** porta il prefisso `_g_` dei "
      "contatori, ### **quindi un lettore la crede coperta**, e non lo e' perche' e' un `float`.")
    P("### ✅ **REQUISITO PER IL SIGILLO DEL COMMIT 3, scritto QUI e PRIMA:** deve "
      "confrontare ### **anche queste tre**, non solo il registro e i contatori interi.")
    P("")
    P("## 5. L'ORDINE DEI PEZZI DI OGNI CONCATENAZIONE -- **%d**, e sta nella TABELLA"
      % len(conc))
    P("")
    P("### **Per una CONCATENAZIONE l'ordine conta SEMPRE e per qualunque tipo**, perche' decide "
      "### **quale valore va a quale INDICE**: non e' l'ultimo bit, e' il **significato**. "
      "*(Permutare `concatenate([i[keep], a, m])` non sposta un bit: cambia quali nodi sono "
      "collegati.)*")
    P("")
    P("### ➜ **Riga per riga, l'ordine sta nella colonna `ordine_pezzi` di "
      "`doc/REGOLE_nascita.tsv`**, abbinato ### **PER ANCORA** *(la funzione `mitosi` copre DUE "
      "eventi, quindi `(funzione, grandezza)` non basta a scegliere la riga)*.")
    P("")
    P("| | |")
    P("|---|--:|")
    P("| righe della tabella | **%d** |" % (len(nuove) - 1))
    P("| abbinate a UNA concatenazione | **%d** |" % conti["uniche"])
    P("| senza concatenazione nel perimetro misurato | %d |" % conti["zero"])
    P("| ### con ancora NON UNIVOCA *(dichiarate, non scelte)* | ### **%d** |" % conti["molte"])
    P("")
    P("### ⚠ **E le %d senza concatenazione NON sono un buco:** sono le regole il cui valore "
      "nasce da una **scrittura diversa** *(una `np.full`, una mutazione in posto, una regola di "
      "`phi` che passa da una locale)*. ### **La colonna lo DICE invece di lasciare un campo "
      "vuoto**, perche' un campo vuoto si legge come *«non misurato»*."
      % conti["zero"])
    P("")
    P("---")
    P("")
    P("## ⛔ CHE COSA QUESTO CONTRATTO **NON** DICE")
    P("")
    P("| | |")
    P("|---|---|")
    P("| **non dice che il commit 3 lo rispettera'** | dice ### **qual e' l'ordine.** La verifica "
      "e' il **sigillo**, e il criterio e' **byte-identico fino al 72, contatori compresi** |")
    P("| ### **non copre un'altra CONFIGURAZIONE** | la sequenza delle estrazioni dipende dai "
      "flag: `ANTIFASE_ADD` spento, `COPPIA_MIT = 1.0`, `MITOSI_DIR = 0.0`, `REGIME` "
      "deterministico. ### **Con altri flag l'ordine cambia, e questo documento NON vale** |")
    P("| ### **non copre le riduzioni del ramo spento** | `MITOSI_DIR = 0.0`: le due `add.at` "
      "non girano, e ### **il contratto di oggi non le descrive** |")
    P("")

    if prova:
        print("--prova: NON scrivo niente. Le prime righe del documento:")
        for x in doc[:14]:
            print("    " + x)
        return 0
    io.open(REGOLE, "w", encoding="utf-8", newline=NL).write(NL.join(nuove) + NL)
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(doc).rstrip(NL) + NL)
    print("  SCRITTI: doc/REGOLE_nascita.tsv (colonna `ordine_pezzi`) e doc/CONTRATTO_nascita.md")
    print("  blob tabella: %s   blob contratto: %s" % (blob(REGOLE)[:8], blob(FUORI)[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
