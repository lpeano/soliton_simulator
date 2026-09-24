# -*- coding: utf-8 -*-
"""LA SEZIONE `CURE VERIFICATE` della CODA UNICA, **generata** (`P1-ter`).

Decisione di Luca, 2026-09-22: per ogni cura **flag . sigillo . prova . esito . stato**, e si
aggiorna **nello stesso commit** in cui una cura viene sigillata o provata.

⚠ COSA E' GENERATO E COSA E' SCRITTO A MANO, perche' la differenza conta:
  * **il DEFAULT del flag** si legge DAL SORGENTE a ogni giro -- e' il campo che si sfalsa piu'
    facilmente, ed e' quello che decide se una cura **gira davvero** nei run;
  * **l'esito del sigillo** si legge DAL SUO REFERTO quando c'e' un file da leggere;
  * **prova, esito e stato** sono LETTURE: si scrivono a mano, **ciascuna col suo commit**.
    Un'interpretazione non si genera; una condizione del codice si'.

⚠ E LA DISTINZIONE CHE LA SEZIONE DEVE FARE, senza la quale il conto e' falso:
    CURA                 corregge un DIFETTO. Il flag esiste per l'A/B; il default e' `False`
                         e **il driver la accende in ogni run**.
    PROVA DI SPEGNIMENTO diagnostico. Il flag e' `True` (la legge GIRA) e spegnerlo e' il test.
                         **NON e' una cura**, e metterla fra le cure gonfierebbe il conto.

SOLA LETTURA sul simulatore: lo legge come TESTO, non lo importa.
ASCII PURO.
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
CODA = os.path.join(RADICE, "doc", "STATO_RUN.md")
INI, FIN = "<!-- CURE-INIZIO -->", "<!-- CURE-FINE -->"

# (flag, nome, sigillo, file del referto, prova, esito, stato)
#   `None` come file del referto = l'esito del sigillo e' scritto a mano perche' il file non
#   esiste piu' in forma leggibile: si dichiara invece di inventare un percorso.
CURE = [
    ("PEQ_ESATTO", "`C1` rilassamento di `peq` in forma ESATTA", "`7/7`",
     "csv/_seal_fork/_sigillo_peq_esatto_2026-09-21.txt",
     "in **ogni** run del fork *(`--peq-esatto=on`)*",
     "`peq` non puo' piu' scavalcare sotto zero: combinazione convessa, **dimostrato** e non "
     "imposto. Cura `D17`",
     "VERIFICATA-SPENTA *(default `False`, accesa dal driver)*"),
    ("PEQ_NASCITA_LOCALE", "`C2` nascita LOCALE di `peq`", "`6/6`",
     "csv/_seal_fork/_sigillo_peq_nascita_2026-09-21.txt",
     "in **ogni** run del fork", "una sola legge di nascita; via la mediana GLOBALE *(`A2`)*",
     "VERIFICATA-SPENTA *(default `False`, accesa dal driver)*"),
    ("SCALA_MIN_PASSO", "`C3` il freno UNA VOLTA per passo", "`6/6`",
     "csv/_seal_fork/_sigillo_scala_min_passo_2026-09-21.txt",
     "`G4` riferimento e i due spegnimenti, 600 passi",
     "cura il cricchetto **d'ORDINE** di `Z91`. **⚠ MA NON IL CRICCHETTO DI VERSO:** "
     "`Z113` lo DIMOSTRA sulla formula, ed e' **`D31`**",
     "VERIFICATA-SPENTA — **e la legge che applica e' DIFETTOSA**"),
    ("COES_CAUSALE", "`C4` coesione: istante unico e cono LOCALE", "`5/5`",
     "csv/_seal_fork/_sigillo_coes_causale_2026-09-21.txt",
     "in **ogni** run del fork", "cura `D18`. Il tetto locale **non e' sempre piu' stretto**: "
     "dove il cono e' veloce **allarga**",
     "VERIFICATA-SPENTA *(default `False`, accesa dal driver)*"),
    ("COES_ADIM", "coesione ADIMENSIONALE", "— *(non ha un sigillo suo)*", None,
     "in **ogni** run del fork",
     "`|F_adim| <= 1` **per costruzione**. **L'unica legge delle quattro schede con le unita' "
     "giuste senza che un clip gliele dia**", "VERIFICATA-SPENTA"),
    ("ANOM_SIMM", "`C1-bis` anomalia simmetrica, senza pavimento", "`6/6`",
     "csv/_seal_fork/_sigillo_anom_simm_2026-09-21.txt",
     "in **ogni** run del fork",
     "toglie `max(peq, 1e-9)`, che con `peq < 0` **RIBALTAVA IL SEGNO** *(`Z94`, `D17`)*",
     "VERIFICATA-SPENTA"),
    ("INVARIANTI", "`C5` domini di stato, due livelli", "`3/3`",
     "csv/_seal_fork/_sigillo_invarianti_2026-09-21.txt",
     "in **ogni** run: **zero violazioni** in tutti e tre i bracci di `G4`",
     "legge soltanto; su un run sano non cambia un bit", "**ACCESA DI DEFAULT** *(`True`)*"),
    ("RITMO_WRAP_2PI", "**`A1`** il wrap del ritmo sul periodo GIUSTO *(`2π`)*",
     "`4/4` + **`6/6` di `CURA 1`** *(`csv/_seal_fork/_sig_cura1/REFERTO.txt`)*", None,
     "✅ **`G4`, 600 passi** *(`Z123`)* + **giro corto di `CURA 1`**",
     "cura **`D34`** *(`Z117`: il wrap a `4π` e' l'IDENTITA')*. **`6/8` come previsto e il bilancio CHIUDE (`9.595e-14`), ma TUTTI gli aggregati peggiorano e la mia previsione ⑤ era SBAGLIATA** *(la quota al tetto SALE: -> `S09`)*",
     "✅✅ **APPROVATA DA LUCA il 2026-09-24. IL DRIVER LA ACCENDE IN OGNI RUN** "
     "*(`--ritmo-wrap-2pi`)*. Default nel sorgente **`False`**, come tutte le cure "
     "pre-epoca-3. **`D34` passa da difetto aperto a CURA IN CODICE.**"),
    ("TEMPO_UNICO_MITOSI", "**`CURA 2`** UN SOLO OROLOGIO dentro `mitosi()`",
     "⏸ *(l'esito si legge dal referto)*", "csv/_seal_fork/_sig_cura2/REFERTO.txt",
     "✅ **giro corto di 120 passi contro `_cura1_corto`** *(un interruttore di differenza, "
     "due processi freschi a un solo braccio)*",
     "gli usi di `tau_pp` come TEMPO passano all'orologio `dt_e`; i **quattro** usi come "
     "POSIZIONE sull'asse della torsione restano INTOCCATI *(dall'AST, `T3`)*. **La mitosi "
     "vive** *(eventi `67` -> `76`)*, **il bilancio chiude** *(`5.304e-14`)*, e **la "
     "saturazione di `tanh(grad)` passa da `0.0034 %` a ZERO** *(`A11` cor.6; il massimo "
     "misurato `0.8861` contro il `0.8884` PREVISTO dall'intervallo di `r`)*. "
     "**⚠ MA due delle tre sostituzioni formali sono INERTI in questo regime:** il clip "
     "alto su `prob` non morde **mai** *(0 su 63 128 409)* e l'Eulero non ha **mai** "
     "`dt/τ > 1`. **⚠ E la previsione di `×2.5`-`×3` su `d0` NON regge: `±3 %`**",
     "✅✅ **APPROVATA DA LUCA il 2026-09-24. IL DRIVER LA ACCENDE IN OGNI RUN** "
     "*(`--tempo-unico-mitosi`)*. Default nel sorgente **`False`**, come tutte le cure "
     "pre-epoca-3."),
    ("FASE_2PI", "**§D** `φ` come fase ordinaria su `[0, 2π)`",
     "⏸ *(l'esito si legge dal referto)*",
     "csv/_seal_fork/_sig_fase_2pi/REFERTO.txt",
     "❌ **PROVATA sul giro CORTO (120 passi, `Z127`): `2/4`, `E1` NON PASSA**",
     "**LA LETTURA CADE.** La cura fa cio' che dichiara su `phi` *(`E4` PASSA, bilancio "
     "`4.041e-14`)*, **ma la generazione di materia SI FERMA**: mitosi `62` -> `1` evento, "
     "Schwinger `28` -> `0`. **`|tw|` si dimezza e nessun arco raggiunge piu' la soglia** "
     "*(`MAX 4.37 = 1.39 pi` contro `2pi`)*. **-> `D36`**",
     "❌ **IN CODICE e SIGILLATA, ma la PROVA la BOCCIA.** Default **SPENTO**, e ci resta: "
     "il punto 2 del par.D va riaperto *(decisione di Luca)*"),
]

# Le PROVE DI SPEGNIMENTO: NON sono cure, e stanno a parte perche' il conto resti onesto.
SPEGNIMENTI = [
    ("GRAV_BIFASE", "la gravita' bifase", "`7/7`",
     "`G3`, 600 passi", "**NON e' il motore di `d0`** *(`Z107`)*"),
    ("MEM_MOTO", "la scrittura della memoria del moto su `d0`", "`8/8`",
     "`G4`, 600 passi", "**non e' il motore**, ma pesa *(`Z109`)*"),
    ("MEM_MOTO_TUTTO", "l'INTERO blocco della memoria del moto", "`10/10`",
     "`G4-bis`, 600 passi", "**spegnere di piu' da' PIU' crescita** *(`Z115`, `Z116`)*"),
]


def default(flag):
    """Il default, letto DAL SORGENTE. E' il campo che si sfalsa piu' facilmente."""
    t = io.open(SORGENTE, encoding="utf-8").read()
    m = re.search(r"^%s\s*=\s*(True|False)\b" % re.escape(flag), t, re.M)
    return m.group(1) if m else None


VERDETTO = re.compile(
    r"^\s*(?:SIGILLO\b[^\n:]*|ESITO)\s*:\s*(\d+)\s*/\s*(\d+)\s*$", re.M | re.I)


def verdetto(testo):
    """L'esito del sigillo, ANCORATO a una riga di verdetto: `SIGILLO <NOME>: n/m`
    oppure `ESITO: n/m`.

    LE DUE FORME NON SONO UN CAPRICCIO: i sigilli di `RITMO_WRAP_2PI` e `FASE_2PI`
      scrivono `ESITO: n/m`, i precedenti `SIGILLO <NOME>: n/m`. Ho preferito INSEGNARE
      al lettore le due forme che i referti hanno DAVVERO, invece di ricopiare i numeri
      a mano (`P1-ter`): un numero generato ha una provenienza, uno ricopiato no.
      **Cio' che NON si allarga e' l'ANCORAGGIO A INIZIO RIGA**, che e' la parte che
      impedisce il `0/0` di `U6`.

    ⚠ CORRETTO SUBITO DOPO AVERLO SCRITTO. La prima versione cercava il primo `n/m` del file
      e su `_sigillo_anom_simm` prendeva **`0/0`** -- che veniva da `U6`, dove `0/0` e' il
      CASO FISICO (vuoto su vuoto), non un verdetto. **Un `0/0` come esito di un sigillo e'
      un numero IMPOSSIBILE, ed e' cosi' che il difetto si e' denunciato da solo** (par.9).
    """
    m = VERDETTO.search(testo)
    return (m.group(1), m.group(2)) if m else None


def esito_sigillo(percorso, scritto):
    """Se il referto c'e' E ha una riga di verdetto, si legge; altrimenti si DICHIARA."""
    if not percorso:
        return scritto
    p = os.path.join(RADICE, percorso)
    if not os.path.exists(p):
        return scritto + " ⚠ *(referto non trovato: `%s`)*" % percorso
    v = verdetto(io.open(p, encoding="utf-8", errors="replace").read())
    if v is None:
        # ⚠ la prima stesura spezzava questa stringa DOPO il `return`: la seconda meta' era
        #   codice morto e il messaggio usciva troncato. Trovato rileggendo, non da un test.
        return (scritto + " ⚠ *(nessuna riga `SIGILLO ...: n/m` nel referto: "
                          "**scritto a mano**)*")
    return "`%s/%s` *(letto dal referto)*" % v


def collaudo(W):
    """`P1-sexies`: il lettore del verdetto su testi a risposta NOTA."""
    W("COLLAUDO (`P1-sexies`), PRIMA di generare\n" + "-" * 92 + "\n")
    e = []
    buono = ("U4   PASS max|anom| = 1.999960\n"
             "U6   PASS `0/0` E' DEFINITO ZERO: 525973 archi su 12626500 (4.17%)\n"
             "\nSIGILLO ANOM_SIMM: 6/6\n")
    v = verdetto(buono)
    ok1 = (v == ("6", "6"))
    W("K1 legge il VERDETTO `6/6` e non il `0/0` del testo -> %s  (%s)\n"
      % ("OK" if ok1 else "*** NO ***", v))
    e.append(ok1)
    # IL CASO CHE DEVE FALLIRE: la vecchia regola avrebbe preso il primo `n/m`
    vecchio = re.search(r"(\d+)\s*/\s*(\d+)", buono)
    ok2 = (vecchio.group(1), vecchio.group(2)) != ("6", "6")
    W("K2 IL CASO CHE DEVE FALLIRE: la regola VECCHIA (primo `n/m`) da' `%s/%s` -> %s\n"
      % (vecchio.group(1), vecchio.group(2),
         "OK: il difetto e' riprodotto" if ok2 else "*** non si riproduce ***"))
    e.append(ok2)
    ok3 = verdetto("nessun verdetto qui, solo 3/4 di testo\n") is None
    W("K3 SECONDO CASO CHE DEVE FALLIRE: un file SENZA riga di verdetto -> `None`, non un "
      "numero inventato -> %s\n" % ("OK" if ok3 else "*** inventa un esito ***"))
    e.append(ok3)
    # LA FORMA NUOVA: `ESITO: n/m`, e il `0/0` di prima NON deve vincere
    nuovo = ("U6   PASS `0/0` E' DEFINITO ZERO: 525973 archi\n"
             "\n===========\nESITO: 6/6\n===========\n")
    v4 = verdetto(nuovo)
    ok4 = (v4 == ("6", "6"))
    W("K4 legge la forma `ESITO: n/m` dei referti nuovi, e NON il `0/0` -> %s  (%s)\n"
      % ("OK" if ok4 else "*** NO ***", v4))
    e.append(ok4)
    # TERZO CASO CHE DEVE FALLIRE: `ESITO` senza numeri non e' un verdetto
    ok5 = verdetto("ESITO: PASSATO, tutti i test\nqualche 3/4 nel testo\n") is None
    W("K5 TERZO CASO CHE DEVE FALLIRE: `ESITO: PASSATO` (senza `n/m`) -> `None` -> %s\n"
      % ("OK" if ok5 else "*** inventa un esito ***"))
    e.append(ok5)
    # QUARTO: `esito` NON a inizio riga (dentro la prosa) non conta. E' la parte
    # dell'ancoraggio che NON si allarga: senza, ogni frase diventa un verdetto.
    ok6 = verdetto("il suo esito: 9/9 secondo me\n") is None
    W("K6 QUARTO CASO CHE DEVE FALLIRE: `esito: 9/9` DENTRO la prosa -> `None` -> %s\n"
      % ("OK" if ok6 else "*** legge la prosa come verdetto ***"))
    e.append(ok6)
    ok = all(e)
    W("-" * 92 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    if not collaudo(sys.stdout.write):
        return 1
    righe = []
    W = righe.append
    W(INI)
    W("")
    W("## ✅ CURE VERIFICATE — **flag · sigillo · prova · esito · stato**")
    W("")
    W("> **Decisione di Luca, 2026-09-22.** Si aggiorna **nello stesso commit** in cui una cura "
      "viene sigillata o provata.")
    W("> **Generata da `csv/_cure_verificate.py`:** il **DEFAULT** si legge dal sorgente a ogni "
      "giro e l'esito del sigillo dal suo referto; **prova, esito e stato sono LETTURE**, "
      "scritte a mano.")
    W(">")
    W("> **⚠ IL FATTO CHE LA TABELLA RENDE VISIBILE:** **quasi tutte le cure hanno default "
      "`False`** e **le accende il DRIVER, run per run**. Non sono «nel codice»: sono "
      "**nell'argv**. **Un run che dimentica un flag gira su un sistema che si sa difettoso** "
      "*(`P2`)*, e nessuno se ne accorgerebbe dal sorgente.")
    W("")
    W("| flag | cura | **default** | sigillo | prova | esito | stato |")
    W("|---|---|:--:|--:|---|---|---|")
    n_on = 0
    for flag, nome, sig, ref, prova, esito, stato in CURE:
        d = default(flag)
        if d == "True":
            n_on += 1
        dd = ("**`%s`**" % d) if d else "— **assente**"
        W("| `%s` | %s | %s | %s | %s | %s | %s |"
          % (flag, nome, dd, esito_sigillo(ref, sig), prova, esito, stato))
    W("")
    W("**Cure con default ACCESO: %d su %d.**" % (n_on, len(CURE)))
    W("")
    W("### ⛔ E QUESTO NON E' UNA CURA: e' un **PRESIDIO STRUTTURALE**")
    W("")
    W("> Non corregge un difetto MISURATO, perche' la legge **non ha mai girato** e quindi non "
      "ha prodotto nulla da curare. **Impedisce** che venga accesa. Metterlo fra le cure "
      "gonfierebbe il conto.")
    W("")
    W("| flag | che cosa impedisce | **default** | come | sigillo |")
    W("|---|---|:--:|---|--:|")
    W("| `TW_SPINORE` | **il PONTE INVERSO**: `tw` (la cui scala viene da `phi`) scrive lo "
      "SPINORE — `tw` -> `omega_s` -> `_psi_spinor` (`:3090-3100`). Le **uniche due** "
      "`INVERSA` su 139 punti della mappa del `4pi` | **`%s`** | il simulatore **RIFIUTA DI "
      "PARTIRE** in `_applica_flag`, col messaggio che nomina la ragione. **Il ramo resta** "
      "(par.10) | **`6/6`** *(`CURA 1`)* |" % (default("TW_SPINORE") or "?"))
    W("")
    W("### ⚠ E QUESTE NON SONO CURE: sono **PROVE DI SPEGNIMENTO**")
    W("")
    W("> Il flag e' **`True`** — la legge **gira** — e **spegnerlo e' il test**. "
      "Metterle fra le cure gonfierebbe il conto.")
    W("")
    W("| flag | legge | **default** | sigillo | prova | esito |")
    W("|---|---|:--:|--:|---|---|")
    for flag, nome, sig, prova, esito in SPEGNIMENTI:
        d = default(flag)
        W("| `%s` | %s | %s | %s | %s | %s |"
          % (flag, nome, ("**`%s`**" % d) if d else "—", sig, prova, esito))
    W("")
    W(FIN)
    blocco = "\n".join(righe)

    t = io.open(CODA, encoding="utf-8", newline="").read()
    if INI in t and FIN in t:
        a = t.index(INI)
        b = t.index(FIN) + len(FIN)
        t = t[:a] + blocco + t[b:]
        dove = "rigenerata"
    else:
        anc = "\n<!-- DIFETTI-NUOVI-INIZIO -->"
        assert t.count(anc) == 1, "ancora non unica"
        t = t.replace(anc, "\n" + blocco + "\n" + anc)
        dove = "inserita prima dei DIFETTI"
    io.open(CODA, "w", encoding="utf-8", newline="\n").write(t)
    print("sezione CURE VERIFICATE %s: %d cure (%d accese di default), %d prove di spegnimento"
          % (dove, len(CURE), n_on, len(SPEGNIMENTI)))
    print(blocco)
    return 0


if __name__ == "__main__":
    sys.exit(main())
