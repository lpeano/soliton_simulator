# -*- coding: utf-8 -*-
"""**LA STORIA DELLE REGOLE -> `doc/STORIA_REGOLE.md`** *(mandato di Luca 2026-09-26, punto `f`)*.

**L'archivio e' VERBATIM e si legge dal TAG, non dal disco.** `CLAUDE.md` viene riscritto dal
riordino: se questo script leggesse il disco, alla seconda esecuzione archivierebbe **il file
gia' asciugato** e la storia sparirebbe in silenzio. La fonte e' quindi
**`git show regole-pre-riordino:CLAUDE.md`**, e lo script **si ferma** se il tag non c'e'.

**Che cosa archivia:** ogni sezione di `CLAUDE.md` PRIMA del riordino **tranne `par.9`**, che e'
gia' in `doc/FATTI_dal_codice.md` (punto `e` dello stesso mandato). Per ogni sezione dice
**dove vive oggi la regola**, cosi' l'archivio non diventa una seconda verita'.

    python csv/_riordino_storia.py            # scrive doc/STORIA_REGOLE.md
    python csv/_riordino_storia.py --verifica # solo il controllo, non scrive
    python csv/_riordino_storia.py --estrai <titolo>   # stampa UNA sezione dal tag

ASCII puro.
"""
import io
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Archivia prosa da un tag di git.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
USCITA = os.path.join(RADICE, "doc", "STORIA_REGOLE.md")
TAG = "regole-pre-riordino"
SALTA = "## 9. FATTI VERIFICATI DAL CODICE"

# dove vive OGGI la regola di ciascuna sezione: una riga per sezione, nessuna senza destinazione
DOVE_ORA = {
    "0-zero": "`CLAUDE.md` par.1 (il bersaglio)",
    "0.": "`CLAUDE.md` par.2 (ruolo e postura)",
    "0-bis": "`CLAUDE.md` par.0 (che cosa si legge all'avvio)",
    "0-ter": "i `P` si sono divisi: `P1`, `P1-bis`, `P1-quater`, `P2` in `CLAUDE.md`; "
             "`P1-sexies`, `P3`, `P4`, `P5`, `P6` in `doc/PATTERN_DI_PROVA.md`; "
             "`P1-ter` assorbita da `L-NUMERI`; `P1-quinquies` tolta (e' `A11`)",
    "1.": "`CLAUDE.md` par.3 (un interruttore alla volta)",
    "2.": "`doc/PATTERN_DI_PROVA.md`, la lista di controllo di un sigillo",
    "3.": "`doc/ASSIOMI.md` `A1` (la legge, non il numero)",
    "4.": "`doc/REGISTRO_FISICA.md` (sono fisica, non flusso di lavoro)",
    "5.": "`CLAUDE.md` par.5 (politiche di commit), asciugata",
    "5-novies": "`CLAUDE.md` par.6 punto 3; la fisica e' gia' automatica (`H-REG-R`)",
    "5-bis": "assorbita dall'indice (`doc/INDICE_ID.tsv`) e dal suo validatore",
    "5-quinquies": "`CLAUDE.md` par.7 (il codice di una misura si recupera)",
    "5-octies": "`CLAUDE.md` par.4 (la regola unica della relazione)",
    "5-quater": "assorbito dall'indice: i fronti sono voci di `doc/INDICE_ID.tsv`",
    "5-ter": "`CLAUDE.md` par.4 (la regola unica della relazione)",
    "5-sexies": "`CLAUDE.md` par.4 (la regola unica della relazione)",
    "5-septies": "`CLAUDE.md` par.8 (il task history)",
    "6.": "`doc/STATO_RUN.md` (e' STATO, non una regola)",
    "7.": "`CLAUDE.md` par.0 (l'elenco dei documenti)",
    "8.": "`CLAUDE.md` par.10 (il principio guida)",
    "9-bis": "`doc/PATTERN_DI_PROVA.md`, fusa dentro `P3` (un numero porta la sua epoca)",
    "10.": "`doc/COMPONENTI_PROMOSSE.md` (il criterio vive dove vive il registro)",
    "11.": "`CLAUDE.md` par.9 (l'indice dei difetti)",
}


def dal_tag(percorso):
    q = subprocess.run(["git", "show", "%s:%s" % (TAG, percorso)], cwd=RADICE,
                       capture_output=True)
    if q.returncode:
        raise SystemExit("il tag %s non esiste, o non contiene %s: %s"
                         % (TAG, percorso, (q.stderr or b"").decode("utf-8", "replace")[:200]))
    return q.stdout.decode("utf-8")


def sezioni(testo):
    """Taglia il documento sui titoli di secondo livello. Restituisce [(titolo, righe)]."""
    righe = testo.split(NL)
    tagli = [i for i, r in enumerate(righe) if r.startswith("## ")]
    fuori = [("(intestazione)", righe[:tagli[0]])] if tagli and tagli[0] else []
    for k, i in enumerate(tagli):
        j = tagli[k + 1] if k + 1 < len(tagli) else len(righe)
        fuori.append((righe[i], righe[i:j]))
    return fuori


def chiave(titolo):
    """Da '## 5-quinquies. IL CODICE ...' a '5-quinquies'; da '## 0. RUOLO' a '0.'."""
    t = titolo[3:].strip()
    testa = t.split(" ")[0]
    for c in (testa, testa.rstrip("."), testa.rstrip(".") + "."):
        if c in DOVE_ORA:
            return c
    return testa


def costruisci():
    testo = dal_tag("CLAUDE.md")
    tutte = sezioni(testo)
    fuori = []
    fuori.append("# LA STORIA DELLE REGOLE - **archivio verbatim, PRIMA del riordino "
                 "del 2026-09-26**")
    fuori.append("")
    fuori.append("> **NON SI LEGGE ALL'AVVIO.** Si apre quando serve sapere **da quale errore "
                 "una regola e' nata** - il *perche'*, che `CLAUDE.md` non porta piu'.")
    fuori.append(">")
    fuori.append("> **La fonte e' il tag `%s`** (`git show %s:CLAUDE.md`), **non il disco**: "
                 "il disco e' stato riscritto dal riordino." % (TAG, TAG))
    fuori.append("> *(Generato da `csv/_riordino_storia.py`.)*")
    fuori.append(">")
    fuori.append("> **`par.9` NON e' qui:** i fatti dal codice stanno in "
                 "`doc/FATTI_dal_codice.md`, ordinati per funzione.")
    fuori.append("")
    fuori.append("| sezione di allora | dove vive OGGI la sua regola |")
    fuori.append("|---|---|")
    senza = []
    tenute = []
    for tit, righe in tutte:
        if tit.startswith(SALTA):
            continue
        if tit == "(intestazione)":
            tenute.append((tit, righe))
            continue
        k = chiave(tit)
        if k not in DOVE_ORA:
            senza.append(tit)
        # l'etichetta e' l'ID della sezione (`par.0-ter`), non il titolo: cosi' il rimando e'
        #   LETTERALE e un controllo che cerca `par.0-ter` lo trova (`STANDARD 9`).
        fuori.append("| **par.%s** — %s | %s |"
                     % (k.rstrip("."), tit[3:].split(".", 1)[-1].split("(")[0].strip()[:52],
                        DOVE_ORA.get(k, "**SENZA DESTINAZIONE**")))
        tenute.append((tit, righe))
    fuori.append("")
    fuori.append("---")
    fuori.append("")
    for tit, righe in tenute:
        fuori.extend(righe)
        fuori.append("")
    t = NL.join(fuori).rstrip(NL) + NL
    # UNA sostituzione, asserita PER SE' (`P1-quater`): il `par.5-quinquies` di allora conteneva
    # un byte NUL VERO dentro la formula di `git hash-object`. Un NUL fa dichiarare BINARIO il
    # file a `grep`, e un presidio che ci passa sopra **non trova piu' niente**: qui diventa
    # visibile come due caratteri.
    n_nul = t.count(chr(0))
    if n_nul != 1:
        raise SystemExit("byte NUL attesi 1, trovati %d: l'ancora non e' unica" % n_nul)
    t = t.replace(chr(0), chr(92) + "0")
    return t, testo, senza


def perse(nuovo, originale):
    dentro = set(nuovo.split(NL))
    fuori = []
    dentro9 = False
    for r in originale.replace(chr(0), chr(92) + "0").split(NL):
        if r.startswith(SALTA):
            dentro9 = True
        elif dentro9 and r.startswith("## "):
            dentro9 = False
        if dentro9 or not r.strip():
            continue
        if r not in dentro:
            fuori.append(r)
    return fuori


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--estrai" in a:
        cerca = a[a.index("--estrai") + 1]
        for tit, righe in sezioni(dal_tag("CLAUDE.md")):
            if tit.startswith("## " + cerca):
                print(NL.join(righe))
                sys.exit(0)
        sys.exit("sezione non trovata nel tag: %s" % cerca)
    nuovo, originale, senza = costruisci()
    mancanti = perse(nuovo, originale)
    print("=" * 92)
    print("CLAUDE.md (tag %s) -> doc/STORIA_REGOLE.md" % TAG)
    print("=" * 92)
    print("  righe di CLAUDE.md al tag ...... %d" % originale.count(NL))
    print("  sezioni archiviate ............. %d" % (nuovo.count(NL + "## ")))
    print("  sezioni SENZA destinazione ..... %d %s"
          % (len(senza), (", ".join(senza)[:70] if senza else "")))
    print("  righe NON RITROVATE (par.9 escluso) %d" % len(mancanti))
    for r in mancanti[:8]:
        print("      %s" % r[:88])
    if mancanti or senza:
        sys.exit(1)
    if "--verifica" not in a:
        io.open(USCITA, "w", encoding="utf-8", newline=NL).write(nuovo)
        print("  SCRITTO doc/STORIA_REGOLE.md (%d righe)" % nuovo.count(NL))
    sys.exit(0)
