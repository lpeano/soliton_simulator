# -*- coding: utf-8 -*-
"""IL MANDATO `5` — **`P-REG`: OGNI REGOLA DI GESTIONE E' UNA VOCE, E `CLAUDE.md` SI GENERA.**

> ### ⛔ **Il mandato, alla lettera:** *«ogni regola di gestione è una **VOCE** dell'indice
> *(`STANDARD` se **scritta**, `PRESIDIO` se **cablata**)* … Ogni voce porta **il file di
> dettaglio** e **CHI LA FA RISPETTARE** *(l'ID del presidio, oppure «regola scritta»
> dichiarata, `A9`)*»*; e *«`CLAUDE.md`: **la sezione delle regole SI GENERA**
> dall'indice … **la parte generata modificata a mano → RIFIUTATA**»*.

### ⭐ **E <<CHI LA FA RISPETTARE>> E' IL CAMPO CHE RENDE `A9` VERIFICABILE.** Fino a oggi
`CLAUDE.md` diceva *«regola scritta, NON un presidio»* ### **in prosa**, e una prosa
### **non si conta.** ### ✅ **Con un campo, <<quante regole non hanno nessuno che le faccia
rispettare>> diventa UN NUMERO** — e quel numero è ### **la misura di `A9` sul flusso di
lavoro**, che prima non esisteva.

### ⛔ **E IL PRESIDIO CHE CONTA NON E' <<il generato coincide>>: E' <<NESSUNA REGOLA SI
PERDE>>.** Un errore qui ### **non fa cadere un collaudo: fa sparire una regola** — e una
regola sparita ### **non si vede, perché il file è più corto e sembra più pulito.**
### ⚠ **`CLAUDE.md` più corto NON è un successo: è un SOSPETTO**, e il collaudo confronta
l'insieme delle regole citate ### **con `git`.**

### 📌 **COME SI LEGGE UNA REGOLA DALL'INDICE.** Una voce è una regola di gestione se ha
### **`classe` in `(STANDARD, PRESIDIO)`** e ### **`dominio` in `(METODO,
INFRASTRUTTURA, DOCUMENTAZIONE)`** — ### ⛔ **cioè da CAMPI, non dal titolo** *(par. `9`,
e la voce `DECISIONE-VUOLE-UN-CAMPO`)*. ### ⚠ **E non tutte vanno in `CLAUDE.md`: ci vanno
quelle che la voce DICHIARA**, col metadato `meta.in_claude` — ### **perché `CLAUDE.md` è
il flusso di lavoro e non il catalogo dei presidi:** ce ne sono ### **`91`**, e il tetto è
### **`400` righe.**

### ⚠ **E LE SEZIONI GENERATE SONO DUE, UNA PER PARAGRAFO, e non è una comodità:** i due
paragrafi di `CLAUDE.md` che ### **SONO** tabelle di regole sono ### **due** — il `11`
*(le regole di lavoro)* e il `12` *(i presidi automatici)*. ### ⛔ **Una sezione sola li
fonderebbe, e fondere due elenchi che Luca ha tenuto separati sarebbe una decisione di
struttura che non mi è stata chiesta.** ### ⭐ **E il gruppo non si indovina: si legge da
`meta.dettaglio_regola`** — cioè ### **da un campo**, che è `DECISIONE-VUOLE-UN-CAMPO`
applicata ### **a se stessa.**
"""
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-REG"

CLAUDE = os.path.join(RADICE, "CLAUDE.md")
REGOLE = os.path.join(RADICE, "doc", "REGOLE")
VOCI = os.path.join(RADICE, "doc", "indice", "voci.jsonl")

CLASSI = ("STANDARD", "PRESIDIO")
DOMINI = ("METODO", "INFRASTRUTTURA", "DOCUMENTAZIONE")

# ### i paragrafi che hanno una sezione generata, in ordine.
PARAGRAFI = ("par11.md", "par12.md")

INTESTAZIONE = {
    "par11.md": "| id | la regola | chi la fa rispettare |",
    "par12.md": "| id | che cosa **impedisce** | chi la fa rispettare |",
}

# ### ⚠ **LA FORMA DI UN ID CITATO IN `CLAUDE.md`**, e si conta dai backtick in
# ### grassetto: è così che il file li scrive, e una forma diversa non è una citazione
# ### di regola -- è prosa.
# ### ⛔ **E LE PARENTESI DI `[[ID]]` SONO OPZIONALI, e me lo ha insegnato un conteggio
# ### SBAGLIATO MIO:** il `par.9` dice *«negli scritti NUOVI un ID si cita `[[ID]]`»*,
# ### e la sezione generata usa quella forma. ### **La mia prima regex non la vedeva, e
# ### diceva `15` regole citate dove prima erano `23`** — cioe- ### **mi diceva che
# ### avevo perso OTTO regole.**
# ### ⭐ **E l-ho scoperto facendo il confronto PRIMA/DOPO con `git`, che e- il controllo
# ### che il task history aveva fissato come <<il solo che conta davvero>>: `0` perse.**
# ### ⚠ **Se mi fossi fidato del contatore, avrei cercato un difetto che non c-era.**
_CITATO = re.compile(r"\*\*`\[?\[?([A-Z][A-Za-z0-9:_-]{1,})\]?\]?`\*\*")


def _apre(par):
    return ("<!-- REGOLE GENERATE %s -- NON SI SCRIVE A MANO: "
            "python csv/_regole_gestione.py --scrivi -->" % par)


def _chiude(par):
    return "<!-- FINE REGOLE GENERATE %s -->" % par


def voci():
    return [json.loads(r) for r in io.open(VOCI, encoding="utf-8").read().split(NL)
            if r.strip()]


def regole(v=None):
    """### Le voci che ### **SONO regole di gestione**, da CAMPI e non dal titolo."""
    return [x for x in (v if v is not None else voci())
            if x.get("classe") in CLASSI and x.get("dominio") in DOMINI]


def in_claude(v=None):
    """### Le regole che la voce ### **DICHIARA** di volere in `CLAUDE.md`."""
    fuori = [x for x in regole(v)
             if str(((x.get("meta") or {}).get("in_claude")) or "").strip()]
    return sorted(fuori, key=lambda x: x["id"])


def citate(testo=None):
    """Gli ID ### **citati in grassetto-backtick** in `CLAUDE.md` e PRESENTI nell-indice."""
    t = testo if testo is not None else io.open(CLAUDE, encoding="utf-8").read()
    per = {x["id"] for x in voci()}
    return sorted({m.group(1) for m in _CITATO.finditer(t)} & per)


def citate_a(commit):
    """Gli ID citati in `CLAUDE.md` ### **a un commit**, per il confronto PRIMA/DOPO."""
    q = subprocess.run(["git", "show", "%s:CLAUDE.md" % commit], cwd=RADICE,
                       capture_output=True)
    return citate(q.stdout.decode("utf-8", "replace"))


def chi_la_fa_rispettare(x):
    """### `(sintesi, chi)`: l-ID del presidio, oppure ### **<<regola scritta>>.**

    ### ⛔ **Non si deduce: si LEGGE da `meta.in_claude`**, della forma
    `<sintesi> || <chi>`. ### **Dedurlo dal titolo sarebbe leggere la prosa.**
    """
    s = str(((x.get("meta") or {}).get("in_claude")) or "")
    pezzi = [p.strip() for p in s.split("||")]
    return (pezzi[0] if pezzi else ""), (pezzi[1] if len(pezzi) > 1 else "")


def file_di_dettaglio(x):
    """Il file di `doc/REGOLE/` ### **dichiarato dalla voce**, o `""`."""
    return str(((x.get("meta") or {}).get("dettaglio_regola")) or "").strip()


def sezione(par, v=None):
    """### La sezione generata ### **di UN paragrafo**, come righe.

    ### ⛔ **Il dettaglio NON è una colonna:** il file è ### **lo stesso per tutte le
    regole del paragrafo** *(è il paragrafo)*, e una colonna che ripete lo stesso valore
    ### **ventidue volte occupa righe senza dire niente** — e il tetto è `400`.
    ### ✅ **Sta nella riga di coda, UNA VOLTA.**
    """
    el = [x for x in in_claude(v) if file_di_dettaglio(x) == par]
    R = [_apre(par), ""]
    R.append(INTESTAZIONE[par])
    R.append("|---|---|---|")
    for x in el:
        sintesi, chi = chi_la_fa_rispettare(x)
        R.append("| **`[[%s]]`** | %s | %s |"
                 % (x["id"], sintesi,
                    ("**`%s`**" % chi) if chi and chi != "regola scritta"
                    else "⚠ **regola scritta** *(`A9`)*"))
    senza = [x["id"] for x in el
             if chi_la_fa_rispettare(x)[1] in ("", "regola scritta")]
    R.append("")
    R.append("> ### ⚠ **`%d` di queste `%d` NON HANNO NESSUN PRESIDIO che le faccia "
             "rispettare** *(`A9`)*%s. ### **E il numero esiste perche' <<chi la fa "
             "rispettare>> e' UN CAMPO: in prosa non si contava.** "
             "### **IL DETTAGLIO:** `doc/REGOLE/%s`."
             % (len(senza), len(el),
                (": " + ", ".join("`%s`" % i for i in senza)) if senza else "", par))
    R.append("")
    R.append(_chiude(par))
    return R


def scrivi():
    """### Mette ### **le due sezioni** in `CLAUDE.md`, fra le loro marche."""
    t = io.open(CLAUDE, encoding="utf-8", newline="").read()
    for par in PARAGRAFI:
        a0, b0 = _apre(par), _chiude(par)
        if a0 not in t or b0 not in t:
            raise AssertionError(
                "### LE MARCHE DI `%s` NON CI SONO in `CLAUDE.md`. ### Vanno messe A MANO "
                "una volta, nel posto dove la sezione deve stare: generare il file INTERO "
                "sarebbe riscriverlo, e il resto di `CLAUDE.md` E- SCRITTO A MANO." % par)
        a = t.index(a0)
        b = t.index(b0) + len(b0)
        t = t[:a] + NL.join(sezione(par)) + t[b:]
    io.open(CLAUDE, "w", encoding="utf-8", newline="").write(t)
    return t


def errori():
    """Gli errori di `P-REG`, o `[]`."""
    err = []
    t = io.open(CLAUDE, encoding="utf-8", newline="").read()
    for par in PARAGRAFI:
        a0, b0 = _apre(par), _chiude(par)
        if a0 not in t or b0 not in t:
            err.append("`P-REG`: le marche di `%s` NON SONO in `CLAUDE.md`. ### Senza di "
                       "loro non c-e- niente da generare, e la <<sezione delle regole>> "
                       "e- una frase" % par)
            continue
        a = t.index(a0)
        b = t.index(b0) + len(b0)
        if t[a:b] != NL.join(sezione(par)):
            err.append("`P-REG`: la sezione generata `%s` di `CLAUDE.md` NON COINCIDE col "
                       "generato. ### E- stata MODIFICATA A MANO, oppure va rigenerata "
                       "con `python csv/_regole_gestione.py --scrivi`. ### Come le altre "
                       "viste: una vista scritta a mano DIVERGE dalla fonte, e allora la "
                       "fonte NON E- PIU- LA FONTE" % par)
    for x in in_claude():
        det = file_di_dettaglio(x)
        if det and det not in PARAGRAFI:
            err.append("`P-REG` `%s`: dichiara il dettaglio `%s`, che NON E- fra i "
                       "paragrafi con una sezione generata %s. ### Allora la sua riga NON "
                       "COMPARE in `CLAUDE.md`, e una regola dichiarata <<in CLAUDE>> che "
                       "non c-e- e- PEGGIO di una non dichiarata"
                       % (x["id"], det, list(PARAGRAFI)))
        elif not det:
            err.append("`P-REG` `%s`: e- in `CLAUDE.md` e NON DICHIARA un file di "
                       "dettaglio (`meta.dettaglio_regola`). ### Il punto 4: una regola "
                       "citata senza voce o SENZA FILE e- rifiutata" % x["id"])
            continue
        if det and not os.path.exists(os.path.join(REGOLE, det)):
            err.append("`P-REG` `%s`: dichiara `doc/REGOLE/%s`, che NON ESISTE. ### Un "
                       "rimando a un file che non c-e- e- PEGGIO di nessun rimando: "
                       "sembra che il dettaglio ci sia" % (x["id"], det))
        s, _chi = chi_la_fa_rispettare(x)
        if len(s) < 20:
            err.append("`P-REG` `%s`: la sintesi e- di %d caratteri, e il minimo e- 20. "
                       "### Una riga che non dice la regola NON E- UNA SINTESI: e- un "
                       "segnaposto" % (x["id"], len(s)))
    return err


def perse(commit):
    """### ⛔ **LE REGOLE PERSE fra un commit e adesso.** ### **Il controllo che conta.**

    ### ⭐ **Il task history di questo mandato lo ha fissato come <<il solo controllo che
    conta davvero>>:** un errore in questo mandato ### **non fa cadere un collaudo, fa
    sparire una regola** -- e una regola sparita ### **non si vede, perche' il file e'
    piu' corto e SEMBRA PIU' PULITO.**
    ### ⚠ **`CLAUDE.md` piu' corto NON e' un successo: e' un SOSPETTO.**
    """
    pri, ora = set(citate_a(commit)), set(citate())
    return sorted(pri - ora)


def duplicati():
    """### I SEGNALI: due regole con ### **la stessa sintesi** *(punto `5`)*."""
    visti, fuori = {}, []
    for x in in_claude():
        s = " ".join(chi_la_fa_rispettare(x)[0].lower().split())
        if s in visti:
            fuori.append("`P-REG` segnale: `%s` e `%s` hanno LA STESSA SINTESI. ### Due "
                         "regole con lo stesso contenuto sono UNA regola scritta due "
                         "volte, e `9-ter` dice che a parita- di effetto vince chi ne ha "
                         "meno" % (visti[s], x["id"]))
        visti[s] = x["id"]
    return fuori


def conta():
    """I numeri, ### **per il referto** *(`L-NUMERI`)*."""
    tutte, el = regole(), in_claude()
    senza = [x["id"] for x in el
             if chi_la_fa_rispettare(x)[1] in ("", "regola scritta")]
    righe = io.open(CLAUDE, encoding="utf-8").read().count(NL)
    return {"nell_indice": len(tutte), "in_claude": len(el),
            "senza_presidio": len(senza), "senza": senza,
            "citate": len(citate()), "righe_claude": righe,
            "per_paragrafo": {p: len([x for x in el if file_di_dettaglio(x) == p])
                              for p in PARAGRAFI}}


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--scrivi" in argv:
        scrivi()
        c = conta()
        print("  scritte le sezioni in CLAUDE.md: %s" % c["per_paragrafo"])
        print("  righe di CLAUDE.md: %d (il tetto e- 400)" % c["righe_claude"])
        return 0
    c = conta()
    print("  `P-REG`: %d regole di gestione nell-indice, %d dichiarate in `CLAUDE.md` %s"
          % (c["nell_indice"], c["in_claude"], c["per_paragrafo"]))
    print("     SENZA UN PRESIDIO che le faccia rispettare: %d  (`A9`)"
          % c["senza_presidio"])
    print("     citate in `CLAUDE.md` e presenti nell-indice: %d" % c["citate"])
    print("     righe di `CLAUDE.md`: %d su 400" % c["righe_claude"])
    err = errori()
    for x in err + duplicati():
        print("  " + x)
    if err:
        print("  ### `P-REG` FALLISCE: %d errori" % len(err))
        return 1
    print("  ### `P-REG`: TUTTO A POSTO")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
