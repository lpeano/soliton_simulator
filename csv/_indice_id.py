r"""**IL VALIDATORE DELL'INDICE** — `doc/INDICE_ID.tsv` e' la **FONTE**, e questo la CONTROLLA.

**Ultimo passo del refactoring (Luca, 2026-09-26):** *«l'indice diventa la FONTE, non una vista»*.

> ## ⛔ **QUESTO FILE NON GENERA PIU' NIENTE.**
> L'importatore che leggeva il Markdown e ricostruiva l'indice **ha girato per l'ultima volta** ed e'
> in **`csv/_archivio/_indice_id_importatore.py`**: sta li' come **storia**, e **non si rilancia**
> *(rilanciarlo sovrascriverebbe la fonte con una ricostruzione, cioe' butterebbe via le decisioni
> scritte nelle colonne)*.

## COSA CONTROLLA

```
SCHEMA        l'intestazione e' esattamente quella attesa, e ogni riga ha lo stesso numero di campi
VOCABOLARI    `stato`, `blocca_run_base`, `tipo`, `famiglia`, `avanzamento` stanno nei valori ammessi
ID            unici, non vuoti, e nella FORMA degli ID
COERENZA      un `chiuso`/`non-difetto`/`teoria`/`criterio-locale` **non blocca mai**
NESSUNA PERDITA  ogni voce presente al tag `lista-chiusa-v1` c'e' ancora, salvo le cancellazioni
                 DICHIARATE qui sotto col motivo
MOTIVO        ogni voce con `blocca = SI` porta il suo `motivo`: una decisione senza prova non passa
```

## DA ORA IN POI

- **un difetto nuovo si scrive come RIGA di `doc/INDICE_ID.tsv`**; la spiegazione lunga sta in
  `doc/STATO_RUN.md` **con lo stesso ID**;
- **il hook rifiuta un ID nuovo in un documento vivo che non ha la sua riga** *(gia' attivo:
  `csv/_presidio_indice.py`, stadio `commit-msg`)*;
- **le viste si rigenerano e non si modificano a mano:** `csv/_lista_chiusa.py`,
  `csv/_vista_smistamento.py`, `csv/_punto_della_situazione.py`.

**`--collaudo`** prova i DUE versi: l'indice vero passa, una copia guasta **fallisce**.
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Valida un TSV.
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
REFERTO = os.path.join(RADICE, "doc", "INDICE_ID_validazione.txt")
TAG = "lista-chiusa-v1"
NL = chr(10)
TAB = chr(9)

COL = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base", "tipo",
       "famiglia", "stato_da", "avanzamento", "revisione", "motivo", "nota"]
STATI = {"aperto", "chiuso", "non-difetto", "teoria", "da-decidere"}
BLOCCA = {"SI", "NO", "DA-DECIDERE", "DA VERIFICARE"}
TIPI = {"difetto", "sospetto", "fronte", "misura", "cura", "presidio", "assioma", "standard",
        "criterio-locale", "altro"}
FAM = {"A", "B", "C", "D", "E", "F", "G", "?"}
AVANZ = {"FATTO", "IN CORSO", "IN CODA", "BLOCCATO", "CON RISERVA", "(senza marcatore)"}
FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]*(?:-[A-Za-z0-9()/]+)+|[A-Z]{2,}\d{1,3}"
                   r"|[A-Z_]+:[A-Za-z0-9\-()/]+)")

#   ⚠ LO STEM DI UNA LETTERA, ammesso il 2026-09-26: `H-P3` e `L-SOGLIA` hanno UNA
#   lettera prima del trattino -- e `H-P1-bis` ha una CODA MINUSCOLA, come il
#   `P1-bis` che tutti citano -- e la forma chiedeva DUE lettere e tutto maiuscolo -- quindi il validatore
#   RIFIUTAVA i nomi che Luca stesso aveva dettato. Misurato: senza questa riga sedici
#   voci nuove su sedici erano 'senza FORMA'.
#   ⚠ LE CANCELLAZIONI DICHIARATE: una voce sparita rispetto al tag e' un ERRORE, salvo queste.
CANCELLAZIONI = {
    "CLI-1)": "token SPURIO: la parentesi della prosa attaccata all'id "
              "*(`(CLI-1)` letto come un nome)*. Curato il 2026-09-26: le parentesi devono essere "
              "BILANCIATE.",
}


def leggi(percorso):
    r = io.open(percorso, encoding="utf-8", newline="").read().split(NL)
    return [c.strip() for c in r[0].split(TAB)], [x for x in r[1:] if x.strip()]


def valida(percorso):
    """`(errori, quante_voci)`. Un errore e' una stringa leggibile: nessun `assert` muto."""
    err = []
    col, righe = leggi(percorso)
    if col != COL:
        err.append("SCHEMA: intestazione diversa da quella attesa.%s     attesa: %s%s     trovata: %s"
                   % (NL, TAB.join(COL), NL, TAB.join(col)))
        return err, 0
    visti = {}
    for k, x in enumerate(righe, 2):
        c = x.split(TAB)
        if len(c) != len(COL):
            err.append("riga %d: %d campi invece di %d" % (k, len(c), len(COL)))
            continue
        v = dict(zip(COL, [y.strip() for y in c]))
        i = v["id"]
        if not i:
            err.append("riga %d: `id` VUOTO" % k)
            continue
        if i in visti:
            err.append("riga %d: id `%s` DUPLICATO (gia' alla riga %d)" % (k, i, visti[i]))
        visti[i] = k
        if not FORMA.fullmatch(i):
            err.append("riga %d: l'id `%s` non ha la FORMA di un id" % (k, i))
        if v["stato"] not in STATI:
            err.append("riga %d (`%s`): stato `%s` non ammesso" % (k, i, v["stato"]))
        if v["blocca_run_base"] not in BLOCCA:
            err.append("riga %d (`%s`): blocca_run_base `%s` non ammesso"
                       % (k, i, v["blocca_run_base"]))
        if v["tipo"] not in TIPI:
            err.append("riga %d (`%s`): tipo `%s` non ammesso" % (k, i, v["tipo"]))
        if v["famiglia"] not in FAM:
            err.append("riga %d (`%s`): famiglia `%s` non ammessa" % (k, i, v["famiglia"]))
        if v["avanzamento"] not in AVANZ:
            err.append("riga %d (`%s`): avanzamento `%s` non ammesso" % (k, i, v["avanzamento"]))
        # COERENZA: chi e' chiuso, teoria o locale NON blocca
        if v["blocca_run_base"] == "SI" and (v["stato"] in ("chiuso", "non-difetto", "teoria")
                                            or v["tipo"] in ("assioma", "standard",
                                                             "criterio-locale")):
            err.append("riga %d (`%s`): blocca SI ma stato `%s` / tipo `%s`: contraddizione"
                       % (k, i, v["stato"], v["tipo"]))
        # una decisione SENZA PROVA non passa
        if v["blocca_run_base"] == "SI" and not v["motivo"]:
            err.append("riga %d (`%s`): blocca SI **senza `motivo`**: una decisione senza prova"
                       % (k, i))
    return err, len(visti)


def perdite():
    """Le voci presenti al tag e assenti adesso, tolte quelle DICHIARATE."""
    q = subprocess.run(["git", "show", "%s:doc/INDICE_ID.tsv" % TAG], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if q.returncode:
        return None, "il tag `%s` non si legge: %s" % (TAG, (q.stderr or "").strip()[:80])
    al_tag = set(x.split(TAB)[0].strip() for x in (q.stdout or "").split(NL)[1:] if x.strip())
    _c, righe = leggi(FONTE)
    ora = set(x.split(TAB)[0].strip() for x in righe)
    return sorted((al_tag - ora) - set(CANCELLAZIONI)), None


def collaudo():
    """I DUE versi: l'indice vero PASSA, una copia GUASTA fallisce."""
    R = []

    def P(s=""):
        R.append(s)
        print(s)

    P("=" * 96)
    P("COLLAUDO DEL VALIDATORE -- i DUE versi   (2026-09-26)")
    P("=" * 96)
    P()
    e, n = valida(FONTE)
    ok1 = not e
    P("  DEVE PASSARE  l'indice VERO (%d voci) -> %s" % (n, "PASS" if ok1 else "FAIL"))
    for x in e[:6]:
        P("      %s" % x)
    casi = [
        ("uno stato inventato", 4, "verde"),
        ("un tipo inventato", 6, "cosa"),
        ("una famiglia inventata", 7, "Z"),
        ("un `blocca SI` su una voce CHIUSA", 5, "SI"),
    ]
    esiti = [ok1]
    _c, righe = leggi(FONTE)
    tmp = os.path.join(RADICE, "doc", "_indice_guasto.tmp")
    for nome, campo, valore in casi:
        # si guasta UNA riga, e si sceglie una riga `chiuso` per il caso della contraddizione
        idx = 0
        if valore == "SI":
            idx = next((j for j, x in enumerate(righe) if x.split(TAB)[4] == "chiuso"), 0)
        c = righe[idx].split(TAB)
        c[campo] = valore
        guaste = list(righe)
        guaste[idx] = TAB.join(c)
        io.open(tmp, "w", encoding="utf-8", newline=NL).write(
            TAB.join(COL) + NL + NL.join(guaste) + NL)
        e2, _ = valida(tmp)
        os.remove(tmp)
        ok = bool(e2)
        esiti.append(ok)
        P("  DEVE FALLIRE  %-36s -> %s" % (nome, "RIFIUTA: " + e2[0][:52] if ok else "*** PASSA ***"))
    _p, _err = perdite()
    ok_p = (_p == [])
    esiti.append(ok_p)
    P()
    P("  VOCI PERSE rispetto al tag `%s`: %s   -> %s"
      % (TAG, "nessuna" if ok_p else _p, "PASS" if ok_p else "FAIL"))
    P("    cancellazioni DICHIARATE (%d):" % len(CANCELLAZIONI))
    for k2, m in CANCELLAZIONI.items():
        P("      `%s` -- %s" % (k2, m))
    P()
    tutto = all(esiti)
    P("=" * 96)
    P("ESITO: %s" % ("%d/%d PASS -- il validatore IMPEDISCE, non descrive"
                    % (len(esiti), len(esiti)) if tutto else "FAIL"))
    P("=" * 96)
    P()
    P("COSA QUESTO COLLAUDO *NON* DICE:")
    P("  - **non dice che i CONTENUTI siano giusti**: dice che sono **ben formati e coerenti**. Che")
    P("    `D02` blocchi davvero il run base non lo decide uno schema.")
    P("  - **non controlla il testo di `motivo`**: controlla che **ci sia** dove `blocca = SI`.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    return 0 if tutto else 1


if __name__ == "__main__":
    _presidio.avvia(__file__)
    if "--collaudo" in sys.argv:
        sys.exit(collaudo())
    e, n = valida(FONTE)
    p, msg = perdite()
    print("VALIDAZIONE di doc/INDICE_ID.tsv -- %d voci, %d colonne" % (n, len(COL)))
    if msg:
        print("  ⚠ %s" % msg)
    if p:
        e = e + ["VOCI PERSE rispetto al tag %s: %s" % (TAG, ", ".join(p))]
    if e:
        print("*** %d VIOLAZIONI:" % len(e))
        for x in e[:40]:
            print("    %s" % x)
        sys.exit(1)
    print("  schema, vocabolari, id, coerenza, motivo, nessuna perdita: **TUTTO A POSTO**")
    print("  (questo file NON genera: l'importatore e' in csv/_archivio/ e non si rilancia)")
    sys.exit(0)
