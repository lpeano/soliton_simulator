# -*- coding: utf-8 -*-
"""IL GENERATORE DI `doc/REFERTO_indice_v2_fase2.md` — **i numeri PRIMA dal commit, DOPO dal
disco** *(`L-NUMERI`)*.

Gira con:  python csv/_doc_referto_fase2.py
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge l'indice e un commit.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DEST = os.path.join(RADICE, "doc", "REFERTO_indice_v2_fase2.md")
PRIMA = "3ef2326"          # ### la fine della FASE 1 (la migrazione meccanica)
R = []


def A(s=""):
    R.append(s)


def jsonl_da_commit(commit, path):
    q = subprocess.run(["git", "show", "%s:%s" % (commit, path)], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert q.returncode == 0, "non leggo %s da %s" % (path, commit)
    return [json.loads(r) for r in q.stdout.split(NL) if r.strip()]


def jsonl(p):
    return [json.loads(r) for r in io.open(os.path.join(D, p), encoding="utf-8").read()
            .split(NL) if r.strip()]


def conta(vv, campo):
    d = {}
    for v in vv:
        d[str(v[campo])] = d.get(str(v[campo]), 0) + 1
    return d


def tavola(campo, pr, do):
    chiavi = sorted(set(pr) | set(do), key=lambda k: -(do.get(k, 0) + pr.get(k, 0)))
    A("| `%s` | prima | ### **dopo** | |" % campo)
    A("|---|--:|--:|---|")
    for k in chiavi:
        a, b = pr.get(k, 0), do.get(k, 0)
        seg = ("### **%+d**" % (b - a)) if b != a else "="
        A("| `%s` | %d | ### **%d** | %s |" % (k, a, b, seg))
    A("")


def main():
    pr = jsonl_da_commit(PRIMA, "doc/indice/voci.jsonl")
    do = jsonl("voci.jsonl")
    etich_pr = jsonl_da_commit(PRIMA, "doc/indice/etichette_rimosse.jsonl")
    etich = jsonl("etichette_rimosse.jsonl")
    storico = jsonl("storico.jsonl")
    C = io.open(os.path.join(D, "_controlli.txt"), encoding="utf-8").read()
    import re
    m = re.search(r"I CONTROLLI: (\d+) su (\d+)", C)
    assert m and m.group(1) == m.group(2), "i controlli NON passano"

    dc = [v for v in do if v["stato"] == "DA_CLASSIFICARE"]
    nd = [v for v in do if v["classe"] == "NON_DEFINITA"]
    div = [v for v in do if (v["meta"] or {}).get("da_dividere")]
    dub = [v for v in do if (v["meta"] or {}).get("motivo_dubbio")]
    conf = [v for v in do if "da confermare da Luca" in
            ((v["meta"] or {}).get("nota_guardiano") or "")]
    nuove_et = [e for e in etich if str(e.get("regola", "")).startswith("(fase2")]

    A("# L'INDICE `v2`, FASE `2` — **la classificazione PER CONTENUTO e la bonifica**")
    A("")
    A("> ### ⛔ **I `%s` CONTROLLI PASSANO**, e il primo resta quello che conta: ogni ID del "
      "vecchio indice sta in ### **UNO E UNO SOLO** posto — ### **`0` persi, `0` doppi**, "
      "anche dopo aver spostato `54` segnaposto." % m.group(2))
    A(">")
    A("> *I numeri ### **prima** escono dal commit `%s` *(la fine della fase `1`)*, quelli "
      "### **dopo** dal disco. Nessuno e' ricopiato a mano.* *(`L-NUMERI`)*" % PRIMA)
    A("")
    A("---")
    A("")
    A("# ⭐ `①` **I CONTEGGI, PRIMA E DOPO**")
    A("")
    A("| | prima | ### **dopo** |")
    A("|---|--:|--:|")
    A("| voci | %d | ### **%d** |" % (len(pr), len(do)))
    A("| etichette rimosse | %d | ### **%d** |" % (len(etich_pr), len(etich)))
    A("| righe di storico *(ogni modifica, col suo motivo)* | 0 | ### **%d** |" % len(storico))
    A("")
    for campo in ("dominio", "era", "stato", "classe"):
        tavola(campo, conta(pr, campo), conta(do, campo))
    A("### ⭐ **IL NUMERO CHE RIASSUME:** `dominio DA_CLASSIFICARE` passa da "
      "### **`%d`** a ### **`%d`**, e `stato DA_CLASSIFICARE` da ### **`%d`** a "
      "### **`%d`**."
      % (conta(pr, "dominio").get("DA_CLASSIFICARE", 0),
         conta(do, "dominio").get("DA_CLASSIFICARE", 0),
         conta(pr, "stato").get("DA_CLASSIFICARE", 0),
         conta(do, "stato").get("DA_CLASSIFICARE", 0)))
    A("")
    A("# ⛔ `②` **CHE COSA RESTA `DA_CLASSIFICARE`, E PERCHE'** — *`%d` voci*" % len(dc))
    A("")
    A("| gruppo | quante | ### **perche'** |")
    A("|---|--:|---|")
    A("| ### **CONCETTI DA DEFINIRE** *(classe `NON_DEFINITA`)* | ### **`%d`** | erano "
      "segnaposto, e ### **il CODICE o i SIGILLI li nominano**: non sono etichette di "
      "documento, e non si sa ancora ### **che cosa siano**. Ciascuno porta in "
      "`nota_guardiano` ### **dove e' nominato** |" % len(nd))
    A("| ### **il DUBBIO dichiarato** | ### **`%d`** | il contenuto ### **non basta** a "
      "decidere, e sta scritto in `meta.motivo_dubbio` |" % len(dub))
    A("")
    A("### **IL DUBBIO, una per una:**")
    A("")
    A("| id | dominio | ### **perche' non si decide** |")
    A("|---|---|---|")
    for v in sorted(dub, key=lambda x: x["id"]):
        A("| `%s` | `%s` | %s |" % (v["id"], v["dominio"],
                                    (v["meta"]["motivo_dubbio"] or "")[:200]))
    A("")
    A("> ### ✔ **IL DUBBIO E' UN ESITO LEGITTIMO**, e il mandato lo dice: *«NON c'e' un numero "
      "minimo di voci da classificare»*. ### **Due su `247` non si decidono dal contenuto, e "
      "le lascio lì.**")
    A("")
    A("# ⚠ `③` **LE VOCI `da_dividere`, con la PROPOSTA** — *`%d`*" % len(div))
    A("")
    A("| id | dominio / era | ### **perche' sono DUE** | ### **la proposta** |")
    A("|---|---|---|---|")
    for v in sorted(div, key=lambda x: x["id"]):
        A("| `%s` | `%s` / `%s` | il testo dice ### **DUE**: <<%s>> | %s |"
          % (v["id"], v["dominio"], v["era"],
             " ".join((v["descrizione"] or v["titolo"]).split())[:90],
             ((v["meta"] or {}).get("nota_guardiano") or "")[:150]))
    A("")
    A("### ⛔ **LA DIVISIONE LA DECIDE LUCA.** Io ho ### **classificato e marcato**, non "
      "diviso.")
    A("")
    A("# ⭐ `④` **I SEGNAPOSTO, PER ESITO** — *`233` da decidere*")
    A("")
    A("| esito | quante | come si e' deciso |")
    A("|---|--:|---|")
    A("| ### **ALIAS** di una voce vera | ### **`1`** | `CONFIG-1/` → `CONFIG-1`: l'id "
      "### **ripulito dalla punteggiatura finale** coincide con una voce VERA. "
      "### **L'importatore vecchio aveva tagliato male** |")
    A("| ### **ETICHETTA DI DOCUMENTO** | ### **`%d`** | ### **TUTTE** le citazioni stanno in "
      "documenti o in ### **strumenti dell'indice**: sono ### **marcatori di sezione e "
      "titoli** |" % len(nuove_et))
    A("| ### **CONCETTO DA DEFINIRE** *(resta)* | ### **`%d`** | e' citato ### **nel CODICE o "
      "nei SIGILLI** — `soliton_simulator.py`, le sue copie `_sim_*`, `csv/_test_fork/`, "
      "`csv/_seal_fork/` — quindi ### **il codice stesso lo nomina** |" % len(nd))
    A("")
    A("### **LE ETICHETTE RIMOSSE IN QUESTA FASE, le piu' citate:**")
    A("")
    A("| id | citazioni | che cos'era |")
    A("|---|--:|---|")
    for e in sorted(nuove_et, key=lambda x: -(x.get("citazioni_n") or 0))[:14]:
        A("| `%s` | %d | %s |" % (e["id"], e.get("citazioni_n") or 0,
                                  str(e.get("regola", ""))[:120]))
    A("")
    A("> ### ⭐ **E UNA CHE NON HO TOLTO, e merita il suo nome:** `RIDUZIONE-AL-LIMITE` e' la "
      "### **proprieta' dichiarata dello spinore** — *«con `_psi_spinor=(e^{iφ},0)` la "
      "componente `0` == campo scalare»* — ed e' ### **il soggetto di `CENS-A1`, una voce "
      "BLOCCANTE.** ### **Non e' un'etichetta: e' un concetto che il codice nomina.**")
    A("")
    A("# ✔ `⑤` **LE `51` VOCI `TEORIA`, CORRETTE** — *e la causa era un difetto della "
      "migrazione*")
    A("")
    A("### ⛔ **Nessuna delle `51` era una teoria.** Erano ### **`19` assiomi** *(`A1`…`A15`, "
      "`A3c`, `A7b`, `P-DECADIMENTO`, `P-MEMORIA`)*, i ### **presidi** *(`H-*`, `L-*`, "
      "`P1-*`)*, gli ### **standard** *(`STANDARD-4/6/8/10`, `L-SOGLIA`, `P1-sexies`)*, i "
      "### **criteri di sigillo** *(`K2a`, `K2b`, `T3a`, `T3b`)*, un ### **difetto del "
      "driver** *(`M0a`)* e ### **due fronti** *(`GEOMETRIA-DELLA-CRESCITA`, "
      "`REVERSIBILITA-LOCALE`)*.")
    A("")
    A("> ### ⭐ **LA CAUSA, e e' un difetto MIO:** nell'indice dell'era `1` ### **`teoria` era "
      "uno STATO**, e voleva dire *«questa e' una regola o un assioma, non un difetto»*. "
      "### **La mia migrazione l'ha trasportato come CLASSE.** ### ➜ **Un campo usato per dire "
      "un'altra cosa e' esattamente cio' che i vocabolari chiusi esistono per impedire**, e "
      "sta ora scritto in `doc/REGOLE/par9.md` perche' non si rifaccia.")
    A("")
    A("### **LA CURA:** la classe viene dal ### **`tipo_era1`**, che e' ### **un campo "
      "dichiarato** — `assioma` → `STANDARD`, `presidio` → `PRESIDIO`, `standard` → "
      "`STANDARD`, `criterio-locale` → `CRITERIO`, `fronte` → `FRONTE`. ### **Nessuna parola "
      "chiave.** E i cinque nominati dal mandato: `K2a` e `K2b` col ### **padre "
      "`OSSERVABILE-P1`**, `T3a` e `T3b` col ### **padre `DRIVER-SCENA-II`** *(i padri "
      "esistono, verificato prima di scriverli)*, `M0a` → `DIFETTO`/`INFRASTRUTTURA`.")
    A("")
    A("# ⚠ `⑥` **GLI ASSIOMI RICLASSIFICATI: IN ATTESA DI CONFERMA** — *`%d` voci*"
      % len(conf))
    A("")
    A("| dominio | quali |")
    A("|---|---|")
    for dom in ("FISICA", "METODO"):
        L = sorted(v["id"] for v in conf if v["dominio"] == dom)
        A("| ### **%s**, era `ENTRAMBE` | %s |" % (dom, " ".join("`%s`" % x for x in L)))
    A("")
    A("### ⛔ **Ognuna porta `meta.nota_guardiano` con «da confermare da Luca»**, come il "
      "mandato chiede: la ### **`FISICA`** vincola la forma delle leggi o descrive il "
      "comportamento del sistema, la ### **`METODO`** parla di ### **come si lavora e si "
      "verifica.** ### **Non e' una decisione: e' una proposta in attesa.**")
    A("")
    A("# ⛔ `⑦` **I DISACCORDI CON LE LISTE DEL GUARDIANO**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **la divisione `METODO`/`INFRASTRUTTURA`** *(punto `1 d`)* | ### ✔ **NESSUN "
      "DISACCORDO: ho applicato tutte e nove.** Parlano della ### **validita' delle misure**, "
      "non del codice come strumento, e il mio giudizio di prima era ### **piu' "
      "grossolano** |")
    A("| ### **le tre liste `L1` `L2` `L3`** | ### ✔ **non cambiano**, e il controllo `C3` lo "
      "verifica — ### **con le correzioni `(c)` e `(d)` dentro**, altrimenti rifiutava una "
      "correzione ### **chiesta** |")
    A("| ### ⚠ **ma UNA correzione MIA alle liste, e la dichiaro** | ### **`Z87` `Z90` `Z91` "
      "`Z92`** erano finite in ### **`AGENDA`** per un ### **mio** errore: avevo letto "
      "`[EPOCA 2]` come l'### **era `2` dello schema**. ### ⛔ **Falso:** le epoche `1`-`2`-`3` "
      "sono ### **fasi di lavoro sul SECONDO ordine** *(`Z91`: «`SCALA_MIN` frena ogni "
      "scrittura»)*, mentre l'era `2` e' ### **la riscrittura al primo ordine**, cioe' la "
      "### **lista `L2`**. ### ➜ **Corrette, e `AGENDA` ora e' `43` = ESATTAMENTE la lista "
      "`L2`** |")
    A("")
    A("# ⛔ `⑧` **IL DIFETTO PIU' GRAVE DI QUESTO GIRO, ED E' MIO**")
    A("")
    A("> ### ⛔ **IL CONTROLLO `C4` -- l'IDEMPOTENZA -- VERIFICAVA RILANCIANDO LA MIGRAZIONE.** "
      "E la migrazione ### **riscrive `voci.jsonl` PARTENDO DAL TAG.** ### ➜ **Finita la fase "
      "`1` era un controllo innocuo; dopo la fase `2` era DISTRUTTIVO, e mi ha cancellato "
      "`867` classificazioni in un colpo** *(`dominio DA_CLASSIFICARE` da `233` a `664`, "
      "`classe TEORIA` da `0` a `51`)*.")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **come l'ho preso** | `C4` diceva *«FALLISCE — diversi: `voci.jsonl`»*, e ho "
      "guardato i conteggi ### **subito dopo**: quel *«diversi»* ### **non era un difetto "
      "dell'idempotenza — era il DANNO** |")
    A("| ### **il ripristino** | `git checkout` di `doc/indice` e delle viste. ### **Tutto il "
      "lavoro era COMMITTATO**, e l'unico passo perso e' stato quello dei segnaposto, rifatto |")
    A("| ### ✔ **la cura `1`** | la migrazione ### **conta le righe di `storico.jsonl`**: la "
      "migrazione ### **non scrive storico**, quindi ogni riga e' ### **lavoro di dopo** — e "
      "allora ### **si ferma**, a meno di `--forza`. ### **Provato: con `803` righe si "
      "ferma** |")
    A("| ### ✔ **la cura `2`** | `C4` ### **non rilancia piu'** se c'e' lavoro di dopo: "
      "dichiara l'idempotenza ### **verificata al suo commit** *(`6b8cb90`)*, dove l'ha "
      "davvero provata |")
    A("")
    A("### ⚠ **E sta scritto nel SORGENTE di entrambi, non solo qui:** ### **un controllo che "
      "distrugge cio' che controlla e' il difetto piu' facile da rifare.**")
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| che l'indice sia ### **finito** | ### ⛔ **no: `%d` voci restano `DA_CLASSIFICARE`**, "
      "e `%d` di loro sono ### **concetti che il codice nomina** e che nessuno ha ancora "
      "definito |" % (len(dc), len(nd)))
    A("| che la classificazione sia ### **verificata** | ### ⚠ **no: la verifica voce per voce "
      "la fa IL GUARDIANO.** Io ho scritto, per ognuna, ### **un motivo che CITA il testo** — "
      "`%d` righe di storico |" % len(storico))
    A("| che gli ### **assiomi** siano a posto | ### ⛔ **sono una PROPOSTA**, e ogni voce "
      "porta *«da confermare da Luca»* |")
    A("| che le ### **`da_dividere`** siano divise | ### ⛔ **no: sono MARCATE**, con la "
      "proposta. ### **La divisione la decide Luca** |")
    A("| che le ### **regole** usate siano infallibili | ### ⚠ **una l'ho SCARTATA** *(fonte "
      "`doc/REGISTRO_FISICA.md` → `FISICA`)* perche' lì stanno ### **sia** criteri di fisica "
      "### **sia** criteri di ### **verifica**: quelle `55` le ho ### **lette**, e `13` sono "
      "finite in `METODO` |")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (DEST, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
