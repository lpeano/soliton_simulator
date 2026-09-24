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

# le cure che il driver DEVE accendere in ogni run, e che NON dipendono da un `=on` del comando
OBBLIGATORIE = ("RITMO_WRAP_2PI", "TEMPO_UNICO_MITOSI")

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
    g = {"__name__": "__main__", "__file__": DRIVER}
    vecchio = list(sys.argv)
    sys.argv = (["_scena_video.py", "1", os.path.join(DEST, "_scarto")]
                + INVOCAZIONI[sys.argv[2] if len(sys.argv) > 2 else "NUDA"])
    try:
        exec(compile(testa, DRIVER, "exec"), g)
    finally:
        sys.argv = vecchio
    S = g.get("S") or sys.modules["soliton_simulator"]
    for nome in sorted(set(OBBLIGATORIE) | set(_flag_delle_cure())):
        sys.stdout.write("STATO %s %s\n" % (nome, getattr(S, nome, "ASSENTE")))
    return 0


def _flag_delle_cure():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    try:
        from _cure_verificate import CURE
        return [c[0] for c in CURE]
    except Exception:
        return []


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
    for modo in ("NUDA", "CAMPAGNA"):
        cmd = [sys.executable, os.path.abspath(__file__), "--figlio", modo]
        r = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        d = {}
        for riga in (r.stdout or "").splitlines():
            m = re.match(r"^STATO (\w+) (\S+)$", riga.strip())
            if m:
                d[m.group(1)] = m.group(2)
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
    P("  %-24s %-10s %-10s %s\n" % ("flag", "NUDA", "CAMPAGNA", ""))
    esiti = []
    nudi_spenti = []
    for nome in sorted(letti["NUDA"]):
        vn, vc = letti["NUDA"][nome], letti["CAMPAGNA"].get(nome, "?")
        if nome in OBBLIGATORIE:
            ok = (vn == "True" and vc == "True")
            esiti.append(ok)
            nota = "**DEVE essere True in ENTRAMBE** -> %s" % ("PASS" if ok else "*** FAIL ***")
        else:
            if vn != "True" and vc == "True":
                nudi_spenti.append(nome)
                nota = "⚠ **accesa SOLO dal comando**"
            else:
                nota = "*(dipende dal comando)*"
        P("  %-24s %-10s %-10s %s\n" % (nome, vn, vc, nota))
    P("\n  ⚠ CURE CHE L'INVOCAZIONE NUDA NON ACCENDE: %d su %d -- %s\n"
      % (len(nudi_spenti), len(letti["NUDA"]), ", ".join(nudi_spenti) or "nessuna"))
    P("     Non e' un difetto del driver: e' il FATTO che `CURE VERIFICATE` rende visibile.\n")
    P("     Quelle cure **non sono nel codice: sono nell'argv di CHI LANCIA**, e un comando\n")
    P("     che ne dimentica una gira su un sistema che si sa difettoso (`P2`) **senza che\n")
    P("     nessun sigillo se ne accorga**. Le DUE obbligatorie sono le uniche che il DRIVER\n")
    P("     accende da se', e quindi le uniche che non si possono dimenticare.\n")

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 92 + "\nESITO: %d/%d sulle cure OBBLIGATORIE\n" % (n, len(esiti)) + "=" * 92 + "\n")
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
