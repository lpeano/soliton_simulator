# -*- coding: utf-8 -*-
"""LA PATCH DI `TORS-W8-AVVOLGIMENTO`: la fase si avvolge col suo periodo, il
dipolo no.

*(Il **braccio 0** del sigillo: applicata al blob di **prima** deve ridare il
blob di **oggi**, al byte.)*

### GLI HUNK VENGONO DAL DIFF VERO *(`difflib.SequenceMatcher`)*, non da cio'
che credevo di aver cambiato, e il generatore ha **VERIFICATO la ricostruzione**
**confrontando i blob PRIMA di scrivere questo file**.

### ⚠ **E IL CONTESTO DI OGNI HUNK E' MISURATO, non scelto:** si allarga di una
riga per volta finche' il vecchio testo non e' **unico** nel file di partenza
*(`P1-quater`)*.

**CHE COSA CAMBIA, in ordine:** il registro degli **INVARIANTI** *(`twp` cambia
descrizione -- da *«torsione precedente»* a *«la FASE precedente d'arco»* -- e
`twp_dip` entra con la sua eccezione dichiarata)*; il **`REGISTRO_STATO`**; la
forma **`dip`** nel controllore degli invarianti; le **due regole di nascita** di
`twp_dip` *(divisione e Schwinger)*; **`_allaccia`** *(la semina)* e
**`__init__`**; il **blocco della torsione** del ramo `TORS_4PI`; e il
**contatore `A8`** della guardia di `_tau_tw_locale` *(rilievo `E4` del
guardiano)*.

### ⛔ **IL RAMO NON-`4π` NON SI TOCCA**, e il sigillo lo verifica.

**Il ramo vecchio e' COPIATO** in `csv/_archivio/_rami_off_tors_w8.py`, e il
*prima* si rilancia dal tag **`pre-tors-w8-cura`** con
`git cat-file -p <ref>:soliton_simulator.py` **in BINARIO** *(par.7)*.

USO:  python csv/_seal_fork/_tors_w8_patch.py <partenza> <uscita>
"""
# ESENTE-H-P8: un FALSO POSITIVO, e lo nomino invece di riformularlo. Il rilevatore
#   cerca `cat-file` dentro una STRINGA con una parola tipo <<prima>> vicino: qui la stringa
#   e' LA DOCSTRING, che SPIEGA a chi legge come estrarre il *prima* -- e nomina
#   ### IL TAG `pre-tors-w8-cura`, NON `HEAD`. Questa patch non legge git affatto: riceve i
#   due file da `argv`, e il *prima* lo estrae il SIGILLO, dal padre del commit.
#   ### POTEVO TOGLIERE LA PAROLA `cat-file` DALLA DOCSTRING E PASSARE IL CONTROLLO: NON LO
#   FACCIO. Quella riga dice al lettore la cosa GIUSTA -- che i byte si recuperano con
#   `git cat-file -p` in binario e non con `git checkout` (la trappola CRLF del par.7) --
#   e disarmare un presidio cancellando un'istruzione vera e' peggio del falso positivo.
#   E' la SESTA volta per la stessa ragione, e la quinta e' nel patch di `Z43 CURA (2)`.
import hashlib
import io
import sys

NL = chr(10)
TAG = "pre-tors-w8-cura"          # il blob di PRIMA
BLOB_PRIMA = "f7237563"
BLOB_DOPO = "cf2a1ac8"

# Ogni hunk: (etichetta, il VECCHIO testo, il NUOVO). Il vecchio e' ASSERITO
# UNICO a ogni applicazione (`P1-quater`), e il CONTESTO accanto a ciascuno e'
# quanto e' bastato per renderlo unico -- non una scelta, una MISURA del
# generatore.
HUNK = [
    ('hunk 1 (replace), contesto 0 righe',
     NL.join([
    "    'twp':      ('finito', 'torsione precedente'),",
     ]),
     NL.join([
    "    # [TORS-W8-AVVOLGIMENTO, cura del 2026-10-06] `twp` E' LA FASE PRECEDENTE D'ARCO, e ora",
    "    #   lo e' in ENTRAMBI i rami: prima il ramo `TORS_4PI` ci scriveva",
    '    #   `_w8(dph + twist_dip)` e il ramo non-4pi ci scriveva `dph`. Un nome, due significati:',
    "    #   l'eccezione e' TOLTA, non spostata.",
    "    'twp':      ('finito', 'la FASE precedente d arco (dph del passo prima)'),",
    "    # ⚠ `twp_dip` HA UN'ECCEZIONE DICHIARATA, ed e' la STESSA forma di `peq`: un arco appena",
    "    #   nato porta `nan` finche' non vede il suo primo passo di torsione, che e' il punto in",
    '    #   cui la spinta vale ZERO e i due stati si registrano.',
    "    #   ### E IL <<MAI OLTRE UN PASSO>> E' STRUTTURALE, non vigilato: il passo di torsione",
    '    #   scrive `twp_dip` INCONDIZIONATAMENTE su ogni arco, quindi dopo QUALUNQUE passo di',
    '    #   torsione nessun arco ha `nan`. Il sigillo `S1` lo DIMOSTRA.',
    "    'twp_dip':  ('dip',    'il DIPOLO precedente d arco: finito, e `nan` SOLO su un arco '",
    "                           'che non ha ancora visto un passo di torsione'),",
     ])),
    ('hunk 2 (insert), contesto 1 righe',
     NL.join([
    '    i, j = net.i, net.j',
    '    if len(net.phivel) < net.n or len(i) == 0:',
     ]),
     NL.join([
    '    i, j = net.i, net.j',
    '    # [A8, cura TORS-W8-AVVOLGIMENTO 2026-10-06] LA GUARDIA SI CONTA. Rilievo del guardiano',
    '    #   (`E4`): `TAU_TW` entra in gioco per TRE vie, non due -- il ramo non locale, il',
    '    #   docstring che dice 3.1831, e QUESTA GUARDIA. Se scattasse, `tau_tw` passerebbe da',
    '    #   ~2-6 (misurato: mediana 2.4055 al passo 50) a 20: un fattore 3-10 sul tetto di',
    "    #   equilibrio, e NESSUNO lo contava. ### UN RAMO SILENZIOSO NON E' UN RAMO.",
    '    #   ### BYTE-INERTE: quattro contatori e nessun cambio di valore restituito.',
    "    net._g_tautw_tot = getattr(net, '_g_tautw_tot', 0) + 1",
    '    if len(net.phivel) < net.n or len(i) == 0:',
     ])),
    ('hunk 3 (insert), contesto 1 righe',
     NL.join([
    '    if len(net.phivel) < net.n or len(i) == 0:',
    '        return TAU_TW',
     ]),
     NL.join([
    '    if len(net.phivel) < net.n or len(i) == 0:',
    "        net._g_tautw_salti = getattr(net, '_g_tautw_salti', 0) + 1",
    '        net._g_tautw_forma = (len(net.phivel), net.n, len(i))',
    '        net._g_tautw_quando = net._g_tautw_tot',
    '        return TAU_TW',
     ])),
    ('hunk 4 (insert), contesto 1 righe',
     NL.join([
    '    ("twp", ("m",), "float64"),',
    '    ("vd", ("m",), "float64"),',
     ]),
     NL.join([
    '    ("twp", ("m",), "float64"),',
    "    # [TORS-W8-AVVOLGIMENTO] il DIPOLO precedente d'arco. ### STA DOPO `twp`, quindi dopo",
    '    #   `tw`: il VINCOLO 4 (`perc_geom` subito dopo `tw`) non si tocca, e i suoi due `raise`',
    "    #   lo verificano all'import.",
    '    ("twp_dip", ("m",), "float64"),',
    '    ("vd", ("m",), "float64"),',
     ])),
    ('hunk 5 (insert), contesto 1 righe',
     NL.join([
    '',
    '@_nascita_regola("divisione", "vd", "eredita dall\'arco che si spezza",',
     ]),
     NL.join([
    '',
    '@_nascita_regola("divisione", "twp_dip", "`nan`: il marcatore di ARCO NUOVO",',
    '                 "self.twp_dip = np.concatenate([self.twp_dip[keep], nn, nn])",',
    '                 "### `nan` E\' IL MARCATORE: al primo passo di torsione la spinta vale ZERO "',
    '                 "e i due stati si registrano. ### PERCHE\' UN MARCATORE E NON IL VALORE "',
    '                 "ALLA NASCITA: il dipolo si legge da `chi_torsione`, che con `CHI_CORE` o "',
    '                 "`CHI_COOP` viene da una CACHE scritta NEL PASSO DELLA TORSIONE -- quindi "',
    '                 "il valore letto qui NON e\' quello che l\'arco vedra\'. Il marcatore vale "',
    '                 "per QUALUNQUE via di nascita e NON dipende da nessun flag")',
    'def _rn_div_twp_dip(net, c):',
    '    nn = np.full(c["quante"], np.nan)',
    '    net.twp_dip = np.concatenate([net.twp_dip[c["keep"]], nn, nn])',
    '',
    '',
    '@_nascita_regola("divisione", "vd", "eredita dall\'arco che si spezza",',
     ])),
    ('hunk 6 (insert), contesto 1 righe',
     NL.join([
    '                              net._wphi(c["anti"] - net.phi[c["bb"]])])',
    '',
     ]),
     NL.join([
    '                              net._wphi(c["anti"] - net.phi[c["bb"]])])',
    '',
    '',
    '@_nascita_regola("schwinger", "twp_dip", "`nan`: il marcatore di ARCO NUOVO",',
    '                 "self.twp_dip = np.concatenate([self.twp_dip, nn2, nn2])",',
    '                 "lo STESSO marcatore della divisione, e per lo stesso motivo: una sola "',
    '                 "legge per tutte le vie di nascita")',
    'def _rn_sch_twp_dip(net, c):',
    '    nn2 = np.full(c["nc"], np.nan)',
    '    net.twp_dip = np.concatenate([net.twp_dip, nn2, nn2])',
    '',
     ])),
    ('hunk 7 (insert), contesto 1 righe',
     NL.join([
    '        self.peq = np.zeros(0); self.tw = np.zeros(0); self.twp = np.zeros(0)',
    '        # [(3) BONIFICA 2026-09-17] MEMORIA DELLA REPULSIONE, per ARCO. Vedi `mitosi()`.',
     ]),
     NL.join([
    '        self.peq = np.zeros(0); self.tw = np.zeros(0); self.twp = np.zeros(0)',
    "        self.twp_dip = np.zeros(0)   # [TORS-W8-AVVOLGIMENTO] il dipolo precedente d'arco",
    '        # [(3) BONIFICA 2026-09-17] MEMORIA DELLA REPULSIONE, per ARCO. Vedi `mitosi()`.',
     ])),
    ('hunk 8 (insert), contesto 1 righe',
     NL.join([
    '        self.twp = np.concatenate([self.twp, np.zeros(len(dd))])',
    '        self._grado()',
     ]),
     NL.join([
    '        self.twp = np.concatenate([self.twp, np.zeros(len(dd))])',
    "        # [TORS-W8-AVVOLGIMENTO] IL MARCATORE ANCHE QUI, ed e' la via che il difetto (ii)",
    '        #   colpiva: `twp = 0` faceva ricevere a OGNI arco della scena tutta la sua',
    "        #   differenza di fase (piu' il dipolo) come torsione al primo passo.",
    '        #   ### MISURATO sul blob di prima: spinta mediana 3.0950, MASSIMA 9.4248 = 3pi',
    '        #   esatto, e al passo 2 quella spinta era diventata `|tw|`.',
    '        self.twp_dip = np.concatenate([self.twp_dip, np.full(len(dd), np.nan)])',
    '        self._grado()',
     ])),
    ('hunk 9 (insert), contesto 1 righe',
     NL.join([
    "                          '(ammessi ora: %d)' % int(np.sum(_amm)))",
    "            elif forma == 'indice':",
     ]),
     NL.join([
    "                          '(ammessi ora: %d)' % int(np.sum(_amm)))",
    "            elif forma == 'dip':",
    '                # [TORS-W8-AVVOLGIMENTO] IL DIPOLO PRECEDENTE: finito, oppure `nan` su un',
    "                #   arco che non ha ancora visto un passo di torsione -- e quello e' un arco",
    "                #   con `tw == 0` ESATTO, perche' tutte e tre le regole di nascita lo",
    '                #   azzerano e solo il passo di torsione lo muove.',
    "                #   ### SI PRECISA, NON SI ALLARGA: e' la lezione di `peq`.",
    '                vf = v.astype(float, copy=False)',
    '                _nan = ~np.isfinite(vf)',
    "                _twv = np.asarray(getattr(self, 'tw', []), float)",
    '                _amm = (np.zeros(len(vf), dtype=bool) if len(_twv) != len(vf)',
    '                        else (_twv == 0.0))',
    "                self._g_inv_dip_nan_ok = (getattr(self, '_g_inv_dip_nan_ok', 0)",
    '                                          + int(np.sum(_nan & _amm)))',
    '                cattivo = _nan & ~_amm',
    "                regola = ('finito, e `nan` SOLO su archi con `tw == 0` esatto, cioe mai '",
    "                          'passati dalla torsione (ammessi ora: %d)' % int(np.sum(_amm)))",
    "            elif forma == 'indice':",
     ])),
    ('hunk 10 (replace), contesto 0 righe',
     NL.join([
    '            self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw',
    '            self.twp = self._w8(dph + twist_dip)',
     ]),
     NL.join([
    '            # [TORS-W8-AVVOLGIMENTO, cura del 2026-10-06] LA FASE SI AVVOLGE COL SUO',
    '            #   PERIODO, IL DIPOLO NON SI AVVOLGE.',
    "            #   ### IL DIFETTO: `dph = _wphi(...)` vive su un periodo di 4pi (`FASE_2PI` e'",
    "            #   False) e `_w8` ha periodo 8pi -- un salto di 4pi NON e' un multiplo del suo",
    '            #   periodo, quindi NON viene riparato. MISURATO: 142114 calci di modulo 4pi',
    '            #   ESATTI in 150 passi, e il ramo non-4pi (`_w4`, periodo 4pi) ripara entro',
    '            #   1.9e-15.',
    "            #   ### LA CURA NON E' SCEGLIERE FRA `_w4` E `_w8`: si avvolge la DIFFERENZA DI",
    '            #   FASE col periodo giusto e si somma la differenza del dipolo NON avvolta.',
    '            #   `twist_dip` sta fra -pi e pi, cambia al massimo di 2pi, e NON ha periodo.',
    "            #   ### E L'ARCO NUOVO HA SPINTA ZERO al suo primo passo, per QUALUNQUE via di",
    "            #   nascita: `twp_dip = nan` e' il marcatore, e `np.where` scarta il ramo col",
    '            #   `nan` senza propagarlo. Senza questo, un arco appena nato riceveva il suo',
    '            #   dipolo (divisione, Schwinger) o TUTTA la sua differenza di fase (semina).',
    '            _nuovo = np.isnan(self.twp_dip)',
    '            _fp = np.where(_nuovo, dph, self.twp)',
    '            _dp = np.where(_nuovo, twist_dip, self.twp_dip)',
    "            self._g_tors_nuovi = getattr(self, '_g_tors_nuovi', 0) + int(np.sum(_nuovo))",
    '            self.tw += (self._w4(dph - _fp) + (twist_dip - _dp)',
    '                        - dt_e * self.tw / _ttw)',
    '            self.twp = dph',
    '            self.twp_dip = twist_dip * np.ones_like(dph)',
     ])),
]


def applica(sorgente, dst):
    t = io.open(sorgente, encoding="utf-8", newline="").read()
    b0 = hashlib.sha1(io.open(sorgente, "rb").read()).hexdigest()[:8]
    if b0 != BLOB_PRIMA:
        raise SystemExit("[FERMO] la partenza e' %s, non %s (il blob di PRIMA)." % (b0, BLOB_PRIMA))
    for et, vecchio, nuovo in HUNK:
        n = t.count(vecchio)
        if n != 1:
            raise SystemExit("[FERMO] %s: il vecchio testo compare %d volte, non 1." % (et, n))
        t = t.replace(vecchio, nuovo)
        print("  ok  " + et)
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    b1 = hashlib.sha1(io.open(dst, "rb").read()).hexdigest()[:8]
    print("  uscita: blob %s   atteso %s   -> %s"
          % (b1, BLOB_DOPO, "COINCIDE" if b1 == BLOB_DOPO else "### DIVERSO"))
    return 0 if b1 == BLOB_DOPO else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(applica(sys.argv[1], sys.argv[2]))
