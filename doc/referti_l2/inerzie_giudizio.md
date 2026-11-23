# [M0149] LE QUATTRO INERZIE (S16) E IL COMPOSTO (S4): LA LETTURA *(i numeri da `doc/referti_l2/inerzie.txt`, `inerzia_suite.py lettura`, d63135de; i derivati da un `python -c` del 2026-11-23, 03:06)* [[PROGETTO-MITOSI]]

> **Le corse:** I2 *(+E, -E, E = 0)*, I4 *(phi congelato k 0.010 e k 0, phi libero k 0.010)*, S4 *(t000 k 0.010 e k 0)*: lanciate 02:08:48-02:08:57, finite 02:25:52-02:26:15, tutte uscita 0. **Lo stato di partenza:** F0 compatto, `tenuta/S1_cima/stato_001500` *(w 7.8)*; I3 dallo stato LARGO *(la caduta di [M0908] partiva dallo stampo)*.

## DUE CORREZIONI MIE, PRIMA DEI NUMERI

- ### **I3: il segno stampato da `inerzia_suite.py` per V3 e' SBAGLIATO** *(errore mio nel codice della lettura, POST-HOC)*: la lettura metteva la forza sempre col verso positivo. **Dalle righe del collegamento:** V3 = la fase (a), un'energia per particella `-e0 (N - 1)`: **la forza va verso `N` piu' ALTO** *(VIA)*: `F = -e0 |dN/dy|` nel verso VERSO-positivo; V2 = `cs = s N`, `d omega/dN = +0.6255 > 0`: **la forza va verso `N` piu' BASSO** *(VERSO)*: `F = +0.6255 |dN/dy|`. **Con i versi giusti: `m_N(V3) = -19.205`, `m_N(V2) = -19.362`** *(il referto stampa `+19.205` per V3: vale questo)*.
- **La carta sez. 2 scriveva le proiezioni `E0, E0/2, 3 E0/2`:** **sono `[1.0, -0.5, 0.5]`** *(`A2` punta a `(-1/2, sqrt 3/2)`; la corsa le ha calcolate dai vettori: il log di I2)*.
- ### **I2: il SEGNO di `m_E` non e' determinato.** Ho scritto `dk/dt = +e w E0` senza verificare il verso dell'accoppiamento minimale *(se `k_cinetico = k - e A`, il segno si rovescia)*: **la grandezza `|m_E|` e' misurata, il segno no.** **Il controllo che lo decide** *(non fatto)*: un `A` uniforme e costante senza `E` sposta il mattone come un calcio di `+e A` o di `-e A`.

## LA TABELLA S16 *(per particella)*

| | l'inerzia | chi spinge | lo stato | il valore | l'incertezza |
|---|---|---|---|---|---|
| I1 | la banda *(il calcio)* | `e^{i k x}`, `k 0.010` | compatto | `k/v` **`-18.133`**; `k/(v - v0)` **`-16.138`** *(v0 `+6.8e-05`, `80` sigma)* | `0.017` |
| I1 | la banda | | largo | **`-19.26`** *(massa_calcio.txt)* | |
| I2 | il campo U | `E` uniforme, `e w E0 = 2.0e-05`/tick | compatto | **`abs(m_E) = 16.614`** *(+E `16.602`, -E `16.626`)*, **il segno non determinato** | `0.038` |
| I3 | il tempo, V3 | la fase (a): `-e0 grad N` | largo | **`-19.205`** | |
| I3 | il tempo, V2 | `cs = s N`: `+(d omega/dN) grad N` | largo | **`-19.362`** | |
| I4 | il vuoto | il calcio con `phi` congelato | compatto | `k/v` **`-18.361`** *(libero `-18.133`)*; `k/(v - v0)` **`-17.487`** *(libero `-16.138`)* | |
| I5 | l'orologio | -- | compatto / largo | `omega/c^2` **`80.46` / `80.53`** *(c_sol)*, `86.71` / `86.79` *(c_banda)*; `Delta(1)/c^2` `142.1` / `153.1` | |

## I CRITERI

- **K1** *(casi noti)*: I2 con `E = 0` ridà la deriva del calcio a `k 0`: **PASSA** *(`+6.818e-05` contro `+6.818e-05`: lo stesso tick, al bit nel numero stampato)*; I4 con `phi` libero ridà I1: **PASSA** *(`-18.133`)*.
- **K2** I2: segni opposti sotto `+E` e `-E` *(`+1.205e-06` a `366` sigma, `-1.203e-06` a `278` sigma)*: **PASSA**.
- **K3** *(entro il `15%`, per grandezza; il segno a parte)*: **I3 contro I1 dello STESSO stato (largo):** V3 `0.997`, V2 `1.005` -- **COINCIDONO** *(entro lo `0.5%`)*, **col segno** *(tutte negative)*. **I2 contro I1 (compatto):** `|m_E|/|k/v|` `0.916`, `|m_E|/|k/(v - v0)|` `1.030` -- **entro il `15%` in grandezza con tutte e due le definizioni di I1**; il segno di I2 non e' determinato *(sopra)*.
- **K4** I4: col `m* = k/v` *(la definizione della carta)* `Delta m*/m* = +0.0126`: **il vuoto NON partecipa** *(< 5%)*; ### **ma con `k/(v - v0)`** *(la deriva tolta, come in I2)* **`+0.0836`: PARTECIPA** -- **il verdetto dipende da come si toglie la deriva propria del mattone compatto: NON robusto**, lo dico.
- **K5** S4: il triangolo t000 *(col tick V0, `chi` tolto; la massa `3044074` = `3.059` mattoni)*: `m*_tri` `k/v` **`-17.494`**, `k/(v - v0)` `-17.739`; contro il mattone compatto `0.965` *(`k/v`)* e `1.099` *(`k/(v - v0)`)*; `M*_tri/(3 M*_mattone)` **`0.984`**: **ADDITIVA** con tutte e due le definizioni *(il mattone del triangolo non e' lo stato compatto di k 1500: dichiarato)*.

## LE PREVISIONI DEL GUARDIANO, CONTRO I NUMERI

- **P1** K1 passa `80%`: **si'**; K2 passa `65%`: **si'**.
- **P2** m_E coincide con I1 entro il `15%` `60%`: **si' in grandezza** *(il segno non determinato)*; **m_N NON coincide con I1 `85%`: SMENTITA** -- **m_N coincide con I1 dello stesso stato entro lo `0.5%`** *(e' la legge della caduta S3, `K/K_th 0.996`, letta come inerzia)*; I5 non si riconcilia con nessuna `75%`: **si'** *(`80` contro `16-19`)*.
- **P3** I4 `|Delta m*/m*| < 5%` `55%`: **si' con `k/v`, no con `k/(v - v0)`**.
- **P4** S4 additiva entro il `20%` `55%`: **si'**.

## LA LETTURA *(mia, POST-HOC)*

- **La banda, il campo e il tempo danno la STESSA inerzia** *(I1, I2 in grandezza, I3), a parita' di stato:* **l'inerzia e la risposta al gradiente di N (per particella) sono la stessa cosa qui** -- **cio' SUGGERISCE** *(non prova: I3 e' una lettura dallo stato largo, una volta sola)* **che Eotvos (S4) non nasca da due inerzie diverse, ma da cio' che fa variare m* con lo stato** *(`-19.26` largo, `-17.03`/`-16.14` compatto: la forma del mattone)*. **Il controllo che lo direbbe:** I3 dallo stato COMPATTO *(la caduta da k 1500 c'e': `5d`, V2 `-5.04` c_sol contro `-4.15` del largo, `+21%`)*.
- **L'orologio (I5) non e' una massa:** `omega/c^2 ~ 80` contro `|m*| ~ 16-19`.

## LA TABELLA DEL GIUDIZIO *(`doc/SAGOMA.md` sez. 4)*

**Non e' una cura:** nessuna forma, nessun vincolo e nessun collegamento cambia; e' una misura. **Le righe toccate sono informazione** *(S16 riempita, S2 e S3 confermate)*; il verdetto CURA / TOPPA / NULLA / DANNO **non si applica.**
