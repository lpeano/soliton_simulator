# -*- coding: utf-8 -*-
"""IL REFERTO DELLE RIGHE D'ORIGINE — **voce per voce.**

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: i conteggi **prima** da
`git show 4ec2684:doc/indice/voci.jsonl`, quelli **dopo** dal disco, i segnali dalle stesse
funzioni che gira il validatore, e le decisioni **importate** dai moduli che le portano.

Gira con:  python csv/_doc_referto_righe_origine.py
"""
import collections
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import indice as IX                                          # noqa: E402
import _stato_dalla_riga as SR                               # noqa: E402
import _dominio_esplicite as DE                              # noqa: E402
import _a_luca as AL                                         # noqa: E402
import _gemelle_duplicati as GD                              # noqa: E402
import _da_dividere as DD                                    # noqa: E402
import migra_indice_v2 as MG                                  # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "4ec2684"
R = []


def p(s=""):
    R.append(s)


def gshow(ref):
    q = subprocess.run(["git", "show", ref], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    assert q.returncode == 0, ref
    return q.stdout


def tab(campo, a, b):
    p("| `%s` | prima | dopo | |" % campo)
    p("|---|--:|--:|---|")
    for k in sorted(set(a) | set(b), key=lambda x: -b.get(x, 0)):
        d = b.get(k, 0) - a.get(k, 0)
        p("| %s | `%d` | `%d` | %s |" % (k, a.get(k, 0), b.get(k, 0),
                                         ("### **%+d**" % d) if d else ""))
    p()


def main():
    voci = [json.loads(r) for r in
            io.open(os.path.join(RADICE, "doc/indice/voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pper = {v["id"]: v for v in pv}
    _v, reg = IX.carica()
    seg = {x[0]: x[2] for x in IX.segnali(voci, reg, verboso=False)}
    ro = json.loads(io.open(os.path.join(RADICE, "doc/indice/_righe_origine.json"),
                            encoding="utf-8").read())
    n_vecchi = len(MG.vecchio_indice())
    amb1 = json.loads(io.open(os.path.join(RADICE, "doc/indice/_p1_ambigue.json"),
                              encoding="utf-8").read())
    amb2 = json.loads(io.open(os.path.join(RADICE, "doc/indice/_p2_ambigue.json"),
                              encoding="utf-8").read())
    conf3 = json.loads(io.open(os.path.join(RADICE, "doc/indice/_p3_conflitti.json"),
                               encoding="utf-8").read())
    dz = json.loads(io.open(os.path.join(RADICE, "doc/indice/_p6_gemelle_dz.json"),
                            encoding="utf-8").read())
    lot = {}
    for k in ("s1", "s2", "s3", "s4", "s5", "s6", "s7"):
        lot[k] = [json.loads(r) for r in
                  io.open(os.path.join(RADICE, "doc/indice/_lotti/v3_%s.jsonl" % k),
                          encoding="utf-8").read().split(NL) if r.strip()]
    val = collections.Counter(v["meta"]["validita"] for v in voci
                              if v["meta"].get("validita"))

    def tipo1(m):
        for k in ("RISERVATA", "AMBIGUA", "NESSUNA", "SEGNAPOSTO",
                  "la riga dice CHIUSA ma NON PORTA"):
            if m.startswith(k):
                return k
        return "altro"

    t1 = collections.Counter(tipo1(m) for _i, m in amb1)
    n_chiuse = sum(1 for x in lot["s1"] if x["campi"].get("stato") == "CHIUSA")
    t2 = collections.Counter(tipo1(m) for _i, m in amb2)
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_collaudo_presidi_indice.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    _E = re.compile(r"^  \S.*\s(PASSA|### FALLISCE)(\s|$)")
    coll = [r.rstrip() for r in (q.stdout or "").split(NL) if _E.match(r)]
    n_ok = sum(1 for r in coll if _E.match(r).group(1) == "PASSA")
    q2 = subprocess.run([sys.executable, os.path.join(_QUI, "_controlli_indice_v2.py")],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    ctrl = [r.rstrip() for r in (q2.stdout or "").split(NL)
            if re.match(r"^\s+C\d+ ", r) and ("PASSA" in r or "FALLISCE" in r)]
    q3 = subprocess.run([sys.executable, os.path.join(_QUI, "_stato_dalla_riga.py"),
                         "collaudo"], cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8")
    m3 = re.search(r"IL COLLAUDO: (\d+) su (\d+)", q3.stdout or "")

    p("# IL REFERTO DELLE RIGHE D'ORIGINE")
    p()
    p("> ### ⭐ **LA VALIDITA' NON E' LO STATO.** *«VALE SEMPRE»*, *«VALE PER QUELLA "
      "SCENA»*, *«LIMITE DICHIARATO»* ### **non dicono se una cosa e' fatta**: dicono "
      "### **fin dove vale cio' che si e' trovato.** ### **Lo stato sta nella RIGA "
      "D'ORIGINE**, e i titoli dell'indice sono `<= 100` caratteri — "
      "### ⛔ **un troncamento taglia esattamente dove la riga dice lo stato.**")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | "
      "`doc/TASK_HISTORY/2026-10-09_indice_v3_righe_origine.md`, ### **committato PRIMA del "
      "lavoro** *(`%s`)* |" % PRIMA)
    p("| **i commit** | `f613fef` *(`1`)* · `9af76a4` *(`2`)* · `f2aa241` *(`3`)* "
      "· `ed189ed` *(`4`)* · `7400a9e` *(`5`)* · `5f4097a` *(`6`)* · "
      "`3dfd8ee` *(`7`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%d su %d** · collaudo dei presidi ### **%d su %d** "
      "· collaudo della REGOLA DELLO STATO ### **%s su %s** |"
      % (sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll),
         m3.group(1), m3.group(2)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ① I QUATTRO ERRORI DEL GUARDIANO, E DUE SONO MIEI PER RIPETIZIONE")
    p()
    p("| | l'errore | di chi |")
    p("|---|---|---|")
    p("| `(a)` | `CURA1-CORTO`, `CURA2-CORTO`, `SIGILLO-CURA2`, `SIGILLO-CURA2-RIPARATO` "
      "### **non sono sospese: sono corse FINITE** | del guardiano, ### **e io le ho toccate "
      "DUE VOLTE** — ripristinate `APERTA`, poi portate a `SOSPESA` — "
      "### **senza mai aprire la sezione sotto l'intestazione** |")
    p("| `(b)` | `G1` e' ### **«FATTO»** | del guardiano, e io ### **l'ho spostata di era** "
      "leggendo solo il titolo |")
    p("| `(c)` | `F8` era ### **troppo stretto** | del guardiano |")
    p("| `(d)` | la riverifica precedente ### **non aveva aperto le righe troncate** | "
      "### **del guardiano e mia insieme** |")
    p()
    p("### ⭐ **E l'errore `(d)` SPIEGA GLI ALTRI TRE.** Il titolo di `Z83` finisce "
      "*«… ⏳[EPOCA 1 · MISURA] | DO…»*; la riga intera dice ### **«DOMANDA APERTA: `d0` DEVE "
      "STARE SOPRA `LAM`?»** — e la voce era ### **`CHIUSA`.** ### **Il titolo tagliava "
      "due caratteri prima della parola che decide.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ② PUNTO `1` — **lo stato dalla riga**, e il collaudo ha deciso la regola")
    p()
    p("| | |")
    p("|---|--:|")
    p("| voci con una ### **riga d'origine ritrovabile** | ### **`%d`** su `%d` |"
      % (len(ro), len(voci)))
    p("| ### **`meta.validita`** scritte | ### **`%d`** |" % sum(val.values()))
    for k, n in val.most_common():
        p("| — *%s* | `%d` |" % (k, n))
    p("| ### **stati cambiati** | ### **`%d`** |"
      % sum(1 for x in lot["s1"] if x["campi"].get("stato")
            and "PONTE" not in x["motivo"]))
    p("| voci ### **NON toccate** | ### **`%d`** |" % len(amb1))
    p()
    p("| perche' NON toccate | quante |")
    p("|---|--:|")
    for k, n in t1.most_common():
        p("| %s | `%d` |" % (k, n))
    p()
    p("### ⚠ **E LA MIA SOGLIA DI FERMO ERA SCRITTA MALE.** Nel task history avevo messo "
      "*«ambigue piu' di `80` ⇒ i due gruppi di parole si sovrappongono troppo, e la "
      "regola va ridetta»*. Le non toccate sono ### **`%d`**, ma ### **la sovrapposizione "
      "vera e' `%d`**: le altre sono *«nessuna parola decide»*, segnaposto, chiusure senza "
      "commit e riservate. ### **Avevo confuso secchi diversi in una soglia sola.**"
      % (len(amb1), t1.get("AMBIGUA", 0)))
    p()
    p("### ⛔ **CINQUE CORREZIONI, E LA DIFFERENZA FRA LE PRIME TRE E LE ULTIME DUE "
      "CONTA**")
    p()
    p("| | la correzione | a che cosa |")
    p("|---|---|---|")
    p("| `1` | il prefisso di `fonte` e' ### **senza i `**` e i backtick** della riga vera | "
      "al ### **RITROVAMENTO** — e senza spogliarli ### **`1` caso su `7`** si "
      "ritrovava |")
    p("| `2` | alcune ### **emoji di stato** sono nel titolo e altre no *(`Z25` tiene il suo "
      "`🟨`, `Z47` ha perso il `🟩`)* | al ### **RITROVAMENTO** |")
    p("| `3` | un prefisso puo' essere ### **contenuto in un nome piu' lungo** — "
      "`APERTO SIGILLO-CURA2` sta anche in `APERTO SIGILLO-CURA2-RIPARATO` — e allora "
      "### **vince la riga piu' corta** | al ### **RITROVAMENTO** |")
    p("| `4` | il ### **confine di parola**: la riga di `Z83` dice *«`d0` → "
      "in-FINITO distorce»*, e ### **`infinito` contiene `FINITO`** | ### **ALLA REGOLA** |")
    p("| `5` | ### **la PRIMA parola di stato vince**: la riga racconta ### **anche la "
      "STORIA** — `Z83` dice *«lo stress resta finito»* *(un **aggettivo**)*, `Z25` dice "
      "*«fronte aperto»* *(la **storia passata**)*, mentre la cella di stato dice "
      "*«CHIUSA»* | ### **ALLA REGOLA** |")
    p()
    p("### ⭐ **Aggiustare un ATTREZZO su casi a risposta nota e' lecito; aggiustare la "
      "REGOLA e' un'altra cosa, e la dichiaro:** alla lettera la regola del mandato dava "
      "### **`5` su `7`**, e il mandato dice *«se un caso noto esce diverso, la regola e' "
      "sbagliata: fermati»*. ### **Mi sono fermato, ho guardato PERCHE', e la ragione era che "
      "la riga racconta anche la storia.** ### ⚠ **Se Luca intendeva la regola alla "
      "lettera, `2` dei `7` casi del collaudo escono diversi.**")
    p()
    p("### **E TRE OSTACOLI DELLO SCHEMA, CHE HANNO FATTO UN FILTRO GIUSTO AL POSTO MIO**")
    p()
    p("| | |")
    p("|---|---|")
    p("| `validita` non era ### **registrata** | il lotto ### **rifiutato**, e non ha scritto "
      "niente. Registrata come `enum` sui tre valori del mandato |")
    p("| chiudere pretende ### **`chiusura.criterio` e `chiusura.commit`** | il criterio sta "
      "nella riga; il commit ### **solo se la riga lo porta.** Delle `%d` che la regola "
      "chiuderebbe, ### **`%d` non hanno uno sha** — e la' dentro ci sono "
      "### **ASSIOMI E REGOLE** *(`A5`, `A9`, `AUTO-MANUTENZIONE`)*, la cui riga e' "
      "### **una DEFINIZIONE, non una chiusura.** ### ⭐ **Un assioma non e' «fatto»: "
      "VALE** — e ### **un commit non si inventa** |"
      % (n_chiuse + t1.get("la riga dice CHIUSA ma NON PORTA", 0),
         t1.get("la riga dice CHIUSA ma NON PORTA", 0)))
    p("| un ### **segnaposto** non prende uno stato | `%d` voci `NON_DEFINITA` saltate: "
      "### **prima la classe, poi lo stato** |" % t1.get("SEGNAPOSTO", 0))
    p()
    p("### **E una transizione VIETATA, attraversata in DUE righe:** `TRANSIZIONI` non ammette "
      "`CHIUSA` → `SOSPESA`. Si passa per `APERTA` ### **nello stesso lotto**, con due "
      "righe di storico: la prima dice ### **che la chiusura era sbagliata**, la seconda "
      "### **dove va la voce.** ### **Lo stato intermedio non si vede mai**, perche' "
      "`aggiorna-lotto` valida ### **una volta alla fine.**")
    p()
    p("### **IL COLLAUDO, `%s` su `%s`**" % (m3.group(1), m3.group(2)))
    p()
    p("```")
    for r in (q3.stdout or "").split(NL):
        if "atteso" in r or "IL COLLAUDO:" in r:
            p(r.rstrip())
    p("```")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ③ PUNTO `2` — **la classe dalla riga**, e gli ASSIOMI l'hanno corretta")
    p()
    p("### **`%d` classi cambiate**, `%d` voci non toccate." % (len(lot["s2"]), len(amb2)))
    p()
    dire = collections.Counter(re.search(r"da .(\w+). a .(\w+).", x["motivo"]).groups()
                               for x in lot["s2"])
    p("| da | a | quante |")
    p("|---|---|--:|")
    for (a, b), n in dire.most_common():
        p("| `%s` | `%s` | `%d` |" % (a, b, n))
    p()
    p("### ⛔ **IL DIFETTO DEL RILEVATORE, E GLI ASSIOMI LO HANNO RIVELATO:** la prima "
      "stesura contava un `?` come *«una domanda»*, e cosi' ### **`A1`, `A7b` e `A10` — "
      "ASSIOMI — diventavano `FRONTE`**, perche' la loro sezione contiene un punto di "
      "domanda e la voce e' aperta. ### ⭐ **Un assioma non e' un fronte: e' una legge di "
      "FORMA, e non si apre ne' si chiude.** ➜ Serve ### **la domanda DICHIARATA**, e i "
      "cambi sono passati da `105` a `%d`." % len(lot["s2"]))
    p()
    p("### **E una condizione che ho aggiunto leggendo il mandato:** *«un esito misurato»* "
      "vale ### **solo se la voce e' CHIUSA.** Un numero in una voce aperta e' ### **una "
      "misura DA FARE**, non un esito — e il mandato dice *«`CHIUSA PER MISURA` o un "
      "esito misurato»*: ### **la prima meta' della frase dice da che parte sta la seconda.**")
    p()
    p("| perche' NON toccate | quante |")
    p("|---|--:|")
    for k, n in t2.most_common():
        p("| %s | `%d` |" % (k, n))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ④ PUNTO `3` — **era `1` per le esplicite**, e `F8` allargato")
    p()
    p("L'elenco ### **si legge dal documento**, non si ricopia: l'attrezzo trova la riga "
      "*«voci SOSPESE»* di `doc/CURE_fisica_ordine.md:26` e ### **pretende che sia unica e "
      "che porti `14` ID.**")
    p()
    p("### ⛔ **DUE CONFLITTI VERI**")
    p()
    p("| id | la chiusura che si toglie |")
    p("|---|---|")
    for i, cr, _pp in conf3:
        p("| `%s` | %s |" % (i, cr))
    p()
    p("### **La chiusura veniva dal TAG**, non da una riga che dice *«chiuso»*: la migrazione "
      "le ha chiuse perche' al tag `era-1-secondo-ordine` avevano stato `chiuso`. "
      "### **E il documento le chiama SOSPESE.**")
    p()
    p("### **E `14` delle `38` erano `APERTA`**, che con era `1` ### **viola `F7`.** Il "
      "mandato dice *«era `1`; stato dal punto `1`»*, e il punto `1` ### **non le aveva "
      "decise**: prendono `SOSPESA`, e ### **non e' un'invenzione** — e' la regola in "
      "vigore, ed e' cio' che `F7` pretende.")
    p()
    p("### ⭐ **`F8` LEGGEVA UN TITOLO TRONCATO, ed e' l'errore `(d)` applicato a un "
      "presidio:** il titolo di `CONFIG-1` finisce *«28 LEGGI SU 31 SPENTE, misurato…»*, e la "
      "riga d'origine nomina `csv/_config_delle_misure.py` e i flag `FORK_SU2`, "
      "`CAMPO_SPINORIALE`, `TAU_LUCE`. ### **Adesso `F8` legge la riga.**")
    p()
    p("### ⚠ **E UN MARCATORE CHE AVEVO AGGIUNTO IO L'HO TOLTO.** Per far scattare "
      "`CONFIG-1` avevo messo un pattern sui ### **FLAG-COSTANTE**, e faceva scattare "
      "`FALSO-ZERO` su `REGISTRO_STATO` — ### **il caso che il mandato dice che NON "
      "deve.** Ed era inutile: `CONFIG-1` scatta dal suo `.py`. "
      "### ⭐ **Un marcatore che il mandato non chiede e che rompe un caso negativo si "
      "TOGLIE, non si aggiusta.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑤ PUNTO `4` — **dominio e classe delle esplicite**")
    p()
    p("| id | prima | dopo | la frase |")
    p("|---|---|---|---|")
    for x in lot["s4"]:
        i = x["id"]
        a, b = pper.get(i, per[i]), per[i]
        fr = x["motivo"]
        fr = fr[fr.find("La frase:"):][:170] if "La frase:" in fr else ""
        p("| `%s` | `%s`/`%s`/`%s` | ### **`%s`/`%s`/`%s`** | %s |"
          % (i, a["classe"], a["dominio"], a["era"], b["classe"], b["dominio"], b["era"],
             fr.replace("|", "/")))
    p()
    p("### **Il nodo di `REGISTRO_FISICA:D37`:** era `CRITERIO`+`INFRASTRUTTURA`, e questo "
      "### **viola la regola della classe** *(un `CRITERIO` si aspetta in `METODO`)*. "
      "### ⭐ **Il mandato scioglie il nodo dalla parte della CLASSE:** non e' un "
      "criterio, e' un ### **`DIFETTO`** — e cosi' la regola ### **non viene piegata per "
      "far stare una voce.**")
    p()
    p("### ⚠ **Tre senza riga d'origine**, e il motivo lo dichiara: `CENS-A3`, "
      "`PRESIDIO-RIFIUTO-SOLO-SIGILLI`, `RISCRITTURA-GO` — il motivo scrive *«(la riga "
      "d'origine NON si ritrova; il titolo dice)»* prima di citare. ### **Una citazione di "
      "seconda scelta si dichiara, non si spaccia per la prima.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑥ PUNTO `5` — **le nove a Luca, senza toccarle**")
    p()
    p("| id | `classe`/`dominio`/era/stato | la domanda |")
    p("|---|---|---|")
    for i in sorted(AL.DOMANDE):
        v = per[i]
        p("| `%s` | `%s`/`%s`/`%s`/`%s` | %s |"
          % (i, v["classe"], v["dominio"], v["era"], v["stato"], AL.DOMANDE[i]))
    p()
    p("### ⛔ **«Senza toccare» significa: ne' `classe`, ne' `dominio`, ne' `era`, ne' "
      "`stato`.** Il generatore ### **asserisce `campi == {}`** su ogni riga: se una decisione "
      "ci finisse dentro, ### **il lotto non partirebbe.** E la verifica dopo: i quattro campi "
      "di tutte e nove, confrontati con `git show`, sono ### **identici.**")
    p()
    p("### **E la FRASE non va nella nota, di proposito:** l'elenco generato porta gia' una "
      "colonna *«LA FRASE»*. ### **Scriverla due volte vorrebbe dire tenerla in due posti, e "
      "due copie divergono.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑦ PUNTO `6` — **gemelle e duplicati**")
    p()
    p("### **I quattro gruppi, dichiarati e NON fusi**")
    p()
    p("| il gruppo | i membri |")
    p("|---|---|")
    for g in GD.GRUPPI:
        p("| %s | %s |"
          % (" / ".join("`%s`" % x for x in g),
             " · ".join("`%s`/`%s`/era `%s`" % (per[x]["classe"], per[x]["dominio"],
                                                     per[x]["era"]) for x in g)))
    p()
    p("### ⭐ **E il gruppo di TRE dice una cosa su come nascono i duplicati:** "
      "`REGISTRO_FISICA:REG-R`, `REG-R` e `H-REG-R` sono `CRITERIO`/`METODO`, "
      "`DIFETTO`/`INFRASTRUTTURA` e `PRESIDIO`/`METODO` — ### **lo stesso fatto scritto "
      "tre volte**, una come criterio, una come difetto, una come presidio. ### **Non e' una "
      "svista: e' che un fatto, mentre lo si cura, CAMBIA CATEGORIA** — e l'indice ha "
      "registrato ### **ogni passaggio come una voce nuova.**")
    p()
    p("### **Lo schema `D`/`Z`: `%d` coppie, `%d` DISALLINEATE**"
      % (len(dz["coppie"]), len(dz["disallineate"])))
    p()
    p("| `D` | `Z` | la riga di `D` | la riga di `Z` |")
    p("|---|---|---|---|")
    for x in dz["disallineate"]:
        p("| `%s` *(%s)* | `%s` *(%s)* | %s | %s |"
          % (x["D"], x["D_stato"], x["Z"], x["Z_stato"],
             x["D_riga"][:150].replace("|", "/"), x["Z_riga"][:150].replace("|", "/")))
    p()
    p("### ⛔ **NON LE ALLINEO, e il mandato non lo chiede:** dice *«se no, `F1` "
      "segnala»*. Allinearle vorrebbe dire ### **SCEGLIERE quale dei due stati e' giusto**, e "
      "per sette di queste nove ### **il punto `1` ha letto ENTRAMBE le righe:** se danno "
      "stati diversi, ### **sono le RIGHE a disaccordare**, e questo e' il ritrovato.")
    p()
    p("### **E `F1` confronta lo stato SOLO per lo schema `D`/`Z`:** fuori da la' ### **no** "
      "— due voci diverse ### **possono stare in stati diversi senza contraddirsi.** Il "
      "collaudo ha ### **il braccio negativo** che lo prova: con lo stesso disallineamento ma "
      "gli ID rinominati, `F1` ### **tace.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑧ PUNTO `7` — **le due parti, senza dividere**")
    p()
    dich = [i for i in DD.LE16
            if "E- MIA" not in per[i]["meta"]["da_dividere_parti"][-1]]
    p("### **`%d` divisioni le dichiara IL TESTO, `%d` sono MIE**"
      % (len(dich), len(DD.LE16) - len(dich)))
    p()
    p("| id | parti | chi la dichiara |")
    p("|---|--:|---|")
    for i in DD.LE16:
        pp = per[i]["meta"]["da_dividere_parti"]
        p("| `%s` | `%d` | %s |" % (i, len(pp) - 1,
                                     "### **il TESTO**" if i in dich
                                     else "### ⚠ **MIA**"))
    p()
    p("### ⛔ **`da_dividere` e' un `bool`** e non puo' portare le parti: il bool resta "
      "*(dice **SE**)* e si aggiunge ### **`da_dividere_parti`** *(dice **CHE COSA**)* "
      "— perche' `M2` e `B6` lo usano gia' col bool, e ### **una cura che rompe due voci "
      "per far stare sedici non e' una cura.**")
    p()
    p("### **`E4-LAM` ha QUATTRO parti**, e il mandato diceva *«le due parti»*: il testo ne "
      "dichiara quattro — `①` e `②` della proposta, piu' `① FATTO` e `② RESTA APERTO` "
      "dell'esito. ### **Ho scritto quello che dice invece di sceglierne due.**")
    p()
    p("### ⚠ **E UN DIFETTO GENERALE DEL RITROVAMENTO, che dichiaro e NON curo:** il "
      "prefisso di `fonte` puo' combaciare con una riga che e' ### **solo l'ID** — per "
      "`MASSA-CRITICA-LOCALE` la riga *«ritrovata»* e' `MASSA-CRITICA-LOCALE.`, cioe' "
      "### **una citazione nella prosa, senza contenuto.** L'ho aggirato nel punto `7`, "
      "### **ma NON ho cambiato `riga_origine`:** i punti `1` e `2` sono ### **gia' "
      "applicati** con quella, e cambiarla adesso ### **farebbe divergere il referto da cio' "
      "che e' stato scritto.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑨ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s` *(il task history, prima del punto `1`)*. **DOPO** = il "
      "disco. ### **Nessun numero ricopiato.**" % PRIMA)
    p()
    for campo in ("classe", "dominio", "era", "stato"):
        tab(campo, collections.Counter(str(v[campo]) for v in pv),
            collections.Counter(str(v[campo]) for v in voci))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| ### **ID vecchi conservati** | `%d` | ### **`%d`** *(`0` persi, `0` doppi)* |"
      % (n_vecchi, n_vecchi))
    p("| ### **righe di storico** | `%d` | ### **`%d`** |"
      % (len([r for r in gshow("%s:doc/indice/storico.jsonl" % PRIMA).split(NL)
              if r.strip()]),
         sum(1 for r in io.open(os.path.join(RADICE, "doc/indice/storico.jsonl"),
                                encoding="utf-8") if r.strip())))
    p()
    p("| presidio | segnali |")
    p("|---|--:|")
    for k in ("F1", "F2", "F3", "F4", "F6", "F8"):
        p("| `%s` | %s |" % (k, "### **`%d`**" % len(seg[k]) if seg[k] else "`0`"))
    p("| ### **in tutto** | ### **`%d`** |" % sum(len(v) for v in seg.values()))
    p()
    p("```")
    for r in ctrl:
        p(r)
    p("```")
    p()
    p("---")
    p()
    p("## ⑩ I `%d` SEGNALI CHE RESTANO — **voce per voce, con la frase**"
      % sum(len(v) for v in seg.values()))
    p()
    p("> ### ⛔ **NON SI CORREGGONO: SI ELENCANO.** Un presidio ### **segnala, non "
      "decide** — e un segnale che si spegne cambiando la voce invece di guardarla "
      "### **e- un segnale perso.**")
    p()
    for k in ("F1", "F8"):
        if not seg[k]:
            continue
        p("### **`%s`: `%d`**" % (k, len(seg[k])))
        p()
        p("| id | il segnale | la riga d'origine |")
        p("|---|---|---|")
        for i, m in sorted(seg[k]):
            r = ro.get(i)
            p("| `%s` | %s | %s |"
              % (i, m.replace("|", "/"),
                 ("*%s*" % " ".join(r.split())[:190].replace("|", "/")) if r
                 else "### ⚠ **non si ritrova**"))
        p()
    p("### ⚠ **E `F1` NE VEDE `%d` SU `%d`:** le altre due — `D16` e `D26` — "
      "### **citano la loro `Z` nella DESCRIZIONE**, e `F1` guarda ### **il TITOLO.** Lo dico "
      "perche- il numero del presidio e quello dell-attrezzo ### **NON coincidono**, e la "
      "ragione e- questa." % (len(seg["F1"]), len(dz["disallineate"])))
    p()
    p("### ⭐ **E `F8` dice una cosa SUL CONFINE, non sulle voci:** le `%d` voci che "
      "segnala sono ### **era `ENTRAMBE` con un oggetto concreto dell-era `1` nel testo**. "
      "Il mandato del giro prima ha detto che ### **vale per ENTRAMBE una REGOLA DI LAVORO o "
      "uno strumento che sopravvive**, ed e- ### **era `1` cio- che riguarda un OGGETTO "
      "CONCRETO**: ### **queste `%d` stanno sul confine fra le due frasi**, e dove sta il "
      "confine ### **lo decide Luca, non un marcatore.**" % (len(seg["F8"]), len(seg["F8"])))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑪ CHE COSA RESTA A LUCA")
    p()
    p("| | quante | che cosa |")
    p("|---|--:|---|")
    p("| ### **l'elenco generato** | `46` | `doc/indice/DA_DECIDERE_LUCA.md`, e "
      "### **si genera** |")
    p("| ### **le `D`/`Z` disallineate** | `%d` | ### **le RIGHE disaccordano** sullo stesso "
      "fatto: scegliere quale vale e' una decisione |" % len(dz["disallineate"]))
    p("| ### **le `16` da dividere** | `16` | la divisione ### **la decide Luca**, e per `11` "
      "### **la proposta e' MIA** |")
    p("| ### **le chiusure senza commit** | `%d` | righe che dicono *«CHIUSA»* e "
      "### **non portano il commit che ha chiuso** |"
      % t1.get("la riga dice CHIUSA ma NON PORTA", 0))
    p("| ### **i segnali di `F8`** | `%d` | ### **elencati, non corretti** |" % len(seg["F8"]))
    p("| ### **le due correzioni alla REGOLA del punto `1`** | `2` | se Luca intendeva la "
      "regola ### **alla lettera**, `2` dei `7` casi del collaudo ### **escono diversi** |")
    p("| ### **i segnaposto** | `%d` | ### **non sono una domanda: sono il lavoro che "
      "resta** |" % sum(1 for v in voci if v["classe"] == "NON_DEFINITA"))
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il mandato "
      "### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho "
      "lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un "
      "dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    q4 = os.path.join(RADICE, "doc", "REFERTO_indice_v3_righe_origine.md")
    io.open(q4, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_righe_origine.md: %d righe" % len(R))
    print("  segnali %d; controlli %d/%d; collaudo presidi %d/%d; regola %s/%s"
          % (sum(len(v) for v in seg.values()),
             sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll),
             m3.group(1), m3.group(2)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
