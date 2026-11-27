# -*- coding: utf-8 -*-
r"""**[M1107] A4: IL LANCIATORE A SECCO DALLA CARTELLA NUOVA** *(DECISIONE DI LUCA, 2026-11-27 `11:07`; nessun lancio: `coda_m1446.py` non ha un modo a secco, quindi si IMPORTA senza chiamare `main()`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/prova_secco_coda.py > doc/referti_l2/prova_secco_coda.txt

**DEVE**, dalla cartella nuova *(`E:\soliton_lavoro\wt_lapse_u`)*: la radice del lanciatore e' la cartella nuova; la lista `coda_m1446.json` si legge; lo stato `E:\soliton_simulator\controllo\M1446\coda_stato.json` *(il percorso vecchio)* si legge; lo script del registro `csv/solitone/_registro_corse.py` esiste sotto la radice nuova, e il suo `REGISTRO` *(`doc/REGISTRO_CORSE.md`, nel repo)* e le sue `TAPPE` *(`E:\soliton_simulator\registro_tappe`, il percorso vecchio)* esistono; la cartella degli stati `E:\soliton_simulator\controllo\M2034\coppia\d1` *(il percorso vecchio)* ha i suoi `25` stati; **nessuna corsa da lanciare** *(ogni voce della lista ha gia' uno stato nel file di stato)*. **Nessun file si scrive.**
"""
import glob
import importlib.util
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
_RAD = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(_RAD, "csv"))


def carica(nome, f):
    sp = importlib.util.spec_from_file_location(nome, f)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "coda_m1446.py"))
    _presidio.avvia(__file__)
    print("=" * 110)
    print("[M1107] A4: coda_m1446.py A SECCO dalla cartella nuova (importato, main() NON chiamato)")
    print("=" * 110)
    OK = []

    def deve(che, ok, nota=""):
        OK.append(bool(ok))
        print("  DEVE: %-75s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    Q = carica("coda_m1446", os.path.join(_QUI, "coda_m1446.py"))
    deve("la radice del lanciatore e' la cartella nuova", os.path.normcase(os.path.abspath(Q._RADICE)) == os.path.normcase(os.path.abspath(r"E:\soliton_lavoro\wt_lapse_u")), Q._RADICE)
    L = json.load(open(Q.LISTA, encoding="utf-8"))
    deve("la lista si legge", isinstance(L, dict) and L.get("corse"), "%s: %d voci" % (Q.LISTA, len(L.get("corse", []))))
    S = json.load(open(Q.STATO, encoding="utf-8"))
    deve("lo stato (il percorso vecchio) si legge", "corse" in S, "%s: %d corse; l'ultimo evento: %s" % (Q.STATO, len(S["corse"]), S["eventi"][-1] if S.get("eventi") else "-"))
    fr = os.path.join(Q._RADICE, "csv", "solitone", "_registro_corse.py")
    deve("lo script del registro esiste sotto la radice nuova", os.path.isfile(fr), fr)
    R = carica("_registro_corse", fr)
    deve("il REGISTRO (nel repo) esiste", os.path.isfile(R.REGISTRO[0]), R.REGISTRO[0])
    deve("le TAPPE (il percorso vecchio) esistono", os.path.isdir(R.TAPPE[0]), R.TAPPE[0])
    st = sorted(glob.glob(r"E:\soliton_simulator\controllo\M2034\coppia\d1\stato_*.npz"))
    deve("gli stati di d1' (il percorso vecchio): 25", len(st) == 25, "%d" % len(st))
    pend = [c["nome"] for c in L["corse"] if c["nome"] not in S["corse"]]
    deve("nessuna corsa da lanciare", not pend, "%s" % pend)
    print("### %d DEVE: %d PASSANO" % (len(OK), sum(OK)))
    print("=" * 110)
    return 0 if all(OK) else 1


if __name__ == "__main__":
    sys.exit(main())
