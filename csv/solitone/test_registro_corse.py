# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DEL REGISTRO DELLE CORSE DELL'ERA 2** *(Luca `2026-11-13` `10:20`, punto `5`; la decisione (b) delle `12:58`; il task history `doc/TASK_HISTORY/2026-11-13_registro_corse.md`, sez. `2`, `6`)*.

    python csv/solitone/test_registro_corse.py > doc/referti_l2/registro_corse_collaudo.txt

### **Su un registro e una cartella delle tappe TEMPORANEI** *(`_registro_corse.su_file`)*: **il registro vero e la cartella vera delle tappe non si toccano.**
**DEVE PASSARE:** la prova a secco *(una `lunga` finta di `10` tick: `APERTO`, una tappa a `5`, `FINITO` a `10`)*; **una tappa NON cambia il registro e scrive nel file esterno;** **la chiusura copia
le tappe nel registro, nell'ordine, e sposta il file;** **una `breve` con una `lunga` aperta: ACCETTATA;** il registro cresce solo in coda.
**DEVE FALLIRE** *(`apri` deve RIFIUTARE)*: **una seconda `lunga` con una `lunga` aperta; lo stesso nome aperto due volte.** **Controlli:** `forza` senza testo; il riavvio senza `visto_da_luca`;
**un file di tappe rimasto con quel nome.**
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


def contenuto(p):
    with open(p, "rb") as f:
        return f.read()


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "_registro_corse.py"))
    _presidio.avvia(__file__)
    vero = RC.REGISTRO[0]
    sha_vero = RC.sha1_byte(vero)
    tappe_vere = sorted(os.listdir(RC.TAPPE[0])) if os.path.isdir(RC.TAPPE[0]) else None
    print("=" * 120)
    print("IL COLLAUDO DEL REGISTRO DELLE CORSE DELL'ERA 2 (la decisione (b): le tappe fuori dal repo): su un registro e una cartella temporanei; il registro vero %s sha1-BYTE %s; le tappe vere in %s"
          % (os.path.relpath(vero, RC.RADICE), sha_vero[:8], RC.TAPPE[0]))
    print("=" * 120)
    cartella = tempfile.mkdtemp(prefix="collaudo_registro_")
    try:
        with RC.su_file(os.path.join(cartella, "REGISTRO_CORSE.md"), os.path.join(cartella, "registro_tappe")) as p:
            storia = [b""]

            def cresce():
                b = contenuto(p)
                buono = b.startswith(storia[-1]) and len(b) > len(storia[-1])
                storia.append(b)
                return buono
            code = []
            # ---------------------------------------------------------------- la prova a secco
            ok1, ev = tenta(RC.apri, "secco-lunga", "lunga", "python finto.py --tick 10", "la prova a secco del collaudo", None)
            code.append(cresce())
            print("  APERTO: %s" % (ev if not ok1 else {k: ev[k] for k in ("nome", "tipo", "ora", "comando")}))
            if ok1:
                print("    HEAD %s, file modificati %s; il nucleo: %d file, uguali alla tabella: %s; le tappe in %s" % (ev["git"].get("head"), ev["git"].get("file_modificati"), ev["nucleo"]["file"],
                                                                                                               ev["nucleo"]["uguali_alla_tabella"], os.path.relpath(ev["tappe_in"], cartella)))
            ok_t, ferma = True, True
            for k in range(1, 11):     # ### i 10 tick finti
                if k == 5:
                    prima = contenuto(p)
                    ok, _ = tenta(RC.tappa, "secco-lunga", "tick %d" % k)
                    ok_t = ok_t and ok
                    ferma = ferma and contenuto(p) == prima
            tt = RC.tappe_di("secco-lunga")
            esito("una tappa NON cambia il registro e scrive nel file esterno", ok_t and ferma and [x["punto"] for x in tt] == ["tick 5"],
                  "il registro uguale: %s; le tappe esterne %s" % (ferma, [x["punto"] for x in tt]), True)
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
            tap = [e for e in evs if e["nome"] == "secco-lunga" and e["ev"] == "TAPPA"]
            fine = [e for e in evs if e["nome"] == "secco-lunga" and e["ev"] == "CHIUSO"]
            ct = os.path.join(cartella, "registro_tappe")
            spostati = sorted(f for f in os.listdir(ct) if f.startswith("secco-lunga.chiuso."))
            print("  gli eventi della lunga finta: %s; la tappa copiata: %s; la chiusura: %s; il file delle tappe dopo: %s" % (
                seq, [(e["punto"], e.get("copiata_alla_chiusura")) for e in tap], fine[0]["esito"] + " a " + fine[0]["punto"] if fine else None, spostati))
            print("  gli eventi dopo i rifiuti %d (i rifiuti e le tappe non scrivono nel registro: 2 attesi = APERTO della lunga, APERTO della breve)" % n_dopo_rifiuti)
            esito("la prova a secco: APERTO, la tappa COPIATA alla chiusura, FINITO a tick 10; il file delle tappe spostato; nessuna voce aperta",
                  ok1 and ok_c and ok_cb and seq == atteso and tap and tap[0]["punto"] == "tick 5" and tap[0].get("copiata_alla_chiusura") is True and fine[0]["esito"] == "FINITO"
                  and fine[0]["punto"] == "tick 10" and not RC.aperte() and not os.path.exists(os.path.join(ct, "secco-lunga.txt")) and len(spostati) == 1, "%s" % (seq,), True)
            esito("i rifiuti e le tappe non scrivono niente nel registro", n_dopo_rifiuti == 2, "%d eventi" % n_dopo_rifiuti, True)
            esito("il registro cresce solo in coda (ogni contenuto comincia col precedente)", all(code), "%d scritture" % len(code), True)
            # ---------------------------------------------------------------- un file di tappe rimasto
            with open(os.path.join(ct, "secco-rimasto.txt"), "w", encoding="utf-8") as f:
                f.write('{"ora": "finta", "punto": "tick 1"}\n')
            ok_rim, m_rim = tenta(RC.apri, "secco-rimasto", "lunga", "python rimasto.py", "un file di tappe rimasto", None)
            esito("controllo: apri rifiuta se il file delle tappe di quel nome c'e' gia'", not ok_rim, m_rim if not ok_rim else "accettato", True)
            os.remove(os.path.join(ct, "secco-rimasto.txt"))
            # ---------------------------------------------------------------- il riavvio con visto_da_luca
            tenta(RC.apri, "secco-riavvio", "lunga", "python lunga.py", "una voce rimasta aperta", None)
            tenta(RC.tappa, "secco-riavvio", "tick 500")
            tenta(RC.tappa, "secco-riavvio", "tick 750")
            ult = RC.aperte().get("secco-riavvio", {}).get("ultima_tappa")
            ok_rv, ev_rv = tenta(RC.chiudi_dopo_riavvio, "secco-riavvio", "vista da Luca nel collaudo (finta)")
            tap_rv = [e["punto"] for e in RC.eventi() if e["nome"] == "secco-riavvio" and e["ev"] == "TAPPA"]
            esito("controllo: il riavvio con visto_da_luca copia le tappe e chiude FERMATO all'ultima",
                  ok_rv and ult == "tick 750" and ev_rv["esito"] == "FERMATO" and ev_rv["punto"] == "tick 750" and tap_rv == ["tick 500", "tick 750"] and not RC.aperte(),
                  "l'ultima tappa letta %s; le copiate %s; %s a %s" % (ult, tap_rv, ev_rv.get("esito"), ev_rv.get("punto")) if ok_rv else ev_rv, True)
    finally:
        shutil.rmtree(cartella, ignore_errors=True)
    dopo = sorted(os.listdir(RC.TAPPE[0])) if os.path.isdir(RC.TAPPE[0]) else None
    esito("il registro vero e la cartella vera delle tappe NON toccati", RC.sha1_byte(vero) == sha_vero and dopo == tappe_vere, "%s; le tappe vere %s" % (sha_vero[:8], dopo), True)
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
