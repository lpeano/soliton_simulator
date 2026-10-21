# TRIANGOLI, GRADINO 2-BIS: `R1` *(`cs` + `CAMM-FASE-VUOTO`)* SUL TORO TRIANGOLARE

> **Il mandato:** decisione di Luca del `2026-10-21` alle `23:35` *(«prima (a), poi (b)»: questo e' `(a)`)*;
> gradino `2` `bb0ef057`. ### **Una MISURA. NESSUNA CURA.** ### **`leggi.yaml` intatto, `eps 0.5`, sul quadrato
> TUTTO AL BIT.**

**LIVELLO:** `L2`, triangoli.

## 0. LA STELLA POLARE

1. **`A14`:** ### **`cs` e' per nodo** *(`Lambda/(Lambda + Lambda_c)`)*, `CAMM-FASE-VUOTO` e' il punto fisso
   ### **sul nodo**: raggio `0` anche su `6` vicini.
2. **Il gradino:** `(a)` ### **il caso che deve fallire** e' l'isotropia `C6` di `R1` sul quadrato; `(b)` ###
   **`R1` ACCENDE `cs`**: e' la differenza da `R2`; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **No.** `Lambda_c = RAPPORTO * Lambda medio`, ### **`RAPPORTO = 1`
   come `594417f6`.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`c_s` SI'**, ed e' il punto: `cs` acceso.
5. **Emergente o imposto?** ### **Misurato.**

## 1. RAGIONAMENTO PRELIMINARE

- ### **UN BRACCIO SOLO, `SN`** *(il mandato)*. ### **Il perche' la scala non dovrebbe contare neanche con
  `cs`:** ### **`Lambda_c` e' RELATIVO** *(`RAPPORTO * Lambda` medio)*, quindi `cs = Lambda/(Lambda+Lambda_c)`
  ### **vede solo il rapporto**, come `S3`. ### **Non verificato per `CAMM-FASE-VUOTO`** *(i termini di
  `Omega`)*: ### **se la misura desse un segno che la scala conta, lo dico e si misura `SE`.** ### ⚠ **Ma un
  braccio solo NON puo' mostrare che la scala conta:** ### **la verifica e' la lettura dal codice**, non il
  numero.
- **I VALORI DEL QUADRATO** *(dal `jsonl` di `594417f6`, letti prima delle corse)*: ### **il `0.545` e il
  `0.480` del mandato sono lo stimatore degli AUTOVALORI** *(`meta_eig`: `0.5445` a `(pi, pi)`, `0.4798` a
  `(pi, 0)`)*; ### **lo stimatore della NORMA da' `0.5411` a `(pi, pi)` e `0.4779` a `(pi, 0)`**, `k = 0`
  `0.0273`. ### **La banda del quadrato** *(`punto_banda`, norma)* ### **e' `(pi, 0)` stesso, `0.4779`.** ### **Il
  rapporto si fa con lo STESSO stimatore** *(`0.5411`)*, ### **e accanto il `0.545` del mandato.**
- ### ⭐ **LA PREVISIONE, SCRITTA PRIMA DEI NUMERI:** sui quadrati `R1` e' dominato dal picco a `(pi, pi)`
  *(`0.541`)* e dal bordo `(pi, 0)` *(`0.478`)*. ### **Sui triangoli il picco alternato non c'e'** *(gradino
  `2`)*, ### **e in `R2` il bordo era il punto piu' quieto** *(`M` `0.127`, `K` `0.095`)* ### **e il massimo stava
  all'interno, a `0.938` del quadrato.** ### **Credo che il massimo di `R1` sui triangoli valga `~0.45`**
  *(fra `0.41` e `0.48`: il `0.478` del bordo del quadrato ridotto come in `R2`)*, ### **all'INTERNO della
  zona**, ### **e il bordo `M` e `K` sotto il massimo.** ### **Quindi il guadagno rispetto al quadrato: `~17%`
  del massimo** *(da `0.541` a `~0.45`)*.
- **Cosa NON so:** ### **se il bordo dei triangoli in `R1` resta quieto** *(in `R1` il bordo del quadrato e'
  forte: `(pi, 0)` `0.478`)*; ### **quanti giri chiede il punto fisso di `Omega` sui triangoli.**

## 2. LA PROGETTAZIONE: I PASSI, E COSA MI FA FERMARE

- **Lo strumento:** `csv/_triangoli_r1.py`, ### **le funzioni di `csv/_stabilita_triangoli.py` con `cs`
  ACCESO** *(la funzione di Green passa `acceso` a `_stabilita_lineare.passo`, che chiama
  `tick.tick_con_cs`)*; ### **la sequenza di `_stabilita_lineare.braccio_proiettato` con `acceso`, nello
  stesso ordine** *(`lm`, `Lambda_c`, `cs_m`, `accendi_cs`, la scala)*, ### **il tempo proprio `t dtau cs_m`.**
- **`gamma(k)`:** la pendenza della NORMA sulla seconda meta' *(`pend["meta_norm"]`)*. ### **`R1`: `cs` acceso,
  `Lambda_c = 1 * Lambda` medio, lato `32`, `dtau 0.125`, `x 0.1`, base proiettata, `N dtau = 100`, `SN`.**

### I CONTROLLI *(copiati dal mandato)*

- ### **DEVONO RIUSCIRE:**
  1. ### **`R1` di `594417f6` AL BIT sul quadrato del costruttore generale** *(i `10` campi)*. ### **Se no:
     STOP**;
  2. ### **la camminata sola esatta** *(come il gradino `2`: `N * 64` ulp)*;
  3. ### **`P1` e `P3` con `cs` acceso** *(le cache azzerate al bit; nessuna memoria in `mot`, al bit o `<= 64`
     ulp)*;
  4. ### **la base `<= 1e3` ulp**;
  5. ### **la linearita'** `1e-7` contro `1e-6`: `<= 1e-3 * max gamma`;
  6. ### **l'isotropia `C6` di `gamma(k)` sui triangoli**, entro la stessa banda;
  7. ### **`s <= 1` a ogni nodo** *(il cono)*: ### **il massimo di `max(dtau_nodo)/dtau_rif` dopo il tick della
     base, su tutto l'intervallo** *(e il nucleo lo asserisce comunque a ogni tick)*;
  8. ### **il contatore degli avvisi del punto fisso STAMPATO** *(`mot.avvisi_omega`, oltre `100` giri)*, coi
     giri massimi e il fattore massimo.
- ### **DEVE FALLIRE:** ### **l'isotropia `C6` di `R1` sul QUADRATO.**
- ### **COSA MI FA FERMARE:** il controllo `1`; la camminata sola che cresce; `P1`, `P3`; la base; ### **una
  scena fuori dal cono** *(il nucleo alza)*.

### LE LETTURE, FISSATE QUI *(copiate dal mandato)*

- ### **il massimo, dove** *(`centro`, `M`, `K`, `interno`, la mappa del gradino `2`)*, ### **e il rapporto con
  `R1` del quadrato, STESSO stimatore** *(`0.5411`)*, accanto al `0.545` del mandato;
- ### **STABILE** se il massimo `<= 1e-3 * 0.545`;
- ### **IL BORDO** *(`M` e `K`)* ### **accanto a `(pi, 0)` `0.4779` e `(pi, pi)` `0.5411` del quadrato** *(norma;
  il mandato `0.480` e `0.545`)*;
- ### **LA BANDA** *(escluso `centro`, `M`, `K`)* ### **accanto a quella di `R2` sui triangoli** *(`0.3768`)*;
- ### **QUANTO DELL'INSTABILITA' TOTALE I TRIANGOLI TOLGONO:** ### **`1 - max_triangoli / max_quadrato`**,
  stesso stimatore, ### **in `R1` e in `R2`** *(`R2`: `0.3768` contro `0.4018`, dai referti)*.

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_triangoli_r1.py`: commit, poi la corsa.
3. Il referto `doc/referti_l2/triangoli_r1.txt` e `.jsonl`; la voce `[[GRIGLIA-A-TRIANGOLI]]`; la relazione.
4. ### **Poi la coda passa a `(b)`.**
