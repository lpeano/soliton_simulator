# -*- coding: utf-8 -*-
"""SIGILLO DEI FLAG DEL DRIVER -- ogni opzione `=on` ARRIVA DAVVERO AL MODULO. [BLOCCANTE]

⚠ PERCHE' ESISTE, e non e' un principio generale: il 2026-09-21 il ramo D e' girato per 1200
  passi con `SCALA_MIN` e `COES_ADIM` **SPENTI** mentre il comando li chiedeva **ACCESI**.
  Le opzioni erano PARSATE -- `--scala-min=on` non finiva in `_resti`, non dava errore, non
  stampava nulla di anomalo -- ma **non venivano MAI aggiunte all'argv del simulatore**.
  **Un'opzione che si accetta e si ignora e' peggio di un'opzione che non esiste, perche' non si
  lamenta.**
  E nessun sigillo esistente poteva accorgersene: `_sigillo_ramo_D.py` e `_sigillo_Z1c.py`
  costruiscono `sys.argv` DA SOLI e **non passano dal driver**; `_sigillo_chicoop_driver.py`
  copriva `--chi-coop` e basta. **Mancava il test che attraversa il percorso del driver.**

COSA FA, e la parte che conta e' che **NON HA UN ELENCO SCRITTO A MANO**:
  scopre le opzioni booleane LEGGENDO IL SORGENTE del driver (quelle il cui parsing impone
  `("on", "off")`), ne deriva il nome del flag di modulo, e verifica che:
    F1  [BLOCCANTE] con `=on`  il flag nel MODULO e' True
    F2  [BLOCCANTE] con `=off` il flag nel MODULO e' False
    F3  [BLOCCANTE] ogni opzione scoperta e' anche CABLATA nell'argv: se il sorgente la parsa ma
        non la inoltra, F1 fallisce -- e F3 lo dice per NOME, cosi' il messaggio punta al difetto
        invece che al sintomo.
  **Se domani qualcuno aggiunge un'opzione e si dimentica di cablarla, questo sigillo la trova
  DA SOLO**, perche' l'elenco nasce dal codice e non da una lista che va ricordata (`A9`).

I flag si leggono DAL MODULO, dal blocco che il driver stampa dopo `_applica_flag` -- P6: dai
dati, non dal comando.
ASCII PURO.
"""
import os
import re
import shutil
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_flag_driver")
NF = 1          # UN frame: qui non si misura fisica, si guarda un blocco di stampa

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-4s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


def opzioni_dal_sorgente():
    """Le opzioni booleane del driver, SCOPERTE dal codice. Sono quelle il cui parsing impone
    `("on", "off")`: e' la firma di un interruttore, e distingue `--chi-basc=` da `--sep=`."""
    src = open(DRIVER, encoding="utf-8").read()
    opz = {}
    for m in re.finditer(r'_x\.startswith\("--([a-z0-9-]+)="\)\s*:', src):
        nome = m.group(1)
        coda = src[m.end():m.end() + 600]
        mv = re.search(r'([A-Z_0-9]+)\s*=\s*_x\.split', coda)
        if not mv:
            continue
        var = mv.group(1)
        if '("on", "off")' not in coda and "('on', 'off')" not in coda:
            continue            # non e' un interruttore: e' un valore (--sep=, --serie=)
        # e' CABLATO nell'argv?
        cablato = bool(re.search(r'\[\s*"--%s"\s*\]\s*if\s+%s\s*==' % (re.escape(nome), var), src))
        opz[nome] = (var, cablato)
    return opz


def gira(extra):
    dest = os.path.join(BASE, "run")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    cmd = [sys.executable, DRIVER, str(NF), dest] + list(extra)
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-1500:])
        raise SystemExit("il driver e' uscito con %d: %s" % (pr.returncode, " ".join(extra)))
    d = {}
    for m in re.finditer(r"^    ([A-Z_0-9]+)\s+(True|False|ASSENTE)\s*$", pr.stdout, re.M):
        d[m.group(1)] = m.group(2)
    return d


def main():
    os.makedirs(BASE, exist_ok=True)
    opz = opzioni_dal_sorgente()
    print("opzioni booleane SCOPERTE dal sorgente del driver: %d" % len(opz))
    for n, (v, cab) in sorted(opz.items()):
        print("   --%-14s variabile %-10s cablata nell'argv: %s"
              % (n + "=", v, "si'" if cab else "*** NO ***"))
    print("")
    if not opz:
        segna("F0", False, "nessuna opzione scoperta: il criterio non ha nulla da controllare")
        return 1

    non_cablate = sorted(n for n, (v, c) in opz.items() if not c)
    segna("F3", not non_cablate,
          "ogni opzione PARSATA e' anche CABLATA nell'argv: %s"
          % ("si'" if not non_cablate
             else "NO -> %s (parsate e IGNORATE, in silenzio)" % non_cablate))

    nomi = sorted(opz)
    flag = {n: n.replace("-", "_").upper() for n in nomi}
    print("\nbraccio ON   tutte le opzioni a `on`")
    on = gira(["--%s=on" % n for n in nomi])
    print("braccio OFF  tutte le opzioni a `off`")
    off = gira(["--%s=off" % n for n in nomi])
    print("")

    manca = [f for f in flag.values() if f not in on]
    if manca:
        print("   ⚠ questi flag NON sono nel blocco stampato dal driver, quindi non si possono")
        print("     verificare DAL MODULO: %s" % manca)
    male_on = [(n, flag[n], on.get(flag[n])) for n in nomi if on.get(flag[n]) != "True"]
    male_off = [(n, flag[n], off.get(flag[n])) for n in nomi if off.get(flag[n]) != "False"]

    segna("F1", not male_on and not manca,
          "con `=on` ogni flag e' True nel MODULO: %s"
          % ("si' (%d su %d)" % (len(nomi), len(nomi)) if not male_on and not manca
             else "NO -> %s" % [(a, c) for a, b, c in male_on] + (" ; non stampati: %s" % manca if manca else "")))
    segna("F2", not male_off and not manca,
          "con `=off` ogni flag e' False nel MODULO: %s"
          % ("si' (%d su %d)" % (len(nomi), len(nomi)) if not male_off and not manca
             else "NO -> %s" % [(a, c) for a, b, c in male_off]))

    print("")
    print("   il quadro completo, letto DAL MODULO (P6: dai dati, non dal comando):")
    for n in nomi:
        f = flag[n]
        print("     --%-14s %-18s on=%-8s off=%s" % (n + "=", f, on.get(f, "?"), off.get(f, "?")))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: ogni opzione del driver ARRIVA al modulo, in entrambi i versi.")
    else:
        print("VERDETTO: *** UN'OPZIONE NON ARRIVA AL SIMULATORE. *** Un run lanciato con quella")
        print("  opzione misurerebbe una configurazione DIVERSA da quella che il comando chiede,")
        print("  e non se ne accorgerebbe nessuno: e' gia' successo al ramo D il 2026-09-21.")
    print("")
    print("NB: UN frame. Qui non si misura fisica: si verifica che un interruttore sia collegato.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
