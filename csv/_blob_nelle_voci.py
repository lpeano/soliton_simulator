# -*- coding: utf-8 -*-
"""QUANTE VOCI DEL REGISTRO PORTANO IL BLOB DEL CODICE CHE LE HA PRODOTTE.

PERCHE' ESISTE
  "Nessun numero senza il suo blob" e' stato chiesto come PRESIDIO. Prima di scriverne uno, si
  MISURA quanto e' grande il buco: "alcune voci ce l'hanno (Z33, Z48), la maggioranza no" e'
  un'IMPRESSIONE, e un presidio costruito su un'impressione protegge da un problema immaginato.

COSA FA, E SOLO QUESTO
  Scorre le voci TABELLARI dei registri (righe `| **SIGLA** | ... |`) e guarda se la voce contiene
  un blob (8+ cifre esadecimali fra backtick). Riporta il conteggio e l'elenco delle voci SENZA.

*** COSA NON FA, E VA DETTO PRIMA CHE QUALCUNO CI CONTI ***
  - NON verifica che il blob citato sia QUELLO GIUSTO: verifica che ce ne sia UNO. Una voce che
    cita il blob sbagliato passa. Per verificare il blob giusto bisognerebbe sapere quale run ha
    prodotto quel numero, e QUELLO non e' scritto da nessuna parte -- e' esattamente il buco.
  - NON copre la PROSA: i marchi in testa ai registri, i paragrafi di `CLAUDE.md`, i referti in
    `doc/`. Li' un numero puo' stare in mezzo a una frase, e non esiste un confine di "voce".
  - NON impedisce NIENTE. E' una MISURA, non una guardia: non fallisce, non blocca un commit.
    **Chiamarlo presidio sarebbe il difetto che descrive `A9`.**

  Un presidio VERO -- che RIFIUTI una voce nuova senza blob -- e' possibile solo sulle tabelle,
  perche' solo li' c'e' una struttura. Su prosa libera non ho trovato un meccanismo affidabile:
  ogni riga di prosa contiene numeri (date, percentuali, righe di codice), e un controllo che
  segnala tutto non viene letto da nessuno. LO DICHIARO invece di scrivere l'ennesima nota.
ASCII PURO.
"""
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
REGISTRI = ["doc/RAMIFICAZIONI.md", "doc/COMPONENTI_PROMOSSE.md", "doc/INVENTARIO_strumenti.md"]
VOCE = re.compile(r"^\|\s*\*\*([A-Za-z0-9._-]{1,12})\*\*\s*\|")
BLOB = re.compile(r"`[0-9a-f]{8,40}`")
# un numero "di misura": decimale, percentuale, o notazione scientifica
NUMERO = re.compile(r"\d+\.\d+|\d+\s*%|\d+e[+-]?\d+")


def main():
    tot = con = senza_blob_con_numeri = 0
    elenco = []
    for rel in REGISTRI:
        p = os.path.join(RADICE, rel)
        if not os.path.exists(p):
            print("ASSENTE: %s" % rel)
            continue
        n_f = c_f = 0
        for riga in open(p, encoding="utf-8"):
            m = VOCE.match(riga)
            if not m:
                continue
            n_f += 1
            ha_blob = bool(BLOB.search(riga))
            if ha_blob:
                c_f += 1
            elif NUMERO.search(riga):
                senza_blob_con_numeri += 1
                elenco.append((rel, m.group(1)))
        tot += n_f
        con += c_f
        print("%-34s voci %3d   col blob %3d   (%.0f %%)"
              % (rel, n_f, c_f, 100.0 * c_f / n_f if n_f else 0))
    print("")
    print("TOTALE: %d voci, %d col blob (%.0f %%), %d SENZA blob ma CON numeri di misura"
          % (tot, con, 100.0 * con / tot if tot else 0, senza_blob_con_numeri))
    print("")
    print("Le voci senza blob che citano numeri (le prime 40):")
    for rel, sigla in elenco[:40]:
        print("   %-34s %s" % (rel, sigla))
    if len(elenco) > 40:
        print("   ... e altre %d" % (len(elenco) - 40))
    print("")
    print("NB: questa e' una MISURA, non una guardia. Non fallisce e non blocca niente, e non")
    print("    verifica che il blob citato sia QUELLO GIUSTO: verifica che ce ne sia UNO.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
