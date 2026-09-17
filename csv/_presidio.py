# -*- coding: utf-8 -*-
"""PRESIDIO COMUNE agli script di misura e di sigillo. **Due presidi, UNA riga da ricordare.**

PERCHE' ESISTE, e la ragione e' un fallimento di REGOLA, non di codice:
  `CLAUDE.md par.5-quinquies` dice, dal 2026-09-16, che il codice di una misura dev'essere
  recuperabile PER COSTRUZIONE. Il 2026-09-17 `_esperimento_spin_feedback.py` ha prodotto un run
  intero **senza essere tracciato da git**, e nulla lo ha segnalato.
  **Una regola scritta che non impedisce il ripetersi di un difetto non e' un presidio: e' una
  testimonianza.** Questo modulo e' il tentativo di sostituirla con un MECCANISMO.

  Lo stesso vale per l'encoding: `# -*- coding: utf-8 -*-` riguarda il SORGENTE, non lo STDOUT, e
  lo stdout di Windows e' cp1252. E' morto uno script SETTE volte, la settima proprio quello che
  stava contando le occorrenze precedenti.

  I due presidi sono messi INSIEME di proposito: quello dell'encoding e' gia' in 74 script su 74,
  cioe' e' gia' una riga che nessuno dimentica. Agganciare il timbro git alla STESSA riga lo fa
  arrivare dove l'altro e' gia' arrivato, invece di chiedere di ricordarsene una seconda volta.

COSA FA
  `avvia(__file__)`  -> (1) forza stdout/stderr a utf-8;
                        (2) calcola lo sha1 dei BYTE GREZZI dello script (mai `git hash-object`:
                            applica il filtro CRLF e nasconde la differenza -- par.5-quinquies);
                        (3) chiede a git se il file e' TRACCIATO e se differisce da HEAD;
                        (4) STAMPA il timbro in testa all'output;
                        (5) mette il timbro in `SOLITON_DRIVER` nell'ambiente, cosi' un eventuale
                            sottoprocesso puo' scriverlo nei propri dati;
                        (6) se lo script e' un SIGILLO (`_sigillo_*.py`) e non e' pulito, ESCE.

  La distinzione del punto (6) e' voluta e non e' timidezza:
    - un DIAGNOSTICO che gira da codice non committato produce un numero **da dichiarare**, ed e'
      spesso esattamente cio' che si sta facendo mentre lo si scrive: rifiutarsi di girare
      renderebbe impossibile il lavoro esplorativo, e il divieto verrebbe aggirato;
    - un SIGILLO che gira da codice non committato produce un timbro **privo di valore per
      definizione** (par.2.6: il gate certifica un BLOB). Li' non c'e' uso legittimo, e rifiutare
      non costa nulla.

COSA NON FA, e va detto:
  **non impedisce** di girare uno script non tracciato: lo fa DICHIARARE. La differenza rispetto
  a una nota in CLAUDE.md e' che la dichiarazione finisce **nell'output**, cioe' dentro il referto
  che qualcuno leggera' fra sei mesi, invece che nella memoria di chi ha lanciato il comando.
ASCII PURO.
"""
import hashlib
import os
import subprocess
import sys

__all__ = ["avvia", "timbro"]


def _git(args, cwd):
    try:
        p = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)
        return (p.returncode, (p.stdout or "").strip())
    except Exception as e:
        return (-1, "git non eseguibile: %s" % e)


def timbro(percorso):
    """Stato git dello script, misurato sui BYTE GREZZI. Non solleva mai."""
    p = os.path.abspath(percorso)
    d = os.path.dirname(p)
    out = {"path": p, "sha1": None, "tracciato": None, "blob_head": None,
           "dirty": None, "repo": None}
    try:
        out["sha1"] = hashlib.sha1(open(p, "rb").read()).hexdigest()
    except Exception:
        return out
    rc, radice = _git(["rev-parse", "--show-toplevel"], d)
    if rc != 0:
        return out
    out["repo"] = radice
    rel = os.path.relpath(p, radice).replace(os.sep, "/")
    rc, _ = _git(["ls-files", "--error-unmatch", rel], radice)
    out["tracciato"] = (rc == 0)
    if not out["tracciato"]:
        out["dirty"] = True          # non tracciato: per definizione non recuperabile da HEAD
        return out
    rc, blob = _git(["rev-parse", "HEAD:%s" % rel], radice)
    if rc == 0:
        out["blob_head"] = blob
        # confronto sui BYTE: si estrae il blob di HEAD e si ri-calcola lo sha1 grezzo, invece di
        # chiedere a `git diff` -- che applica il filtro CRLF e puo' dire "nessuna differenza" su
        # due file con byte diversi (la trappola misurata il 2026-09-16, par.5-quinquies).
        try:
            q = subprocess.run(["git", "cat-file", "-p", "HEAD:%s" % rel],
                               cwd=radice, capture_output=True)
            out["dirty"] = (hashlib.sha1(q.stdout).hexdigest() != out["sha1"]) if q.returncode == 0 else None
        except Exception:
            out["dirty"] = None
    return out


def avvia(percorso, silenzioso=False):
    """Il punto d'ingresso. UNA riga in testa a ogni script: `_presidio.avvia(__file__)`."""
    for flusso in (sys.stdout, sys.stderr):
        try:
            flusso.reconfigure(encoding="utf-8")
        except Exception:
            pass
    t = timbro(percorso)
    nome = os.path.basename(t["path"])
    if t["repo"] is None:
        stato = "FUORI DA UN REPO GIT"
    elif not t["tracciato"]:
        stato = "!! NON TRACCIATO -- questo output NON e' riproducibile dal repo (par.5-quinquies)"
    elif t["dirty"]:
        # NB: `blob_head` e' l'hash GIT (filtro CRLF applicato), `sha1` e' quello dei BYTE.
        # Sono due spazi di hash diversi: stamparli accanto senza dirlo sarebbe la trappola
        # CRLF travestita da riga di log.
        stato = "!! MODIFICATO rispetto a HEAD (blob-git %s) -- i byte che girano NON sono quelli committati" % (
            (t["blob_head"] or "?")[:8])
    elif t["dirty"] is None:
        stato = "tracciato, confronto con HEAD NON RIUSCITO"
    else:
        stato = "committato e pulito"
    if not silenzioso:
        print("[TIMBRO] %s  sha1-BYTE %s  %s" % (nome, (t["sha1"] or "?")[:8], stato), flush=True)
    os.environ["SOLITON_DRIVER"] = "%s:%s:%s" % (
        nome, (t["sha1"] or "?")[:8], "dirty" if t["dirty"] else "clean")
    if nome.startswith("_sigillo_") and (t["repo"] is not None) and (not t["tracciato"] or t["dirty"]):
        print("[TIMBRO] RIFIUTO DI GIRARE: un SIGILLO certifica un BLOB (par.2.6), e questo blob\n"
              "         non e' nel repo. Committa lo script, poi rilancia. Per un diagnostico\n"
              "         questo controllo NON blocca: dichiara e prosegue.", flush=True)
        sys.exit(2)
    return t
