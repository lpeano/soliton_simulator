# -*- coding: utf-8 -*-
"""**`RELAZIONE_PER_CLAUDE.md` -> UN FILE PER GIORNO in `doc/relazioni/`**
*(mandato di Luca 2026-09-26, punto `g`)*.

**Perche' non e' estetica:** la relazione e' il file che una sessione nuova legge **per primo**,
e a **20436 righe non la legge nessuno per intero** -- quindi il suo scopo e' **gia' perso**.
Il file vivo tiene **solo il giorno corrente**; i giorni chiusi stanno in
`doc/relazioni/<AAAA-MM-GG>.md`, e `git log` resta l'indice.

**LA REGOLA DI TAGLIO, dichiarata perche' il taglio e' un GIUDIZIO e non una misura:**

* si taglia su **ogni intestazione (`#` o `##`) che CONTIENE una data** `20\\d\\d-\\d\\d-\\d\\d`;
* il pezzo che segue appartiene a **quella** data, **fino al taglio successivo**;
* cio' che precede il **primo** taglio e' il **preambolo** e resta nel file vivo, perche' dice
  **come si legge** la relazione, non che cosa e' successo un giorno;
* **il blocco dell'INDICE DELL'ARCHIVIO si SCARTA prima di tagliare, e si RIGENERA.** Quel blocco
  lo scrive questo script, la sua intestazione **contiene una data** *("il file vivo tiene SOLO
  <giorno>")*, e quindi **senza questa regola il taglio lo manderebbe dentro un GIORNO**: l'indice
  di come si legge la relazione finirebbe archiviato come se fosse un fatto di quel giorno.
  ### **Se il blocco non si trova, o se se ne trova piu' d'uno, lo script SI FERMA** -- un indice
  duplicato in silenzio sarebbe peggio di un errore (`A9`);
* **le righe dei giorni GIA' archiviati si CONSERVANO alla lettera**, prese dalla tabella vecchia:
  quei file non si riscrivono, quindi **il loro conteggio non si ricalcola** *(ricalcolarlo da un
  file con l'intestazione d'archivio darebbe un numero diverso da quello che il giorno aveva, e
  sarebbe un numero inventato: `L-NUMERI`)*;
* **una riga non si riscrive e non si perde:** un controllo confronta le righe in ingresso con
  la somma di quelle in uscita **piu' le righe dell'indice scartato**, e lo script **si ferma**
  se non torna.

    python csv/_archivio_relazioni.py --oggi=2026-10-02            # archivia e asciuga il file vivo
    python csv/_archivio_relazioni.py --oggi=2026-10-02 --verifica  # misura e basta, non tocca niente

**`--oggi` dice QUALE giorno resta nel file vivo**, ed e' obbligatorio: ### **senza, il giorno
corrente lo deciderebbe l'orologio della macchina**, e un archivio che dipende da quando lo si
lancia non e' riproducibile. ASCII puro.
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Divide un documento per giorno.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
VIVO = os.path.join(RADICE, "RELAZIONE_PER_CLAUDE.md")
ARCHIVIO = os.path.join(RADICE, "doc", "relazioni")
DATA = re.compile(r"20\d\d-\d\d-\d\d")
CAPO_INDICE = "## L'ARCHIVIO PER GIORNO"
RIGA_TABELLA = re.compile(r"^\| `(20\d\d-\d\d-\d\d)` \| +(\d+) \|")


def scarta_indice(righe):
    """Toglie il BLOCCO DELL'INDICE che questo script genera, e ne restituisce le righe.

    Si ferma se i blocchi non sono esattamente UNO: zero vuol dire che il formato e' cambiato
    sotto i piedi, piu' d'uno vuol dire che un giro precedente l'ha duplicato -- e in entrambi i
    casi tacere produrrebbe un archivio sbagliato in silenzio (`A9`).
    Restituisce `(righe_senza_indice, righe_dell_indice, {giorno: conteggio})`.
    """
    capi = [i for i, r in enumerate(righe) if r.startswith(CAPO_INDICE)]
    if len(capi) != 1:
        raise SystemExit("** blocchi di indice trovati: %d (atteso 1). NON TOCCO NIENTE. **"
                         % len(capi))
    i = capi[0]
    fine = None
    for k in range(i + 1, len(righe)):
        if righe[k].strip() == "---":
            fine = k
            break
    if fine is None:
        raise SystemExit("** l'indice non e' chiuso da un `---`. NON TOCCO NIENTE. **")
    blocco = righe[i:fine + 1]
    gia = {}
    for r in blocco:
        m = RIGA_TABELLA.match(r)
        if m:
            gia[m.group(1)] = int(m.group(2))
    return righe[:i] + righe[fine + 1:], blocco, gia


def dividi(testo):
    """[(giorno|None, righe)] -- il primo elemento e' il preambolo, con giorno `None`."""
    righe = testo.split(NL)
    tagli = []
    for i, r in enumerate(righe):
        if r.startswith("# ") or r.startswith("## "):
            m = DATA.search(r)
            if m:
                tagli.append((i, m.group(0)))
    pezzi = []
    if not tagli or tagli[0][0] > 0:
        pezzi.append((None, righe[:tagli[0][0] if tagli else len(righe)]))
    for k, (i, g) in enumerate(tagli):
        j = tagli[k + 1][0] if k + 1 < len(tagli) else len(righe)
        pezzi.append((g, righe[i:j]))
    return pezzi


def per_giorno(pezzi):
    d = {}
    for g, righe in pezzi:
        if g is None:
            continue
        d.setdefault(g, []).extend(righe)
    return d


def testa_viva(preambolo, giorni, gia, oggi):
    """Il file vivo: il preambolo + SOLO il giorno corrente + l'indice dell'archivio.

    `gia` sono i conteggi dei giorni archiviati nei giri PRECEDENTI, letti dalla tabella vecchia:
    si ricopiano **alla lettera**, perche' quei file non si riscrivono in questo giro e il loro
    numero lo ha prodotto il giro che li ha staccati.
    """
    fuori = list(preambolo)
    while fuori and not fuori[-1].strip():
        fuori.pop()
    if fuori and fuori[-1].strip() == "---":
        fuori.pop()        # il separatore lo riscrive la riga qui sotto: senno' a ogni rilancio
        while fuori and not fuori[-1].strip():   # ne cresce uno in piu' (misurato: `---` doppio)
            fuori.pop()
    righe_tab = dict(gia)
    for g in giorni:
        if g != oggi:
            righe_tab[g] = len(giorni[g])
    fuori += ["", "---", "",
              "%s - **il file vivo tiene SOLO %s**" % (CAPO_INDICE, oggi), "",
              "> **Regola di Luca, 2026-09-26.** A 20436 righe questo file non lo leggeva "
              "nessuno per intero, **quindi il suo scopo era gia' perso**. I giorni chiusi "
              "stanno in `doc/relazioni/`, uno per giorno, e `git log` resta l'indice.",
              "> *(Diviso da `csv/_archivio_relazioni.py`, che dichiara la regola di taglio.)*",
              "", "| giorno | righe | file |", "|---|--:|---|"]
    for g in sorted(righe_tab):
        fuori.append("| `%s` | %d | [`doc/relazioni/%s.md`](doc/relazioni/%s.md) |"
                     % (g, righe_tab[g], g, g))
    fuori += ["", "---", ""]
    fuori += giorni.get(oggi, ["*(nessuna voce ancora per oggi)*"])
    return NL.join(fuori).rstrip(NL) + NL


if __name__ == "__main__":
    argv = sys.argv[1:]
    solo = "--verifica" in argv
    oggi = None
    for a in argv:
        if a.startswith("--oggi="):
            oggi = a.split("=", 1)[1].strip()
    if oggi is None or not DATA.fullmatch(oggi):
        raise SystemExit("USO: python csv/_archivio_relazioni.py --oggi=AAAA-MM-GG [--verifica]"
                         + NL + "  `--oggi` e' OBBLIGATORIO: il giorno corrente non lo decide"
                         + NL + "  l'orologio della macchina, senno' l'archivio non e'"
                         + NL + "  riproducibile.")
    testo = io.open(VIVO, encoding="utf-8").read()
    righe_tutte = testo.split(NL)
    righe, blocco_indice, gia = scarta_indice(righe_tutte)
    pezzi = dividi(NL.join(righe))
    preambolo = pezzi[0][1] if pezzi and pezzi[0][0] is None else []
    giorni = per_giorno(pezzi)
    n_in = len(righe_tutte)      # elementi del taglio: la somma delle uscite conta cosi'
    n_out = len(preambolo) + len(blocco_indice) + sum(len(v) for v in giorni.values())
    print("=" * 92)
    print("RELAZIONE_PER_CLAUDE.md -> doc/relazioni/<giorno>.md     (oggi = %s)" % oggi)
    print("=" * 92)
    print("  righe in ingresso .............. %d" % n_in)
    print("  righe di preambolo (restano) ... %d" % len(preambolo))
    print("  righe dell'indice SCARTATO ..... %d   (si RIGENERA, non si archivia)"
          % len(blocco_indice))
    print("  giorni gia' archiviati prima ... %d   %s" % (len(gia), " ".join(sorted(gia))))
    print("  giorni riconosciuti ............ %d" % len(giorni))
    for g in sorted(giorni):
        print("      %s  %6d righe%s" % (g, len(giorni[g]),
                                         "   <- OGGI, resta nel file vivo" if g == oggi else ""))
    print("  righe in uscita (somma) ........ %d" % n_out)
    if n_in != n_out:
        print("  ** NON TORNA: %d righe di differenza **" % (n_in - n_out))
        sys.exit(1)
    if solo:
        sys.exit(0)
    if not os.path.isdir(ARCHIVIO):
        os.makedirs(ARCHIVIO)
    for g in sorted(giorni):
        if g == oggi:
            continue
        cap = ["# RELAZIONE - **%s**" % g, "",
               "> *(Archivio: staccato da `RELAZIONE_PER_CLAUDE.md` il %s da "
               "`csv/_archivio_relazioni.py`. **Verbatim**, nessuna riga riscritta.)*" % oggi, ""]
        io.open(os.path.join(ARCHIVIO, "%s.md" % g), "w", encoding="utf-8",
                newline=NL).write(NL.join(cap + giorni[g]).rstrip(NL) + NL)
    nuovo = testa_viva(preambolo, giorni, gia, oggi)
    io.open(VIVO, "w", encoding="utf-8", newline=NL).write(nuovo)
    print("  SCRITTI %d file in doc/relazioni/" % (len(giorni) - (1 if oggi in giorni else 0)))
    print("  RELAZIONE_PER_CLAUDE.md ora e' %d righe" % nuovo.count(NL))
    sys.exit(0)
