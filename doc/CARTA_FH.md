# FH ALLA PROVA: EOTVOS, LA TENUTA LUNGA, LA MITOSI *(il mandato di Luca [M0326], 2026-11-23 dopo le `03:20`: «lo facciamo ora»; scritta PRIMA del codice)* [[PROGETTO-MITOSI]]

> **La forma predefinita NON cambia qui:** si misura cio' che manca per decidere. **[M0149] e' FERMO coi suoi referti e non si riapre.**

## 0. Il caso noto *(S1)*

- **Ogni pezzo con FH e lo stesso pezzo con F0 dallo stesso stato e con lo stesso script**; dove il numero di F0 e' gia' registrato *(Eotvos `eta` `0.120` V2, `0.138` V3; la tenuta di oggi)* **si cita e non si rifa'** -- **piu' UNA corsa di controllo** *(la tenuta `x0.8` di F0 con lo script nuovo: deve ridare `omega` di `Q_tenuta_x0.8` entro il `2%`, e per costruzione al bit: K1)*.
- **Come FH entra nelle scene di ieri** *(le righe)*: le scene di `csv/solitone/mattone.scena` mettono `materia_vuoto.pezzi = _screening_forme_s3.pezzi_di("S1")` *(sez. 9 della carta del torneo)*: **lo script nuovo, prima di aprire la scena, fa `MV.scegli(forma)` e sostituisce in memoria `_screening_forme_s3.pezzi_di` con una funzione che rende i `pezzi` del NUCLEO** *(`torneo_tenuta.nucleo()`)*: **cosi' la scena di ieri gira con la forma del nucleo, senza toccare `eotvos.py` ne' `eotvos_v2.py`** *(in memoria, dichiarato; il caso noto S1 lo verifica: a S1 le due S1 sono uguali al bit)*.

## 1. EOTVOS CON FH *(S2, [M0326-Q])*

- **Le righe di [M1446-Q]:** `eotvos.tenuta` *(N = 1, 1000 tick, `omega`)* e `eotvos_v2.caduta` *(V2 e V3 nel gradiente di [M0908], 2000 tick, gli stati ogni 250)*, **le norme `x0.8` e `x1.2`** *(`psi_h x sqrt(scala)` dallo stampo)*; **`eta = 2 (a1 - a2)/(a1 + a2)`** con l'incertezza *(`eotvos_v2.a_caduta` e il conto di `eotvos_v2.lettura`)*.
- ### ⚠ **Le corse sono SEI, non dieci:** **due tenute e quattro cadute** *(`x0.8`, `x1.2` per V2 e V3)*: **`eta` vuole solo le cadute**; gli orologi e i calci di [M1446-Q] *(otto e due)* servivano alla PREVISIONE di `eta`, che qui non e' chiesta -- lo dico, e se Luca le vuole sono otto corse in piu'.
- **K2:** MIGLIORA se `eta_FH < eta_F0` di almeno `3 sigma`; PEGGIORA se maggiore di `3 sigma`; LASCIA altrimenti.

## 2. LA TENUTA LUNGA *(S3, [M0326-T])*

- **FH e F0 a `N = 1` per `10000` tick dallo stato a `k 1500`** *(`fondo_suite_v2.carica`, il campo dal file, i `pezzi` del nucleo)*: gli stati ogni `250` *(col campo)*, **`omega` a ogni tick** *(`-arg vdot`)*; **la ripresa P8:** se la cartella ha gia' degli stati, la corsa riparte dall'ultimo *(lo stato, il campo, la serie di `omega` fino a quel `k`)*. **La lettura:** `w`, il picco, i pezzi ogni `250`; **K3:** un pezzo e `w` entro `+-30%` della media di `w` dopo `k 1500` *(della corsa)*; **il respiro:** il periodo dal massimo dello spettro di `w(k)` *(tolta la media)*, l'ampiezza `(max - min)/2`. **Il confronto di F0 a `20000` di `chi_mattone_v2`** *(con `chi`)*: **solo qualitativo**, dichiarato.

## 3. LA MITOSI CON FH *(S4, [M0326-N])* -- ### ⚠ **NON SI PUO' FARE SENZA UNA DECISIONE**

- **Dalle righe:** MITOSI-v2 e' `doc/referti_l2/mitosi_rami_v2.py riparti` **sul ramo `mitosi`** *(`wt_mitosi`; il registro di quel ramo, la voce `mitosi-ramo-MITOSI-v2`)*. **Il suo nucleo NON ha la forma FH:** FH esiste solo nel nucleo di `lapse-u` *(90813637)*. **Far girare la mitosi con FH vuol dire portare il codice della mitosi in `lapse-u`, o il nucleo di `lapse-u` nel ramo `mitosi`: e' un merge** *(R-NAVI: nessun merge senza un mandato che lo nomini)*. **La corsa non si scrive e non si accoda:** FERMO su S4, la domanda a Luca.

## 4. IL CASO NOTO DELLA COPPIA *(S5, [M0326-K])*

- **Dalle righe:** il referto di [M1310-P] *(`pound_rebka_GU.txt`)* misura gli OROLOGI delle coppie, **non contiene una regola di riscalatura di `Delta a`**; il numero registrato della coppia F0 in fase e' **`a = -1.2603e-06` a `d 39`** *(F-off, G+U, dallo stampo: `gravita_due_corpi.txt`)*. **La corsa:** la stessa scena *(`gravita_fase.prepara` con `D = 35` in memoria, le fasi `0, 0`)*, il tick V0 *(G+U, `N = 1`)*, `2000` tick, `D(k)` ogni `10`, `a` dal fit di `gravita_due_corpi_misure.fit`. **I confronti:** con il `-1.0e-06 +- 15%` del mandato; **con `-1.2603e-06 x 39/35 = -1.404e-06`** *(la legge `1/d` del 2D: mia, dichiarata)*; con `-1.387e-06` dallo stato compatto *(M0149)*.

## 5. IL SEGNO DI m_E *(S6, [M0326-S])*

- **Le righe dell'accoppiamento** *(`primo_ordine/flussi_parziali._hop_psi_mezzo`)*: sull'arco `a`, il lato `1` nuovo e' `alpha v1 + beta (U v0)` e il lato `0` nuovo `alpha v0 + beta (U^dag v1)`, con `U = e^{i e A}` *(`_u1_prototipo.scrivi_U`)*: **l'ampiezza che passa dal capo `0` al capo `1` prende `e^{+i e A}`.** **Per un'onda `e^{i k x}` che va da `0` a `1` questo equivale a `k_cin = k - e A`** *(se il capo `0` del motore e' `ii` del campo: lo script lo controlla)*: **un `A` uniforme e costante deve spostare il mattone come un calcio di `-e A`**, e **un `E` che fa crescere `A` da' `dk_cin/dt = -e w E0`: `m_E = -16.61`, negativo, coerente con I1** *(la previsione dalle righe)*.
- **Il controllo:** F0 da `k 1500`, **`A <- A + A0 (a . x)`** con `e A0 = +0.010` *(lo stesso `k` del calcio)*, `U` riscritto, nessun `E`; `200` tick; `v` dal fit lineare su `k 50 ... 200` meno la deriva `v0` del calcio a `k 0`; **il segno di `v - v0` contro quello del calcio `k = +0.010`** *(`v - v0 = -6.2e-04`)*: **stesso segno = `k_cin = k + e A`** *(m_E positivo)*; **segno opposto = `k_cin = k - e A`** *(m_E negativo)*.

## 6. I CRITERI E LE PREVISIONI *(copiati dal mandato)*

- **K1** S5 entro il `15%` di `-1.0e-6`; F0 negli script nuovi ridà i numeri registrati entro il `2%`; la norma a `1e-12` in tutte. **K2** Eotvos come sopra. **K3** la tenuta lunga come sopra. **K4** la mitosi *(FERMO)*. **K5** il segno di m_E deciso dalle righe e dal controllo; negativo = coerente con I1. **K6** la tabella del giudizio di FH: CURA se nessuna riga PEGGIORA e almeno una MIGLIORA; TOPPA se una PEGGIORA; le righe NON MISURATE elencate.
- **LE PREVISIONI DEL GUARDIANO:** **P1** K1 passa `80%`. **P2** Eotvos FH: `eta` fra `0.08` e `0.18` *(LASCIA)* `55%`; MIGLIORA `25%`; PEGGIORA `20%`. **P3** la tenuta lunga: FH regge `10000` tick `70%`; respira con periodo diverso da F0 `60%`, piu' corto `55%`. **P4** la mitosi FH: nasce `65%`; sugli assi del favo `75%`; Theta max piu' piccolo `50%`. **P5** il segno di m_E negativo `80%`. **P6** il giudizio di FH: CURA `40%`, TOPPA `35%`, righe NON MISURATE `100%`.
- **L'ordine in coda** *(S7)*: priorita' `0`: S5, S6, le tenute di Eotvos *(FH x0.8, x1.2, e il controllo F0 x0.8)*, le quattro cadute FH; priorita' `1`: la tenuta lunga FH, poi F0. **La mitosi: no** *(sez. 3)*.

## 7. LA TABELLA DEL GIUDIZIO DI FH *(vuota: si riempie coi referti)*

| riga | F0 | FH | giudizio |
|---|---|---|---|
| S1-S16 | | | **riempita in `doc/referti_l2/FH_giudizio.md`**: S4 PEGGIORA *(`eta` V2 `0.227`, V3 `0.303`, `3.9` sigma)*, S5 MIGLIORA, S1 S2 S15 LASCIA, S13 NON MISURATO per decisione: **FH = TOPPA** |

- ### **S4, LA DECISIONE DI LUCA** *(2026-11-23 dopo le `03:45`)*: **la mitosi con FH NON ora; il merge `lapse-u` -> `mitosi` con un mandato a se', di giorno, a corse ferme** *(MITOSI-v2 non si tocca)*. **Si va avanti con Eotvos, la coppia a `d 36`, le tenute lunghe.** Nella tabella del giudizio di FH la riga S13 *(le nascite)* resta **NON MISURATO** con questo motivo.

## 8. DUE ERRORI DEL GUARDIANO *(il mandato [M0528], 2026-11-23)*

- **n.235:** il riferimento `-1.0e-06` della coppia *(sez. 4 e 6)* era **di un altro stato** *(`coppia_GU_L162`, il mattone cotto su L 162)*; **il riferimento giusto a parita' di stato e' F-off o lo stato compatto riscalati per `1/d`** *(`1.021` / `1.034`, `doc/referti_l2/coppia_caso_noto.txt`)*.
- **n.236:** **il criterio K3 della tenuta lunga** *(sez. 2)* **misurava il respiro** *(`w` `+-50%`, anche per F0)* **e non lo scioglimento** *(`doc/referti_l2/tenuta_lunga_FH.txt`)*.
