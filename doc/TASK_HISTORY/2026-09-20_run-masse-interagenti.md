# TASK HISTORY — il run nuovo: masse che si parlano. Il pilota decide `sep`

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `c7fc3ec` · **blob** `775ceab7`
(sha1 dei byte grezzi verificato) · albero **pulito** · nessun processo in esecuzione.

> **Il pilota e' BLOCCANTE. Nessuna cura, nessuna promozione, nessun cambio di default.**
> **Nessun verdetto di fisica.**

---

## 1. ⚠ UNA PREMESSA DEL MANDATO NON REGGE — **`sep` NON e' la distanza fra le masse**

**Dal codice** (`_semina_n_masse`): le masse stanno su un **cerchio di raggio `sep`**,
`centro = (sep*cos(2*pi*k/nm), sep*sin(2*pi*k/nm), 0)`. **Con `nm = 3` la distanza fra due masse e'
`sep*sqrt(3)`, non `sep`.**

**E l'ho MISURATO dai dati** *(snapshot al passo 6, i centri e i raggi delle quattro componenti)*:

```
comp 0   n=900   centro [ -0.03  -0.00  -0.02 ]   raggio p95 = 3.944   rmax = 4.074
comp 1   n=497   centro [  8.01  -0.01   0.03 ]   raggio p95 = 0.691   rmax = 0.722
comp 2   n=497   centro [ -4.00   6.93  -0.01 ]   raggio p95 = 0.694   rmax = 0.735
comp 3   n=497   centro [ -3.97  -6.91   0.02 ]   raggio p95 = 0.692   rmax = 0.718

distanze fra i CENTRI            fra i BORDI
  massa - massa   13.82 - 13.87     12.44
  massa - vuoto    7.94 -  8.04      3.31 - 3.41
```

> **Il mandato calcola i bordi come `sep - 1.4 = 6.6`. Il valore vero e' `12.44`: il doppio.**
> **Non erano tre volte troppo lontane: erano CINQUE volte troppo lontane** *(12.44 contro un `rc`
> che parte da ~2.4)*. **Il raggio nominale `0.7` invece e' confermato: `rmax` misurato 0.72.**

**Il conto corretto, e sostituisce quello del mandato:**

```
distanza fra i bordi  =  sep*sqrt(3) - 2r  =  1.7321*sep - 1.4
non compenetrarsi     ->  sep > 2r/sqrt(3)      =  0.808
interagire            ->  sep < (rc + 1.4)/sqrt(3)
                          con rc = 2.4  ->  sep < 2.194
                          con rc = 0.36 (pavimento)  ->  sep < 1.016
```

**`sep = 1.8`, il candidato del mandato, da' bordi a `1.72`** — sotto `rc = 2.4`, **sopra il
pavimento `0.36`**. **Quindi e' un candidato ragionevole, ma il suo esito dipende dal `rc` VERO, che
va misurato.** *(Il mandato lo diceva: «il valore vero va MISURATO».)*

### ⚠ E UNA CONSEGUENZA CHE IL MANDATO NON POTEVA VEDERE, perche' nasce dal raggio del vuoto
**Il vuoto e' una sfera di raggio ~4 centrata nell'origine.** Con `sep = 1.8` **le tre masse
finiscono DENTRO quella sfera.** Quindi «componenti < 4» potrebbe verificarsi **attraverso il
vuoto**, senza che due masse si tocchino mai direttamente.

> **Sono due fatti diversi e il pilota li deve separare:**
> **archi massa-massa DIRETTI** contro **archi massa-vuoto**. **Un solo numero non distingue
> «le masse si parlano» da «le masse parlano col vuoto, che parla con tutti».**

## 2. RAGIONAMENTO PRELIMINARE — cosa credo prima di misurare

`rc = 3*median(lambda_nodi())`, e **la mediana e' presa su TUTTI i nodi, vuoto compreso**. Con il
vuoto che e' il 38 % dei nodi alla semina, la mediana e' tirata dal vuoto, non dalle masse.
**Mi aspetto `rc` piu' vicino al valore alto (~2.4) all'inizio, e in calo col maturare** — perche'
`lambda_nodi` scende quando `rho` sale, fino al pavimento `0.15*LAM`.

**Cosa NON so:** se `rc` cali abbastanza in fretta da **riseparare** le componenti dopo averle
unite. **Sarebbe la quarta lettura del mandato, e sarebbe un fenomeno, non un errore di setup.**

## 3. IL PILOTA — cosa misura, e cosa decide

**Uno script a parte** *(`csv/_test_fork/_pilota_sep.py`)*, **committato prima di girarlo**.
**Non tocca ne' il simulatore ne' il driver.** Semina la scena a un `sep` dato e fa **200-300
passi**, misurando a piu' istanti:

1. **`median(lambda_nodi())` e quindi `rc` VERO**, e **la sua traiettoria**;
2. **il numero di COMPONENTI CONNESSE** e le taglie;
3. **gli ARCHI FRA COMPONENTI DIVERSE**, e **separatamente**: **massa-massa** contro
   **massa-vuoto** *(la distinzione del §1)*;
4. **la DURATA per 100 passi** e **la dimensione del primo snapshot compresso**;
5. **`n`**, che decide il costo di tutto il resto.

**Si prova `sep = 1.8`**, e in caso si scende. **Ogni valore provato si riporta con la sua misura.**

### LE LETTURE, fissate PRIMA
| # | esito | conclusione |
|---|---|---|
| **A** | componenti **< 4** e archi fra componenti **> 0** | **si procede**, e si dichiara **per quale via**: massa-massa o via vuoto |
| **B** | componenti **= 4** | `sep` ancora troppo grande: **si riprova piu' stretto** e si riporta la scala |
| **C** | componenti **= 1 GIA' ALLA SEMINA** | le masse si sono **compenetrate**: non sono tre masse. **`sep` troppo piccolo, si risale** |
| **D** | si fondono e poi si **RISEPARANO** | **e' un fenomeno, non un errore**: si riporta |

**E una quinta casella, che viene dal §1:** **componenti < 4 ma ZERO archi massa-massa** ->
**le masse NON si parlano fra loro: parlano col vuoto.** **Si riporta cosi'**, e si dice a Luca
che per un contatto diretto serve `sep` ancora piu' piccolo *(o un raggio di massa maggiore)*.

## 4. IL PROBLEMA DEL DRIVER, e come lo risolvo senza romperlo

**`csv/_test_fork/_scena_video.py` ha `--sep 8` CABLATO** nel suo `sys.argv`: **non e'
parametrizzabile da riga di comando.** Per il run vero serve.

**Non lo tocco adesso.** Il pilota e' uno script a parte. **Dopo il pilota**, il cambiamento al
driver e' **un commit solo, con il suo sigillo**: `--sep=X` **nominale, default `8`**, cioe'
**esattamente l'idioma che il driver gia' usa e documenta** per `--serie` e `--csv-progresso`
*(«sono NOMINALI e non posizionali di proposito... il comando di `Z49` deve restare riproducibile
VERBATIM»)*. **Il sigillo e': a default il driver fa esattamente quello che faceva.**

## 5. I PRESIDI
- **il pilota NON e' il run:** i suoi numeri servono a scegliere `sep`, **non entrano in un referto
  di fisica**;
- **distribuzioni bimodali -> due popolazioni separate**, mai una mediana (A3c);
- **A8:** ogni contatore stampato, **inclusi quelli dell'archivio**;
- **la cartella del pilota NON si cancella** (`Z31`, ripetuto due volte);
- **`--tau-luce` ha il sigillo `6/7` con `T3` dichiarato**: va in testa al referto del run;
- **un seme, una scena.**

## 6. COSA MI FA FERMARE
- **lettura `C`** (un blocco solo gia' alla semina) -> **si risale, non si procede**;
- **componenti < 4 ma zero archi massa-massa** -> **si riporta a Luca prima di lanciare**: e' una
  scena diversa da quella che il mandato descrive;
- **la stima di durata o di spazio fuori scala** -> **si riporta prima di lanciare**, e si dirada la
  cadenza, **mai si accorciano i passi**;
- **il driver da cambiare** -> **non si lancia il run finche' quel commit non e' sigillato.**

## 7. TODO DEL NEXT STEP
1. [fatto] blob/branch dal disco; la geometria **misurata** e la premessa corretta;
2. il **pilota**, committato **prima** di girarlo;
3. `sep`, `rc`, componenti, archi massa-massa, durata, spazio -> **STOP e riporto**;
4. il commit del driver con `--sep` nominale **e il suo sigillo**;
5. previsioni qualitative -> `STATO_RUN.md` -> il run da 10.000 passi.
