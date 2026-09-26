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
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. E' un presidio su documenti.
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
# ❌ LA FORMA CORRETTA il 2026-09-26, e due voci vere ne erano ESCLUSE:
#   `A3-DISEGNO` — nata dalla rinomina del `PASSO 1` — ha lo stem di **due** caratteri, e la
#   forma ne chiedeva **tre**; `FRAG1` ha **le cifre in coda** (`[A-Z]{2,}\d{1,3}`) e nessuna
#   alternativa la copriva. **Il collaudo della vista le ha trovate mancanti**, ed e' il
#   motivo per cui il collaudo si scrive prima.
#   ⚠ RESTA FUORI, dichiarato: un'etichetta di UNA SOLA PAROLA MAIUSCOLA senza cifre ne'
#   trattino (`CONTAGIO`) **non e' un ID in questo spazio** — e' la specifica di Luca
#   («nomi MAIUSCOLI col trattino»), e accettarla vorrebbe dire prendere ogni parola
#   maiuscola della prosa. **Quelle voci hanno bisogno di un ID, non di una regex piu'
#   larga.**
#   ⚠ LO STEM DI UNA LETTERA, ammesso il 2026-09-26. Senza, `L-DOPO-STOP` veniva
#   letto come `DOPO-STOP` -- cioe' il presidio segnalava come IGNOTO un pezzo di un
#   id che nell'indice C'E'. Misurato: 2 falsi ignoti su 6.
FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9()/]+)+|[A-Z]{2,}\d{1,3})")


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


TAB = chr(9)


def leggi_tsv(p):
    """`(colonne, righe)` di un TSV: serve al collaudo del punto 3, che aggiunge una riga vera."""
    r = io.open(p, encoding="utf-8", newline="").read().split(NL)
    return [c.strip() for c in r[0].split(TAB)], [x for x in r[1:] if x.strip()]


def _ripulisci(tok):
    """Toglie una parentesi che appartiene alla PROSA, non all'ID.

    ⚠ `()` sta nella forma per `INERZIA-1(C)`, ma cosi' `(LETTORI-INDICE)` veniva letto
    **con la parentesi attaccata** -- e il presidio segnalava un ID che non esiste, dentro un
    messaggio che citava una voce **presente** nell'indice. **Le parentesi devono essere
    BILANCIATE**: se il token finisce con `)` e non contiene `(`, la parentesi non e' sua.
    """
    while tok.endswith(")") and "(" not in tok:
        tok = tok[:-1]
    while tok.startswith("(") and ")" not in tok:
        tok = tok[1:]
    return tok


def esamina(testo):
    """Gli ID di un testo, divisi in `(ignoti, ambigui)`."""
    noti, escl, amb = carica()
    ign, ambi = set(), set()
    for m in FORMA.finditer(testo or ""):
        t = _ripulisci(m.group(0))
        if not t:
            continue
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
    # ❌❌ RIPIEGO RIMOSSO il 2026-09-26, ed era un difetto GRAVE: leggevo
    #   `.git/COMMIT_EDITMSG` in `pre-commit` credendo che git l'avesse gia' scritto. **NON e'
    #   vero: git lo scrive DOPO il `pre-commit`** *(l'ordine e' `pre-commit` -> `prepare-commit-msg`
    #   -> `commit-msg`)*, quindi leggevo **il messaggio del commit PRECEDENTE**. Un solo commit con
    #   `[SENZA-INDICE: ...]` **avrebbe spento il presidio per tutti i commit successivi**, fino al
    #   cambio di quel file. **L'ha trovato il collaudo end-to-end**, che e' esattamente il ramo che
    #   un presidio non deve saltare. Ora il controllo vive in **UN solo stadio: `commit-msg`**,
    #   dove il messaggio ESISTE e l'eccezione si puo' leggere.
    if msg_file and os.path.exists(msg_file):
        msg = io.open(msg_file, encoding="utf-8", errors="replace").read()
        if "[SENZA-INDICE:" in msg:
            sys.stderr.write("[H-INDICE] eccezione DICHIARATA nel messaggio: non controllo." + NL)
            return 0
        testo += NL + msg
    ign, ambi = esamina(testo)
    if not ign and not ambi:
        return 0
    sys.stderr.write(NL + "[H-INDICE] *** COMMIT RIFIUTATO ***" + NL + NL)
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


def sentinella():
    """Un ID che **non e' nell'indice**, scelto ORA.

    ⚠ UNA SENTINELLA SCRITTA NEL CODICE NON REGGE, e il perche' e' misurato **due volte**:
    `ZZ999` e' finito nel **referto** del collaudo, `QQ777` nella **relazione** -- e l'indice legge
    i referti e la relazione. Al giro dopo la sentinella **era un ID noto**, e i due casi che DEVONO
    fallire **passavano**. Saltare i propri referti non basta: **il racconto di un collaudo e' esso
    stesso un documento.** Percio' la sentinella si sceglie a run time e si **verifica** ignota.
    """
    for k in range(700, 999):
        cand = "QX%d" % k
        ign, _amb = esamina(cand)
        if ign:
            return cand
    raise RuntimeError("nessuna sentinella ignota fra QX700 e QX998: l'indice le contiene tutte")


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
    _sent = sentinella()
    _sent2 = sentinella.__wrapped__ if False else None
    for _k2 in range(700, 999):                  # una seconda sentinella, diversa dalla prima
        _c2 = "QX%d" % _k2
        if _c2 != _sent and esamina(_c2)[0]:
            _sent2 = _c2
            break
    P("  sentinelle scelte ORA e verificate ignote: `%s`, `%s`" % (_sent, _sent2))
    P()
    casi = [
        ("DEVE PASSARE", "un ID noto: `%s`" % (_un_noto[0] if _un_noto else "D01"),
         "la riga cita `%s` e basta" % (_un_noto[0] if _un_noto else "D01"), True),
        ("DEVE PASSARE", "una forma ESCLUSA: `%s`" % (_un_escl[0] if _un_escl else "BYTE-INERTE"),
         "il commit dice %s" % (_un_escl[0] if _un_escl else "BYTE-INERTE"), True),
        ("DEVE FALLIRE", "una sentinella ignota: `%s`" % _sent,
         "questa riga cita %s, che non esiste" % _sent, False),
        ("DEVE FALLIRE", "una seconda sentinella: `%s`" % _sent2,
         "e questa cita %s" % _sent2, False),
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
                _f.write(NL + "<!-- collaudo del presidio: %s non esiste -->" % _sent + NL)
            subprocess.run(["git", "add", "--", "doc/LISTA_CHIUSA.md"], cwd=RADICE,
                           capture_output=True, text=True)
            # il messaggio FINTO, senza eccezione dichiarata: e' il caso che DEVE fallire
            _msgf = os.path.join(RADICE, "doc", "_collaudo_msg.tmp")
            io.open(_msgf, "w", encoding="utf-8", newline=NL).write("collaudo" + NL)
            _h = subprocess.run([sys.executable, os.path.join(RADICE, "csv",
                                                              "_presidio_indice.py"),
                                 "--commit-msg", _msgf], cwd=RADICE, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
            os.remove(_msgf)
        finally:
            subprocess.run(["git", "reset", "-q", "--", "doc/LISTA_CHIUSA.md"], cwd=RADICE,
                           capture_output=True, text=True)
            shutil.move(_vivo + ".collaudo.bak", _vivo)
        _sha1 = hashlib.sha1(io.open(_vivo, "rb").read()).hexdigest()
        _visto = _sent in (_h.stderr or "") or _sent[1:] in (_h.stderr or "")
        _ok_e2e = (_h.returncode == 1 and _visto and _sha1 == _sha0)
        P("  DEVE FALLIRE  il HOOK VERO su una riga con `%s`      -> uscita %d, ID segnalato %s"
          % (_sent, _h.returncode, _visto))
        P("                il documento e' tornato identico: %s" % (_sha1 == _sha0))
        P("                esito: %s" % ("PASS" if _ok_e2e else "FAIL"))
        esiti.append(_ok_e2e)
    P()
    # ---------------------------------------------------------------- IL PUNTO 3 DEL MANDATO
    #   «un difetto nuovo si scrive come RIGA dell'indice; il hook rifiuta un ID nuovo in
    #   `STATO_RUN` che non ha la sua riga». Si prova NEI DUE VERSI, sul HOOK VERO, con backup e
    #   ripristino verificati per sha1.
    import shutil
    _sr = os.path.join(RADICE, "doc", "STATO_RUN.md")
    _ix = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
    _st2 = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=RADICE,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if (_st2.stdout or "").strip():
        P("  PUNTO 3 NON ESEGUITO: c'erano modifiche in STAGE, e non le tocco.")
        P("    (lo dichiaro invece di dare per buono un ramo che non ho provato.)")
    else:
        _id = _sent            # la sentinella: ignota per costruzione
        _h0 = hashlib.sha1(io.open(_sr, "rb").read()).hexdigest()
        _h1 = hashlib.sha1(io.open(_ix, "rb").read()).hexdigest()
        shutil.copy(_sr, _sr + ".bak")
        shutil.copy(_ix, _ix + ".bak")
        _msgf = os.path.join(RADICE, "doc", "_collaudo_msg3.tmp")
        io.open(_msgf, "w", encoding="utf-8", newline=NL).write("collaudo punto 3" + NL)
        try:
            # (a) l'ID nuovo SOLO in STATO_RUN
            with io.open(_sr, "a", encoding="utf-8", newline=NL) as _f:
                _f.write(NL + "| **%s** | difetto nuovo del collaudo | \u2014 | `APERTO` |" % _id + NL)
            subprocess.run(["git", "add", "--", "doc/STATO_RUN.md"], cwd=RADICE,
                           capture_output=True, text=True)
            _a = subprocess.run([sys.executable, os.path.join(RADICE, "csv",
                                                             "_presidio_indice.py"),
                                 "--commit-msg", _msgf], cwd=RADICE, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
            _okA = (_a.returncode == 1 and (_id in (_a.stderr or "")
                                            or _id[1:] in (_a.stderr or "")))
            # (b) con la RIGA nell'indice
            _c, _rr = leggi_tsv(_ix)
            _nuova = [_id, "", "difetto nuovo del collaudo", "doc/STATO_RUN.md::collaudo",
                      "aperto", "DA-DECIDERE", "difetto", "?", "", "(senza marcatore)", "", "", ""]
            io.open(_ix, "w", encoding="utf-8", newline=NL).write(
                TAB.join(_c) + NL + NL.join(_rr + [TAB.join(_nuova)]) + NL)
            subprocess.run(["git", "add", "--", "doc/STATO_RUN.md", "doc/INDICE_ID.tsv"],
                           cwd=RADICE, capture_output=True, text=True)
            _b = subprocess.run([sys.executable, os.path.join(RADICE, "csv",
                                                             "_presidio_indice.py"),
                                 "--commit-msg", _msgf], cwd=RADICE, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
            _okB = (_b.returncode == 0)
        finally:
            subprocess.run(["git", "reset", "-q", "--", "doc/STATO_RUN.md", "doc/INDICE_ID.tsv"],
                           cwd=RADICE, capture_output=True, text=True)
            shutil.move(_sr + ".bak", _sr)
            shutil.move(_ix + ".bak", _ix)
            if os.path.exists(_msgf):
                os.remove(_msgf)
        _h0b = hashlib.sha1(io.open(_sr, "rb").read()).hexdigest()
        _h1b = hashlib.sha1(io.open(_ix, "rb").read()).hexdigest()
        _okC = (_h0 == _h0b and _h1 == _h1b)
        P("  PUNTO 3, NEI DUE VERSI (sentinella `%s`):" % _id)
        P("    DEVE FALLIRE  l'ID nuovo SOLO in `STATO_RUN` -> uscita %d, segnalato %s   %s"
          % (_a.returncode, _id in (_a.stderr or "") or _id[1:] in (_a.stderr or ""),
             "PASS" if _okA else "FAIL"))
        P("    DEVE PASSARE  lo stesso ID **con la RIGA nell'indice** -> uscita %d   %s"
          % (_b.returncode, "PASS" if _okB else "FAIL"))
        P("    i due documenti sono tornati identici (sha1): %s   %s"
          % (_okC, "PASS" if _okC else "FAIL"))
        esiti += [_okA, _okB, _okC]
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
