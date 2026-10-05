# -*- coding: utf-8 -*-
"""LA PATCH DELLA CURA (2) DI `MEM-HEBB-VERSO`: il flag `MEM_FASE`.

*(Il **braccio 0** del sigillo: applicata al blob di **prima** deve ridare il blob di
**oggi**, al byte.)*

### ⛔ **I DUE BLOCCHI SONO ESTRATTI DAL SORGENTE CURATO, non ritrascritti a mano:**
una trascrizione e' **una seconda copia** che puo' divergere, cioe' le *«due leggi»* che
`9-ter` vieta. ### **E il generatore ha VERIFICATO la ricostruzione confrontando i blob
PRIMA di scrivere questo file.**

USO:  python csv/_seal_fork/_mem_fase_patch.py <sorgente_di_partenza> <uscita>
"""
import hashlib
import io
import sys

NL = chr(10)
BLOB_PRIMA = "e2940b3c"
BLOB_DOPO = "1feb9b0a"

# --- l'ancora del blocco 1: l'ultima riga del commento di `MEM_MOTO_TUTTO`
ANCORA_1 = "                         # Come `MEM_MOTO`: nessun flag da riga di comando, si imposta SUL MODULO."
BLOCCO_1 = [
    "MEM_FASE = False         # `MEM_FASE` [MEM-HEBB-VERSO, cura (2), decisione di Luca del",
    "                         # 2026-10-04] recinta LA SCRITTURA DELLA MEMORIA DEL MOTO SU `phi`",
    "                         # (il sito del TRASCINAMENTO DI FASE, qui sotto nella stessa",
    "                         # funzione). `MEM_FASE` e' il nome, e questo commento lo NOMINA",
    "                         # perche' `H-P7` lo pretende: un commento che non nomina il suo",
    "                         # flag resta MUTO se una patch si inserisce fra i due.",
    "                         # ⛔ IL DEFAULT E' `False`, E NON E' UN FLAG BYTE-INERTE: spento,",
    "                         #   LA FISICA CAMBIA. E' la fisica DECISA -- il sito NON scrive piu'",
    "                         #   `phi`. Acceso riproduce il comportamento storico, BYTE-IDENTICO.",
    "                         #   E' il CONTRARIO del caso normale di questo repo, dove un flag",
    "                         #   nuovo nasce OFF **e inerte**: qui OFF toglie una legge.",
    "                         # IL PERCHE', MISURATO (`doc/REFERTO_mem_hebb_verso_2026-10-05.md`,",
    "                         #   commit `2717308`): il sito SCARTAVA IL 97.3% dei contributi che",
    "                         #   calcolava -- `phi[ii] = ...` con `ii` CHE CONTIENE RIPETIZIONI, e",
    "                         #   in numpy l'indicizzazione fancy IN SCRITTURA fa VINCERE L'ULTIMO.",
    "                         #   Rapporto dei moduli scartati/applicati: 36.2. Un nodo e' primo",
    "                         #   estremo di fino a 90 archi, e 89 contributi su 90 sparivano IN",
    "                         #   SILENZIO. ⛔ QUALE sopravvivesse dipendeva dall'ORDINE DELL'ARRAY:",
    "                         #   non e' una legge, e' un artefatto dell'ordine.",
    "                         # ⚠ SPEGNE SOLO LA SCRITTURA SU `phi`. `mem_mot` continua ad",
    "                         #   aggiornarsi, `proiezione_trasversale` e `shift_fase_dinamico`",
    "                         #   restano CALCOLATI, e il taglio `pi/4` resta applicato a",
    "                         #   `shift_fase_dinamico`: si toglie SOLO il contributo a `phi`,",
    "                         #   com'e' per `MEM_MOTO` sul contributo a `d0`.",
    "                         # ⚠ E TOGLIE ANCHE IL `% self._dphi()` su `phi[ii]`, non solo la",
    "                         #   somma: il commento di `:9516` dichiara che `(phi + 0) % (4 pi)`",
    "                         #   e' un NO-OP **solo se `phi` sta gia' nel dominio**.",
    "                         # ⛔ GLI ALTRI DUE DIFETTI DEL SITO NON SONO CURATI QUI, e spegnere",
    "                         #   NON E' CURARE: <<solo l'estremo `ii` riceve>> resta in",
    "                         #   `MEM-HEBB-VERSO`, e `dir_laterale = (-y, x, 0)` -- che privilegia",
    "                         #   l'asse `z` del LABORATORIO mentre i nodi stanno in 3D -- e' la",
    "                         #   voce `FASE-TRASCINAMENTO-3D`, che RESTA APERTA: la legge in 3D",
    "                         #   NON si scrive ora (decisione di Luca).",
    "                         # Come `MEM_MOTO` e `MEM_MOTO_TUTTO`: nessun flag da riga di comando,",
    "                         # si imposta SUL MODULO. E' la TERZA volta della stessa forma.",
]

# --- l'ancora del blocco 2: il commento che precede la scrittura su `phi`
ANCORA_2 = "                    # Applica lo shift al campo di fase senza alterare le coordinate fisse dei puntatori (net.pos)"
VECCHIA_2 = "                    self.phi[ii] = (self.phi[ii] + shift_fase_dinamico) % self._dphi()"
BLOCCO_2 = [
    "                    # [MEM_FASE, cura (2) di MEM-HEBB-VERSO, decisione di Luca del 2026-10-04]",
    "                    # IL SITO SI SPEGNE CON UN FLAG PROPRIO, e il DEFAULT lo tiene SPENTO.",
    "                    # ⛔ MISURATO: scartava il 97.3% dei contributi, perche' `ii` CONTIENE",
    "                    #   RIPETIZIONI e l'indicizzazione fancy in scrittura FA VINCERE L'ULTIMO.",
    "                    #   Rapporto dei moduli scartati/applicati 36.2 (referto `2717308`).",
    "                    #   QUALE contributo sopravvivesse dipendeva dall'ORDINE DELL'ARRAY.",
    "                    # ⚠ E QUESTO `if` TOGLIE ANCHE IL `% self._dphi()`, non solo la somma:",
    "                    #   vedi il commento otto righe sopra. Se `phi` uscisse dal dominio la",
    "                    #   differenza sarebbe piu' grande di `shift_fase_dinamico`.",
    "                    # `MEM_MOTO` e `MEM_MOTO_TUTTO` NON cambiano, e `mem_mot` continua ad",
    "                    # aggiornarsi: si recinta QUESTA scrittura e nient'altro.",
    "                    if MEM_FASE:",
    "                        self.phi[ii] = (self.phi[ii] + shift_fase_dinamico) % self._dphi()",
]


def applica(testo):
    """Le due sostituzioni, ciascuna ASSERITA UNICA (`P1-quater`)."""
    n = testo.count(ANCORA_1)
    if n != 1:
        raise SystemExit("[FERMO] ancora 1 presente %d volte, non 1." % n)
    testo = testo.replace(ANCORA_1, ANCORA_1 + NL + NL.join(BLOCCO_1), 1)
    vecchio = ANCORA_2 + NL + VECCHIA_2
    n = testo.count(vecchio)
    if n != 1:
        raise SystemExit("[FERMO] ancora 2 presente %d volte, non 1." % n)
    return testo.replace(vecchio, ANCORA_2 + NL + NL.join(BLOCCO_2), 1)


def main(argv):
    src, dst = argv[1], argv[2]
    t = io.open(src, encoding="utf-8").read()
    b = hashlib.sha1(io.open(src, "rb").read()).hexdigest()[:8]
    print("  partenza: %s  (atteso %s)" % (b, BLOB_PRIMA))
    out = applica(t)
    io.open(dst, "w", encoding="utf-8", newline=NL).write(out)
    bd = hashlib.sha1(io.open(dst, "rb").read()).hexdigest()[:8]
    print("  uscita:   %s  (atteso %s)   %s"
          % (bd, BLOB_DOPO, "COINCIDE" if bd == BLOB_DOPO else "### NON COINCIDE"))
    return 0 if bd == BLOB_DOPO else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
