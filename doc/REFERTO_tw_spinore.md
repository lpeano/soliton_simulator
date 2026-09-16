# REFERTO — `TW_SPINORE`: la legge CODIFICATA non e' quella DICHIARATA

> **2026-09-16.** Branch `fork-su2`. Blob del simulatore al momento della misura: quello del commit
> `5c6e770` (promozione dello Step 2). **Due run veri**, 150 passi, seme 1, **`--cs-dinamico`
> acceso** (§4), configurazione del fork completa. Strumento committato **prima** del run (§5):
> `csv/_test_fork/_misura_tw.py`; analisi sui `.pkl` gia' prodotti, **senza run nuovi**:
> `csv/_test_fork/_analisi_tw.py` -> `_analisi_tw.txt`.
>
> **Il mandato diceva «`TW_SPINORE` sigillato e poi acceso». NON l'ho acceso e NON ho scritto il
> sigillo: P1 — *ogni affermazione che contraddica un fatto misurato va SEGNALATA, non eseguita*.**

---

## 0. IL VERDETTO IN TRE RIGHE

> 1. Il commento dice che la torsione **«pilota il Bloch di `tw/2`»**, cioe' un **ANGOLO**. Il codice
>    somma `tw/(4π)` a una **VELOCITA' ANGOLARE**. L'angolo che ne esce e' **628 volte piu' piccolo**.
> 2. Il termine finisce in **`self.omega_s`**, la **MEMORIA persistente** — non nella rotazione
>    istantanea. **Lo stesso file, 1400 righe sopra, dichiara che farlo «darebbe accumulo/divergenza».**
> 3. **Non concludo che sia trascurabile.** Il suo peso in ampiezza e' **0.054 %**, ma l'argomento di
>    ampiezza su una domanda di direzione **e' un errore che ho gia' fatto** (§9). Serve la misura
>    giusta, e non e' questa.

---

## 1. COSA DICE IL CODICE (verificato dal sorgente, non dai commenti — §0)

```python
# :2143   omega_new e' una VELOCITA' ANGOLARE
omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)
if TW_SPINORE:                                                          # :2144
    _twh = self.tw[mask] / (2.0 * max(PHI_CRIT, 1e-9))                  # :2149  = tw/(4 pi)
    _axis = np.where(cl[:, None] > 0, [1.,0.,0.], [0.,0.,1.])           # :2150  asse FISSO
    ...
    omega_new = omega_new + _otw / np.maximum(_degt[:, None], 1.0)      # :2154  somma DIRETTA
...
self.omega_s = omega_new.copy()                                         # :2313  MEMORIA
```

E l'angolo di rotazione, poche righe piu' in la':

```python
theta = _on * _dts          # :2210   |omega| * dt      (ramo --spinore-corretto)
ang   = on * dtn_c          # :2296   idem, ramo non-corretto
```

**Quindi `omega` e' una velocita' angolare, senza ambiguita'.**

---

## 2. I NUMERI (209 852 archi, run ON, misura TRASVERSALE a un solo istante)

*(Trasversale e non temporale di proposito: il presidio §9 dice che una spiegazione dev'essere
decisa da un test che **non contiene il tempo**.)*

| | grandezza | valore |
|---|---|---|
| | modulo di `tw`, mediana | **1.965e+00** rad |
| **(a)** | **DICHIARATO** dal commento: angolo/passo `= tw/2` | **9.827e-01 rad** |
| **(b)** | **CODIFICATO** (`:2149`): il termine `tw/(4π)` sommato a `omega` | **1.564e-01** |
| **(c)** | **l'angolo che (b) produce davvero** `= (b)·dt_n` | **1.564e-03 rad** |
| | **RAPPORTO (a)/(c) `= 2π/DT`** | **628.3** |

`dt_n` mediano `= DT = 0.01` perche' **`median(r) = 1.0` esatto per costruzione** (presidio P4:
`ritmo()` normalizza `r` sulla propria mediana).

> **(a) e (c) non sono due modi di dire la stessa cosa: sono due leggi diverse, e quella che gira
> e' (c).** Il fattore `2π/DT` non e' un'approssimazione, e' **un'unita' di misura mancante**.

---

## 3. E DOVE FINISCE: nella MEMORIA, dove il file stesso dice di non metterlo

`_otw` entra in `omega_new` -> `self.omega_s` (`:2313`), che **ogni passo** riceve `+tw/(4π)` e perde
`-omega_s/τ`. All'equilibrio quel solo termine vale **`tw/(4π) · τ/dt_n`**.

| | valore |
|---|---|
| `τ/dt_n` al pavimento (`TAU_A·0.05/DT`, §9) | **250** passi |
| contributo TW all'equilibrio | **3.910e+01** |
| modulo di `omega_s`, mediana misurata, run **ON** | **7.239e+04** |
| modulo di `omega_s`, mediana misurata, run **OFF** | **7.319e+04** |
| **peso in ampiezza** | **0.054 %** |

**E QUI IL CONFRONTO CHE RENDE IL PUNTO NON-TEORICO.** Il commento di `SYNC_SPINORE`
(`:724` e `:2157-2160`) dice, dello stesso blocco:

> *«E' un torque ISTANTANEO: entra nella rotazione (`omega_sync`), MAI in `omega_s` (memoria:
> darebbe accumulo/divergenza).»*

**`TW_SPINORE` fa esattamente cio' che quella riga dichiara divergente.** E, **unico fra i termini
del blocco**, `_otw` **non e' diviso per l'inerzia**: ogni altro contributo entra come
`coppia/inerzia`, questo no.

---

## 4. IL CONTROLLO POSITIVO C'E', MA E' DEBOLE — e va detto

| | OFF | ON |
|---|---|---|
| nodi a 150 passi | **2849** | **3047** |

**I due run DIVERGONO (+6.9 %): il flag non e' codice morto.** Ma le **shape sono diverse**, quindi
il confronto punto-a-punto **non esiste** (§9, la trappola del `max|A-B| = 0.000e+00`): da qui si
legge **CHE** cambia qualcosa, **non di quanto**. Su un sistema caotico una divergenza del 6.9 % in
150 passi **non e' di per se' un effetto fisico** — lo produce anche una perturbazione a `1e-16`
(§9, il caso `N = 3164 -> 3209`).

**Stabilita' col flag ON** (controllo minimo, **non** un sigillo): la norma dello spinore sta a 1
entro **2.220e-16** su 3047 nodi, nessun NaN/inf, `max|x| = 9.348`.

---

## 5. QUELLO CHE QUESTO REFERTO **NON** DICE — e mi ci fermo apposta

**NON dice che `TW_SPINORE` sia trascurabile.** Lo 0.054 % e' un'**ampiezza**, e la domanda vera e'
**direzionale**: il termine TW ha un **asse FISSO** (`sigma_x` o `sigma_z` secondo la chiralita' del
legame) e **persistente**, mentre il resto di `omega` e' un **random walk smorzato** (§9). Un
contributo piccolo ma **coerente in direzione** puo' pesare molto piu' della sua ampiezza — **ed e'
esattamente la ragione per cui Luca lo aveva scelto per primo** («l'unico meccanismo il cui asse non
svanisce all'allineamento»).

> **E' lo stesso errore che ho gia' commesso, in specchio** (§9, `doc/FIX_cache_cs.md`): allora
> avevo detto *«`cs` varia dello 0.023 %, quindi non puo' spostare la pendenza»*, confrontando
> **un'ampiezza** con una domanda di **correlazione**. **Non lo rifaccio al contrario.**

**NON dice nemmeno che la legge vada corretta in un modo piuttosto che in un altro.** Le opzioni
esistono (dividere per `dt_n`, o per l'inerzia, o spostare il termine in `omega_tot` come
`SYNC_SPINORE`), **ma sceglierne una e' una decisione di fisica, e non e' mia.**

---

## 6. PERCHE' NON HO SCRITTO IL SIGILLO

Il §10 ② chiede un sigillo **con controllo positivo**, e §9 chiede che **il criterio si scriva da una
MISURA**. Un sigillo di `TW_SPINORE` dovrebbe verificare *«la torsione ruota il Bloch di `tw/2`»* —
e **quel criterio fallirebbe di un fattore 628**, non per un difetto del codice ma perche' **il
criterio verrebbe dalla descrizione invece che dal codice**. Sarebbe il **quarto** criterio stale in
due giorni (`N3b`, `M1b`/`M3`, `M3c`).

**Un sigillo scritto sulla descrizione di una legge che il codice non implementa non e' un sigillo:
e' un modo elaborato di certificare un malinteso.**

---

## 7. LA DECISIONE — **PRESA: resta spento** (Luca, 2026-09-16)

> ### **STRADA 3. `TW_SPINORE` resta OFF, e il cablaggio non si tocca in questo giro.**

**Cosa significa, detto con precisione:**
- la componente **non e' respinta** — il criterio ① e' plausibile in linea di principio;
- **non e' promossa** — il criterio ② **non e' scrivibile** finche' codice e descrizione divergono;
- **il fronte `W` NON si chiude:** resta aperto come **difetto di cablaggio**, e il suo criterio di
  chiusura e' **una decisione di fisica** (quale delle due leggi e' quella voluta), **non una misura
  in piu'**;
- **il commento nel codice resta FALSO**, e questo e' il rischio vero: non che la componente venga
  dimenticata, ma che **qualcuno la riaccenda credendo di aggiungere `tw/2`**. Per questo il fatto e'
  scritto in **`CLAUDE.md` §9**, che si legge a ogni sessione — **non solo qui**.
  *(Stessa classe di `VERSO_CHI`, muto sotto `CHI_CORE`: un flag che non fa cio' che dichiara e'
  peggio di un flag assente.)*

**E `soliton_simulator.py` NON e' stato toccato**, nemmeno per l'annotazione: **due run video stavano
girando su quel blob** (`video_fisica_completa.mp4` e `-rete.mp4`), e cambiare il file avrebbe rotto
la corrispondenza fra il blob sul disco e quello che ha prodotto gli output (§5-quinquies).
**Il presidio e' andato dove non costa quella proprieta'.**

---

## 7-bis. LE TRE STRADE, per il verbale *(la 3 e' quella scelta)*

1. **Correggere** il cablaggio (e allora e' una **correzione di difetto**, §10: *nessun flag*), poi
   sigillare la legge corretta e valutarne la promozione.
2. **Tenerlo com'e'** e sigillarlo **per quello che fa davvero** — un termine `tw/(4π)` nella memoria
   angolare, ad asse fisso — dichiarando che il commento va riscritto.
3. **Lasciarlo spento** e passare a un altro dei tredici, registrando questo referto.

**Finche' non decide, `TW_SPINORE` resta OFF.** Intanto **`--tw-spinore` e' acceso nel run del video
`video_fisica_completa.mp4`** in corso: come immagine va bene, ma quel video **non e' una misura di
`tw/2`**.
