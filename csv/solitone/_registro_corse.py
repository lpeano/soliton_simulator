# -*- coding: utf-8 -*-
r"""**IL REGISTRO DELLE CORSE DELL'ERA 2** *(Luca `2026-11-13` `10:20`; il task history `doc/TASK_HISTORY/2026-11-13_registro_corse.md`)*.

### **Il file:** `doc/REGISTRO_CORSE.md`, **APPEND-ONLY**, **una riga per evento** `- {json}` *(`ev` in `APERTO`, `TAPPA`, `CHIUSO`)*.
### **Le regole:** **al piu' UNA `lunga` e UNA `breve` aperte insieme;** **mai lo stesso nome aperto due volte;** **`forza` solo col TESTO di una decisione di Luca, scritto nella voce;**
**dopo un riavvio una voce APERTA si chiude come `FERMATO (riavvio)` all'ultima tappa SOLO con `visto_da_luca`.** ### **Il controllo legge SOLO questo registro.**
### **NON tocca** `csv/_stato_run.py` **ne'** `doc/STATO_RUN.md` *(il registro dell'era 1)*.

    python csv/solitone/_registro_corse.py apri --nome N --tipo lunga|breve --comando "..." --note "..." [--forza "la decisione di Luca"]
    python csv/solitone/_registro_corse.py tappa --nome N --punto "tick 1000"
    python csv/solitone/_registro_corse.py chiudi --nome N --esito FINITO|FERMATO|FALLITO --punto "tick 1500"
    python csv/solitone/_registro_corse.py aperte

### ⚠ **Il registro e' un file TRACCIATO: niente `apri`, `tappa`, `chiudi` mentre gira la suite** *(la suite rimette i byte dei file tracciati che cambiano mentre gira)*.
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
REGISTRO = [os.path.join(RADICE, "doc", "REGISTRO_CORSE.md")]   # ### una lista: il collaudo la punta a un file temporaneo (su_file)
NUCLEO_MD = os.path.join(RADICE, "doc", "NUCLEO_CONGELATO.md")
TIPI = ("lunga", "breve")
ESITI = ("FINITO", "FERMATO", "FALLITO")
RIGA_NUCLEO = re.compile(r"^\| `(primo_ordine/[^`]+)` \| `([0-9a-f]{8})` \| `([0-9a-f]{8})` \|")
INTESTAZIONE = "\n".join([
    "# IL REGISTRO DELLE CORSE DELL'ERA 2",
    "",
    "> **APPEND-ONLY. Si scrive SOLO con `csv/solitone/_registro_corse.py`** *(`apri`, `tappa`, `chiudi`)*, **mai a mano.** Il task history: `doc/TASK_HISTORY/2026-11-13_registro_corse.md`; la skill: `.claude/skills/registro-corse/SKILL.md`.",
    ">",
    "> - **una riga per evento, `- {json}`:** `ev` = `APERTO` *(l'ora, `HEAD`, l'impronta dei file del nucleo di `doc/NUCLEO_CONGELATO.md`, il comando verbatim)*, `TAPPA` *(il punto raggiunto)*, `CHIUSO` *(`FINITO`, `FERMATO`, `FALLITO`, il punto esatto)*;",
    "> - **al piu' UNA `lunga` e UNA `breve` aperte insieme; mai lo stesso nome aperto due volte; `forza` solo con una decisione di Luca, scritta nella voce;**",
    "> - **dopo un riavvio una voce rimasta APERTA si chiude `FERMATO (riavvio)` all'ultima tappa SOLO dopo che Luca l'ha vista: fino ad allora blocca le corse del suo tipo.**",
    "",
    "## GLI EVENTI",
    "",
]) + "\n"


class Rifiuto(Exception):
    """### `apri`, `tappa`, `chiudi` rifiutati dalle regole."""


class su_file(object):
    """### **Punta il registro a un altro file** *(il collaudo: mai il registro vero)*; **rimette il percorso all'uscita.**"""

    def __init__(self, percorso):
        self.percorso, self.prima = percorso, None

    def __enter__(self):
        self.prima = REGISTRO[0]
        REGISTRO[0] = self.percorso
        return self.percorso

    def __exit__(self, *a):
        REGISTRO[0] = self.prima


def ora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha1_byte(percorso):
    with open(percorso, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def impronta_nucleo():
    """### **I file del nucleo DALLA TABELLA di `doc/NUCLEO_CONGELATO.md`** *(la colonna «il nucleo unificato»)*: **lo `sha1-BYTE` dal disco di ciascuno, e se coincidono tutti.**"""
    with io.open(NUCLEO_MD, encoding="utf-8") as f:
        righe = [RIGA_NUCLEO.match(r) for r in f]
    righe = [m for m in righe if m]
    assert righe, "nessun file del nucleo nella tabella di doc/NUCLEO_CONGELATO.md"
    files, diversi = {}, []
    for m in righe:
        p = os.path.join(RADICE, *m.group(1).split("/"))
        s = sha1_byte(p)[:8] if os.path.exists(p) else "MANCA"
        files[m.group(1)] = s
        if s != m.group(3):
            diversi.append(m.group(1))
    return {"file": len(files), "uguali_alla_tabella": not diversi, "diversi": diversi, "sha1_byte": files}


def git_head():
    def g(*a):
        return subprocess.check_output(["git"] + list(a), cwd=RADICE).decode("utf-8", "replace").strip()
    try:
        return {"head": g("rev-parse", "--short=8", "HEAD"), "ramo": g("rev-parse", "--abbrev-ref", "HEAD"),
                "file_modificati": len([r for r in g("status", "--porcelain", "--untracked-files=no").splitlines() if r.strip()])}
    except (subprocess.CalledProcessError, OSError) as x:
        return {"head": None, "errore": str(x)}


def eventi():
    """### **Gli eventi, dal SOLO registro** *(le righe `- {`)*."""
    p = REGISTRO[0]
    if not os.path.exists(p):
        return []
    out = []
    with io.open(p, encoding="utf-8") as f:
        for r in f:
            if r.startswith("- {"):
                out.append(json.loads(r[2:]))
    return out


def aperte():
    """### **Le voci APERTE:** `{nome: l'evento APERTO, con 'ultima_tappa'}`."""
    st = {}
    for e in eventi():
        if e["ev"] == "APERTO":
            st[e["nome"]] = dict(e, ultima_tappa=None)
        elif e["ev"] == "TAPPA" and e["nome"] in st:
            st[e["nome"]]["ultima_tappa"] = e["punto"]
        elif e["ev"] == "CHIUSO":
            st.pop(e["nome"], None)
    return st


class _lucchetto(object):
    """### **Un processo alla volta scrive:** `O_EXCL` nella cartella temporanea del sistema *(FUORI dal repo)*; **attesa al piu' `60` s, poi ALZA.**"""

    def __init__(self):
        chiave = hashlib.sha1(os.path.abspath(REGISTRO[0]).encode("utf-8")).hexdigest()[:12]
        self.p = os.path.join(tempfile.gettempdir(), "registro_corse_%s.lock" % chiave)
        self.fd = None

    def __enter__(self):
        t0 = time.time()
        while True:
            try:
                self.fd = os.open(self.p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() - t0 > 60.0:
                    raise Rifiuto("il lucchetto %s e' preso da piu' di 60 s: un altro processo scrive, o ne e' rimasto uno (va guardato, non tolto da soli)" % self.p)
                time.sleep(0.2)

    def __exit__(self, *a):
        os.close(self.fd)
        os.remove(self.p)


def _aggiungi(evento):
    """### **APPEND-ONLY e ATOMICO:** il nuovo contenuto = il vecchio + una riga *(controllato)*; **un temporaneo accanto e `os.replace`.**"""
    p = REGISTRO[0]
    vecchio = b""
    if os.path.exists(p):
        with open(p, "rb") as f:
            vecchio = f.read()
    else:
        vecchio = INTESTAZIONE.encode("utf-8")
    riga = ("- " + json.dumps(evento, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    assert b"\n" not in riga[:-1], "un evento su piu' righe"
    if vecchio and not vecchio.endswith(b"\n"):
        vecchio += b"\n"
    nuovo = vecchio + riga
    assert nuovo.startswith(vecchio), "il registro NON cresce solo in coda"
    fd, tmp = tempfile.mkstemp(prefix=".registro_", suffix=".tmp", dir=os.path.dirname(p))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(nuovo)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return evento


def apri(nome, tipo, comando, note, forza):
    """### **APERTO.** `forza`: `None`, o il TESTO della decisione di Luca *(non vuoto)*. ### **RIFIUTA:** lo stesso nome aperto; una `lunga` con una `lunga` aperta; una `breve` con una `breve`."""
    if tipo not in TIPI:
        raise Rifiuto("il tipo %r non e' fra %s" % (tipo, TIPI))
    if not nome or not comando:
        raise Rifiuto("il nome e il comando vanno dati")
    if forza is not None and not str(forza).strip():
        raise Rifiuto("forza senza il testo della decisione di Luca")
    with _lucchetto():
        ap = aperte()
        if nome in ap:
            raise Rifiuto("la voce %r e' gia' APERTA (dalle %s)" % (nome, ap[nome]["ora"]))
        stesso = [n for n, e in ap.items() if e["tipo"] == tipo]
        if stesso and forza is None:
            raise Rifiuto("c'e' gia' una corsa %s aperta: %s (al piu' una lunga e una breve insieme)" % (tipo, stesso))
        ev = {"ev": "APERTO", "nome": nome, "tipo": tipo, "ora": ora(), "git": git_head(), "nucleo": impronta_nucleo(), "comando": comando, "note": note}
        if forza is not None:
            ev["forza"] = {"decisione_di_luca": forza, "aperte_allora": sorted(stesso)}
        return _aggiungi(ev)


def tappa(nome, punto):
    with _lucchetto():
        if nome not in aperte():
            raise Rifiuto("la voce %r non e' APERTA" % nome)
        return _aggiungi({"ev": "TAPPA", "nome": nome, "ora": ora(), "punto": punto})


def chiudi(nome, esito, punto):
    if esito not in ESITI:
        raise Rifiuto("l'esito %r non e' fra %s" % (esito, ESITI))
    with _lucchetto():
        if nome not in aperte():
            raise Rifiuto("la voce %r non e' APERTA" % nome)
        return _aggiungi({"ev": "CHIUSO", "nome": nome, "ora": ora(), "esito": esito, "punto": punto})


def chiudi_dopo_riavvio(nome, visto_da_luca):
    """### **`FERMATO (riavvio)` all'ULTIMA tappa, SOLO con `visto_da_luca`** *(il testo: quando e come Luca l'ha vista)*."""
    if not visto_da_luca or not str(visto_da_luca).strip():
        raise Rifiuto("una voce rimasta aperta dopo un riavvio si chiude SOLO dopo che Luca l'ha vista: manca visto_da_luca")
    with _lucchetto():
        ap = aperte()
        if nome not in ap:
            raise Rifiuto("la voce %r non e' APERTA" % nome)
        return _aggiungi({"ev": "CHIUSO", "nome": nome, "ora": ora(), "esito": "FERMATO", "motivo": "riavvio", "visto_da_luca": visto_da_luca,
                          "punto": ap[nome]["ultima_tappa"] or "nessuna tappa (dall'apertura)"})


def main(argv):
    ap = argparse.ArgumentParser(description="il registro delle corse dell'era 2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("apri")
    a.add_argument("--nome", required=True)
    a.add_argument("--tipo", required=True, choices=TIPI)
    a.add_argument("--comando", required=True)
    a.add_argument("--note", required=True)
    a.add_argument("--forza")
    t = sub.add_parser("tappa")
    t.add_argument("--nome", required=True)
    t.add_argument("--punto", required=True)
    c = sub.add_parser("chiudi")
    c.add_argument("--nome", required=True)
    c.add_argument("--esito", required=True, choices=ESITI)
    c.add_argument("--punto", required=True)
    r = sub.add_parser("riavvio")
    r.add_argument("--nome", required=True)
    r.add_argument("--visto-da-luca", required=True)
    sub.add_parser("aperte")
    x = ap.parse_args(argv)
    try:
        if x.cmd == "apri":
            ev = apri(x.nome, x.tipo, x.comando, x.note, x.forza)
        elif x.cmd == "tappa":
            ev = tappa(x.nome, x.punto)
        elif x.cmd == "chiudi":
            ev = chiudi(x.nome, x.esito, x.punto)
        elif x.cmd == "riavvio":
            ev = chiudi_dopo_riavvio(x.nome, x.visto_da_luca)
        else:
            ap_ = aperte()
            print("%d voci APERTE nel registro %s" % (len(ap_), REGISTRO[0]))
            for n, e in sorted(ap_.items()):
                print("  %s  %s  dalle %s  HEAD %s  l'ultima tappa: %s  il comando: %s" % (n, e["tipo"], e["ora"], e["git"].get("head"), e["ultima_tappa"], e["comando"]))
            return 0
    except Rifiuto as z:
        print("RIFIUTATO: %s" % z)
        return 2
    print("%s %s alle %s" % (ev["ev"], ev["nome"], ev["ora"]))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
