# REPERTO — **`T5` DEL SIGILLO DI `CURA 2` È INVALIDO: DUE RUN NELLO STESSO PROCESSO NON PARTONO DALLO STESSO MONDO**

> **`Z145`.** Difetto **del mio strumento**, non della cura. Blob del simulatore `b881db89`,
> sigillo `a11e3c5`, codice `c04d2b0`, run `391bae9`.
> **Il sigillo ha stampato `5/5 PASS`. Quattro dei cinque valgono. Il quinto no.**

---

## 1. COSA HA STAMPATO, E PERCHÉ SEMBRAVA UN SUCCESSO

```
T1  PASS  il default e' spento
T2  PASS  GATE (AST): i quattro rami stanno SOLO in mitosi()
T3  PASS  i quattro usi TORSIONE sono INTOCCATI
T4  PASS  BYTE-INERTE spento: 206 identici, 0 diversi, 4 non confrontati
T5  PASS  CONTROLLO POSITIVO acceso: 109 campi diversi
```

**`T5` chiedeva `dv > 0`, e `dv = 109`.** Il criterio è soddisfatto. **È soddisfatto per la
ragione sbagliata.**

## 2. IL NUMERO CHE NON TORNA

| run | `n` al passo 120 | archi | durata |
|---|--:|--:|--:|
| **riferimento** `_cura1_corto` *(processo fresco, flag spento)* | **`2660`** | `526 302` | `509.0 s` |
| **`T4` SPENTO** *(1º run del processo del sigillo)* | **`2660`** | `526 302` | `404.5 s` |
| **`T5` ACCESO** *(2º run dello STESSO processo)* | **`901`** | **`59 731`** | **`33.3 s`** |

**E al passo 12 il sistema ha già `n = 2515`** *(`_g4_corto/scena_000012.pkl.gz`)*.

## 3. LA DIMOSTRAZIONE — **`n` NON PUÒ SCENDERE**

Cercato **su tutto il file**, non su una finestra *(`PATTERN_DI_PROVA` standard 9)*:

```
def rimuovi|elimina|annichil|pota|fonde|merge   ->  NESSUNA
self.n -=   |   self.n = self.n -               ->  NESSUNA
np.delete                                       ->  NESSUNA
```

**`MAX_NODI = 4000000` è dichiarato nel codice stesso come «GUARDIA DI MEMORIA, non di
fisica»**, ed è un **tetto**, non una potatura.

> ### ❗ **NEL SIMULATORE NON ESISTE NESSUN MECCANISMO CHE TOLGA NODI. `n` PUÒ SOLO CRESCERE.**
> **Quindi un run che al passo 120 ha `n = 901` NON può essere partito dal mondo che al passo 12
> ne aveva `2515`.** Il secondo run **è partito da un mondo diverso e più piccolo.**

**Non è una congettura sul meccanismo: è un'impossibilità.** Il *perché* il mondo fosse diverso
resta da stabilire *(candidato: stato di modulo mutato dal primo run e non ricostruito dal
secondo, `runpy.run_path` due volte nello stesso processo)* — **e finché non è stabilito, non lo
si scrive come causa.**

## 4. COSA È INVALIDATO E COSA NO

| | stato |
|---|---|
| **`T1`, `T2`, `T3`** | ✅ **VALGONO**: leggono il **sorgente**, non un run |
| **`T4`** | ✅ **VALE, ed è il test più forte**: è il **primo** run del processo, e dà `206` campi **identici** al riferimento girato in un processo **fresco e separato**. **Il processo parte pulito.** Copre anche l'estrazione **senza flag** di `_cs_arco_da_nodo` |
| **`T5`** | ❌ **INVALIDO.** Il `dv = 109` misura **due mondi diversi**, non l'effetto del flag |
| **il controllo positivo di `CURA 2`** | ⚠ **NON ESTABLITO.** Non è noto se la cura faccia qualcosa |

> **È LA FORMA SPECULARE DEL DIFETTO GIÀ CATALOGATO.** Il registro ha già
> *«`max|A−B| = 0.000e+00` può significare **nessun confronto**»*. Questo è il gemello:
> ### **`dv > 0` può significare «due mondi diversi», non «il flag fa qualcosa».**
> **Uno zero letto come identità; un non-zero letto come effetto. Lo stesso errore, ribaltato.**

## 5. ⚠ IL MIO COLLAUDO NON POTEVA PRENDERLO, E VA DETTO PERCHÉ

`P1-sexies` è stato rispettato: **sei casi a risposta nota, due dei quali DEVONO fallire, e
falliscono.** Ma **ho collaudato i CRITERI — le formule — e non il BANCO**: nessuno dei sei
casi chiede *«i due bracci partono dallo stesso mondo?»*.

> **Un collaudo delle formule non collauda l'apparato che le alimenta.**
> **È una voce nuova per `PATTERN_DI_PROVA.md`**, e la propongo, non la promuovo.

## 6. ✅ CIÒ CHE IL SIGILLO HA COMUNQUE PRODOTTO — **il criterio `K`, già risposto, senza un run in più**

Dal run **`T4`**, che è **certificato** *(byte-identico al riferimento)*:

| contatore | valore | su | lettura |
|---|--:|--:|---|
| **`_tum_clip_prob`** | **`0`** | `63 148 047` | **il clip su `prob` NON HA MAI MORSO** |
| **`_tum_clip_rep`** | **`0`** | `63 148 047` | **il clip alto su `rep` NON HA MAI MORSO** |

*(`63 148 047 ≈ 120 × 526 302`: il conto torna con gli archi.)*

> ### ❗ **CONSEGUENZA PER LA CURA: LA SOSTITUZIONE DEL CLIP CON POISSON È FORMALE.**
> Il par.8 punto 1 della scheda ⑨ lo dava come **da misurare**, e la misura dice **zero su
> sessantatré milioni**. **La cura di `:5244` non cambia un numero: cambia la FORMA**, e toglie
> un limite che `A11` classifica come patch. **È corretta e inerte.**
>
> ### ❗ **E PER LA SCELTA `piana` / `tanh` DELLA SCHEDA ⑪: il clip alto su `rep` non morde mai.**
> **⚠ MA IL CONTATORE GUARDA SOLO IL LATO ALTO** *(`−resp > 1`)*. **Il clip a ZERO — il lato
> basso — NON è contato**, e quello morde ogni volta che `resp > 0`. **Dire «il clip non morde»
> sarebbe falso: morde in basso, e quanto non lo so.** → in coda.

## 7. I CONTATORI DEL RUN ACCESO — **si riportano, NON si usano**

`_tum_eulero_gt1 = 0` su `7 167 603`; le tre guardie *(`_r_corrente`, `_cs_nodo_prev`,
`_dt_e_ultimo`)* **`120` invocazioni e ZERO salti ciascuna**.

> **VENGONO DAL RUN INVALIDO.** Le guardie a zero salti sono un **buon segno**, e i criteri
> `C`/`H` li vogliono — **ma su un mondo che non è quello del confronto.** **Si rifanno nel giro
> corto.** *(`9-bis`: un numero porta la sua epoca; questo porta il suo mondo.)*

## 8. LA RIPARAZIONE, PROPOSTA E NON ESEGUITA

**`T5` deve girare in un PROCESSO SEPARATO**, come `T4` di fatto già fa *(è il primo)*.

> **E LA RIPARAZIONE È QUASI GRATIS, perché lo strumento giusto è già previsto dal mandato:**
> **il GIRO CORTO `--cura2-corto` È un processo fresco a un solo braccio**, e il suo termine di
> paragone `_cura1_corto` **è anch'esso un processo fresco a un solo braccio**.
> ### **`_cura1_corto` contro `_cura2_corto` È il controllo positivo fatto bene.**

**NON L'HO LANCIATO.** Il sigillo è il **cancello** del giro corto, e il suo verdetto
*«il giro corto può partire»* poggia su un test che ora so invalido. **Lanciarlo sarebbe
«aggiustare al volo dentro lo stesso passo»**, che il par.5 vieta.
**Reperto, commit, stop. La decisione è di Luca.**
