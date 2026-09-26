r"""**PRESIDIO DELL'INDICE** — ogni ID **aggiunto** da un commit esiste in `doc/INDICE_ID.tsv`.

**Ordine di Luca, 2026-09-26** *(`PASSO 2`)*: *«ogni ID citato in un documento vivo o in un commit
NUOVO esiste nell'indice (come id o alias)»*.

## CHE COSA GUARDA, ed e' la scelta che lo rende usabile

```
LE RIGHE AGGIUNTE dal commit ai documenti VIVI   (git diff --cached -U0, righe che cominciano con +)
IL MESSAGGIO del commit                          (in modalita' `--commit-msg <file>`)
```

**Solo cio' che il commit AGGIUNGE.** Un presidio che guardasse i file interi rifiuterebbe **ogni**
commit finche' l'indice non e' perfetto, e verrebbe aggirato il primo giorno *(`A9`: un presidio
aggirato non e' un presidio)*. **Cosi' invece il debito vecchio resta visibile nell'indice, e il
debito NUOVO non si crea.**

## TRE ESITI, non due

```
NOTO        l'ID e' nell'indice come `id` o come `alias`                       -> passa
ESCLUSO     e' in `doc/INDICE_ID_ESCLUSI.tsv` (non e' un identificatore)       -> passa
AMBIGUO     la forma NUDA di un ID con namespace, definita da DUE registri     -> AVVISA e RIFIUTA
IGNOTO      non e' in nessuno dei due                                          -> RIFIUTA
```

**L'`AMBIGUO` e' il servizio vero:** se `V8` e' definito **sia** in una scheda **sia** altrove, la
forma nuda non ha un alias, e il presidio **lo dice** invece di scegliere per conto proprio.

**LA VIA D'USCITA ESISTE E OBBLIGA A DICHIARARE:** `[SENZA-INDICE: <motivo>]` nel messaggio di
commit — stessa forma di `[SENZA-RELAZIONE: ...]`. **Un'eccezione resta possibile, ma lascia una
traccia leggibile in `git log`.**

**COLLAUDO NEI DUE VERSI:** `python csv/_presidio_indice.py --collaudo`.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. E' un presidio su documenti.
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
INDICE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
ESCLUSI = os.path.join(RADICE, "doc", "INDICE_ID_ESCLUSI.tsv")
NL = chr(10)
TAB = chr(9)

VIVI = ["doc/STATO_RUN.md", "doc/RAMIFICAZIONI.md", "doc/ASSIOMI.md", "doc/REGISTRO_FISICA.md",
        "doc/COMPONENTI_PROMOSSE.md", "doc/PATTERN_DI_PROVA.md", "doc/LISTA_CHIUSA.md",
        "CLAUDE.md"]
FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]{2,}(?:-[A-Z0-9()/]+)+)")


def carica():
    """`(noti, esclusi, ambigue)`: gli id e gli alias, le forme escluse, le forme nude ambigue."""
    noti, ambigue = set(), set()
    nudo_a = {}
    for k, riga in enumerate(io.open(INDICE, encoding="utf-8", newline="").read().split(NL)):
        if k == 0 or not riga.strip():
            continue
        c = riga.split(TAB)
        noti.add(c[0])
        if c[1]:
            noti |= set(x for x in c[1].split(",") if x)
        if ":" in c[0]:
            nudo = c[0].split(":", 1)[1]
            nudo_a.setdefault(nudo, []).append(c[0])
    for nudo, chiavi in nudo_a.items():
        if len(chiavi) > 1 and nudo not in noti:
            ambigue.add(nudo)
    escl = set()
    for k, riga in enumerate(io.open(ESCLUSI, encoding="utf-8", newline="").read().split(NL)):
        if k and riga.strip():
            escl.add(riga.split(TAB)[0])
    return noti, escl, ambigue


def esamina(testo):
    """Gli ID di un testo, divisi in `(ignoti, ambigui)`."""
    noti, escl, amb = carica()
    ign, ambi = set(), set()
    for m in FORMA.finditer(testo or ""):
        t = m.group(0)
        if t in noti or t in escl:
            continue
        if t in amb:
            ambi.add(t)
        else:
            ign.add(t)
    return sorted(ign), sorted(ambi)


def _aggiunte():
    q = subprocess.run(["git", "diff", "--cached", "-U0", "--"] + VIVI,
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return NL.join(r[1:] for r in (q.stdout or "").split(NL)
                   if r.startswith("+") and not r.startswith("+++"))


def pre_commit(msg_file=None):
    testo = _aggiunte()
    msg = ""
    if msg_file and os.path.exists(msg_file):
        msg = io.open(msg_file, encoding="utf-8", errors="replace").read()
        if "[SENZA-INDICE:" in msg:
            sys.stderr.write("[INDICE] eccezione DICHIARATA nel messaggio: non controllo." + NL)
            return 0
        testo += NL + msg
    ign, ambi = esamina(testo)
    if not ign and not ambi:
        return 0
    sys.stderr.write(NL + "[INDICE] *** COMMIT RIFIUTATO ***" + NL + NL)
    if ign:
        sys.stderr.write("  ID che il commit AGGIUNGE e che NON sono nell'indice (%d):" % len(ign)
                         + NL + "    " + ", ".join(ign[:30]) + NL + NL)
    if ambi:
        sys.stderr.write("  forme NUDE AMBIGUE (definite da piu' registri, senza alias) (%d):"
                         % len(ambi) + NL + "    " + ", ".join(ambi[:30]) + NL
                         + "    -> si citano col namespace (`REGISTRO_FISICA:V8`)" + NL + NL)
    sys.stderr.write("  CHE FARE, una delle tre:" + NL
                     + "    1. definire la voce in un registro e rigenerare:"
                     + "  python csv/_indice_id.py" + NL
                     + "    2. se non e' un identificatore: aggiungerla a"
                     + " doc/INDICE_ID_ESCLUSI.tsv col motivo" + NL
                     + "    3. dichiarare l'eccezione nel messaggio: [SENZA-INDICE: <motivo>]"
                     + NL + NL)
    return 1


def collaudo():
    _presidio.avvia(__file__)
    noti, escl, amb = carica()
    R = []

    def P(s=""):
        R.append(s)
        print(s)

    P("=" * 96)
    P("COLLAUDO DEL PRESIDIO DELL'INDICE -- i DUE versi   (2026-09-26)")
    P("=" * 96)
    P()
    P("  indice: %d fra id e alias      esclusi: %d      forme nude AMBIGUE: %d"
      % (len(noti), len(escl), len(amb)))
    P()
    _un_noto = sorted(x for x in noti if re.fullmatch(r"D\d\d", x))[:1]
    _un_escl = sorted(escl)[:1]
    casi = [
        ("DEVE PASSARE", "un ID noto: `%s`" % (_un_noto[0] if _un_noto else "D01"),
         "la riga cita `%s` e basta" % (_un_noto[0] if _un_noto else "D01"), True),
        ("DEVE PASSARE", "una forma ESCLUSA: `%s`" % (_un_escl[0] if _un_escl else "BYTE-INERTE"),
         "il commit dice %s" % (_un_escl[0] if _un_escl else "BYTE-INERTE"), True),
        ("DEVE FALLIRE", "un ID inventato: `ZZ999`", "questa riga cita ZZ999, che non esiste",
         False),
        ("DEVE FALLIRE", "un difetto plausibile ma assente: `D97`",
         "il difetto D97 sarebbe nuovo", False),
    ]
    esiti = []
    for atteso, che, testo, deve_passare in casi:
        ign, ambi = esamina(testo)
        passa = not ign and not ambi
        ok = (passa == deve_passare)
        esiti.append(ok)
        P("  %-13s %-42s -> %-8s %s"
          % (atteso, che, "passa" if passa else "RIFIUTA", "PASS" if ok else "FAIL"))
        if ign:
            P("                  ignoti: %s" % ", ".join(ign[:6]))
    P()
    # ---------------------------------------------------------------- il ramo END-TO-END
    #   Provare la FUNZIONE non prova il HOOK: fra i due c'e' `git diff --cached`, ed e' la' che un
    #   presidio si spegne in silenzio. Qui si scrive una riga con un ID inventato in un documento
    #   VIVO **generato** (`LISTA_CHIUSA`, che si rigenera), si mette in stage, si chiama il hook
    #   VERO, e poi si ripristina verificando lo sha1.
    import hashlib
    import shutil
    _vivo = os.path.join(RADICE, "doc", "LISTA_CHIUSA.md")
    _sha0 = hashlib.sha1(io.open(_vivo, "rb").read()).hexdigest()
    _st = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=RADICE,
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if (_st.stdout or "").strip():
        P("  END-TO-END NON ESEGUITO: c'erano modifiche in STAGE, e non le tocco.")
        P("    (lo dichiaro invece di dare per buono un ramo che non ho provato.)")
        _ok_e2e = None
    else:
        shutil.copy(_vivo, _vivo + ".collaudo.bak")
        try:
            with io.open(_vivo, "a", encoding="utf-8", newline=NL) as _f:
                _f.write(NL + "<!-- collaudo del presidio: QQ777 non esiste -->" + NL)
            subprocess.run(["git", "add", "--", "doc/LISTA_CHIUSA.md"], cwd=RADICE,
                           capture_output=True, text=True)
            _h = subprocess.run([sys.executable, os.path.join(RADICE, "csv", "_hook_presidi.py"),
                                 "--pre-commit"], cwd=RADICE, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
        finally:
            subprocess.run(["git", "reset", "-q", "--", "doc/LISTA_CHIUSA.md"], cwd=RADICE,
                           capture_output=True, text=True)
            shutil.move(_vivo + ".collaudo.bak", _vivo)
        _sha1 = hashlib.sha1(io.open(_vivo, "rb").read()).hexdigest()
        _visto = "QQ777" in (_h.stderr or "") or "Q777" in (_h.stderr or "")
        _ok_e2e = (_h.returncode == 1 and _visto and _sha1 == _sha0)
        P("  DEVE FALLIRE  il HOOK VERO su una riga con `QQ777`     -> uscita %d, ID segnalato %s"
          % (_h.returncode, _visto))
        P("                il documento e' tornato identico: %s" % (_sha1 == _sha0))
        P("                esito: %s" % ("PASS" if _ok_e2e else "FAIL"))
        esiti.append(_ok_e2e)
    P()
    _tutto = all(x for x in esiti if x is not None)
    P("  ESITO: %s" % ("%d/%d PASS -- il presidio IMPEDISCE e non solo avvisa"
                       % (len(esiti), len(esiti)) if _tutto else "FAIL"))
    P()
    P("COSA QUESTO COLLAUDO *NON* DICE:")
    P("  - **non dice che l'indice sia completo**: dice che un ID FUORI dall'indice viene")
    P("    RIFIUTATO e uno DENTRO passa.")
    P("  - il presidio guarda **solo le righe AGGIUNTE** ai documenti vivi e il messaggio: il")
    P("    debito vecchio resta visibile nell'indice, e **non blocca ogni commit**. E' una scelta,")
    P("    e senza di essa il presidio verrebbe aggirato il primo giorno (`A9`).")
    io.open(os.path.join(RADICE, "doc", "COLLAUDO_presidio_indice.txt"), "w",
            encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    return 0 if _tutto else 1


if __name__ == "__main__":
    if "--collaudo" in sys.argv:
        sys.exit(collaudo())
    if "--commit-msg" in sys.argv:
        i = sys.argv.index("--commit-msg")
        sys.exit(pre_commit(sys.argv[i + 1] if len(sys.argv) > i + 1 else None))
    if "--pre-commit" in sys.argv:
        sys.exit(pre_commit())
    _presidio.avvia(__file__)
    print(__doc__.split("##")[0].strip())
    sys.exit(0)
