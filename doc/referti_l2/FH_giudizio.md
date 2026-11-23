# [M0326] FH ALLA PROVA: EOTVOS, LA COPPIA A d 36, LA TENUTA LUNGA -- LA LETTURA E LA TABELLA DEL GIUDIZIO *(i numeri da `eotvos_FH.txt`, `coppia_caso_noto.txt`, `tenuta_lunga_FH.txt`, `segno_mE.txt`; i rapporti da un `python -c` del 2026-11-23, 05:10 da `date`)* [[PROGETTO-MITOSI]]

> **Le corse:** le tenute e le cadute di Eotvos 03:36:52-04:08:00; la coppia a d 36 03:54:14-04:16:19; le tenute lunghe 03:54:16-05:07:34; tutte uscita 0. **La forma predefinita NON cambia qui:** la decisione e' di Luca.

## I CASI NOTI *(K1)*

- **F0 `x0.8` con lo script nuovo:** `omega 0.6264217267` contro `0.6264217267` della tenuta di ieri: **AL BIT, PASSA.** La norma costante a 10 cifre in tutte le corse.
- **La coppia F0 in fase dallo stampo a `d 36`:** `a = -1.3940e-06 +- 1.1e-08`. **Contro il `-1.0e-06` del mandato, riscalato `x 35/36`: il rapporto `1.434` -- ### K1 S5 FALLISCE come scritto.** **Contro i numeri REGISTRATI:** F-off `-1.2603e-06` a d 39 riscalato `x 39/36`: `1.021`; lo stato compatto `-1.3867e-06` a d 35 *(M0149)* riscalato: `1.034`. **La mia lettura (POST-HOC):** la coppia ridà le due misure registrate entro il `3.4%` con la legge `1/d`; **il `-1.0e-06` del mandato e' (lo leggo cosi', cercato DOPO la corsa) `coppia_GU_L162`** *(`doc/referti_l2/scatola5_u.txt`: `d0 35.06`, `d'' -1.010e-06`)*: **la coppia G+U del mattone COTTO su `L 162`** *(`csv/solitone/mattone_coppia_L162.py`, il francobollo `L162_MGU_03000`)*, **un altro stato di partenza** *(lo stampo qui)*: **lo stato conta, come per m*** -- il confronto del mandato e quello della carta non erano lo stesso oggetto, **errore mio di non averlo cercato prima di scrivere la carta.** **Il fallimento resta scritto.**

## EOTVOS CON FH *(S4, K2)*

| | F0 *(M1446-Q)* | FH | la differenza |
|---|---|---|---|
| `eta` V2 | `0.120 +- 0.012` | **`0.2265 +- 0.0242`** | `+0.1065`, **`3.9` sigma** |
| `eta` V3 | `0.138 +- 0.014` | **`0.3025 +- 0.0403`** | `+0.1645`, **`3.9` sigma** |

- **K2: PEGGIORA** con tutti e due i collegamenti *(soglia `3` sigma)*: **con FH le due norme cadono PIU' diversamente che con F0** *(V2: `a -7.12e-06` a `x0.8`, `-5.67e-06` a `x1.2`)*.
- ### ⚠ **Il confronto e' con numeri di F0 CITATI, non rifatti** *(la carta sez. 0)*; **lo stesso script e la stessa scena sono garantiti dal controllo al bit della tenuta F0 `x0.8`**, non dalle cadute di F0.

## LA TENUTA LUNGA *(S3 della carta, K3; la riga S1 della sagoma)*

| | F0 | FH |
|---|---|---|
| la media di `w` *(10000 tick dopo k 1500)* | `10.687` | `9.573` *(`0.896`)* |
| `w` min / max | `6.26` / `16.42` *(`-41.5%` / `+53.6%`)* | `4.84` / `15.73` *(`-49.4%` / `+64.3%`)* |
| i pezzi | `1` sempre | `1` sempre |
| K3 *(`+-30%`)* | **NON REGGE** | **NON REGGE** |
| il respiro: il periodo / l'ampiezza | `5125` tick / `5.08` | `5125` tick / `5.44` *(`1.071`)* |
| `omega` *(la media)* | `0.6254411` | `0.6242315` |

- **K3 fallisce per TUTTE E DUE**, F0 compreso: **il mattone a un pezzo RESPIRA** *(`w` va da ~6 a ~16 e torna, due volte in 10000 tick)*; **K3 come scritto misura il respiro, non lo scioglimento** -- nessuno dei due si divide ne' si scioglie.
- ### ⚠ **Il periodo e' lo STESSO BIN dello spettro:** `41` campioni su `10250` tick, la risoluzione e' `~1/10000`: **`5125` e' il secondo bin** *(due cicli)*; **«stesso periodo» vuol dire solo «entro un bin»**, lo dico.

## LE PREVISIONI DEL GUARDIANO, CONTRO I NUMERI

- **P1** K1 passa `80%`: **la tenuta al bit si'; la coppia contro il mandato NO** *(contro i numeri registrati si')*.
- **P2** Eotvos FH LASCIA `55%`, MIGLIORA `25%`, **PEGGIORA `20%`: e' uscito PEGGIORA.**
- **P3** FH regge 10000 tick `70%`: **NO per K3** *(ma nemmeno F0; un pezzo sempre)*; respira con periodo diverso `60%`: **NO** *(stesso bin)*.
- **P4** la mitosi: **non fatta** *(la decisione di Luca, S4)*. **P5** m_E negativo `80%`: **si'** *(`-16.61`)*.
- **P6** il giudizio: CURA `40%`, **TOPPA `35%`: e' uscito TOPPA**; righe NON MISURATE `100%`: **si'**.

## LA TABELLA DEL GIUDIZIO DI FH CONTRO F0 *(`doc/SAGOMA.md` sez. 4; con le righe di [M0149], `torneo_FH_FT_giudizio.md`)*

| riga | F0 | FH | giudizio |
|---|---|---|---|
| S1 | gap sopra, m* `-16.1`; respira *(`w` `6-16`, periodo `5125`)* | gap sopra, m* `-14.7`; respira *(`5-16`, stesso bin, ampiezza `x1.07`)* | LASCIA |
| S2 | R_E `1.19` | `1.29` | LASCIA *(«probabile coincidenza»)* |
| S3 | la legge della caduta | non misurata per FH | NON MISURATO |
| **S4** | Eotvos `eta` V2 `0.120`, V3 `0.138` | **`0.227`, `0.303`** *(`3.9` sigma)* | **PEGGIORA** |
| **S5** | `abs(A/B) 1.22` | **`0.63`**, attrae anche in antifase | **MIGLIORA** |
| S6 | V2 VIA, l'orologio non misurato | VIA | NON MISURATO *(l'orologio no)* |
| S7-S12 | | | NON MISURATO |
| S13 | le nascite | -- | **NON MISURATO: la decisione di Luca** *(la mitosi con FH non ora; il merge con un mandato a se')* |
| S14 | | | NON MISURATO |
| S15 | la caduta V2 respinge *(`-5.04`)* | respinge *(`-5.66`)* | LASCIA |
| S16 | I1 `-16.1`, `m_E -16.61` | I1 `-14.7`; `m_E` non misurato per FH | NON MISURATO *(solo I1)* |

**IL VERDETTO (K6): FH = TOPPA** *(S5 MIGLIORA, S4 PEGGIORA)*. **La cura provvisoria di [M0149] non regge alla riga S4:** FH avvicina la coppia nel verso giusto *(D2 universale)* ma **rompe di piu' l'equivalenza delle norme** -- **la prova piu' dura per una teoria a spinta** *(`doc/IPOTESI_gravita_a_spinta.md`, prova ③)*. **Le righe NON MISURATE:** S3, S6-S14 *(S13 per decisione)*, S16 per FH. **La forma predefinita resta F0: la decisione e' di Luca.**
