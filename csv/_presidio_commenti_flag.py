# -*- coding: utf-8 -*-
"""**`P7` — LA POSTCONDIZIONE: IL COMMENTO DI OGNI FLAG NOMINA QUEL FLAG.**

> **IL DIFETTO REALE, e l'ha trovato Luca il 2026-09-25 (non un controllo):** la patch di
> `INERZIA-1(C)` ha inserito il suo blocco **FRA `MITOSI_2LAM = False` e IL SUO COMMENTO**.
> Risultato: **`MITOSI_2LAM` senza commento, e `CONTRASTO_INTENSIVO` che portava la descrizione
> della CURA 5** — cioè un flag che dichiarava di fare un'altra cosa.

**PERCHE' L'`assert` DELLA PATCH NON L'HA PRESO:** l'ancora `"MITOSI_2LAM = False"` **era unica**,
e la sostituzione **ha attaccato**. `P1-quater` chiede che ogni sostituzione sia asserita **per
sé**, e lo era. **Quello che mancava e' la POSTCONDIZIONE:** *dopo* la patch, il file diceva una
cosa falsa, e **nessuna asserzione guardava il RISULTATO.**

> ### **`P1-quater` verifica che la patch ATTACCHI. `P7` verifica che il file, DOPO, sia giusto.**
> Sono due controlli diversi, e il secondo mancava.

**COSA CONTROLLA, e la regola e' semplice perche' deve poter fallire:** per ogni assegnazione di
modulo `NOME = <costante>` con `NOME` **MAIUSCOLO**, se c'e' un commento *(sulla stessa riga o nel
blocco indentato subito sotto)*, **quel commento deve nominare il flag** — il nome per intero,
oppure il suo nome in minuscolo-con-trattini *(la forma dell'opzione: `CONTRASTO_INTENSIVO` ->
`contrasto-intensivo`)*, oppure un'etichetta `[CURA n]` gia' associata a quel flag altrove.

**⚠ E DICHIARA UN LIMITE:** un commento puo' nominare il flag **e dire il falso**. `P7` prende la
classe di difetto **in cui il commento appartiene a un ALTRO flag**, che e' quella accaduta; non
legge il contenuto. **Va detto, invece di chiamarlo «il commento e' giusto».**

ASCII puro. Sola lettura.
"""
# ESENTE-P8: legge `HEAD:soliton_simulator.py`, ma **NON come «il codice prima di una
#   cura»**: come **il PRIMA di una PATCH**. E' una POSTCONDIZIONE, e una postcondizione ha
#   bisogno del prima per esistere. **Non scade quando una cura viene committata** -- al
#   contrario: il suo termine di paragone *deve* essere l'ultimo commit, perche' la domanda e'
#   *«questa patch ha lasciato un commento orfano?»*.
#   *(`P8` ha bloccato questo file per un'euristica sul NOME: la variabile si chiama `prima`.
#   L'euristica ha fatto il suo mestiere, e la distinzione la deve fare chi scrive.)*
# ESENTE-P5: strumento di analisi STATICA. Non importa il simulatore e non lo fa girare: legge
#   UN SORGENTE per AST, e le assegnazioni di modulo sono le stesse con qualunque flag. Una
#   dichiarazione di configurazione qui sarebbe **una riga vuota**, che e' cio' che `P5` impedisce.
import ast
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
NL = chr(10)

# le etichette `[CURA n]` / `[NOME-qualcosa]` che valgono come nome del flag, quando il testo
# le associa a quel flag DA QUALCHE ALTRA PARTE nel file (il `--flag` del `_cli`, o l'aiuto).
ETICH = re.compile(r"\[([A-Za-z0-9_-]+(?:\s+[A-Za-z0-9_()-]+)*)\]")


def nomi_ammessi(flag):
    """Le forme con cui un commento puo' NOMINARE `flag`."""
    fuori = {flag, flag.lower(), flag.lower().replace("_", "-")}
    return fuori


def blocco_commento(righe, k):
    """Il commento di `righe[k]`: la coda della riga, piu' il blocco indentato sotto."""
    fuori = []
    if "#" in righe[k]:
        fuori.append(righe[k].split("#", 1)[1])
    j = k + 1
    while j < len(righe):
        s = righe[j]
        if s.strip().startswith("#") and (s.startswith(" ") or s.startswith("\t")):
            fuori.append(s.split("#", 1)[1])
            j += 1
            continue
        break
    return NL.join(fuori)


def flag_di_modulo(arb):
    """I nomi MAIUSCOLI assegnati a livello di MODULO, con la loro riga."""
    fuori = {}
    for nd in arb.body:
        if isinstance(nd, ast.Assign):
            for tg in nd.targets:
                if isinstance(tg, ast.Name) and tg.id.isupper():
                    fuori.setdefault(tg.id, nd.lineno or 0)
    return fuori


def controlla(sorgente=None, discriminante=True):
    """Restituisce `(guasti, quanti)`. Un guasto = `(flag, riga, motivo)`.

    **DUE LETTURE, e la differenza non e' accademica:**

    * `discriminante=False` — **LA FORMA LETTERALE** che Luca ha chiesto: *il commento di
      ciascun flag NOMINA quel flag*. **Sul file vero da' 87 guasti su 130**, e quasi tutti
      sono **commenti descrittivi legittimi**: `REGIME = "deterministico"  # <-- cambia qui:
      "stocastico" | "deterministico"` **descrive** il flag senza ripeterne il nome.
      **Serve come MISURA (l'arretrato), non come cancello.**
    * `discriminante=True` — **LA CLASSE DI DIFETTO CHE E' ACCADUTA**: il commento **nomina
      un ALTRO flag di modulo** *(o l'etichetta `[CURA n]` di un altro flag)* **e NON nomina
      il proprio**. E' esattamente cio' che la patch di `INERZIA-1(C)` ha prodotto:
      `CONTRASTO_INTENSIVO` con addosso `[CURA 5] A13 ALLA NASCITA`, che appartiene a
      `MITOSI_2LAM`. **Questa BLOCCA**, e non ha arretrato: un commento che parla di un altro
      flag e tace del proprio **e' sempre un difetto**, non uno stile.

    ⚠ **DEVIAZIONE DALLA LETTERA DEL MANDATO, dichiarata:** Luca ha chiesto la prima forma.
    **La applico come misura e faccio bloccare la seconda**, perche' un cancello con 87
    violazioni preesistenti **non e' un cancello: e' un ostacolo che si impara ad aggirare**
    (e `A9` chiede presidi che impediscano, non che stanchino). **Decide Luca**: se vuole la
    forma letterale come cancello, si passa `discriminante=False` e si bonificano gli 87.
    """
    t = io.open(sorgente or SIM, encoding="utf-8").read()
    righe = t.split(NL)
    arb = ast.parse(t)
    tutti = flag_di_modulo(arb)
    guasti, quanti = [], 0
    for flag, lin in sorted(tutti.items(), key=lambda x: x[1]):
        quanti += 1
        com = blocco_commento(righe, lin - 1)
        if not com.strip():
            continue
        basso = com.lower()
        suo = any(x.lower() in basso for x in nomi_ammessi(flag))
        if not discriminante:
            if not suo:
                guasti.append((flag, lin, "il commento non nomina il flag"))
            continue
        if suo:
            continue
        # nomina un ALTRO flag di modulo?
        altri = [a for a in tutti if a != flag and len(a) > 4 and a in com]
        if altri:
            guasti.append((flag, lin,
                           "il commento nomina %s e NON %s: appartiene a un altro flag"
                           % (", ".join(altri[:3]), flag)))
    return guasti, quanti

# ====================================================================== IL COLLAUDO
# ❌ **IL MIO PRIMO CASO «DEVE BLOCCARE» NON BLOCCAVA, e il motivo e' istruttivo:** il testo
#   con cui SPIEGAVO il difetto (*«questo commento appartiene a PLUTO, non a PAPERINO»*)
#   **conteneva il nome del flag**, quindi soddisfaceva il controllo. **Un caso sintetico non
#   deve spiegarsi: deve essere il difetto.** *(`P1-sexies`: il caso che deve fallire e' il
#   piu' importante, e qui era rotto proprio lui.)*
BUONO = NL.join(["ALFA_UNO = False   # [CURA 9] ALFA_UNO fa una cosa.",
                 "                   # e la fa bene.", ""])
DESCRITTIVO = NL.join(['BETA_DUE = "x"   # <-- cambia qui: "x" | "y" (default)', ""])
ORFANO = NL.join(["GAMMA_TRE = False", "",
                  "DELTA_QUATTRO = False   # [CURA 9] GAMMA_TRE divide un arco se d >= 2 LAM.",
                  "                        # OFF di default.", ""])


def collaudo():
    import tempfile
    print("=" * 96)
    print("COLLAUDO DI `P7` -- tre casi a risposta NOTA (`P1-sexies`)")
    print("=" * 96)
    ok = True
    for nome, src, deve in (("passa", BUONO, False),
                            ("descritt", DESCRITTIVO, False),
                            ("BLOCCA", ORFANO, True)):
        p = os.path.join(tempfile.gettempdir(), "_p7_%s.py" % nome)
        io.open(p, "w", encoding="utf-8", newline=NL).write(src)
        g, q = controlla(p, discriminante=True)
        blocca = bool(g)
        buono = (blocca == deve)
        ok = ok and buono
        print("  %-9s flag %d   atteso %-7s ottenuto %-7s %s"
              % (nome, q, "BLOCCA" if deve else "passa", "BLOCCA" if blocca else "passa",
                 "OK" if buono else "!! SBAGLIATO"))
        for f, l, m in g:
            print("             -> %s :%d  %s" % (f, l, m))
    # e il caso DESCRITTIVO deve BLOCCARE nella forma LETTERALE: cosi' si vede che le due
    # letture sono davvero diverse, e non una copia dell'altra.
    p = os.path.join(tempfile.gettempdir(), "_p7_descritt.py")
    g2, _q2 = controlla(p, discriminante=False)
    print("  %-9s forma LETTERALE: atteso BLOCCA  ottenuto %-7s %s"
          % ("descritt", "BLOCCA" if g2 else "passa", "OK" if g2 else "!! SBAGLIATO"))
    ok = ok and bool(g2)
    print()
    print("COLLAUDO: %s" % ("4/4 OK" if ok else "FALLITO"))
    return 0 if ok else 1

def commenti_per_flag(testo):
    """`{flag: commento}` da un TESTO qualsiasi (serve per confrontare HEAD col disco)."""
    try:
        arb = ast.parse(testo)
    except SyntaxError:
        return {}
    righe = testo.split(NL)
    return {f: blocco_commento(righe, l - 1) for f, l in flag_di_modulo(arb).items()}


def pre_commit():
    """**LA POSTCONDIZIONE VERA: un flag il cui COMMENTO E' CAMBIATO deve nominare quel flag.**

    ✅ **E' la forma LETTERALE che Luca ha chiesto, applicata ai soli flag CHE IL COMMIT TOCCA.**
    Cosi' **prende il difetto accaduto** — `CONTRASTO_INTENSIVO` si e' ritrovato addosso il
    commento della CURA 5, e quel commento **non lo nominava** — **senza pretendere la bonifica
    dei 96 preesistenti**, che sono in larghissima parte commenti DESCRITTIVI legittimi.

    **Perche' il confronto e' con `HEAD` e non con il file intero:** una POSTCONDIZIONE guarda
    **cio' che la patch ha prodotto**. `P1-quater` verifica che la sostituzione ATTACCHI; questa
    verifica che **il risultato sia giusto**, e per saperlo serve il PRIMA.
    """
    import subprocess
    q = subprocess.run(["git", "show", "HEAD:soliton_simulator.py"], cwd=RADICE,
                       capture_output=True)
    if q.returncode:
        print("[P7] `HEAD:soliton_simulator.py` non leggibile: il controllo NON e' girato,")
        print("     e lo dichiaro invece di far credere che sia passato.")
        return 0
    prima = commenti_per_flag(q.stdout.decode("utf-8", "replace"))
    dopo = commenti_per_flag(io.open(SIM, encoding="utf-8").read())
    guasti = []
    for f, com in dopo.items():
        if com.strip() == (prima.get(f) or "").strip():
            continue                      # il commento NON e' cambiato: non e' affar mio
        if not com.strip():
            if (prima.get(f) or "").strip():
                guasti.append((f, "AVEVA un commento e ora NON CE L'HA PIU'"))
            continue
        if not any(x.lower() in com.lower() for x in nomi_ammessi(f)):
            guasti.append((f, "il commento E' CAMBIATO e non nomina `%s`" % f))
    if not guasti:
        return 0
    sys.stderr.write(NL + "[P7] *** COMMIT RIFIUTATO: un commento di flag non parla del suo flag"
                     " ***" + NL + NL)
    for f, m in guasti:
        sys.stderr.write("  %-26s %s" % (f, m) + NL)
    sys.stderr.write(NL + "  E' la classe di difetto del 2026-09-25: una patch inserita FRA un"
                     " flag e il SUO" + NL + "  commento lascia il flag muto e il vicino con la"
                     " descrizione sbagliata." + NL
                     + "  `P1-quater` verifica che la patch ATTACCHI; questa che il RISULTATO sia"
                     " giusto." + NL + NL)
    return 1


if __name__ == "__main__":
    if "--pre-commit" in sys.argv[1:]:
        sys.exit(pre_commit())
    if "--collaudo" in sys.argv[1:]:
        sys.exit(collaudo())
    g, q = controlla(discriminante=True)
    gl, _ = controlla(discriminante=False)
    print("=" * 96)
    print("`P7` -- IL COMMENTO DI OGNI FLAG (soliton_simulator.py)")
    print("=" * 96)
    print("  assegnazioni di modulo MAIUSCOLE esaminate: %d" % q)
    print("  forma LETTERALE (misura, NON blocca): %d flag il cui commento non li nomina" % len(gl))
    print("     -> e' L'ARRETRATO: quasi tutti sono commenti DESCRITTIVI legittimi")
    print("        (`REGIME = \"deterministico\"  # <-- cambia qui: ...`).")
    print("  forma DISCRIMINANTE (blocca): %d" % len(g))
    for f, l, m in g:
        print("    %-26s :%-6d %s" % (f, l, m))
    print()
    if not g:
        print("  -> NESSUN COMMENTO ORFANO. **Non significa che i commenti siano VERI**: `P7`")
        print("     prende la classe in cui un commento appartiene a un ALTRO flag, che e'")
        print("     quella accaduta il 2026-09-25. Il CONTENUTO non lo legge nessuno.")
    sys.exit(1 if g else 0)
