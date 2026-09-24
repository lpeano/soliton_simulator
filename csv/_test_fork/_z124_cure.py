# -*- coding: utf-8 -*-
"""CURE VERIFICATE: il lettore del verdetto accetta anche `ESITO: n/m`, e le due righe nuove."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 0


def s1(t, v, nu):
    global N
    assert t.count(v) == 1, "occ=%d per %r" % (t.count(v), v[:70])
    N += 1
    return t.replace(v, nu)


P = "csv/_cure_verificate.py"
t = io.open(P, encoding="utf-8", newline="").read()

# --- 1. il lettore: DUE forme di riga di verdetto, entrambe ANCORATE a inizio riga.
#     La riga si trova PER PREFISSO, non per pattern con backslash: nessuna escape da sbagliare.
righe = t.split("\n")
idx = [i for i, r in enumerate(righe) if r.startswith("VERDETTO = re.compile(")]
assert len(idx) == 1, idx
vecchia = righe[idx[0]]
assert "SIGILLO" in vecchia and "ESITO" not in vecchia, vecchia
nuova = ('VERDETTO = re.compile(\n'
         '    r"^' + chr(92) + 's*(?:SIGILLO' + chr(92) + 'b[^' + chr(92) + 'n:]*|ESITO)'
         + chr(92) + 's*:' + chr(92) + 's*(' + chr(92) + 'd+)' + chr(92) + 's*/'
         + chr(92) + 's*(' + chr(92) + 'd+)' + chr(92) + 's*$", re.M | re.I)')
righe[idx[0]] = nuova
t = "\n".join(righe)
N += 1

# --- 2. il docstring del lettore dice PERCHE' ci sono due forme
t = s1(t,
       '    """L\'esito del sigillo, ANCORATO alla riga di verdetto `SIGILLO <NOME>: n/m`.',
       '    """L\'esito del sigillo, ANCORATO a una riga di verdetto: `SIGILLO <NOME>: n/m`\n'
       '    oppure `ESITO: n/m`.\n\n'
       '    LE DUE FORME NON SONO UN CAPRICCIO: i sigilli di `RITMO_WRAP_2PI` e `FASE_2PI`\n'
       '      scrivono `ESITO: n/m`, i precedenti `SIGILLO <NOME>: n/m`. Ho preferito INSEGNARE\n'
       '      al lettore le due forme che i referti hanno DAVVERO, invece di ricopiare i numeri\n'
       '      a mano (`P1-ter`): un numero generato ha una provenienza, uno ricopiato no.\n'
       '      **Cio\' che NON si allarga e\' l\'ANCORAGGIO A INIZIO RIGA**, che e\' la parte che\n'
       '      impedisce il `0/0` di `U6`.')

# --- 3. il collaudo: la forma nuova, e TRE casi che devono fallire
t = s1(t,
       '    e.append(ok3)\n    ok = all(e)',
       '    e.append(ok3)\n'
       '    # LA FORMA NUOVA: `ESITO: n/m`, e il `0/0` di prima NON deve vincere\n'
       '    nuovo = ("U6   PASS `0/0` E\' DEFINITO ZERO: 525973 archi\\n"\n'
       '             "\\n===========\\nESITO: 6/6\\n===========\\n")\n'
       '    v4 = verdetto(nuovo)\n'
       '    ok4 = (v4 == ("6", "6"))\n'
       '    W("K4 legge la forma `ESITO: n/m` dei referti nuovi, e NON il `0/0` -> %s  (%s)\\n"\n'
       '      % ("OK" if ok4 else "*** NO ***", v4))\n'
       '    e.append(ok4)\n'
       '    # TERZO CASO CHE DEVE FALLIRE: `ESITO` senza numeri non e\' un verdetto\n'
       '    ok5 = verdetto("ESITO: PASSATO, tutti i test\\nqualche 3/4 nel testo\\n") is None\n'
       '    W("K5 TERZO CASO CHE DEVE FALLIRE: `ESITO: PASSATO` (senza `n/m`) -> `None` -> %s\\n"\n'
       '      % ("OK" if ok5 else "*** inventa un esito ***"))\n'
       '    e.append(ok5)\n'
       '    # QUARTO: `esito` NON a inizio riga (dentro la prosa) non conta. E\' la parte\n'
       '    # dell\'ancoraggio che NON si allarga: senza, ogni frase diventa un verdetto.\n'
       '    ok6 = verdetto("il suo esito: 9/9 secondo me\\n") is None\n'
       '    W("K6 QUARTO CASO CHE DEVE FALLIRE: `esito: 9/9` DENTRO la prosa -> `None` -> %s\\n"\n'
       '      % ("OK" if ok6 else "*** legge la prosa come verdetto ***"))\n'
       '    e.append(ok6)\n'
       '    ok = all(e)')

# --- 4. la riga di RITMO_WRAP_2PI: in codice, sigillata, PROVATA
t = s1(t,
       '    ("RITMO_WRAP_2PI", "**`A1`** il wrap del ritmo sul periodo GIUSTO *(`2\u03c0`)*",\n'
       '     "\u23f8 **da scrivere**", None,\n'
       '     "\u23f8 prova a 600 passi, **da fare**",\n'
       '     "cura **`D34`** *(`Z117`: il wrap a `4\u03c0` e\' l\'IDENTITA\')*",\n'
       '     "\u23f8 **NON ANCORA IN CODICE**"),',
       '    ("RITMO_WRAP_2PI", "**`A1`** il wrap del ritmo sul periodo GIUSTO *(`2\u03c0`)*",\n'
       '     "`4/4` *(scritto a mano: il referto sta nel log, non in un file con la riga di '
       'verdetto)*", None,\n'
       '     "\u2705 **`G4`, 600 passi** *(`Z123`, `csv/_test_fork/_d34_ritmo_wrap`)*",\n'
       '     "cura **`D34`** *(`Z117`: il wrap a `4\u03c0` e\' l\'IDENTITA\')*. **`6/8` come previsto '
       'e il bilancio CHIUDE (`9.595e-14`), ma TUTTI gli aggregati peggiorano e la mia '
       'previsione \u2464 era SBAGLIATA** *(la quota al tetto SALE: -> `S09`)*",\n'
       '     "**PROVATA, default SPENTO** \u2014 la decisione e\' di Luca"),')

# --- 5. la riga di FASE_2PI: in codice, sigillata, prova da fare
t = s1(t,
       '    ("FASE_2PI", "**\u00a7D** `\u03c6` come fase ordinaria su `[0, 2\u03c0)`",\n'
       '     "\u23f8 **da scrivere**", None,\n'
       '     "\u23f8 prova a 600 passi + i **quattro test** `E1`-`E4`, **da fare**",\n'
       '     "la lettura scelta da Luca, **da METTERE ALLA PROVA**. Se un test fallisce, '
       '**cade**",\n'
       '     "\u23f8 **NON ANCORA IN CODICE**"),',
       '    ("FASE_2PI", "**\u00a7D** `\u03c6` come fase ordinaria su `[0, 2\u03c0)`",\n'
       '     "\u23f8 *(l\'esito si legge dal referto)*",\n'
       '     "csv/_seal_fork/_sig_fase_2pi/REFERTO.txt",\n'
       '     "\u23f8 prova a 600 passi + i test `E1`-`E4`, **da fare**",\n'
       '     "la lettura scelta da Luca, **da METTERE ALLA PROVA**. Se un test fallisce, '
       '**cade**. **Cura `D35`** *(l\'antifase `+2\u03c0` che non e\' un\'antifase)*",\n'
       '     "\u2705 **IN CODICE e SIGILLATA**, default **SPENTO**. \u23f8 **NON ANCORA PROVATA**"),')

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni in %s" % (N, P))
