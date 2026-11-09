# -*- coding: utf-8 -*-
"""`H-NUCLEO-CONGELATO` -- SUL RAMO `primo-ordine` IL NUCLEO E' CONGELATO *(decisione di Luca, 2026-11-08 21:47-21:49)*.

### **Che cosa impedisce:** sul ramo `primo-ordine`, ### **un commit che tocca un file sotto `primo_ordine/`**
*(il nucleo, le leggi, i collaudi del nucleo, `collauda.py` compreso)*, **finche' `doc/NUCLEO_CONGELATO.md` dice
`stato: CONGELATO`.** **BLOCCA, non avvisa; NESSUNA via d'uscita nel messaggio.**

### **PERCHE' ESISTE:** **dal 2026-11-08 i rami sono DUE** *(il principale senza v2; `zero-nel-nucleo`, il laterale, con v2)*;
**ogni modifica del nucleo si fa SOLO sul laterale e arriva sul principale con la riunione, per decisione di Luca.**
**Luca: «E' IMPOSTO da un controllo automatico, non dalla memoria».**

### **LE REGOLE DI DECISIONE** *(la funzione `decidi`, pura; il collaudo la prova su casi a risposta nota)*:
- **il ramo NON e' `primo-ordine`** *(anche una testa staccata: il limite, dichiarato, `A9`)*: **passa**;
- **`doc/NUCLEO_CONGELATO.md` ASSENTE nell'indice di git: CONGELATO** *(chiuso per difetto: cancellare il file non sblocca)*;
- **lo stato e' `CONGELATO`: ogni file sotto `primo_ordine/`, anche cancellato o rinominato, RIFIUTA;**
- **lo stato e' diverso da `CONGELATO`: passa SOLO se il file ha una riga `decisione_di_luca:` non vuota** *(lo sblocco e' una decisione SCRITTA di Luca)*; **senza: RIFIUTA ogni commit sul principale.**

**COMANDO:** chiamato dal `pre-commit`. A mano: `python csv/_nucleo_congelato.py --pre-commit` ·
`--collaudo` *(i casi a risposta nota)* · `--prova-git` *(il DEVE e il DEVE FALLIRE con commit VERI, in un clone di prova)*.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
RAMO_CONGELATO = "primo-ordine"
CARTELLA = "primo_ordine/"
FILE_STATO = "doc/NUCLEO_CONGELATO.md"
DECISIONE = "Luca 2026-11-08 21:47-21:49: il nucleo del principale congelato fino alla riunione di zero-nel-nucleo (doc/NUCLEO_CONGELATO.md)"


def leggi_stato(testo):
    """### `(stato, decisione)` dal testo del file; `testo None` (assente) = `("CONGELATO", "")`."""
    if testo is None:
        return "CONGELATO", ""
    stato, dec = "CONGELATO", ""
    for r in testo.splitlines():
        r = r.strip()
        if r.startswith("stato:"):
            stato = r[len("stato:"):].strip().strip("`").strip()
        elif r.startswith("decisione_di_luca:"):
            dec = r[len("decisione_di_luca:"):].strip()
    return stato, dec


def decidi(ramo, nomi, testo_stato):
    """### `(passa, motivo)`. `nomi`: i file nell'indice cambiati dal commit *(anche cancellati)*."""
    if ramo != RAMO_CONGELATO:
        return True, "ramo %r: il congelamento vale solo su %s" % (ramo, RAMO_CONGELATO)
    stato, dec = leggi_stato(testo_stato)
    if stato != "CONGELATO":
        if dec:
            return True, "il nucleo SBLOCCATO (stato %r) dalla decisione: %s" % (stato, dec)
        return False, "%s dice stato %r SENZA una riga `decisione_di_luca:`: lo sblocco e' una decisione SCRITTA di Luca" % (FILE_STATO, stato)
    toccati = sorted(n for n in nomi if n.replace("\\", "/").startswith(CARTELLA))
    if toccati:
        return False, "il commit tocca %d file del NUCLEO CONGELATO: %s" % (len(toccati), ", ".join(toccati))
    return True, "nessun file sotto %s" % CARTELLA


def _git(*a, cwd=RADICE):
    r = subprocess.run(["git"] + list(a), cwd=cwd, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def pre_commit(cwd=RADICE):
    rc, ramo = _git("symbolic-ref", "--short", "-q", "HEAD", cwd=cwd)
    ramo = ramo.strip() if rc == 0 else ""
    _rc, nomi = _git("diff", "--cached", "--name-only", "--no-renames", cwd=cwd)
    rc_s, testo = _git("show", ":" + FILE_STATO, cwd=cwd)
    passa, motivo = decidi(ramo, [n for n in nomi.splitlines() if n.strip()], testo if rc_s == 0 else None)
    if passa:
        print("[H-NUCLEO-CONGELATO] %s." % motivo)
        return 0
    print("[H-NUCLEO-CONGELATO] ### RIFIUTATO: %s." % motivo)
    print("  ### La decisione: %s." % DECISIONE)
    print("  ### Ogni modifica del nucleo si fa SOLO sul ramo zero-nel-nucleo (il worktree C:\\Users\\lpeano\\wt_zero) e arriva qui con la riunione.")
    print("  ### Una modifica URGENTE del nucleo sul principale: FERMO e chiedere a Luca; lo sblocco solo con una sua decisione scritta in %s." % FILE_STATO)
    return 1


OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-96s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:96], "PASSA" if passa else "### FALLISCE", nota))
    return buono


def collaudo():
    """### I casi a risposta nota sulla funzione pura `decidi`."""
    C = "stato: CONGELATO\n"
    S_senza = "stato: SBLOCCATO\n"
    S_con = "stato: SBLOCCATO\ndecisione_di_luca: 2026-12-01 la riunione\n"
    casi = [
        ("C-1 principale, un file del nucleo: RIFIUTATO", ("primo-ordine", ["primo_ordine/leggi/leggi.yaml"], C), False),
        ("C-2 principale, un file della libreria: passa", ("primo-ordine", ["csv/solitone/x.py"], C), True),
        ("C-3 principale, il file di stato ASSENTE e un file del nucleo: RIFIUTATO (chiuso per difetto)", ("primo-ordine", ["primo_ordine/collauda.py"], None), False),
        ("C-4 principale, sbloccato SENZA la decisione di Luca: RIFIUTATO", ("primo-ordine", ["doc/x.md"], S_senza), False),
        ("C-5 principale, sbloccato CON la decisione di Luca, un file del nucleo: passa", ("primo-ordine", ["primo_ordine/collauda.py"], S_con), True),
        ("C-6 testa staccata, un file del nucleo: passa (il limite dichiarato)", ("", ["primo_ordine/collauda.py"], C), True),
        ("C-7 principale, un file del nucleo con la barra di Windows: RIFIUTATO", ("primo-ordine", ["primo_ordine\\passo.py"], C), False),
    ]
    for che, (ramo, nomi, testo), atteso in casi:
        passa, motivo = decidi(ramo, nomi, testo)
        esito(che, passa == atteso, motivo)
    passa, motivo = decidi("zero-nel-nucleo", ["primo_ordine/leggi/leggi.yaml"], C)
    esito("C-F il laterale, lo stesso file del nucleo: RIFIUTATO", not passa, motivo, deve=False)
    return 0 if not FALLITE else 1


def prova_git():
    """### Il DEVE e il DEVE FALLIRE di Luca con COMMIT VERI: un clone di prova *(`--shared`, sparso)*, il `pre-commit` che chiama
    SOLO questo presidio; sul ramo `primo-ordine` un file del nucleo DEVE essere rifiutato, sul ramo `zero-nel-nucleo` lo stesso commit DEVE passare."""
    tmp = tempfile.mkdtemp(prefix="nucleo_congelato_")
    try:
        d = os.path.join(tmp, "clone")
        _git("clone", "-q", "--shared", "--no-checkout", RADICE, d, cwd=tmp)
        _git("sparse-checkout", "set", "--no-cone", "primo_ordine/leggi/leggi.yaml", "csv/_nucleo_congelato.py", FILE_STATO, cwd=d)
        rc, out = _git("checkout", "-q", "-B", RAMO_CONGELATO, "origin/" + RAMO_CONGELATO, cwd=d)
        assert rc == 0, out
        def copia():
            """### lo script e il file di stato di QUESTO albero nel clone: a ogni ramo, perche' il `reset --hard` li toglie."""
            os.makedirs(os.path.join(d, "csv"), exist_ok=True)
            os.makedirs(os.path.join(d, "doc"), exist_ok=True)
            shutil.copyfile(os.path.abspath(__file__), os.path.join(d, "csv", "_nucleo_congelato.py"))
            if os.path.exists(os.path.join(RADICE, FILE_STATO)):
                shutil.copyfile(os.path.join(RADICE, FILE_STATO), os.path.join(d, FILE_STATO))
        hk = os.path.join(tmp, "hooks")
        os.makedirs(hk)
        with open(os.path.join(hk, "pre-commit"), "wb") as f:
            f.write(b'#!/bin/sh\npython "$(git rev-parse --show-toplevel)/csv/_nucleo_congelato.py" --pre-commit || exit 1\n')
        y = os.path.join(d, "primo_ordine", "leggi", "leggi.yaml")
        risultati = {}
        for ramo in (RAMO_CONGELATO, "zero-nel-nucleo"):
            if ramo != RAMO_CONGELATO:
                _git("checkout", "-q", "-B", ramo, "origin/" + RAMO_CONGELATO, cwd=d)
            copia()
            with open(y, "ab") as f:
                f.write(b"\n# prova del congelamento\n")
            _git("add", "-f", "primo_ordine/leggi/leggi.yaml", "csv/_nucleo_congelato.py", FILE_STATO, cwd=d)
            r = subprocess.run(["git", "-c", "core.hooksPath=" + hk, "-c", "user.name=prova", "-c", "user.email=prova@invalid",
                                "commit", "-q", "-m", "prova del congelamento"], cwd=d, capture_output=True)
            testo = (r.stdout + r.stderr).decode("utf-8", errors="replace")
            risultati[ramo] = (r.returncode, testo)
            _git("reset", "-q", "--hard", "origin/" + RAMO_CONGELATO, cwd=d)
        rc0, t0 = risultati[RAMO_CONGELATO]
        esito("G-1 un commit VERO sul ramo primo-ordine che tocca primo_ordine/leggi/leggi.yaml: RIFIUTATO dal presidio",
              rc0 != 0 and "H-NUCLEO-CONGELATO] ### RIFIUTATO" in t0, "codice %d; %s" % (rc0, t0.strip().splitlines()[0] if t0.strip() else ""))
        rc1, t1 = risultati["zero-nel-nucleo"]
        esito("G-F lo stesso commit sul ramo zero-nel-nucleo: RIFIUTATO", rc1 != 0, "codice %d; %s" % (rc1, t1.strip().splitlines()[0] if t1.strip() else ""), deve=False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--pre-commit" in a:
        sys.exit(pre_commit())
    rc = 0
    if "--collaudo" in a:
        rc |= collaudo()
    if "--prova-git" in a:
        rc |= prova_git()
    if not a:
        print("uso: --pre-commit | --collaudo | --prova-git")
        rc = 2
    if "--collaudo" in a or "--prova-git" in a:
        print("### %d su %d come devono%s" % (OK[0], OK[1], ("   FALLITE: " + "; ".join(FALLITE)) if FALLITE else ""))
    sys.exit(rc)
