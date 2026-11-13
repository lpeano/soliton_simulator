# -*- coding: utf-8 -*-
r"""**IL REGISTRO E LA SUITE VERA** *(la decisione (b) di Luca, `2026-11-13` `12:58`; i DEVE del testo delle `12:22`, arrivato alle `13:00`; il task history
`doc/TASK_HISTORY/2026-11-13_registro_corse.md`, sez. `6`)*.

    python csv/solitone/prova_suite_registro.py --modo tappa --nome <una voce APERTA> --log <fuori dal repo> > doc/referti_l2/registro_suite_tappa.txt
    python csv/solitone/prova_suite_registro.py --modo registro --log <fuori dal repo> > doc/referti_l2/registro_suite_registro.txt

### **Lancia `primo_ordine/collauda.py`, legge la sua uscita riga per riga e AGISCE alla riga «TUTTI I COLLAUDI, CON I TEMPI»** *(la suite l'ha appena stampata DOPO la fotografia
dell'albero, `_prima`: cio' che cambia da li' in poi la suite lo vede)*:
- **`tappa`:** **una tappa della voce APERTA `--nome`** *(nel file FUORI dal repo)*: ### **DEVE PASSARE: la suite esce con `0`, il registro del repo uguale, la tappa nel file esterno;**
- **`registro`:** **una TAPPA scritta nel registro DEL REPO** *(`doc/REGISTRO_CORSE.md`, una riga `- {json}` in fondo: il modo di prima della decisione (b))*: ### **DEVE FALLIRE: «la suite esce
  con `0`»** *(la suite se ne accorge e deve uscire con `1`, come oggi)*; **e dopo il registro e' rimesso com'era** *(lo sha prima e dopo; la suite lo rimette con `git checkout`)*.
**L'uscita intera della suite va in `--log`** *(fuori dal repo)*; **qui le righe del verdetto.** **Nessun `sleep`, nessun polling: si agisce sulla riga.**
"""
import argparse
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _registro_corse as RC  # noqa: E402

RIGA_FOTO = "TUTTI I COLLAUDI, CON I TEMPI"      # ### primo_ordine/collauda.py, main: stampata subito dopo _prima = _sporchi()
TRACCIATO = RC.REGISTRO[0]           # ### Luca 12:22: il DEVE FALLIRE scrive una tappa nel registro DEL REPO
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "_registro_corse.py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", required=True, choices=("tappa", "registro"))
    ap.add_argument("--nome")
    ap.add_argument("--log", required=True)
    x = ap.parse_args(argv)
    assert not os.path.abspath(x.log).startswith(os.path.abspath(RC.RADICE)), "il log va FUORI dal repo"
    if x.modo == "tappa":
        assert x.nome in RC.aperte(), "la voce %r NON e' aperta nel registro" % x.nome
    st0 = subprocess.check_output(["git", "status", "--porcelain"], cwd=RC.RADICE).decode("utf-8", "replace")
    sha_reg, sha_tr = RC.sha1_byte(RC.REGISTRO[0]), RC.sha1_byte(TRACCIATO)
    n_tappe = len(RC.tappe_di(x.nome)) if x.modo == "tappa" else None
    print("=" * 120)
    print("IL REGISTRO E LA SUITE VERA, il modo %s: l'albero all'inizio %s; il registro %s; il file toccato nel modo registro %s %s" % (
        x.modo, "PULITO" if not st0.strip() else "con %d righe di stato" % len(st0.splitlines()), sha_reg[:8], os.path.relpath(TRACCIATO, RC.RADICE), sha_tr[:8]))
    print("=" * 120)
    agito = None
    with open(x.log, "w", encoding="utf-8") as log:
        pr = subprocess.Popen([sys.executable, os.path.join(RC.RADICE, "primo_ordine", "collauda.py")], cwd=RC.RADICE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              encoding="utf-8", errors="replace")
        for riga in pr.stdout:
            log.write(riga)
            if agito is None and RIGA_FOTO in riga:
                if x.modo == "tappa":
                    RC.tappa(x.nome, "la tappa scritta DURANTE la suite (il collaudo del registro)")
                    agito = "una tappa di %s nel file esterno" % x.nome
                else:
                    finta = {"ev": "TAPPA", "nome": "prova-suite-registro", "ora": RC.ora(), "punto": "una tappa scritta nel registro DEL REPO durante la suite (DEVE FALLIRE)"}
                    with open(TRACCIATO, "ab") as f:
                        f.write(("- " + json.dumps(finta, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
                    agito = "una tappa scritta in fondo al registro del repo %s" % os.path.relpath(TRACCIATO, RC.RADICE)
                log.write("### [IL DRIVER] %s\n" % agito)
                log.flush()
            if "TUTTI I COLLAUDI PASSANO" in riga or "COLLAUDI FALLISCONO" in riga or "LA SUITE HA SPORCATO" in riga or "RIMESSI A POSTO" in riga:
                print("  la suite: %s" % riga.rstrip())
        rc = pr.wait()
    print("  il driver ha agito: %s; la suite e' uscita con %d" % (agito, rc))
    sha_reg2, sha_tr2 = RC.sha1_byte(RC.REGISTRO[0]), RC.sha1_byte(TRACCIATO)
    st1 = subprocess.check_output(["git", "status", "--porcelain"], cwd=RC.RADICE).decode("utf-8", "replace")
    esito("il driver ha agito DOPO la fotografia dell'albero (la riga %r)" % RIGA_FOTO, agito is not None, str(agito), True)
    if x.modo == "tappa":
        tt = RC.tappe_di(x.nome)
        esito("una tappa scritta durante la suite: la suite esce con 0, il registro del repo uguale, la tappa nel file esterno",
              rc == 0 and sha_reg2 == sha_reg and len(tt) == n_tappe + 1, "uscita %d; il registro %s -> %s; le tappe %d -> %d" % (rc, sha_reg[:8], sha_reg2[:8], n_tappe, len(tt)), True)
    else:
        esito("una tappa scritta nel registro DEL REPO durante la suite: la suite esce con 0", rc == 0, "uscita %d" % rc, False)
        esito("e dopo il registro e' rimesso com'era (lo sha prima e dopo)", sha_tr2 == sha_tr, "%s -> %s" % (sha_tr[:8], sha_tr2[:8]), True)
    esito("l'albero alla fine come all'inizio (git status)", st1 == st0, "%d righe -> %d righe" % (len(st0.splitlines()), len(st1.splitlines())), True)
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
