# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DEL REGISTRO DELLE CORSE DELL'ERA 2** *(Luca `2026-11-13` `10:20`, punto `5`; il task history `doc/TASK_HISTORY/2026-11-13_registro_corse.md`, sez. `2`)*.

    python csv/solitone/test_registro_corse.py > doc/referti_l2/registro_corse_collaudo.txt

### **Su un registro TEMPORANEO** *(`_registro_corse.su_file`)*: **il registro vero `doc/REGISTRO_CORSE.md` non si tocca** *(lo `sha1-BYTE` prima e dopo)*.
**DEVE PASSARE:** la prova a secco *(una `lunga` finta di `10` tick: `APERTO`, una tappa a `5`, `FINITO` a `10`)*; **una `breve` con una `lunga` aperta: ACCETTATA;** il file cresce solo in coda.
**DEVE FALLIRE** *(`apri` deve RIFIUTARE)*: **una seconda `lunga` con una `lunga` aperta; lo stesso nome aperto due volte.** **Controlli:** `forza` senza testo; il riavvio senza `visto_da_luca`.
"""
import os
import shutil
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _registro_corse as RC  # noqa: E402

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-96s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:96], "PASSA" if passa else "### FALLISCE", nota))


def tenta(f, *a):
    """### `(True, l'evento)` se accettato; `(False, il motivo)` se `Rifiuto`."""
    try:
        return True, f(*a)
    except RC.Rifiuto as z:
        return False, str(z)


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "_registro_corse.py"))
    _presidio.avvia(__file__)
    vero = RC.REGISTRO[0]
    sha_vero = RC.sha1_byte(vero)
    print("=" * 120)
    print("IL COLLAUDO DEL REGISTRO DELLE CORSE DELL'ERA 2: su un registro temporaneo; il registro vero %s sha1-BYTE %s" % (os.path.relpath(vero, RC.RADICE), sha_vero[:8]))
    print("=" * 120)
    cartella = tempfile.mkdtemp(prefix="collaudo_registro_")
    try:
        with RC.su_file(os.path.join(cartella, "REGISTRO_CORSE.md")) as p:
            storia = [b""]

            def cresce():
                with open(p, "rb") as f:
                    b = f.read()
                buono = b.startswith(storia[-1]) and len(b) > len(storia[-1])
                storia.append(b)
                return buono
            code = []
            # ---------------------------------------------------------------- la prova a secco
            ok1, ev = tenta(RC.apri, "secco-lunga", "lunga", "python finto.py --tick 10", "la prova a secco del collaudo", None)
            code.append(cresce())
            print("  APERTO: %s" % (ev if not ok1 else {k: ev[k] for k in ("nome", "tipo", "ora", "comando")}))
            if ok1:
                print("    HEAD %s, file modificati %s; il nucleo: %d file, uguali alla tabella: %s" % (ev["git"].get("head"), ev["git"].get("file_modificati"), ev["nucleo"]["file"], ev["nucleo"]["uguali_alla_tabella"]))
            ok_t = True
            for k in range(1, 11):     # ### i 10 tick finti
                if k == 5:
                    ok, _ = tenta(RC.tappa, "secco-lunga", "tick %d" % k)
                    ok_t = ok_t and ok
                    code.append(cresce())
            # ---------------------------------------------------------------- una breve accanto alla lunga
            ok_b, ev_b = tenta(RC.apri, "secco-breve", "breve", "python breve.py", "una breve accanto alla lunga", None)
            code.append(cresce() if ok_b else True)
            esito("una breve aperta mentre una lunga e' aperta: ACCETTATA", ok_b, "" if ok_b else ev_b, True)
            # ---------------------------------------------------------------- i rifiuti
            ok_l2, m_l2 = tenta(RC.apri, "secco-lunga-2", "lunga", "python altra.py", "una seconda lunga", None)
            esito("apri: una seconda lunga con una lunga aperta e' accettata", ok_l2, m_l2 if not ok_l2 else "", False)
            ok_n2, m_n2 = tenta(RC.apri, "secco-lunga", "breve", "python stesso_nome.py", "lo stesso nome", None)
            esito("apri: lo stesso nome aperto due volte e' accettato", ok_n2, m_n2 if not ok_n2 else "", False)
            ok_f, m_f = tenta(RC.apri, "secco-forza", "lunga", "python forza.py", "forza vuota", "  ")
            esito("controllo: forza senza il testo della decisione rifiuta", not ok_f, m_f if not ok_f else "accettata", True)
            ok_r, m_r = tenta(RC.chiudi_dopo_riavvio, "secco-breve", "")
            esito("controllo: il riavvio senza visto_da_luca rifiuta", not ok_r, m_r if not ok_r else "accettato", True)
            n_dopo_rifiuti = len(RC.eventi())
            # ---------------------------------------------------------------- la chiusura
            ok_c, _ = tenta(RC.chiudi, "secco-lunga", "FINITO", "tick 10")
            code.append(cresce())
            ok_cb, _ = tenta(RC.chiudi, "secco-breve", "FINITO", "fine")
            code.append(cresce())
            evs = RC.eventi()
            seq = [(e["ev"], e["nome"]) for e in evs if e["nome"] == "secco-lunga"]
            atteso = [("APERTO", "secco-lunga"), ("TAPPA", "secco-lunga"), ("CHIUSO", "secco-lunga")]
            fine = [e for e in evs if e["nome"] == "secco-lunga" and e["ev"] == "CHIUSO"]
            print("  gli eventi della lunga finta: %s; la chiusura: %s" % (seq, fine[0]["esito"] + " a " + fine[0]["punto"] if fine else None))
            print("  gli eventi dopo i rifiuti %d (i rifiuti non scrivono: 3 attesi = APERTO, TAPPA, APERTO della breve)" % n_dopo_rifiuti)
            esito("la prova a secco: una lunga finta di 10 tick, APERTO, una tappa, FINITO a tick 10, e poi nessuna voce aperta",
                  ok1 and ok_t and ok_c and ok_cb and seq == atteso and fine[0]["esito"] == "FINITO" and fine[0]["punto"] == "tick 10" and not RC.aperte(), "%s" % (seq,), True)
            esito("i rifiuti non scrivono niente nel registro", n_dopo_rifiuti == 3, "%d eventi" % n_dopo_rifiuti, True)
            esito("il registro cresce solo in coda (ogni contenuto comincia col precedente)", all(code), "%d scritture" % len(code), True)
            # ---------------------------------------------------------------- il riavvio con visto_da_luca
            tenta(RC.apri, "secco-riavvio", "lunga", "python lunga.py", "una voce rimasta aperta", None)
            tenta(RC.tappa, "secco-riavvio", "tick 750")
            ok_rv, ev_rv = tenta(RC.chiudi_dopo_riavvio, "secco-riavvio", "vista da Luca nel collaudo (finta)")
            esito("controllo: il riavvio con visto_da_luca chiude FERMATO all'ultima tappa", ok_rv and ev_rv["esito"] == "FERMATO" and ev_rv["punto"] == "tick 750" and not RC.aperte(),
                  "%s a %s" % (ev_rv.get("esito"), ev_rv.get("punto")) if ok_rv else ev_rv, True)
    finally:
        shutil.rmtree(cartella, ignore_errors=True)
    esito("il registro vero NON toccato (lo sha1-BYTE prima e dopo)", RC.sha1_byte(vero) == sha_vero, sha_vero[:8], True)
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
