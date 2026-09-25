# -*- coding: utf-8 -*-
"""SIGILLO -- **IL DRIVER ACCENDE DAVVERO LE CURE APPROVATE?**

> **Un sigillo di cura certifica che il flag FUNZIONA. NON certifica che sia ACCESO.**
> Sono due affermazioni diverse, e la seconda non aveva nessun presidio.

E' il difetto che la sezione `CURE VERIFICATE` rende **visibile** ma non **impedisce**: quasi
tutte le cure hanno `default False` e **le accende il DRIVER, run per run**. Non sono «nel
codice»: sono **nell'argv**. **Un run che dimentica un flag gira su un sistema che si sa
difettoso** *(`P2`)*, e **nessun sigillo se ne accorge**.

**COSA FA:** lancia un PROCESSO NUOVO *(`STANDARD 1`)* che percorre la strada VERA del driver --
la sua `sys.argv` cablata, poi `_cli()`, poi `_applica_flag(a)` -- e **legge lo stato EFFETTIVO
dal MODULO**, non dal comando. **Nessun passo di fisica**: si ferma prima di `avvia_test`.

**E I NOMI DEI FLAG NON SONO UNA LISTA A MANO:** si leggono da `csv/_cure_verificate.py`, la
stessa fonte della sezione `CURE VERIFICATE` -- una cura nuova entra qui **da sola**.

ASCII puro.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
DEST = os.path.join(_QUI, "_sig_driver_accende")

# ⚠ [DECISIONE DI LUCA, 2026-09-24] **IL DRIVER ACCENDE TUTTE LE CURE APPROVATE IN MODO
#   INCONDIZIONATO. UN SOLO MODO DI LANCIARE: NUDA = CAMPAGNA.**
#   Quindi `OBBLIGATORIE` NON e' piu' una lista a mano: sono **TUTTE le cure** di
#   `_cure_verificate.py`, MENO quelle escluse qui sotto **con il loro motivo**.
#   ### E IL PRESIDIO E' PROPRIO QUESTO: una cura nuova che non sia ne' obbligatoria ne'
#   ### esclusa **fa FALLIRE il sigillo**, invece di passare in silenzio.
ESCLUSE = {
    "FASE_2PI": "NON e' approvata: la sua prova la BOCCIA (`Z127`, `2/4`, `E1` non passa -- "
                "mitosi `62` -> `1` evento). Il driver NON deve accenderla.",
    # ✅ `SEMINA_LAM` E' USCITA DALLE ESCLUSE il 2026-09-25 (decisione di Luca, SCENA-1
    #   strada (1)): il vuoto di default del driver e' diventato la SATURAZIONE
    #   (`semina(-1)`, nessun numero), e le scene che seminano masse sopra il vuoto
    #   RIFIUTANO di partire dicendolo (`A9`) invece di adattarsi in silenzio.
    #   **Il criterio `S5` verifica la compatibilita' a ogni corsa**, e se un giorno
    #   tornasse incompatibile lo direbbe.
}

# Le DUE invocazioni, e la differenza fra loro e' il punto di questo sigillo:
#   NUDA      il driver con i soli argomenti posizionali -- cio' che gira se nessuno
#             ricorda gli `=on`;
#   CAMPAGNA  gli argomenti che `_g4_prova.py` passa davvero, copiati dal
#             `CONFIGURAZIONE.txt` di un run vero (non da un ricordo).
INVOCAZIONI = {
    "NUDA": [],
    "CAMPAGNA": ["--sep=4.0", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
                 "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
                 "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on",
                 "--invarianti=on"],
}


def figlio():
    """Percorre la strada VERA del driver e dichiara lo stato del modulo. Senza fisica."""
    os.chdir(RADICE)
    t = io.open(DRIVER, encoding="utf-8").read()
    # si esegue il driver fino ALLA RIGA DOPO `_applica_flag`, poi si esce: il taglio e'
    # sull'ANCORA `_applica_flag(a)`, cercata nel testo INTERO (`STANDARD 9`), non su una riga.
    anc = "S._applica_flag(a)"
    assert t.count(anc) == 1, "ancora non unica nel driver: %d" % t.count(anc)
    testa = t[:t.index(anc) + len(anc)]
    # si cattura l'argv COSTRUITA DAL DRIVER: e' `sys.argv` nel momento in cui chiama
    # `_cli()`, cioe' subito prima dell'ancora. Si aggiunge una riga al testo eseguito,
    # invece di ricostruirla -- **ricostruirla sarebbe una SECONDA formula per la stessa
    # cosa**, ed e' l'errore che questo repo insegue.
    testa += "\n_ARGV_SIM = list(sys.argv)\n"
    g = {"__name__": "__main__", "__file__": DRIVER}
    vecchio = list(sys.argv)
    sys.argv = (["_scena_video.py", "1", os.path.join(DEST, "_scarto")]
                + INVOCAZIONI[sys.argv[2] if len(sys.argv) > 2 else "NUDA"])
    try:
        exec(compile(testa, DRIVER, "exec"), g)
    finally:
        sys.argv = vecchio
    S = g.get("S") or sys.modules["soliton_simulator"]
    for nome in sorted(set(obbligatorie()) | set(_flag_delle_cure())):
        sys.stdout.write("STATO %s %s\n" % (nome, getattr(S, nome, "ASSENTE")))
    # [3, richiesta di Luca 2026-09-24] L'INTERA ARGV che il driver ha costruito per il
    # simulatore. **Le cure della lista non bastano:** `CHI_COOP` era passato `=on` dalla
    # campagna e `"off"` di default nel driver, e il sigillo NON LO VEDEVA perche' non e' in
    # `_cure_verificate.py`. **Era un ORFANO FUORI DALLA LISTA -- il caso esatto che il
    # controllo delle orfane doveva impedire, e che non poteva vedere.**
    # Si dichiara l'argv INTERA, e il confronto fra le due invocazioni non ha piu' una lista
    # a cui essere fedele.
    for k, v in enumerate(g.get("_ARGV_SIM") or sys.modules["soliton_simulator"].__dict__
                          .get("_argv_mai", []) or []):
        sys.stdout.write("ARGV %d %s\n" % (k, v))
    return 0


def _flag_delle_cure():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    try:
        from _cure_verificate import CURE
        return [c[0] for c in CURE]
    except Exception:
        return []


def obbligatorie():
    """TUTTE le cure, meno le `ESCLUSE`. **Non una lista a mano.**"""
    return tuple(f for f in _flag_delle_cure() if f not in ESCLUSE)


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    ref = io.open(os.path.join(DEST, "REFERTO.txt"), "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        ref.write(s)

    P("# SIGILLO -- IL DRIVER ACCENDE DAVVERO LE CURE APPROVATE?\n#\n")
    P("# Un sigillo di cura certifica che il flag FUNZIONA. NON che sia ACCESO.\n")
    P("# Questo certifica il secondo, ed e' l'unico che lo fa.\n#\n")

    # --- COLLAUDO: il criterio deve saper dire NO
    P("COLLAUDO (`P1-sexies`), con il caso che DEVE fallire\n" + "-" * 92 + "\n")
    e = []
    t = io.open(DRIVER, encoding="utf-8").read()
    for nome, atteso in (("--tempo-unico-mitosi", True), ("--flag-che-non-esiste", False)):
        c = ('"%s"' % nome) in t
        ok = (c is atteso)
        P("K%d `%s` nell'argv del driver: %s (atteso %s) -> %s\n"
          % (len(e) + 1, nome, c, atteso, "OK" if ok else "*** NO ***"))
        e.append(ok)
    P("   -> IL SECONDO E' IL CASO CHE DEVE FALLIRE: se il criterio dicesse `True` a tutto,\n")
    P("      direbbe `True` anche a un flag inventato.\n")
    P("   !! E QUESTO E' SOLO IL TESTO. IL TEST VERO E' SOTTO: lo stato del MODULO.\n")
    if not all(e):
        P("\n*** COLLAUDO FALLITO ***\n")
        ref.close()
        return 1
    P("-" * 92 + "\n  -> i criteri PASSANO\n\n")

    # --- i DUE figli
    letti = {}
    argvi = {}
    for modo in ("NUDA", "CAMPAGNA"):
        cmd = [sys.executable, os.path.abspath(__file__), "--figlio", modo]
        r = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        d = {}
        av = []
        for riga in (r.stdout or "").splitlines():
            m = re.match(r"^STATO (\w+) (\S+)$", riga.strip())
            if m:
                d[m.group(1)] = m.group(2)
            m = re.match(r"^ARGV (\d+) (.*)$", riga.rstrip())
            if m:
                av.append(m.group(2))
        argvi[modo] = av
        if r.returncode != 0 or not d:
            P("*** IL FIGLIO %s E' MORTO (rc=%d) ***\n%s\n"
              % (modo, r.returncode, (r.stdout + r.stderr)[-3000:]))
            ref.close()
            return 1
        letti[modo] = d

    P("LO STATO EFFETTIVO DEL MODULO dopo `_cli()` + `_applica_flag(a)`,\n")
    P("percorrendo la sys.argv CABLATA NEL DRIVER, in un PROCESSO NUOVO (`STANDARD 1`).\n")
    P("DUE INVOCAZIONI, e la differenza fra loro e' il punto:\n")
    P("  NUDA      i soli argomenti posizionali -- cio' che gira se nessuno ricorda gli `=on`\n")
    P("  CAMPAGNA  gli argomenti che `_g4_prova.py` passa davvero\n\n")
    OBB = obbligatorie()
    P("  %-24s %-10s %-10s %s\n" % ("flag", "NUDA", "CAMPAGNA", ""))
    esiti = []
    nudi_spenti = []
    orfane = []
    for nome in sorted(letti["NUDA"]):
        vn, vc = letti["NUDA"][nome], letti["CAMPAGNA"].get(nome, "?")
        if nome in OBB:
            ok = (vn == "True" and vc == "True")
            esiti.append(ok)
            if vc == "True" and vn != "True":
                nudi_spenti.append(nome)
            nota = "**DEVE essere True in ENTRAMBE** -> %s" % ("PASS" if ok else "*** FAIL ***")
        elif nome in ESCLUSE:
            ok = (vn != "True" and vc != "True")
            esiti.append(ok)
            nota = "**ESCLUSA, deve restare False** -> %s" % ("PASS" if ok else "*** FAIL ***")
        else:
            orfane.append(nome)
            nota = "⚠ **ORFANA: ne' obbligatoria ne' esclusa**"
        P("  %-24s %-10s %-10s %s\n" % (nome, vn, vc, nota))

    # ================== `S5`: LA SCENA DI DEFAULT E' COMPATIBILE CON `SEMINA_LAM`? ========
    # ⛔ NON E' UNA DOMANDA RETORICA, ed e' la verifica che Luca ha chiesto NELLO STESSO
    #   mandato in cui ha deciso `NUDA = CAMPAGNA`. Il vuoto di default del driver e'
    #   `semina(SEME_INIZIALE)` in raggio `_scala_sistema()*0.5`, e con `SEMINA_LAM` acceso
    #   la semina **RIFIUTA** se `n` supera la saturazione vera.
    #   **Si MISURA, non si deduce**, e il risultato va nel referto anche (e soprattutto) se
    #   dice che le due cose non stanno insieme.
    import importlib.util as _iu2
    _spec = _iu2.spec_from_file_location("sim_s5", os.path.join(RADICE,
                                                               "soliton_simulator.py"))
    _S5 = _iu2.module_from_spec(_spec)
    _spec.loader.exec_module(_S5)
    _S5.SEMINA_LAM = True
    _net5 = _S5.Rete(42)
    _rif, _sat, _err = False, None, ""
    # ⚠ SI PROVA CIO' CHE IL DRIVER FA ADESSO, non la domanda vecchia. Dal 2026-09-25
    #   (`SCENA-1` strada (1)) il vuoto di default e' `semina(-1 if SEMINA_LAM else a.nodi)`,
    #   cioe' **LA SATURAZIONE**. La prima stesura di `S5` chiedeva ancora
    #   `semina(SEME_INIZIALE)`, e diceva INCOMPATIBILE su una strada che il driver non usa
    #   piu': **un criterio che prova la domanda di ieri da' la risposta di ieri.**
    try:
        _net5.semina(-1 if _S5.SEMINA_LAM else _S5.SEME_INIZIALE)
        _sat = int(_net5.n)
    except SystemExit as _e:
        _rif = True
        _err = str(_e)
        for _r in _err.split(chr(10)):
            if "collocati" in _r:
                try:
                    _sat = int(_r.split("=")[1].split()[0])
                except Exception:
                    pass
    P("")
    P("  " + "=" * 96)
    P("  `S5` -- LA SCENA DI DEFAULT DEL DRIVER E' COMPATIBILE CON `SEMINA_LAM`?")
    P("  " + "=" * 96)
    P("     vuoto di default: `semina(%s)` in raggio %.6f    LAM = %.6f"
      % ("-1 = SATURAZIONE" if _S5.SEMINA_LAM else str(_S5.SEME_INIZIALE),
         _S5._scala_sistema() * 0.5, _S5.LAM))
    P("     con `SEMINA_LAM` acceso: %s" % ("RIFIUTA" if _rif else "non rifiuta"))
    P("     saturazione vera: %s nodi   contro %d chiesti" % (_sat, _S5.SEME_INIZIALE))
    if _rif:
        P("     -> ⛔ **INCOMPATIBILE.** Accendere `SEMINA_LAM` nel driver ROMPEREBBE ogni")
        P("        scena che semina il vuoto di DEFAULT. E non si aggira con un numero,")
        P("        perche' **LA CAPIENZA DIPENDE DAL SEME** (misurato: 12807/12783/12812/12790).")
        P("        ✅ E' compatibile con la scena `(ii)`, che semina a `--nodi 0` e costruisce")
        P("        il vuoto da se' fino a SATURAZIONE.")
        P("        ⚠ PER QUESTO `SEMINA_LAM` E' FRA LE `ESCLUSE`, **e non per merito**: e' un")
        P("        CONFLITTO DI SCENA. **La decisione e' di Luca, e questo criterio mette il")
        P("        numero davanti invece di nascondere l'esclusione.**")
    else:
        P("     -> ✅ COMPATIBILE: il vuoto di default e' LA SATURAZIONE (`semina(-1)`), e")
        P("        `SEMINA_LAM` e' OBBLIGATORIA. Il numero di nodi lo decide la GEOMETRIA, non un")
        P("        parametro -- e questo e' cio' che rende la compatibilita' STABILE: non c'e' un")
        P("        numero che possa diventare sbagliato quando il seme cambia.")
        P("        ⚠ E le scene che seminano masse SOPRA il vuoto RIFIUTANO di partire (`A9`):")
        P("        `_massa` solleva con `SEMINA_LAM` acceso. Sono di EPOCA PRE-`A13`.")
    P("")
    P("\n  CURE OBBLIGATORIE: %d   ESCLUSE: %d   ORFANE: %d\n"
      % (len(OBB), len(ESCLUSE), len(orfane)))
    for k, v in sorted(ESCLUSE.items()):
        P("    escl. %-20s %s\n" % (k, v))
    if orfane:
        esiti.append(False)
        P("\n  *** ORFANE: %s ***\n" % ", ".join(orfane))
        P("  Una cura che non e' ne' obbligatoria ne' esclusa **passerebbe in silenzio**.\n")
        P("  Si dichiara in `ESCLUSE` col suo motivo, oppure il driver deve accenderla.\n")
    if nudi_spenti:
        P("\n  *** ACCESE SOLO DAL COMANDO: %s ***\n" % ", ".join(nudi_spenti))
        P("  **NUDA != CAMPAGNA**, e la decisione di Luca del 2026-09-24 dice che devono\n")
        P("  coincidere: *un solo modo di lanciare*. Quelle cure non sono nel codice, sono\n")
        P("  **nell'argv di CHI LANCIA**, e un comando che ne dimentica una gira su un sistema\n")
        P("  che si sa difettoso (`P2`) **senza che nessun sigillo se ne accorga**.\n")
    else:
        P("\n  ✅ **NUDA = CAMPAGNA su tutte le obbligatorie: UN SOLO MODO DI LANCIARE.**\n")
        P("     Nessuna cura approvata si puo' piu' dimenticare da riga di comando.\n")

    # ---------------------------------------------------------------- l'ARGV INTERA
    P("\n" + "=" * 92 + "\nL'ARGV INTERA: NUDA contro CAMPAGNA -- **non solo le cure**\n"
      + "=" * 92 + "\n")
    P("  `CHI_COOP` era passato `=on` dalla campagna e `\"off\"` di default nel driver, e il\n")
    P("  sigillo NON LO VEDEVA: non e' in `_cure_verificate.py`. **ORFANO FUORI DALLA LISTA**\n")
    P("  -- il caso esatto che il controllo delle orfane doveva impedire e non poteva vedere.\n")
    P("  **Qui il confronto non ha piu' una lista a cui essere fedele.** (Rilievo di Luca.)\n\n")
    an, ac = argvi.get("NUDA", []), argvi.get("CAMPAGNA", [])
    P("  NUDA     (%d elementi)\n  CAMPAGNA (%d elementi)\n\n" % (len(an), len(ac)))
    sn, sc = set(an), set(ac)
    solo_c = [x for x in ac if x not in sn]
    solo_n = [x for x in an if x not in sc]
    # le opzioni VALORIZZATE (`--x=v` o `--x v`) si confrontano per NOME, senno' un valore
    # diverso comparirebbe come «due opzioni diverse» invece che come UNA che cambia valore.
    def coppie(a):
        fuori, k = {}, 0
        while k < len(a):
            x = a[k]
            if x.startswith("--") and "=" in x:
                nm, vv = x.split("=", 1)
                fuori[nm] = vv
            elif x.startswith("--") and k + 1 < len(a) and not a[k + 1].startswith("--"):
                fuori[x] = a[k + 1]
                k += 1
            elif x.startswith("--"):
                fuori[x] = True
            k += 1
        return fuori
    cn, cc = coppie(an), coppie(ac)
    diff = []
    for nm in sorted(set(cn) | set(cc)):
        vn, vc = cn.get(nm, "(assente)"), cc.get(nm, "(assente)")
        if vn != vc:
            diff.append((nm, vn, vc))
    if diff:
        P("  ⚠ **DIFFERENZE: %d**\n\n" % len(diff))
        P("    %-26s %-16s %-16s\n" % ("opzione", "NUDA", "CAMPAGNA"))
        for nm, vn, vc in diff:
            P("    %-26s %-16s %-16s\n" % (nm, vn, vc))
        P("\n  **OGNI DIFFERENZA VA SPIEGATA O TOLTA.** Una che resta senza motivo e' un modo\n")
        P("  diverso di lanciare, e la decisione di Luca dice che ce ne deve essere UNO SOLO.\n")
    else:
        P("  ✅ **NESSUNA DIFFERENZA: le due argv COINCIDONO opzione per opzione.**\n")
    P("  (elementi solo in CAMPAGNA: %d, solo in NUDA: %d -- conteggio grezzo)\n"
      % (len(solo_c), len(solo_n)))
    esiti.append(not diff)

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 92 + "\nESITO: %d/%d (obbligatorie + escluse + orfane + argv intera)\n"
      % (n, len(esiti)) + "=" * 92 + "\n")
    P("*** %s ***\n" % ("IL DRIVER LE ACCENDE." if n == len(esiti) else
                        "IL DRIVER NON LE ACCENDE: reperto, commit, STOP."))
    P("\n!! COSA QUESTO SIGILLO NON DICE: che le cure siano GIUSTE, ne' che il flag FUNZIONI.\n")
    P("   Quelli sono i sigilli di ciascuna cura. Questo dice che ACCADONO nei run --\n")
    P("   l'affermazione che non aveva nessun presidio.\n")
    P("\n!! E IL LIMITE: certifica L'ARGV DI QUESTO DRIVER. Un altro strumento che costruisce\n")
    P("   la propria argv (un sigillo in-process, una sonda) NON e' coperto.\n")
    ref.close()
    return 0 if n == len(esiti) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--figlio":
        sys.exit(figlio())
    sys.exit(main())
