# -*- coding: utf-8 -*-
"""**ARCHIVIO: I PAVIMENTI MORTI, usciti dal simulatore il 2026-09-27.**

**QUESTO FILE NON GIRA E NON SI IMPORTA.** E' il **testo esatto** di cio' che e' stato
rimosso da `soliton_simulator.py`, estratto con `git cat-file -p` dal blob taggato --
**non ricopiato a mano**.

**DA DOVE VIENE:** tag **`pre-archivio-pavimenti`**, simulatore blob sha1-BYTE
**`e203f9a8`**. Per rileggere l'originale intero:

    git cat-file -p pre-archivio-pavimenti:soliton_simulator.py

**PERCHE' E' USCITO** *(decisione di Luca del 2026-09-27, passo (b)1 di `ETC-PASSO`)*:
**e' un DOPPIONE INERTE, non una legge.** Con l'argv del driver -- che passa
`--scala-min-passo` -- **nessuno di questi siti esegue**:

  - `_pav_d0` esce dal ramo inerte a `:4453` e restituisce `v` **intatto**:
    misurato **15 chiamate su 15** (`_g_sm_pav_saltati = 15`), e la riga `:4456`
    **ha eseguito 0 volte** su 3 passi pieni (copertura con `sys.settrace`);
  - i due `np.maximum(..., 0.05)` su `d` sono i rami **`else`** di `SCALA_MIN_PASSO`,
    **0 esecuzioni**; e quello di Eulero e' **doppiamente** morto, perche' il driver
    passa `--verlet`.

### **E LA GARANZIA NON SE NE VA CON LORO.**
Cio' che tiene le lunghezze sopra la scala minima e' **`LAM`** *(`SCALA_MIN_PASSO`,
`_nasce`, `SEMINA_LAM`, `MITOSI_2LAM`)*, **che resta e che NON si tocca**. Misurato sui
16 stati del pilota: **`min(d) = 0.800000 = LAM` ESATTAMENTE**, in ogni stato e ogni
checkpoint, **0 archi sotto `LAM`**. E il pavimento vecchio, `0.05`, stava **16 volte
piu' in basso** del minimo osservato: **non avrebbe potuto mordere nemmeno se fosse
stato vivo.**

**⚠ E CHE COSA CAMBIA, dichiarato invece di lasciarlo scoprire:** con **entrambi**
`SCALA_MIN` e `SCALA_MIN_PASSO` **spenti** -- una configurazione che **il driver non
usa** -- prima `d0` aveva un pavimento e ora **non l'ha piu'**. **Non e' una
regressione nascosta: e' il senso dell'archiviazione**, e chi volesse quel
comportamento lo ritrova qui sotto e nel tag.

**E `PAV_COM` diventa INERTE:** era il flag che rendeva `_floor_d0` comovente, e
`_floor_d0` non c'e' piu'. **Il driver lo passa (`--pav-com`)**, e da oggi **non fa
niente**: dichiarato nel `README` e nel commento del flag.
"""

raise SystemExit(__doc__)   # non si importa e non si gira: e' un ARCHIVIO


# ==========================================================================
# `_pav_d0` — il PAVIMENTO su `d0`
# righe 4449-4456 del blob e203f9a8
# ==========================================================================
_ARCHIVIO_4449 = r"""
    def _pav_d0(self, v):
        """⚠ A `SCALA_MIN` ACCESO IL PAVIMENTO SPARISCE: la discesa e' gia' stata smorzata
        alla scrittura, e lasciare anche il pavimento comovente vorrebbe dire DUE leggi
        sovrapposte, con la vecchia che continua a mordere."""
        if SCALA_MIN or SCALA_MIN_PASSO:
            self._g_sm_pav_saltati = getattr(self, '_g_sm_pav_saltati', 0) + 1
            return v
        return np.maximum(v, self._floor_d0())
"""

# ==========================================================================
# `_floor_d0` — il VALORE del pavimento (assoluto 0.05, o comovente con `PAV_COM`)
# righe 4598-4609 del blob e203f9a8
# ==========================================================================
_ARCHIVIO_4598 = r"""
    def _floor_d0(self):
        # PAVIMENTO di d0. Assoluto (0.05) di default; COMOVENTE se PAV_COM: f*median(d0), con
        # f = 0.05/LAM_BASE = il RAPPORTO DI NASCITA (il vecchio pavimento assoluto diviso la
        # lunghezza d'onda fondamentale). LAM caratterizza la nascita: fissa la frazione, poi il
        # pavimento SCALA comovente con median(d0). Sta nella CODA (~6% della mediana), non nel
        # corpo (come median-MAD, che clampava il 73% e falsava la misura). Non-regressivo alla
        # nascita (median~LAM_BASE -> pavimento~0.05). Circolarita' 1/(1-q*f) trascurabile: f<<1.
        if not PAV_COM or not len(self.d0):
            return 0.05
        f = 0.05 / LAM_BASE                       # rapporto di nascita (adimensionale), NON scelto
        return f * float(np.median(self.d0))

"""

# ==========================================================================
# il ramo `else` del sottociclo VERLET — `np.maximum(..., 0.05)` su `d`
# righe 5730-5737 del blob e203f9a8
# ==========================================================================
_ARCHIVIO_5730 = r"""
                #   il freno e' UNO SOLO, dopo il ciclo, sulla variazione TOTALE. Cosi'
                #   `nsub` non moltiplica piu' il bias.
                if SCALA_MIN_PASSO:
                    d_new = self.d + dts * vd_half
                elif SCALA_MIN:
                    d_new = self.d + self._smorza(self.d, dts * vd_half, 'd')
                else:
                    d_new = np.maximum(self.d + dts * vd_half, 0.05)
"""

# ==========================================================================
# il ramo `else` del sottociclo EULERO — `np.maximum(..., 0.05)` su `d`
# righe 5776-5782 del blob e203f9a8
# ==========================================================================
_ARCHIVIO_5776 = r"""
                self.vd = self.vd + dts * (cs_arco ** 2 * lap + src - beta * self.vd)
                if SCALA_MIN_PASSO:
                    self.d = self.d + dts * self.vd
                elif SCALA_MIN:
                    self.d = self.d + self._smorza(self.d, dts * self.vd, 'd')
                else:
                    self.d = np.maximum(self.d + dts * self.vd, 0.05)
"""
