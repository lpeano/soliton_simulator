# -*- coding: utf-8 -*-
"""**LE SEI DECISIONI DI LUCA DEL 2026-09-28** sulle sei pendenze del checkpoint `bd3baa1`,
**piu' la correzione di `SCHED-T2-TIPI`** che il checkpoint stesso aveva dichiarato scaduta.

**Perche' uno script e non una modifica a mano:** `L-NUMERI` -- un valore ricopiato non ha
provenienza. E `P1-quater`: **ogni sostituzione asserisce il proprio ancoraggio** *(la voce esiste
UNA volta, e il valore vecchio e' ESATTAMENTE quello atteso)*, **una alla volta**; un'asserzione
globale sarebbe soddisfatta dalle altre e lascerebbe passare in silenzio quella che non attacca.

LE DECISIONI, come le ha scritte Luca:
  1. il codice di `T3` si approva DOPO il recepimento nel documento delle regole;
  2. `DOPPIA-COP`: subito DOPO `T3` e PRIMA di `T4`, cura a se' col suo sigillo;
  3. `ETC-PASSO`: CHIUSA come superata da `SCHED-PASSO`, e `blocca_run_base = SI` SI SPOSTA;
  4. `CLIP-INVENTARIO`: la tabella per flag DOPO `T3`;
  5. i tre numeri della spinta repulsiva: DOPO `T3` *(voce nuova, nel commit successivo)*;
  6. `MAX_NODI`: fermare il run con errore esplicito *(voce nuova, nel commit successivo)*.

Le decisioni 5 e 6 NON stanno qui: sono VOCI NUOVE, e nascono col punto 7 del checkpoint.

WARNING IL VALIDATORE IMPONE LO SPOSTAMENTO, non e' una preferenza: `blocca = SI` con
`stato = chiuso` e' una CONTRADDIZIONE che `csv/_indice_id.py` rifiuta. Chiudere `ETC-PASSO` senza
spostare il blocco su `SCHED-PASSO` non passerebbe il `pre-commit`.

COMANDO:  python csv/_archivio/_indice_decisioni_6.py
USCITA:   0 se tutte le modifiche attaccano, 1 se una sola non attacca (e allora NON scrive).
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

TSV = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
TAB = chr(9)
NL = chr(10)
OGGI = "2026-09-28"

RIGHE = [l.rstrip(NL).split(TAB) for l in io.open(TSV, encoding="utf-8")]
H = RIGHE[0]
DOVE = {}
for _k, _r in enumerate(RIGHE):
    if _k:
        DOVE.setdefault(_r[0], []).append(_k)

FATTE = []


def _riga(vid):
    q = DOVE.get(vid, [])
    if len(q) != 1:
        raise SystemExit("[ANCORA] la voce `%s` compare %d volte, non 1: non si tocca"
                         % (vid, len(q)))
    return RIGHE[q[0]]


def imposta(vid, colonna, atteso, nuovo):
    """SOSTITUISCE un campo, e FALLISCE se il valore vecchio non e' quello atteso."""
    r = _riga(vid)
    c = H.index(colonna)
    if r[c] != atteso:
        raise SystemExit("[ANCORA] `%s`.%s vale %r, atteso %r: non si tocca"
                         % (vid, colonna, r[c][:90], atteso[:90]))
    if TAB in nuovo or NL in nuovo:
        raise SystemExit("[FORMA] `%s`.%s: un campo non contiene TAB ne' NEWLINE" % (vid, colonna))
    r[c] = nuovo
    FATTE.append((vid, colonna, "SOSTITUITO", len(nuovo)))


def aggiungi(vid, colonna, testo):
    """ACCODA a un campo, e FALLISCE se il testo c'e' GIA': lo script gira UNA volta sola."""
    r = _riga(vid)
    c = H.index(colonna)
    if testo in r[c]:
        raise SystemExit("[GIA' FATTO] `%s`.%s contiene gia' il testo: lo script e' gia' girato"
                         % (vid, colonna))
    if TAB in testo or NL in testo:
        raise SystemExit("[FORMA] `%s`.%s: un campo non contiene TAB ne' NEWLINE" % (vid, colonna))
    r[c] = (r[c] + " " + testo) if r[c] else testo
    FATTE.append((vid, colonna, "ACCODATO", len(r[c])))


# ---- LA CORREZIONE DICHIARATA NEL CHECKPOINT: SCHED-T2-TIPI ------------------------------
T2T = "T2 (i tipi): gli 8 tipi del registro del passo, e dopo L_CONSERVA sono coerenti 8 su 8"
imposta("SCHED-T2-TIPI", "titolo_breve",
        "T2 (i tipi): i tipi dichiarati per le 8 voci del registro. UNA non e' coerente: "
        "rilassa_disegno",
        T2T)
imposta("SCHED-T2-TIPI", "stato", "aperto", "chiuso")
aggiungi("SCHED-T2-TIPI", "nota",
         "CHIUSA il " + OGGI + ": l'UNICA voce non coerente era `rilassa_disegno`, e la causa "
         "(`_togli_rotazione_rigida` -> `calcola_psi` -> psi, psi_spin) e' stata TOLTA con "
         "`L_CONSERVA` (56552f0, simulatore fe00b48a -> 1fc9235f). La verifica statica "
         "csv/_seal_fork/_sig_sched_tipi.py passa ora 8 su 8, e il referto rigirato e' "
         "committato. IL TITOLO PRECEDENTE ERA SCADUTO e diceva ancora <<UNA non e' coerente>>: "
         "lo ha dichiarato il checkpoint bd3baa1 par.8, e questa e' la correzione.")

# ---- DECISIONE 3: ETC-PASSO si CHIUDE, e il blocco SI SPOSTA -----------------------------
imposta("ETC-PASSO", "stato", "aperto", "chiuso")
imposta("ETC-PASSO", "blocca_run_base", "SI", "NO")
imposta("ETC-PASSO", "avanzamento", "IN CORSO", "FATTO")
imposta("ETC-PASSO", "motivo",
        "senza la cura il run base gira con stato MISTO t/t+1 in 4 leggi su 5: 56 letture sporche "
        "su 31 attributi, misurate dall'AST da csv/_test_fork/_etc_letture.py",
        "[SUPERATO il " + OGGI + ", IL BLOCCO E' SU `SCHED-PASSO`] senza la cura il run base gira "
        "con stato MISTO t/t+1 in 4 leggi su 5: 56 letture sporche su 31 attributi, misurate "
        "dall'AST da csv/_test_fork/_etc_letture.py")
aggiungi("ETC-PASSO", "nota",
         "CHIUSA il " + OGGI + " per DECISIONE DI LUCA, come SUPERATA DA `SCHED-PASSO`: la FORMA "
         "della cura non e' piu' <<il passo diventa sincrono>> ma <<il passo diventa uno "
         "SCHEDULATORE>>, e la cura dello stato misto vive dentro `T3`. NON E' UN DIFETTO "
         "RISOLTO: e' una voce la cui forma e' stata sostituita, e il DIFETTO (le 56 letture "
         "sporche) RESTA -- per questo `blocca_run_base = SI` NON si cancella ma SI SPOSTA su "
         "`SCHED-PASSO`, che ne eredita la prova. Il pezzo (c)1 (il confine della fotografia) e' "
         "stato assorbito da `T1` (6ac0008, dab9304).")

# ---- DECISIONE 3-bis: SCHED-PASSO eredita il blocco -------------------------------------
imposta("SCHED-PASSO", "blocca_run_base", "DA-DECIDERE", "SI")
imposta("SCHED-PASSO", "avanzamento", "IN CODA", "IN CORSO")
imposta("SCHED-PASSO", "motivo", "",
        "eredita il blocco da `ETC-PASSO` (chiusa come superata il " + OGGI + "): il run base "
        "gira con stato MISTO t/t+1 in 4 leggi su 5, 56 letture sporche su 31 attributi misurate "
        "dall'AST da csv/_test_fork/_etc_letture.py, e la cura vive in `T3`")
aggiungi("SCHED-PASSO", "nota",
         "DECISIONE DI LUCA del " + OGGI + ": `blocca_run_base` passa da DA-DECIDERE a SI, "
         "ereditato da `ETC-PASSO` che si chiude come superata. La prova del blocco e' la stessa "
         "(le 56 letture sporche), e non si duplica: vive qui. E `T1` e `T2` sono FATTI, quindi "
         "il blocco riguarda ora il solo `T3` (la cura dei flash) piu' `T4` e `T5`.")

# ---- DECISIONE 1: il codice di T3 si approva DOPO il recepimento -------------------------
imposta("SCHED-T3-REGOLE", "avanzamento", "BLOCCATO", "IN CORSO")
aggiungi("SCHED-T3-REGOLE", "nota",
         "LE TRE DECISIONI SONO ARRIVATE (Luca, " + OGGI + "): (1) le decisioni categoriali NON "
         "sono un'eccezione -- la regola <<UNA SOLA legge scrive ogni grandezza-segno>> E' GIA' "
         "VERA PER COSTRUZIONE (e' la cura di `A6-PERCCHI`), va DICHIARATA e non si archivia "
         "niente: :5639 e :5642 sono `if`/`else` della STESSA condizione e non girano mai "
         "insieme, e l'analisi statica non poteva vederlo; verificato a runtime da "
         "csv/_seal_fork/_sig_segni_una_legge.py -- perc_geom SOLO da :5639 (3 su 3 passi), "
         "perc_chi SOLO da :5666 (3 su 3), :5642 ZERO. (2) FORMA 6 `gruppo` ACCETTATA. (3) FORMA "
         "7 `nascita` ACCETTATA. E IL CODICE DI `T3` SI APPROVA SOLO DOPO IL RECEPIMENTO nel "
         "documento delle regole, che il guardiano verifica prima: decisione 1 di Luca del "
         + OGGI + ".")

# ---- DECISIONE 2: DOPPIA-COP fra T3 e T4, cura a se' ------------------------------------
aggiungi("DOPPIA-COP", "nota",
         "QUANDO, deciso da Luca il " + OGGI + ": SUBITO DOPO `T3` e PRIMA di `T4`, come CURA A "
         "SE' COL SUO SIGILLO. NON DENTRO `T3`, e la ragione e' il metodo: sarebbero DUE CAMBI DI "
         "FISICA NELLO STESSO SIGILLO, e un sigillo che ne contiene due non attribuisce piu' un "
         "risultato a un pezzo preciso (la regola d'oro, par.3 di CLAUDE.md). Dentro c'e' "
         "l'inversione del ritmo a 2 pi di :3072, che si INVERTE e non si archivia.")

# ---- DECISIONE 4: CLIP-INVENTARIO dopo T3 -----------------------------------------------
aggiungi("CLIP-INVENTARIO", "nota",
         "QUANDO, deciso da Luca il " + OGGI + ": la tabella PER FLAG (non per ramo) della "
         "famiglia 2 dei 121 rami morti si fa DOPO `T3`. Il pezzo (b)3 resta SOSPESO fino ad "
         "allora, e la priorita' resta la cura.")

# ---- SCRITTURA ---------------------------------------------------------------------------
io.open(TSV, "w", encoding="utf-8", newline=NL).write(
    NL.join(TAB.join(r) for r in RIGHE) + NL)

print("doc/INDICE_ID.tsv -- %d modifiche, tutte con la loro ancora verificata" % len(FATTE))
print("")
print("  %-18s %-16s %-12s %s" % ("voce", "colonna", "come", "lunghezza dopo"))
for vid, col, come, n in FATTE:
    print("  %-18s %-16s %-12s %d" % (vid, col, come, n))
print("")
print("titolo_breve nuovo di SCHED-T2-TIPI: %d caratteri (il tetto e' 100)" % len(T2T))
