# REFERTO — **Non è una Y. Il modo dominante è il DIPOLO, e l'`A_3 = 0.97` sono le tre masse**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** — nessuna cura, **nessun run nuovo**
**Dati:** i sei `.pkl` del run a **tre masse** già esistenti · **Sonda:** `_forma_Y.py`
**Letture fissate PRIMA:** `4cf1817` · **Correzione della soglia, committata:** *(vedi §2)*

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): **ramo NON CERTIFICATO, e ogni
> numero lo eredita.** `--chi-basc` attivo. **UN SEME. NESSUN VERDETTO DI FISICA, NESSUNA
> IDENTIFICAZIONE.**
> **L'osservazione «in mezzo forma una Y» è VISIVA: qui è stata messa alla prova, non confermata.**

---

## 0. IL VERDETTO CONTRO LE CINQUE LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| tre picchi, `A_3` sopra il nullo, **nella regione interna** → struttura topologica | **NO** |
| istogramma piatto, `A_3 ≈ nullo` → **disco** | **NO — e nemmeno questo** |
| **`A_3` grande SOLO includendo l'anello → artefatto delle tre masse** | **✓ È QUESTA** |
| tre picchi che si formano e poi si dissolvono → transitorio | **NO** |
| ⚠ *(mia)* la forma cambia con la soglia → non è un fatto | **i valori cambiano, l'ORDINE dei modi no** |

> **Non è una Y e non è un disco: nella regione interna il modo dominante è `A_1`, il DIPOLO.**
> **Un singolo addensamento spostato dal centro, non tre bracci.**

---

## 1. LA PLANARITÀ È VERIFICATA — proiettare è lecito

```
frame        10      115     190     270     375     400
|z| / r     0.053   0.048   0.055   0.060   0.075   0.077
```

**La scena è piatta al 5-8 %: la proiezione sul piano non è un'assunzione nascosta.**

## 2. ⚠ LA MIA PRIMA SOGLIA ERA SBAGLIATA, e l'ho trovata perché il suo esito era assurdo

Avevo derivato la soglia **per analogia** con `lambda_vuoto = mean(|psi|²)`, l'energia del vuoto che
il codice usa già (`:486-494`), applicandola a `rho_spin`. **L'analogia non regge:**

```
rho_spin al frame 400:   MEDIA 1.4432e+01     MEDIANA 6.4175e-03     ->  RAPPORTO 2249
```

**La media di `rho_spin` NON è il livello di vuoto: è una statistica della CODA.** Selezionava
**1479 nodi, tutti a `r ≈ 7.7`** *(top-200: raggio `p05/med/p95 = 6.88 / 7.68 / 8.67`)* — **l'anello.**
**E dava «nodi interni densi = 0» a ogni istante: non era un fatto sul sistema, era la soglia.**

**Controprova:** con soglia sulla **mediana**, i nodi interni selezionati sono **623 su 811** al
frame 400, con `rho_spin` mediana **`5.56e-02`** = **8.7 volte** la mediana globale. **La regione
interna densa ESISTE: era la soglia a non vederla.**

> **È P1 applicato a una soglia: un'analogia va verificata sulla DISTRIBUZIONE che seleziona, non
> sulla forma della formula.** *(La media resta stampata nell'output come **controesempio
> dichiarato**, per far vedere il difetto invece di nasconderlo.)*

## 3. `A_3 = 0.97` — **ed è l'anello, non una Y**

```
soglia 10x la mediana        A_1      A_2      A_3      A_6    | NULLO    contrasto
frame 400  TUTTI            0.0756   0.2169   0.9652   0.8744  | 0.0292     8.01
frame 400  SOLO INTERNI     0.4001   0.3242   0.2310   0.1358  | 0.1198     3.77
frame 375  SOLO INTERNI     0.2200   0.5745   0.5330   0.1392  | 0.3025     6.76
```

- **Con l'anello: `A_3 = 0.965` contro un nullo di `0.029` — trentatré volte.** **Ma sono le tre
  masse seminate, che stanno a `0°/120°/240°` per costruzione.**
- **Nella sola regione interna: `A_3 = 0.231` contro un nullo di `0.120` — meno di DUE volte**,
  **mentre `A_1 = 0.400` è 3.3 volte il nullo.**

> **Il modo a tre non è il dominante dentro: è il DIPOLO.** **La terza lettura del mandato — «`A_3`
> grande solo includendo l'anello» — è quella che scatta.**

## 4. ⚠ L'ISTOGRAMMA LO MOSTRA DIRETTAMENTE: **un picco, non tre**

Regione interna, frame 400, 370 nodi, pesato su `rho_spin` *(angoli delle masse: `0° / 120° / 240°`)*:

```
  +7.5   1.802  ####################################
 +22.5   1.810  ####################################
 +37.5   1.610  ################################
 +52.5   3.254  #################################################################
 +67.5   3.998  ######################################################################
 +82.5   1.134  ######################
 +97.5   0.577  ###########
…  (il resto fra 0.23 e 0.86)      +172.5  1.352  ###########################
```

> **UN lobo dominante a `+52.5°/+67.5°`, con un rialzo secondario a `+172.5°`.**
> **Il picco NON è su una massa: è FRA due masse (`0°` e `120°`).**
> **Tre bracci a `0/120/240` non ci sono.**

## 5. Robustezza alla soglia — **i valori cambiano, l'ORDINE dei modi no**

```
regione INTERNA, frame 400     A_1      A_3      NULLO    N_eff
soglia 10x mediana            0.4001   0.2310   0.1198    69.6
soglia 100x mediana           0.6106   0.4374   0.2165    21.3
```

**`A_1 > A_3` in entrambe.** **Ma la statistica interna è DEBOLE**: `N_eff` scende a **21** alla
soglia più stretta, e lì il nullo è **`0.22`**, quindi `A_3 = 0.44` è **due volte il nullo**.
**Con undici nodi efficaci al frame 375 (`N_eff = 10.9`, nullo `0.30`) NON si misura nulla, e infatti
non lo leggo.**

## 6. E la regione interna densa **compare tardi**

```
nodi interni sopra soglia (10x mediana):  0, 0, 0, 0, 18, 370   ai frame 10/115/190/270/375/400
```

**Prima del frame 375 non c'è nessuna regione densa interna da misurare.** **Coerente con `Z49`**
*(`rho_spin` interna esplode solo alla fine)*. **Quindi la forma interna è un fenomeno TARDIVO**, e
tutto ciò che si può dire su di essa riguarda **gli ultimi 150 frame**.

---

## 7. COSA QUESTO **NON** DICE

- **NON dice che il video sia sbagliato.** Dice che **la firma a tre bracci non è misurabile nella
  regione interna con questa definizione di «densa»**, e che **`A_3 = 0.97` è spiegato dalle tre
  masse seminate.** **Una forma vista a schermo può avere una firma diversa da quella che ho
  cercato** — e il modo dominante che ho trovato, **il dipolo**, è comunque **una struttura
  anisotropa**, non un disco.
- **NON è un verdetto sulla predizione di Luca**, che riguarda il **CICLO** e si decide col run a due
  masse — **in corso.** **Questa misura toglie UN meccanismo candidato (la Y topologica), non la
  predizione.**
- **NESSUNA IDENTIFICAZIONE.** *(La Y a 120° è la soluzione di Fermat-Steiner e compare in sistemi
  molto diversi: era scritto nel task history PRIMA, proprio perché se fosse uscita non sarebbe stata
  una spiegazione.)*
- **Il controllo geometrico** (raggio di girazione, autovalori) **è riportato nell'output ma NON
  discrimina**: un disco e una Y simmetrica danno entrambi `λ1 ≈ λ2`. **Dichiarato come controllo.**

## 8. I LIMITI

**Un seme, una scena, `--tau-luce` non certificato.** **La statistica interna è debole** (`N_eff`
fra `11` e `70`). **Sei istanti, e solo due hanno una regione interna densa.** **La stessa misura
andrà sul run a DUE masse quando chiude**, e il confronto è la parte che manca.
