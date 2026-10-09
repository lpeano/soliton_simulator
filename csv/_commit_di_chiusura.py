# -*- coding: utf-8 -*-
"""IL PUNTO `1`: **il commit di chiusura SI RICAVA, non si inventa.**

> ### ⛔ **E NEL GIRO SCORSO MI SONO FERMATO TROPPO PRESTO.** Avevo lasciato `47` chiusure
> non fatte scrivendo *«un commit non si inventa»*: ### **non inventarlo era giusto,
> fermarsi lì era una RINUNCIA.** ### ⭐ **E l'errore sotto l'errore: cercavo lo sha DENTRO
> LA RIGA**, e una riga di documento ### **non ha nessun motivo di portare lo sha del commit
> che l'ha scritta.** Cercavo nel posto sbagliato, e ho chiamato *«prudenza»* il non trovare.

**Come si ricava** *(la regola del mandato)*: `git log -S'<frase>' --reverse -- <file>`,
### **il PRIMO** — il commit che ha ### **INTRODOTTO** la frase. ### **Se non si trova:**
il tag `era-1-secondo-ordine`, ### **la stessa regola della migrazione** — e
### **`chiusura.criterio` dice QUALE DEI DUE.**

### ⚠ **E LA FRASE E' QUELLA DEL FILE, non quella del guardiano:** la citazione è
### **normalizzata** *(senza markdown, accenti piegati)*, e `-S` cerca ### **i byte.**
### ➜ **Si ritrova la RIGA GREZZA** che contiene la citazione, e ### **quella riga è
l'ago.**

Gira con:  python csv/_commit_di_chiusura.py
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
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _applica_correzioni_guardiano as AP                   # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
TAG = "era-1-secondo-ordine"


def sha_del_tag():
    q = subprocess.run(["git", "rev-parse", "--short", TAG], cwd=RADICE,
                       capture_output=True, text=True)
    assert q.returncode == 0, "il tag %s non c-e-" % TAG
    return q.stdout.strip()


def riga_grezza(file_, citazione, vicino=0):
    """### La RIGA GREZZA del file che contiene la citazione *(normalizzando)*.

    ### ⛔ **Serve perche- `-S` cerca I BYTE:** la citazione del guardiano e-
    ### **normalizzata**, e cercarla cosi- ### **non trova niente.** ### ✔ **La riga grezza
    e- nel file alla lettera**, quindi e- ### **un ago valido.**

    ### ⚠ **Se piu- righe la contengono, vince la PIU- VICINA alla riga d-origine**: la
    frase di chiusura ### **sta nella sezione della voce**, non in una omonima altrove.
    """
    c = AP.pulisci(citazione).upper()
    if not c:
        return (None, "la citazione e- vuota")
    rr = AP.righe_file(file_)
    if not rr:
        return (None, "il file `%s` non si legge" % file_)
    # ### ⛔ **I CONFINI DI PAROLA, E DUE FALSI LO IMPONGONO:** la citazione di
    # ### `REGISTRO_FISICA:T4` e- ### **<<PASS>>**, e ### **<<passato>> la contiene**; quella
    # ### di `REGISTRO_FISICA:P3` e- ### **<<TIENE>>**, e ### **<<CONTIENE>> la contiene.**
    # ### ➜ **Le due combaciavano con la riga `1` e la riga `11` del registro**, cioe- col
    # ### ### **titolo del documento** -- e il commit <<ricavato>> sarebbe stato
    # ### ### **quello che ha creato il file.**
    # ### ⭐ **E- la stessa lezione di `infinito` che contiene `FINITO`**, due giri fa: la
    # ### ### **terza volta** che una parola dentro un-altra parola mi inganna.
    bordo = re.compile(r"(?<![A-Z0-9])" + re.escape(c) + r"(?![A-Z0-9])")
    trovate = [(n, r) for n, r in enumerate(rr, 1)
               if r.strip() and bordo.search(AP.pulisci(r).upper())]
    if not trovate:
        return (None, "la frase NON si ritrova nel file `%s` (a confine di parola)" % file_)
    trovate.sort(key=lambda x: abs(x[0] - vicino) if vicino else x[0])
    # ### ⚠ **E SI DICE QUANTE RIGHE COMBACIANO:** se sono molte, la frase e-
    # ### ### **generica** e il commit ricavato ### **vale meno.** Il referto lo dichiara.
    return (trovate[0][1].strip(), "riga %d di `%s`%s"
            % (trovate[0][0], file_,
               ("; ### ATTENZIONE: %d righe del file contengono la frase, quindi e- GENERICA"
                % len(trovate)) if len(trovate) > 3 else ""))


def commit_che_introduce(file_, ago):
    """### Il PRIMO commit che introduce `ago` in `file_`, oppure `None`.

    ### ⛔ **`--reverse` da- il PRIMO, e il primo e- quello che INTRODUCE:** l-ultimo
    sarebbe ### **quello che l-ha toccata per ultimo**, che non e- la stessa cosa.
    """
    q = subprocess.run(["git", "log", "-S" + ago, "--reverse", "--format=%h", "--",
                        file_], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if q.returncode != 0:
        return None
    righe = [x.strip() for x in (q.stdout or "").split(NL) if x.strip()]
    return righe[0] if righe else None


def chiusura_di(v, citazione, tag):
    """### La `chiusura` di una voce: ### **criterio, commit, e QUALE DEI DUE.**"""
    file_ = (v["fonte"] or "").split("::")[0]
    _riga, _f, n = AP.RO.riga_origine(v)
    ago, dove = riga_grezza(file_, citazione, n or 0)
    if ago:
        sha = commit_che_introduce(file_, ago)
        if sha:
            return ({"criterio": ("verifica completa del guardiano: %s [COMMIT RICAVATO: "
                                  "il primo commit che introduce la frase in %s, trovato "
                                  "con git log -S --reverse; %s]"
                                  % (citazione, file_, dove))[:400],
                     "commit": sha, "data": DATA},
                    "RICAVATO", dove)
        perche = "la frase e- nel file (%s) ma `git log -S` non la trova nella storia" % dove
    else:
        perche = dove
    # ### ⛔ **IL RIPIEGO E- IL TAG, e il criterio LO DICE:** e- la stessa regola della
    # ### migrazione -- ### **cio- che non si sa datare meglio si data alla fine dell-era
    # ### 1.** ### ⚠ **E non e- una finzione:** il tag ### **esiste**, e dice
    # ### ### **<<entro qui>>**, non <<proprio qui>>.
    return ({"criterio": ("verifica completa del guardiano: %s [DAL TAG %s, la stessa "
                          "regola della migrazione: %s. Il tag dice ENTRO QUI, non PROPRIO "
                          "QUI]" % (citazione, TAG, perche))[:400],
             "commit": tag, "data": DATA},
            "DAL TAG", perche)


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    rap = json.loads(io.open(os.path.join(D, "_p3_guardiano.json"),
                             encoding="utf-8").read())
    senza = [x for x in rap["lasciate"] if "NON PORTA UN COMMIT" in x["perche"]]
    assert len(senza) == 47, "le righe <<chiusure senza commit>> non sono 47: %d" % len(senza)
    dati = AP.leggi_file()
    cit = {x["id"]: x["citazione"] for x in dati}
    tag = sha_del_tag()
    import indice as IX
    lotto, esiti = [], []
    for x in senza:
        i = x["id"]
        v = per[i]
        ch, come, dove = chiusura_di(v, cit[i], tag)
        esiti.append({"id": i, "come": come, "commit": ch["commit"], "dove": dove,
                      "citazione": cit[i], "stato_prima": v["stato"]})
        if "CHIUSA" not in IX.TRANSIZIONI.get(v["stato"], set()) and v["stato"] != "CHIUSA":
            lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                          "motivo": ("(1) PONTE OBBLIGATO da `%s` a `CHIUSA`: TRANSIZIONI "
                                     "non passa. %s" % (v["stato"], ch["criterio"]))[:1200]})
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"stato": "CHIUSA", "chiusura": ch},
                      "motivo": ("(1) IL COMMIT DI CHIUSURA SI RICAVA, NON SI INVENTA. %s"
                                 % ch["criterio"])[:1200]})
    p = os.path.join(D, "_lotti", "v3_chiusure.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(y, ensure_ascii=False) for y in lotto) + NL)
    io.open(os.path.join(D, "_p1_chiusure.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esiti, ensure_ascii=False, indent=1))
    n_ric = sum(1 for y in esiti if y["come"] == "RICAVATO")
    print("  scritto doc/indice/_lotti/v3_chiusure.jsonl: %d righe (%d voci)"
          % (len(lotto), len(senza)))
    print("  ### IL COMMIT RICAVATO DALLA STORIA: %d su %d" % (n_ric, len(esiti)))
    print("  ### DAL TAG %s (%s): %d" % (TAG, tag, len(esiti) - n_ric))
    for y in esiti:
        print("   %-26s %-9s %-9s %s" % (y["id"], y["come"], y["commit"], y["dove"][:70]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
