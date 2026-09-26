# -*- coding: utf-8 -*-
"""**`STANDARD 10` ESCE DAL POSTO 2 E VA IN `CLAUDE.md`** *(decisione di Luca, 2026-09-26)*.

> **«`STANDARD 10` esce dal posto 2 e va in `CLAUDE.md`, accanto alla sezione dell'indice: e' il
> criterio per scegliere fra CURE, non un metodo di misura. Il posto 2 torna a 10. Il tetto NON
> si alza.»**

**COSA FA, in tre mosse, ognuna asserita per se' (`P1-quater`):**

1. toglie la **riga** `STANDARD 10` dalla tabella `STANDARD` di `doc/PATTERN_DI_PROVA.md`;
2. sposta la **sezione lunga** in `CLAUDE.md`, **subito dopo la sezione dell'indice**, e al suo
   posto lascia un **richiamo** *(cosi' il nome resta nel posto 2 e chi lo cerca lo trova)*;
3. riscrive la nota *«il conto non torna»* col conto **che ora torna**.

**IL NUMERO DELLA SEZIONE NUOVA E' `9-ter`, E LA SCELTA E' DICHIARATA.** Non `par.10`: quel
numero, in ogni reperto di questo repo, significa **promozione delle componenti**, e riusarlo
creerebbe la stessa collisione che il 2026-09-26 abbiamo curato per gli ID. Non `par.9-bis`:
era **l'epoca di un numero**, che ora vive dentro `P3`. **Un'etichetta non si ricicla.**

    python csv/_sposta_standard10.py --prova
    python csv/_sposta_standard10.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sposta prosa fra due documenti.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
PDP = os.path.join(RADICE, "doc", "PATTERN_DI_PROVA.md")
CL = os.path.join(RADICE, "CLAUDE.md")

# l'ancora include il parentetico: senza, la sostituzione del titolo lo lasciava DOPPIO
#   (trovato rigirando, 2026-09-26).
APRE = ("## `STANDARD 10` — **UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI** "
        "*(criterio di Luca, 2026-09-25)*")
CHIUDE = "## ⚠ I NOMI CHE SONO CAMBIATI IL 2026-09-26"
ANCORA_CL = "## 10. IL PRINCIPIO GUIDA"

RICHIAMO = (
    "- **Una cura non aumenta il numero delle leggi; a parita' di effetto si preferisce togliere "
    "un'eccezione** *(era `STANDARD 10`)* → **`CLAUDE.md` par.9-ter**. **Decisione di Luca, "
    "2026-09-26:** e' il criterio con cui si scegle fra **CURE**, non il metodo di una **MISURA** "
    "— e con la sua uscita **il posto 2 torna a 10, senza alzare il tetto**."
)

CONTO_NUOVO = """## ✅ IL CONTO TORNA: **DIECI REGOLE PER UN TETTO DI DIECI** *(2026-09-26)*

**Per un giorno sono state ELEVEN, e lo avevo dichiarato invece di arrotondarlo.**
**Ha deciso Luca, e non alzando il tetto:** `STANDARD 10` **esce dal posto 2** e va in
`CLAUDE.md` par.9-ter, *perche' e' il criterio per scegliere fra **CURE**, non un metodo di
misura*. **Il tetto resta 10.**

| | |
|---|--:|
| righe della tabella `STANDARD` al 2026-09-26 sera | **10** |
| tetto | **10** |

**LE DUE CANDIDATE NON SCELTE, e restano scritte perche' la strada scartata informa:**
**`P5` dentro `STANDARD 3`** *(ma `P5` conta **rami** e `STANDARD 3` confronta **istanti**:
fonderle mescola due presidi)* e **`P4` dentro `P1-sexies`** *(la fusione che Luca aveva
**rifiutato** lo stesso giorno)*.

> **E IL MODO IN CUI E' STATA DECISA E' IL PUNTO:** il conto sbagliato era **nella proposta**
> *(annunciava 10 e ne dava 12)*, e a trovarlo e' stato **un controllo che legge l'inventario
> invece di ricopiarlo**. **Un tetto che si alza quando non ci si sta dentro non e' un tetto.**"""


def _sost(t, coppie, dove):
    for vecchio, nuovo in coppie:
        n = t.count(vecchio)
        if n != 1:
            raise SystemExit("%s: ancora attesa 1 volta, trovata %d: %s"
                             % (dove, n, vecchio[:72]))
        t = t.replace(vecchio, nuovo)
    return t


def taglia_sezione(t):
    """La sezione lunga di `STANDARD 10`, dal suo titolo al titolo successivo."""
    a = t.find(APRE)
    b = t.find(CHIUDE)
    if a < 0 or b < 0 or b <= a:
        raise SystemExit("la sezione di STANDARD 10 non si delimita: e' gia' stata spostata?")
    return t[:a], t[a:b], t[b:]


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    print("=" * 92)
    print("`STANDARD 10`: posto 2 -> CLAUDE.md par.9-ter%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)

    t = io.open(PDP, encoding="utf-8", newline="").read()
    if "par.9-ter" in t:
        print("  gia' spostata (il richiamo c'e'): non tocco niente.")
        sys.exit(0)
    testa, sezione, coda = taglia_sezione(t)
    n_sez = sezione.count(NL)

    # 1. la RIGA esce dalla tabella
    righe = testa.split(NL)
    riga = [r for r in righe if r.startswith("| **STANDARD 10** |")]
    if len(riga) != 1:
        raise SystemExit("la riga di STANDARD 10 nella tabella: trovata %d volte" % len(riga))
    righe.remove(riga[0])
    testa = NL.join(righe)

    # 2. il RICHIAMO prende il suo posto nell'elenco dei rimandi
    testa = _sost(testa, [(
        "- **Un difetto DIMOSTRATO si cura",
        RICHIAMO + NL + "- **Un difetto DIMOSTRATO si cura")], "PATTERN (richiamo)")

    # 3. la nota del conto si riscrive col conto che TORNA
    a2 = testa.find("## ⚠ IL CONTO NON TORNA")
    b2 = testa.find("## IN PROVA")
    if a2 < 0 or b2 <= a2:
        raise SystemExit("la nota `IL CONTO NON TORNA` non si delimita")
    testa = testa[:a2] + CONTO_NUOVO + NL + NL + "---" + NL + NL + testa[b2:]

    nuovo_pdp = testa + coda
    nuovo_pdp = _sost(nuovo_pdp, [
        ("| `STANDARD 4` | **fusa dentro `STANDARD 3`** | questo documento |",
         "| `STANDARD 4` | **fusa dentro `STANDARD 3`** | questo documento |" + NL
         + "| `STANDARD 10` | **uscita dal posto 2**, per decisione di Luca | "
           "`CLAUDE.md` par.9-ter |")], "PATTERN (tabella dei nomi)")

    # e in CLAUDE.md la sezione entra ACCANTO a quella dell'indice
    c = io.open(CL, encoding="utf-8", newline="").read()
    sez_cl = sezione.replace(APRE,
                             "## 9-ter. UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI "
                             "*(criterio di Luca, 2026-09-25)*").rstrip(NL)
    sez_cl += (NL + NL + "> *(Stava in `doc/PATTERN_DI_PROVA.md` come `STANDARD 10`. **Esce dal "
               "posto 2 per decisione di Luca del 2026-09-26:** e' il criterio con cui si sceglie "
               "fra **CURE**, non il metodo di una **MISURA** — e il posto 2 torna a 10 "
               "**senza alzare il tetto**. Il numero e' `9-ter` e non `10`: in ogni reperto di "
               "questo repo `par.10` significa **promozione delle componenti**, e un'etichetta "
               "non si ricicla.)*" + NL)
    c = _sost(c, [(ANCORA_CL, sez_cl + NL + "---" + NL + NL + ANCORA_CL)], "CLAUDE.md")

    if scrivi:
        io.open(PDP, "w", encoding="utf-8", newline=NL).write(nuovo_pdp)
        io.open(CL, "w", encoding="utf-8", newline=NL).write(c)
    print("  sezione spostata ............... %d righe" % n_sez)
    print("  doc/PATTERN_DI_PROVA.md ........ %d righe" % nuovo_pdp.count(NL))
    print("  CLAUDE.md ...................... %d righe   (tetto 400)" % c.count(NL))
    sys.exit(0)
