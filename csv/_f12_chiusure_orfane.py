# -*- coding: utf-8 -*-
"""IL PUNTO `2`: **le `chiusura` ORFANE** — piene, su voci che non sono `CHIUSA`.

> ### ⛔ **`F12`: `chiusura` non vuota ⇒ stato `CHIUSA`.** Una voce che porta *«chiusa dal
> commit X con criterio Y»* ### **e non è chiusa MENTE**, e mente ### **in un campo che un
> programma legge.**

**Da dove vengono:** ### **dalla migrazione.** Hanno tutte `commit` = `era-1-secondo-ordine`
*(il NOME del tag, non uno sha)* e criterio *«chiusa nell'era `1` (stato `chiuso` al tag …)»*.
Il lavoro dopo le ha portate a `SOSPESA` ### **lasciando la `chiusura` dietro.**
### ⚠ **Erano `42`; il punto `1` ne ha chiusa UNA**, quindi oggi sono `41`.

**Che cosa si fa, voce per voce:** ### **si rilegge la riga.** Se la riga ### **chiude** →
`CHIUSA`, col commit ### **ricavato** *(punto `1`)*; ### **altrimenti la `chiusura` si
SVUOTA.** ### ⭐ **Non si sceglie fra i due campi a caso: si chiede al DOCUMENTO quale dei
due ha ragione.**

Gira con:  python csv/_f12_chiusure_orfane.py
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _commit_di_chiusura as CC                             # noqa: E402
import _righe_origine as RO                                  # noqa: E402
import _stato_dalla_riga as SR                               # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"


def riga_che_chiude(blocco, parola):
    """### La riga GREZZA del blocco che porta la parola di chiusura, ### **a confine.**

    ### ⛔ **Serve perche- la parola che chiude puo- stare SOTTO l-intestazione:** la riga
    d-origine di una voce puo- essere `## APERTO <ID>` e il *<<chiuso … FINITO>>*
    ### **sta nella sezione.** ### ➜ **L-ago e- la riga che PORTA la parola**, non la prima
    del blocco.
    """
    bordo = re.compile(r"(?<![A-Za-z0-9])" + re.escape(parola) + r"(?![A-Za-z0-9])", re.I)
    for r in (blocco or "").split(NL):
        if r.strip() and bordo.search(SR.norm(r)):
            return r.strip()
    return None


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    orfane = [v for v in voci if (v["chiusura"] or {}) and v["stato"] != "CHIUSA"]
    print("  le `chiusura` ORFANE oggi: %d" % len(orfane))
    tag = CC.sha_del_tag()
    import indice as IX
    lotto, chiude, svuota = [], [], []
    for v in orfane:
        i = v["id"]
        blocco, file_, n = RO.riga_origine(v)
        nuovo, perche = SR.decidi_stato(v, blocco)
        if nuovo == "CHIUSA":
            # ### ✔ **LA RIGA CHIUDE: si chiude, col commit RICAVATO (punto 1).** L-ago e-
            # ### ### **la riga che porta la parola di chiusura**, non la citazione di un
            # ### guardiano -- qui ### **non c-e- nessuna citazione: c-e- il documento.**
            parola = (SR.trova(blocco, SR.CHIUDE) or [("", "")])[0][0]
            ago = riga_che_chiude(blocco, parola) if parola else None
            sha, come = (None, "")
            if ago:
                sha = CC.commit_che_introduce((v["fonte"] or "").split("::")[0], ago)
            if sha:
                come = ("COMMIT RICAVATO: il primo commit che introduce in %s la riga che "
                        "porta <<%s>>" % (file_, parola))
            else:
                sha, come = tag, ("DAL TAG era-1-secondo-ordine: la riga che porta <<%s>> "
                                  "non si ritrova nella storia di %s" % (parola, file_))
            ch = {"criterio": ("(2) `F12`: la `chiusura` era ORFANA e LA RIGA CHIUDE. %s "
                               "[%s]" % (perche, come))[:400],
                  "commit": sha, "data": DATA}
            chiude.append((i, v["stato"], sha, perche))
            if "CHIUSA" not in IX.TRANSIZIONI.get(v["stato"], set()):
                lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                              "motivo": ("(2) PONTE OBBLIGATO da `%s` a `CHIUSA`: "
                                         "TRANSIZIONI non passa. %s"
                                         % (v["stato"], ch["criterio"]))[:1200]})
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"stato": "CHIUSA", "chiusura": ch},
                          "motivo": ("(2) `F12`, E LA RIGA CHIUDE: la `chiusura` era piena e "
                                     "lo stato era `%s`. %s" % (v["stato"],
                                                                ch["criterio"]))[:1200]})
        else:
            # ### ⛔ **LA RIGA NON CHIUDE: la `chiusura` SI SVUOTA.** ### **Non lo stato:**
            # ### lo stato ### **l-ha deciso un lavoro che ha letto la riga**, e la
            # ### `chiusura` ### **e- cio- che e- rimasto indietro.**
            svuota.append((i, v["stato"], perche or "la riga non chiude",
                           (v["chiusura"] or {}).get("criterio", "")[:90]))
            lotto.append({"id": i, "quando": DATA, "campi": {"chiusura": {}},
                          "motivo": ("(2) `F12`: la `chiusura` era ORFANA e LA RIGA NON "
                                     "CHIUDE, quindi SI SVUOTA. Lo stato resta `%s`, perche' "
                                     "lo stato l-ha deciso un lavoro CHE HA LETTO LA RIGA e "
                                     "la `chiusura` e- cio- che e- rimasto indietro (veniva "
                                     "dalla migrazione: <<%s>>). Lettura di oggi: %s"
                                     % (v["stato"],
                                        (v["chiusura"] or {}).get("criterio", "")[:110],
                                        perche or "nessuna parola di stato decide"))[:1200]})
    p = os.path.join(D, "_lotti", "v3_f12.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(y, ensure_ascii=False) for y in lotto) + NL)
    io.open(os.path.join(D, "_p2_f12.json"), "w", encoding="utf-8", newline=NL).write(
        json.dumps({"chiude": chiude, "svuota": svuota}, ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_lotti/v3_f12.jsonl: %d righe" % len(lotto))
    print("  ### LA RIGA CHIUDE -> `CHIUSA`: %d" % len(chiude))
    for i, st, sha, perche in chiude:
        print("   %-26s %-9s -> CHIUSA (%s)  %s" % (i, st, sha, perche[:70]))
    print("  ### LA RIGA NON CHIUDE -> la `chiusura` SI SVUOTA: %d" % len(svuota))
    for i, st, perche, _c in svuota:
        print("   %-26s resta %-9s  %s" % (i, st, perche[:80]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
