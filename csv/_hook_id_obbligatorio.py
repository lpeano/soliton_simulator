# -*- coding: utf-8 -*-
"""IMPEDIMENTO `H-ID-OBBLIGATORIO` — **un commit che tocca la fisica o un referto CITA un ID.**

> ### ⛔ **IL ROVESCIO DI `H-INDICE`.** `H-INDICE` controlla che gli ID citati ### **esistano**;
> questo controlla che ### **ce ne sia almeno UNO** — e solo per i commit che contano:
>
> | tocca | perché |
> |---|---|
> | ### **un file della LISTA** di `csv/_file_fisica.py` | la fisica cambia, e ### **ogni cambio di fisica ha una voce** che lo spiega: senza un ID, il commit dice *«ho cambiato una legge»* ### **e non dice quale problema stava risolvendo** |
> | ### **un `doc/REFERTO_*` o `doc/REPERTO_*`** | un referto ### **è la risposta a una domanda**, e la domanda ### **è una voce.** Un referto che non cita niente è ### **una misura senza committente** |
>
> ### 📌 **E «un referto sotto `doc/`» vuol dire SOLO `doc/REFERTO_*` e `doc/REPERTO_*`**, non
> qualunque file sotto `doc/` — ### **la correzione `C` della coda del 2026-10-09**, e la mia
> definizione era ### **larga.**

**LA VIA D'USCITA OBBLIGA A DICHIARARE:** ### **`[SENZA-INDICE: <motivo>]`** nel messaggio,
### **a inizio riga** — la stessa di `H-INDICE`, e di proposito: ### **chi dichiara di non
avere ID da citare lo dichiara UNA volta.**

Gira con:  python csv/_hook_id_obbligatorio.py --controlla <file-del-messaggio>
           python csv/_hook_id_obbligatorio.py --collaudo
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
# ### ⛔ **I REFERTI SONO SOLO QUESTI DUE PREFISSI**, e lo dice la correzione `C` della coda:
# ### *<<un referto sotto `doc/` vuol dire SOLO i file `doc/REFERTO_*` e `doc/REPERTO_*`, non
# ### qualunque file sotto `doc/`>>*. ### ⚠ **La mia definizione era LARGA**, e una definizione
# ### larga in un presidio ### **rifiuta commit che nessuno voleva rifiutare.**
REFERTI = re.compile(r"^doc/(REFERTO|REPERTO)_")
FUGA = re.compile(r"^\[SENZA-INDICE:\s*(.+?)\]", re.M)


def toccati():
    q = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return [r.strip().replace(chr(92), "/") for r in (q.stdout or "").split(NL) if r.strip()]


def perche_conta(percorsi):
    """### Perche' questo commit deve citare un ID, o ### **`[]` se non deve.**"""
    import _file_fisica as FF
    fuori = []
    for p in percorsi:
        if FF.e_di_fisica(p):
            fuori.append((p, "e- un FILE DI FISICA della LISTA"))
        elif REFERTI.match(p):
            fuori.append((p, "e- un REFERTO (`doc/REFERTO_*` o `doc/REPERTO_*`)"))
    return fuori


def cita_un_id(testo):
    """### Gli ID ### **noti all'indice** citati nel testo.

    ### ⭐ **Si riusa `esamina` di `H-INDICE`**, al rovescio: la- gli ignoti sono il difetto,
    qui ### **i NOTI sono la prova.** ### ⛔ **Due presidi che leggono la stessa forma di ID
    con due parser diversi divergono**, ed e- il difetto che ho appena pagato sul
    `superata_da`.
    """
    import _presidio_indice as PI
    noti, escl, amb = PI.carica()
    del escl
    fuori = set()
    for m in PI.FORMA.finditer(testo or ""):
        t = PI._ripulisci(m.group(0))
        if t and (t in noti or t in amb):
            fuori.add(t)
    return sorted(fuori)


def controlla(msg_file):
    percorsi = toccati()
    conta = perche_conta(percorsi)
    if not conta:
        return 0
    msg = ""
    if msg_file and os.path.exists(msg_file):
        msg = io.open(msg_file, encoding="utf-8", errors="replace").read()
    m = FUGA.search(msg)
    if m:
        sys.stderr.write("[H-ID-OBBLIGATORIO] eccezione DICHIARATA a inizio riga: %s"
                         % m.group(1).strip()[:90] + NL)
        return 0
    ids = cita_un_id(msg)
    if ids:
        return 0
    sys.stderr.write(NL + "[H-ID-OBBLIGATORIO] *** COMMIT RIFIUTATO ***" + NL + NL)
    sys.stderr.write("  Questo commit tocca:" + NL)
    for p, che in conta[:12]:
        sys.stderr.write("    %-46s %s" % (p, che) + NL)
    sys.stderr.write(NL + "  e il messaggio NON CITA NESSUN ID dell-indice." + NL + NL
                     + "  PERCHE- CONTA: la fisica che cambia ha UNA VOCE che la spiega, e un"
                     " referto e- LA RISPOSTA" + NL
                     + "  A UNA DOMANDA -- e la domanda e- una voce. Un commit che cambia una"
                     " legge senza citare" + NL
                     + "  un ID dice <<ho cambiato una legge>> e NON dice quale problema stava"
                     " risolvendo." + NL + NL
                     + "  CHE FARE, una delle due:" + NL
                     + "    1. citare l-ID della voce che questo lavoro riguarda;" + NL
                     + "    2. dichiarare, A INIZIO RIGA: [SENZA-INDICE: <motivo>]" + NL + NL)
    return 1


# =====================================================================================
#   IL COLLAUDO, nei due versi
# =====================================================================================

def collaudo():
    import _presidio
    _presidio.avvia(__file__)
    import _file_fisica as FF
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("COLLAUDO `H-ID-OBBLIGATORIO` -- nei DUE VERSI")
    print("=" * 100)
    sim = FF.FILE_FISICA[0]
    # ### ⛔ **UN ID VERO E UNO IGNOTO**: il vero si prende dall-indice ### **a run time**,
    # ### e l-ignoto e- ### **la sentinella di `H-INDICE`**, scelta a run time e
    # ### ### **verificata ignota** -- perche- una sentinella scritta nel codice
    # ### ### **finisce nei referti e diventa un ID noto** *(e- successo due volte)*.
    import _presidio_indice as PI
    noti, _escl, _amb = PI.carica()
    vero = "A9" if "A9" in noti else sorted(noti)[0]
    ignoto = PI.sentinella()
    print("  un ID VERO: `%s`   |   uno IGNOTO (scelto a run time): `%s`" % (vero, ignoto))
    print()
    print("  (a) QUALI COMMIT CONTANO")
    esito("### CONTA: un file della LISTA di fisica",
          perche_conta([sim]) != [], sim)
    esito("### CONTA: un `doc/REFERTO_*`",
          perche_conta(["doc/REFERTO_qualcosa.md"]) != [])
    esito("### CONTA: un `doc/REPERTO_*`",
          perche_conta(["doc/REPERTO_qualcosa.md"]) != [])
    esito("NON conta: un ALTRO file sotto `doc/`",
          perche_conta(["doc/STATO_RUN.md", "doc/REGOLE/par9.md",
                        "doc/indice/voci.jsonl"]) == [],
          "la correzione `C`: la mia definizione era LARGA")
    esito("NON conta: un file di `csv/`",
          perche_conta(["csv/indice.py", "csv/_file_fisica.py"]) == [])
    esito("NON conta: un `.py` che SOMIGLIA al simulatore ma non e- nella LISTA",
          perche_conta(["soliton_simulator_copia.py", "a/soliton_simulator.py"]) == [],
          "e- la LISTA a decidere, non il nome")
    print()
    print("  (b) IL MESSAGGIO")
    esito("### DEVE rifiutare: nessun ID citato",
          cita_un_id("un messaggio senza ID, e nemmeno una parola maiuscola") == [])
    esito("NON deve rifiutare: un ID VERO citato",
          cita_un_id("questo commit riguarda `%s`, e lo cita" % vero) != [])
    esito("### DEVE rifiutare: SOLO un ID IGNOTO citato",
          cita_un_id("cito `%s`, che non e- una voce" % ignoto) == [],
          "un ID inventato NON vale come citazione")
    esito("NON deve rifiutare: la VIA D-USCITA a inizio riga",
          FUGA.search("prima riga" + NL + "[SENZA-INDICE: nessuna voce riguarda questo]")
          is not None)
    esito("### DEVE rifiutare: la via d-uscita NON a inizio riga",
          FUGA.search("testo [SENZA-INDICE: furbata] in mezzo alla riga") is None,
          "la stessa regola di `H-INDICE` e di `H-NON-TRACCIATI`")
    print("=" * 100)
    print("COLLAUDO `H-ID-OBBLIGATORIO`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(a):
    if "--collaudo" in a:
        return collaudo()
    if "--controlla" in a:
        k = a.index("--controlla")
        return controlla(a[k + 1] if k + 1 < len(a) else "")
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
