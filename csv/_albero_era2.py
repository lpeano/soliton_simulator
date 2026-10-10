# -*- coding: utf-8 -*-
"""PUNTO `3` DEL MANDATO — **`P-ALB`: L'ALBERO DELLE SCELTE, E IL SUO PRESIDIO.**

> ### ⛔ **Il mandato, alla lettera:** *«il **PRESIDIO dell'albero**, collaudato nei due
> versi: una decisione marcata **PRESA** con una dipendenza ancora **APERTA** → **la
> validazione FALLISCE**»*.

### ⭐ **PERCHE' QUESTO PRESIDIO E' IL CUORE DEL MANDATO.** Il mandato `2` mi portava `43`
decisioni **già prese**, e il rischio era **tradirne una**. Questo mandato scrive il piano
delle decisioni che **non sono ancora prese**, e il rischio è ### **farne sembrare presa una
che non lo è** — ed è esattamente ciò che questo presidio impedisce.

### 📌 **E IL CASO VERO E' GIA' SUL TAVOLO:** su `D9` Luca ha ### **dichiarato una
direzione** *(«lo spazio emerge grazie alla mitosi»)*, e il mandato dice nella stessa frase
che ### **la direzione NON è una decisione presa.** ### **La differenza fra le due è ciò che
l'albero serve a tenere separato**, e senza il presidio sarebbe **una frase in un
documento.**

| | che cosa impedisce | perché |
|---|---|---|
| `1` | una dipendenza che ### **non esiste** | un albero con un arco rotto ### **non è un albero** |
| `2` | ### ⛔ **un nodo `presa` con una dipendenza NON `presa`** | ### **è il punto `3` del mandato** |
| `3` | un ### **ciclo** | `A` dipende da `B` e `B` da `A`: ### **nessuno dei due si può prendere mai**, e un albero che lo ammette ### **mente sull'ordine** |
| `4` | un nodo ### **`argomento_noto: false` che è `presa`** | ### **non si può prendere una decisione di cui non si sa l'argomento** |
| `5` | un `id` ### **corto, doppio o che collide** con una decisione che c'è già | è `P-ID` applicato al registro delle decisioni |
| `6` | un'### **etichetta locale usata come `id`** *(`D9`, `T4`…)* | `par.9`: ### **un'etichetta locale NON è un ID** — e `D2`, `D4`, `D5`, `D6` sono ### **già omonimi dell'era `1`** |

### ⚠ **E CIO' CHE QUESTO PRESIDIO NON DICE:** non dice che l'albero sia ### **completo**,
né che le dipendenze siano ### **quelle giuste** — quelle sono decisioni di Luca. Dice che
l'albero è ### **coerente con se stesso** e che ### **nessuna decisione risulta presa prima
di quelle da cui dipende.**
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-ALB"

FONTE = os.path.join(RADICE, "doc", "ALBERO_era2.yaml")

CAMPI = ("id", "etichetta", "titolo", "argomento_noto", "dipende_da", "presa", "fonte")
# ### ⚠ **`nota` e- OPZIONALE**, e il resto e- ### **obbligatorio**: un nodo senza
# ### `dipende_da` e- un nodo che ### **non dice se dipende da qualcosa**, che non e- la
# ### stessa cosa di ### **una lista vuota.**
OPZIONALI = ("nota",)

MIN_CARATTERI = 4
_FORMA_ID = re.compile(r"^DEC-[A-Z0-9-]{3,}$")


def carica():
    """### `(nodi, radici)` dalla fonte. ### **Un solo posto che la legge.**"""
    import yaml
    with io.open(FONTE, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    return list(d.get("nodi") or []), list(d.get("radici_prese") or [])


def decisioni_esistenti():
    """Gli `id` che il registro delle decisioni ### **ha gia-**, dalla sua fonte."""
    import json
    p = os.path.join(RADICE, "doc", "indice", "decisioni.jsonl")
    if not os.path.exists(p):
        return set()
    return {json.loads(r)["id"] for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()}


def controlla(nodi=None, radici=None):
    """### Gli errori dell-albero, o `[]`.

    ### ⛔ **`nodi` e `radici` si possono passare**, e ### **serve al collaudo**: il caso
    che DEVE fallire si costruisce ### **dai nodi veri, in memoria**, senza
    ### **toccare il file sul disco** — cosi- nessun braccio puo- lasciare danno.
    """
    if nodi is None or radici is None:
        nodi, radici = carica()
    err = []
    per = {}
    # ------------------------------------------------------------------ la FORMA
    for n in nodi:
        i = n.get("id") or "<senza id>"
        manca = [c for c in CAMPI if c not in n]
        if manca:
            err.append("`P-ALB` `%s`: gli manca %s. ### Un nodo senza `dipende_da` non "
                       "dice SE dipende da qualcosa, che non e- la stessa cosa di una "
                       "LISTA VUOTA" % (i, ", ".join("`%s`" % x for x in manca)))
        fuori = [c for c in n if c not in CAMPI and c not in OPZIONALI]
        if fuori:
            err.append("`P-ALB` `%s`: campi fuori vocabolario: %s"
                       % (i, ", ".join("`%s`" % x for x in fuori)))
        if i in per:
            err.append("`P-ALB` `%s`: id DOPPIO nell-albero" % i)
        per[i] = n
    # ------------------------------------------------------------------ gli ID
    gia = decisioni_esistenti()
    etich = {str(n.get("etichetta") or "") for n in nodi}
    for n in nodi:
        i = n.get("id") or ""
        if not _FORMA_ID.match(i):
            err.append("`P-ALB` `%s`: la forma di un id e- `DEC-[A-Z0-9-]{3,}`" % i)
        if len(i) < MIN_CARATTERI:
            err.append("`P-ALB` `%s`: ha %d caratteri e il minimo e- %d (`P-ID`)"
                       % (i, len(i), MIN_CARATTERI))
        if i in gia and not i.startswith("DEC-D") and not i.startswith("DEC-INT") \
                and not i.startswith("DEC-T"):
            err.append("`P-ALB` `%s`: COLLIDE con una decisione che c-e- gia-" % i)
        # ### ⛔ **L-ETICHETTA LOCALE NON PUO- ESSERE L-ID** *(par. `9`)*.
        if i in etich:
            err.append("`P-ALB` `%s`: l-id E- un-etichetta locale. ### Par. 9: "
                       "un-etichetta locale NON e- un ID -- e `D2`, `D4`, `D5`, `D6` "
                       "sono GIA- OMONIMI DELL-ERA 1" % i)
    # ------------------------------------------------------------------ gli ARCHI
    noti = set(per) | set(radici) | gia
    for n in nodi:
        for d in (n.get("dipende_da") or []):
            if d not in noti:
                err.append("`P-ALB` `%s`: dipende da `%s`, che NON ESISTE. ### Un albero "
                           "con un arco rotto non e- un albero" % (n.get("id"), d))
    # ------------------------------------------------------------------ il CICLO
    def discendenza(i, visti):
        if i in visti:
            return [i]
        visti = visti | {i}
        for d in ((per.get(i) or {}).get("dipende_da") or []):
            giu = discendenza(d, visti)
            if giu:
                return [i] + giu
        return []
    for n in nodi:
        c = discendenza(n.get("id"), set())
        if c:
            err.append("`P-ALB` `%s`: CICLO -- %s. ### Nessuno dei nodi di un ciclo si "
                       "puo- prendere MAI, e un albero che lo ammette MENTE SULL-ORDINE"
                       % (n.get("id"), " -> ".join("`%s`" % x for x in c)))
            break
    # ------------------------------------------------------------------ ### IL PUNTO 3
    for n in nodi:
        if not n.get("presa"):
            continue
        for d in (n.get("dipende_da") or []):
            giu = per.get(d)
            preso = (d in radici) or (d in gia and giu is None) or bool(
                (giu or {}).get("presa"))
            if not preso:
                err.append("`P-ALB` `%s`: e- marcata PRESA e dipende da `%s`, che NON e- "
                           "PRESA. ### E- IL PUNTO 3 DEL MANDATO: una decisione non si "
                           "puo- prendere PRIMA di quelle da cui dipende, e la "
                           "differenza fra una DIREZIONE DICHIARATA e una DECISIONE "
                           "PRESA e- cio- che questo albero serve a tenere separato"
                           % (n.get("id"), d))
    # ------------------------------------------------------------------ l-ARGOMENTO
    for n in nodi:
        if n.get("argomento_noto") is False and n.get("presa"):
            err.append("`P-ALB` `%s`: e- PRESA e il suo `argomento_noto` e- `false`. "
                       "### NON SI PUO- PRENDERE UNA DECISIONE DI CUI NON SI SA "
                       "L-ARGOMENTO" % n.get("id"))
    return err


def conta():
    """I numeri dell-albero, ### **per il referto** *(`L-NUMERI`)*."""
    nodi, radici = carica()
    return {
        "nodi": len(nodi),
        "radici": len(radici),
        "prese": sum(1 for n in nodi if n.get("presa")),
        "senza_argomento": sum(1 for n in nodi if n.get("argomento_noto") is False),
        "archi": sum(len(n.get("dipende_da") or []) for n in nodi),
        "con_nota": sum(1 for n in nodi if n.get("nota")),
    }


def collaudo():
    import _presidio
    _presidio.avvia(__file__)
    import copy
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    nodi, radici = carica()
    c = conta()
    print("=" * 100)
    print("IL COLLAUDO DI `P-ALB` -- L-ALBERO DELLE SCELTE, nei DUE VERSI")
    print("=" * 100)
    print("  nodi %d   archi %d   radici prese %d   PRESE %d   senza argomento %d"
          % (c["nodi"], c["archi"], c["radici"], c["prese"], c["senza_argomento"]))
    for n in nodi:
        print("     %-22s %-5s %-5s  %s"
              % (n["id"], n["etichetta"],
                 "PRESA" if n.get("presa") else "-",
                 ("<- " + ", ".join(n["dipende_da"])) if n.get("dipende_da") else "radice"))
    print()
    # ------------------------------------------------------------------ il verso SANO
    esito("NON deve scattare: l-albero come e- scritto",
          controlla(nodi, radici) == [],
          "### se non passa, e- L-ALBERO che e- sbagliato, non il presidio")
    esito("### il collaudo ha MATERIA: ci sono archi",
          c["archi"] > 0,
          "%d archi su %d nodi: ### senza archi il punto 3 non si potrebbe nemmeno provare"
          % (c["archi"], c["nodi"]))
    # ### ⛔ **ERA <<NESSUN nodo e- PRESA>>, e il 2026-10-10 NON E- PIU- VERO:**
    # ### Luca ha preso il nodo `INT` *(l-integratore locale a strati)*. ### ⚠ **Un
    # ### braccio che asserisce UN FATTO DI OGGI scade il giorno in cui il fatto
    # ### cambia** -- ed e- la stessa forma del referto-fotografia.
    # ### ✅ **Allora si dichiara IL NUMERO E I NOMI**: cosi- un nodo che diventa
    # ### PRESO ### **in silenzio fa ancora scattare il braccio**, e un nodo preso
    # ### ### **per una decisione di Luca** si aggiunge QUI, dove si vede.
    PRESI_DICHIARATI = ("DEC-INT-INTEGRATORE",)
    _presi = sorted(x["id"] for x in nodi if x.get("presa"))
    esito("### i nodi PRESI sono esattamente quelli DICHIARATI",
          _presi == sorted(PRESI_DICHIARATI),
          "%d presi: %s   ### un nodo che diventa PRESO senza passare da qui FA "
          "SCATTARE" % (len(_presi), ", ".join(_presi) or "nessuno"))

    # ------------------------------------------------- ### IL PUNTO 3, che DEVE fallire
    # ### ⛔ **COSTRUITO DAI NODI VERI, IN MEMORIA** (`P1-sexies`): si prende il nodo che
    # ### ### **ha davvero una dipendenza** e si marca `presa`.
    figlio = next((n for n in nodi if n.get("dipende_da")), None)
    n2 = copy.deepcopy(nodi)
    for n in n2:
        if n["id"] == figlio["id"]:
            n["presa"] = True
    e = controlla(n2, radici)
    esito("### DEVE scattare: un nodo PRESA con una dipendenza NON PRESA",
          any("E- IL PUNTO 3 DEL MANDATO" in x and figlio["id"] in x for x in e),
          "`%s` marcata PRESA mentre `%s` non lo e-"
          % (figlio["id"], figlio["dipende_da"][0]))
    # ### ✅ **E IL ROVESCIO: se si prende ANCHE il padre, NON deve scattare** -- cosi- il
    # ### braccio di sopra non passa ### **per il motivo sbagliato** *(un presidio che
    # ### rifiuta sempre non prova niente)*.
    n3 = copy.deepcopy(n2)
    for n in n3:
        if n["id"] in figlio["dipende_da"]:
            n["presa"] = True
    esito("NON deve scattare: PRESA anche il PADRE, e l-ordine e- rispettato",
          not any("E- IL PUNTO 3" in x for x in controlla(n3, radici)),
          "### e- il braccio che dice che il presidio non rifiuta SEMPRE")

    # ------------------------------------------------- l-ARGOMENTO che non si sa
    # ### ⛔ **LA VITTIMA SI COSTRUISCE, NON SI CERCA NEL REPO.** ### ⚠ **Il
    # ### `2026-10-10` questo braccio si e- ROTTO** *(`TypeError`, `senza` era `None`)*:
    # ### cercava ### **un nodo del repo con `argomento_noto: false`**, e il punto `5`
    # ### del mandato ### **ha dato l-argomento agli ultimi cinque.**
    # ### ⭐ **Un braccio che DEVE fallire e che PESCA LA VITTIMA NEL REPO smette di
    # ### funzionare quando il repo MIGLIORA** -- ed e- la stessa forma del braccio che
    # ### asseriva <<nessun nodo e- PRESA, oggi>>.
    n4 = copy.deepcopy(nodi)
    senza = n4[0]
    senza["argomento_noto"] = False
    senza["presa"] = True
    esito("### DEVE scattare: PRESA una decisione di cui NON si sa l-argomento",
          any("NON SI SA" in x and senza["id"] in x for x in controlla(n4, radici)),
          "`%s`: ### il repo non dice di che cosa decida, e il mandato non lo dice"
          % senza["id"])

    # ------------------------------------------------- l-arco ROTTO
    n5 = copy.deepcopy(nodi)
    n5[0] = dict(n5[0], dipende_da=["DEC-QUESTO-NON-ESISTE"])
    esito("### DEVE scattare: una dipendenza che NON ESISTE",
          any("NON ESISTE" in x for x in controlla(n5, radici)),
          "### un albero con un arco rotto non e- un albero")

    # ------------------------------------------------- il CICLO
    n6 = copy.deepcopy(nodi)
    a, b = n6[0]["id"], n6[1]["id"]
    n6[0] = dict(n6[0], dipende_da=[b])
    n6[1] = dict(n6[1], dipende_da=[a])
    esito("### DEVE scattare: un CICLO",
          any("CICLO" in x for x in controlla(n6, radici)),
          "`%s` <-> `%s`: ### nessuno dei due si potrebbe prendere MAI" % (a, b))

    # ------------------------------------------------- l-ETICHETTA come id
    n7 = copy.deepcopy(nodi)
    n7[0] = dict(n7[0], id=n7[0]["etichetta"])
    esito("### DEVE scattare: l-ETICHETTA LOCALE usata come id",
          any("un-etichetta locale NON e- un ID" in x or "la forma di un id" in x
              for x in controlla(n7, radici)),
          "`%s`: ### par. 9, e `D2`/`D4`/`D5`/`D6` sono GIA- OMONIMI DELL-ERA 1"
          % n7[0]["etichetta"])

    # ------------------------------------------------- un CAMPO che manca
    n8 = copy.deepcopy(nodi)
    n8[0] = {k: v for k, v in n8[0].items() if k != "dipende_da"}
    esito("### DEVE scattare: un nodo SENZA `dipende_da`",
          any("non dice SE dipende" in x for x in controlla(n8, radici)),
          "### <<non dichiarato>> e <<lista vuota>> NON sono la stessa cosa")

    # ------------------------------------------------- il file NON si e- mosso
    esito("### e il file sul disco NON e- stato toccato",
          carica() == (nodi, radici),
          "### ogni caso che DEVE fallire e- costruito IN MEMORIA: un braccio che per "
          "provare qualcosa scrive nel repo e- un braccio che puo- lasciare DANNO")

    # ===================================================================================
    #   ### ⭐ **IL RAMO END-TO-END: provare `controlla()` NON prova `valida`.**
    # ===================================================================================
    # ### ⛔ **Fra la funzione e la validazione c-e- un `import` dentro un `try`**, ed
    # ### e- ### **la- che un presidio si spegne in silenzio**: se `_albero_era2` non si
    # ### importasse, `valida` scriverebbe <<NON E- GIRATO>> e
    # ### ### **continuerebbe a passare.** ### **Quindi qui si scrive davvero nel `yaml`,
    # ### si chiama `valida` COME LO CHIAMA IL `pre-commit`, e si rimette -- verificando
    # ### lo sha1.**
    import hashlib
    import subprocess
    b0 = io.open(FONTE, "rb").read()
    sha0 = hashlib.sha1(b0).hexdigest()
    try:
        # ### il nodo che ha una dipendenza, marcato `presa` NEL FILE
        rotto = b0.decode("utf-8").replace(
            "    id: %s%s    etichetta: %s%s    titolo:"
            % (figlio["id"], NL, figlio["etichetta"], NL),
            "    id: %s%s    etichetta: %s%s    titolo:"
            % (figlio["id"], NL, figlio["etichetta"], NL), 1)
        # ### ⚠ **la sostituzione si fa sulla RIGA `presa: false` DI QUEL NODO**, e
        # ### ### **si CONTA**: un blocco che non si trova una volta sola si rifiuta.
        pezzi = rotto.split("  - id: " + figlio["id"] + NL)
        assert len(pezzi) == 2, "### il nodo `%s` non compare una volta sola" % figlio["id"]
        testa, coda = pezzi
        assert coda.count("presa: false") >= 1
        coda = coda.replace("presa: false", "presa: true", 1)
        io.open(FONTE, "w", encoding="utf-8", newline="").write(
            testa + "  - id: " + figlio["id"] + NL + coda)
        r = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "valida"],
                           cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        fuori = (r.stdout or "") + (r.stderr or "")
        esito("### DEVE scattare END-TO-END: `indice.py valida` ESCE 1",
              r.returncode != 0 and "E- IL PUNTO 3 DEL MANDATO" in fuori,
              "codice %d: ### provare la funzione NON prova la VALIDAZIONE, e fra le due "
              "c-e- un `import` dentro un `try` -- il posto dove un presidio si spegne in "
              "silenzio" % r.returncode)
    finally:
        io.open(FONTE, "wb").write(b0)
    esito("### e la fonte e- tornata IDENTICA AL BYTE",
          hashlib.sha1(io.open(FONTE, "rb").read()).hexdigest() == sha0,
          "`%s`" % sha0[:8])
    r2 = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "valida"],
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    esito("NON deve scattare: rimessa la fonte, `valida` PASSA di nuovo",
          r2.returncode == 0,
          "### il braccio di sopra scattava per L-ALBERO, non per qualcos-altro")

    print("=" * 100)
    print("IL COLLAUDO DI `P-ALB`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    c = conta()
    print("  `P-ALB`: %d nodi, %d archi, %d PRESE, %d senza argomento"
          % (c["nodi"], c["archi"], c["prese"], c["senza_argomento"]))
    for x in err:
        print("  " + x)
    if err:
        print("  ### `P-ALB` FALLISCE: %d errori" % len(err))
        return 1
    print("  ### `P-ALB`: TUTTO A POSTO")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
