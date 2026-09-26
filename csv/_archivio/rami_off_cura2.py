# -*- coding: utf-8 -*-
"""**I RAMI A FLAG SPENTO DI `TEMPO_UNICO_MITOSI`, USCITI DAL SIMULATORE.**

*(Decisione di Luca, 2026-09-27: la `CURA 2` diventa STRUTTURALE. I rami escono, ma
**non si perdono**: sono qui **COPIATI DAL SORGENTE**, non riscritti.)*

> ### ⚠ **QUESTO FILE NON SI IMPORTA E NON GIRA.** E' un ARCHIVIO.
> **Per rilanciare il simulatore com'era, si parte dal TAG:**
> ```
> git cat-file -p pre-cura2-strutturale:soliton_simulator.py > sim_vecchio.py
> ```
> **scritto in BINARIO** *(`git checkout` riscriverebbe le newline: par.5-quinquies)*.
> **Blob del simulatore al tag: `dd4f5ccf`** *(sha1 dei byte grezzi)*.

**I quattro rami, con le righe al tag:**

| `if` a | `else` | che cosa faceva | perche' e' uscito |
|--:|--:|---|---|
| `:5928` | `:5945`-`:5952` | il gradiente che modula la soglia, preso dalla TORSIONE invece che da `r` | col flag strutturale il ramo e' CODICE MORTO: `grad_modula` viene sempre da `r` |
| `:6008` | `:6017`-`:6019` | l'AMPIEZZA della campana moltiplicata per `1/pos_torsione`, cioe' un RITMO FINTO | e' il primo dei due usi di `pos_torsione` COME TEMPO: il difetto di `D32` |
| `:6037` | `:6044`-`:6044` | la probabilita' nel passo senza il fattore di tempo d'arco | dipende SOLO dal ramo qui sopra (`resp_int is None`): cade con lui |
| `:6091` | `:6113`-`:6113` | il rilassamento di `_rep` con `pos_torsione` COME COSTANTE DI TEMPO, in EULERO esplicito | e' il secondo uso come tempo, e l'Eulero e' la forma che `par.4` vieta sui rilassamenti |

**E il perche' GENERALE, che vale per tutti e quattro:** col flag **strutturale**
*(sempre acceso)* ogni ramo `else` e' **codice morto**. Toglierlo e' **byte-inerte per
costruzione**, e **toglie una legge invece di aggiungerne** (`STANDARD 10`): il ritmo
finto `1/pos_torsione` non e' un tempo, e l'Eulero esplicito su `_rep` e' la forma che
`par.4` vieta sui rilassamenti di primo ordine.
"""

# ESENTE-H-P5: e' un ARCHIVIO. Non importa il simulatore, non gira, non scrive referti.

TAG = "pre-cura2-strutturale"
BLOB_AL_TAG = "dd4f5ccf"          # sha1 dei BYTE GREZZI del simulatore al tag


# ==============================================================================================
#  RAMO `else` del `if TEMPO_UNICO_MITOSI` di `:5928` -- righe `:5945`-`:5952` di `mitosi()`
#  al tag `pre-cura2-strutturale` (blob dd4f5ccf)
# ----------------------------------------------------------------------------------------------
#  COSA FACEVA:   il gradiente che modula la soglia, preso dalla TORSIONE invece che da `r`
#  PERCHE' E' USCITO: col flag strutturale il ramo e' CODICE MORTO: `grad_modula` viene sempre da `r`
#  COME SI RILANCIA: git cat-file -p pre-cura2-strutturale:soliton_simulator.py (in BINARIO)
# ==============================================================================================
#                 tors_nodo = np.zeros(self.n)
#                 aw = np.abs(self.tw)
#                 np.add.at(tors_nodo, self.i[self.i < self.n], aw[self.i < self.n])
#                 np.add.at(tors_nodo, self.j[self.j < self.n], aw[self.j < self.n])
#                 tors_nodo = 1.0 + tors_nodo / np.maximum(self._deg, 1) / PHI_CRIT
#                 # a flag SPENTO `grad_modula` e' il gradiente della TORSIONE: un'altra
#                 #   grandezza. **Un nome unico mentirebbe su un ramo dei due** (`D32`).
#                 grad_modula = np.abs(tors_nodo[self.i] - tors_nodo[self.j])

# ==============================================================================================
#  RAMO `else` del `if TEMPO_UNICO_MITOSI` di `:6008` -- righe `:6017`-`:6019` di `mitosi()`
#  al tag `pre-cura2-strutturale` (blob dd4f5ccf)
# ----------------------------------------------------------------------------------------------
#  COSA FACEVA:   l'AMPIEZZA della campana moltiplicata per `1/pos_torsione`, cioe' un RITMO FINTO
#  PERCHE' E' USCITO: e' il primo dei due usi di `pos_torsione` COME TEMPO: il difetto di `D32`
#  COME SI RILANCIA: git cat-file -p pre-cura2-strutturale:soliton_simulator.py (in BINARIO)
# ==============================================================================================
#             tau_locale = 1.0 / pos_torsione                # ritmo (sempre positivo)
#             ampiezza = salita * discesa * tau_locale       # campana positiva (0..max)
#             resp_int = None

# ==============================================================================================
#  RAMO `else` del `if TEMPO_UNICO_MITOSI` di `:6037` -- righe `:6044`-`:6044` di `mitosi()`
#  al tag `pre-cura2-strutturale` (blob dd4f5ccf)
# ----------------------------------------------------------------------------------------------
#  COSA FACEVA:   la probabilita' nel passo senza il fattore di tempo d'arco
#  PERCHE' E' USCITO: dipende SOLO dal ramo qui sopra (`resp_int is None`): cade con lui
#  COME SI RILANCIA: git cat-file -p pre-cura2-strutturale:soliton_simulator.py (in BINARIO)
# ==============================================================================================
#             prob = np.clip(resp, 0.0, 1.0)

# ==============================================================================================
#  RAMO `else` del `if TEMPO_UNICO_MITOSI` di `:6091` -- righe `:6113`-`:6113` di `mitosi()`
#  al tag `pre-cura2-strutturale` (blob dd4f5ccf)
# ----------------------------------------------------------------------------------------------
#  COSA FACEVA:   il rilassamento di `_rep` con `pos_torsione` COME COSTANTE DI TEMPO, in EULERO esplicito
#  PERCHE' E' USCITO: e' il secondo uso come tempo, e l'Eulero e' la forma che `par.4` vieta sui rilassamenti
#  COME SI RILANCIA: git cat-file -p pre-cura2-strutturale:soliton_simulator.py (in BINARIO)
# ==============================================================================================
#             self._rep = self._rep + _dte * (rep - self._rep) / np.maximum(pos_torsione, 1e-12)
