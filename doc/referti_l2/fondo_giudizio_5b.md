# [M2351] 5a-bis E 5b: IL CONTROLLO NEGATIVO DEL FONDO E IL CALCIO -- LA LETTURA E LA TABELLA DEL GIUDIZIO *(i numeri da `doc/referti_l2/fondo_calcio.txt`, `torneo_kt_v2_Z.txt`, `torneo_tenuta_v2_Z.txt`; i derivati da un `python -c` del 2026-11-23, 00:38)* [[PROGETTO-MITOSI]]

## 5a-bis [M2351-Z]: IL CONTROLLO NEGATIVO -- ### **FALLISCE**

- **L0 con la stessa semina `proiezione_Gamma` REGGE come l'oggetto a `lambda = -1`:** `w(3000)/w(1500)` **`1.031`** contro `0.998` *(il DEVE: NON reggere, o `> 1.3`)*; `w` `11.6-14.1` da k 750 a 3000 *(L-1 da k 750: `11.27-14.12`)*, un pezzo da k 750, il picco `816-882` *(L-1: `818-887`)*. **Le due serie sono quasi uguali.**
- **Quindi, come la carta dice: l'oggetto di (a) NON e' un solitone, e' la banda piatta che non lascia muovere niente;** la tenuta di (a) non dice niente sulla non linearita'.
- **`omega`:** L0 `-0.4349456`, costante a `1e-8` *(nessuna non linearita': uno stato stazionario lineare)*, **IN BANDA**, `+0.0477` sopra il fondo piatto `-0.48268` *(la proiezione nodo per nodo sul sottospazio a Gamma non e' uno stato di Bloch della sola banda piatta: porta anche altri `k` e altre bande)*; L-1 `-0.5994483`: **lo spostamento della non linearita' `lambda = -1` e' `-0.1645`** *(F0 alla cima: `+0.1492` sopra `e0`)*.
- **La previsione del guardiano** *(il rapporto fra `1.1` e `1.5`, `55%`)*: **smentita** *(`1.031`)*.

## 5b [M2351-M]: IL CALCIO -- ### **IL CASO NOTO FALLISCE, E m* DEL FONDO NON E' COERENTE: FERMO** *(il mandato: FERMO dopo 5b se m* non e' misurabile)*

- **Il caso noto, F0 da `k 1500`:** `m* = k/v` `-18.133` *(asse 1)*, `-15.925` *(asse 2)*, la media **`-17.029`**, contro `-19.26` entro il `2%`: **lo scarto `-11.6%` -- FALLISCE.** E **F0 a `k = 0` non sta fermo:** `v0 = +6.82e-05 +- 8.5e-07` *(`80` sigma)*; con `v - v0`: `-16.14`, `-14.37`. **L'oggetto dopo il transitorio** *(contratto, `w 7.8` contro `15.5`)* **non ha la massa dello stampo**, e deriva da solo: **il caso noto, come lo chiedeva il mandato, non si puo' ridare da `k 1500`.**
- **Il fondo:** `v0 = -8.61e-05 +- 4.3e-06` *(deriva anche lui, `20` sigma)*; asse 1 `v - v0 = -3.35e-05` *(`5.9` sigma)*, asse 2 `+2.28e-04` *(`37` sigma)*: **sopra il rumore per il criterio scritto, ma col SEGNO OPPOSTO sui due assi** *(`k/v`: `-83.6` e `+70.4`; `k/(v - v0)`: `-299` e `+44`)*. **Una massa che cambia segno con la direzione non e' una massa:** **m* del fondo NON e' misurabile in modo coerente.** Con il controllo L0 *(la banda piatta)* questo e' cio' che ci si aspetta: un pacchetto della banda piatta risponde al calcio con una deriva che dipende da come e' fatto, non con `v = k/m*`.
- **Le previsioni del guardiano:** m* POSITIVA `75%`: **ne' si' ne' no** *(i due assi discordano)*; `|m*| > 50` `60%`: `|k/v|` `83.6` e `70.4` *(si')*, `|k/(v - v0)|` `299` e `44` *(uno no)* -- **non giudicabile**.

## LA TABELLA DEL GIUDIZIO *(`doc/SAGOMA.md` sez. 4; il mattone del fondo contro F0)*

| riga | prima *(F0)* | dopo *(il fondo, L-1 per proiezione)* | giudizio |
|---|---|---|---|
| S1 | `omega 0.626` nel gap sopra, m* `-19.26` | `omega -0.599` sotto il fondo; **ma il controllo L0 tiene uguale**: la tenuta e' la banda piatta; m* non coerente | **NON MISURATO** *(non c'e' un solitone da giudicare)* |
| S2-S15 | | nessuna misura valida *(5c-5f non partono: FERMO)* | NON MISURATO |
| M1-M5 | | | NON MISURATO |

**IL VERDETTO:** **non determinabile** -- l'oggetto del fondo non e' un solitone *(5a-bis)*, e il calcio non da' una massa.
