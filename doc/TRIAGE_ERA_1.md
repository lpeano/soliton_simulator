# IL TRIAGE DELLE VOCI DELL'ERA `1` — **il piano, SCRITTO E NON ESEGUITO**

> ### ⛔ **QUESTO DOCUMENTO NON CHIUDE NESSUNA VOCE.** Descrive la procedura da applicare
> ### **a riscrittura finita**, voce per voce. ### **Eseguirlo adesso sarebbe chiudere difetti
> su una fisica che non esiste ancora.**
>
> *Lo stato di partenza: `629` voci con `SOSPESA-ERA-1`, `86` lasciate come lezioni di metodo,
> `8` bloccanti fra le sospese (`9f23313`). Lo stato dell'era `1` resta al tag
> `era-1-secondo-ordine`.*

---

# 📌 `⓿` **DA DOVE PARTE, dallo schema `2`** *(aggiornato il 2026-10-08)*

> ### ⛔ **IL TRIAGE PARTE DA UN COMANDO, non da una lettura:**

```
python csv/indice.py cerca --stato SOSPESA        # le 46 da triare
python csv/indice.py cerca --stato DA_CLASSIFICARE  # le 480 che aspettano LUCA, NON il triage
```

| | |
|---|---|
| ### **le `SOSPESA`** | sono ### **`46`**, e sono ### **le liste del guardiano applicate**: fisica dell'era `1`, dominio e era ### **dichiarati** |
| ### ⛔ **le `AGENDA` NON PASSANO DAL TRIAGE** | sono ### **`43`**, e sono il ### **programma dell'era `2`**: non sono difetti dell'era `1`, quindi ### **non c'e' niente da triare** — si lavorano |
| ### ⛔ **le `DA_CLASSIFICARE`** | sono ### **`480`**, e ### **non sono materia del triage: sono DECISIONI DI LUCA.** La tavola corta sta in `doc/REFERTO_indice_v2.md` |
| ### **la traccia** | `doc/indice/migrazione_era1.jsonl` dice, per ### **ogni** ID vecchio, ### **dove e' andato e per quale regola** |

### ⚠ **E IL CAMPO CHE IL TRIAGE USA NON E' PIU' `si_riferisce_a`:** quello era riempito
### **cercando nomi nel testo** *(per DIFETTO)*, e vive come metadato `si_riferisce_a_era1`.
### ➜ **I riferimenti VERI sono i campi `leggi`, `variabili` e `assiomi`**, validati contro i
registri — e si cercano con `indice cerca --legge L-… / --variabile V-… / --assioma A…`.

---

# ⭐ `①` **LE TRE USCITE, e come si decide fra loro**

| | l'uscita | quando | ### **che cosa si scrive** |
|---|---|---|---|
| **`S`** | ### **SUPERATA** | ### **la legge non esiste più** *(es. `phivel`, la sincronizzazione, il termostato)* | si ### **chiude**, col ### **rimando alla decisione che l'ha tolta** — la scheda in `doc/REGISTRO_FISICA.md`. ### ⛔ **Non «risolta»: SUPERATA**, e la differenza va scritta nello `stato_da` |
| **`T`** | ### **TRASPORTATA** | la legge è stata ### **tradotta** | il difetto ### **si RICONTROLLA MISURANDO** sulla versione nuova. ### ⛔ **NON a parole:** finché non c'è la misura la voce resta ### **aperta**, con la nuova legge in `si_riferisce_a` |
| **`V`** | ### **ANCORA VALIDA** | il difetto ### **non dipendeva dalla dinamica** *(es. una regola di nascita, un'eredità alla nascita, un default sbagliato)* | ### **resta aperta così com'è**, e `stato` torna a `stato_era_1` |

### ⚠ **E UNA QUARTA USCITA CHE NON E' UN'USCITA, e va prevista:** una voce può risultare
### **NON CLASSIFICABILE** perché ### **non si capisce a quale legge si riferiva**. ### ⛔ **Erano `411` su `629` nello schema `1`; nello schema `2` sono le ### **`480` `DA_CLASSIFICARE`**, e NON sono materia del triage: sono ### **decisioni di Luca** *(il campo `si_riferisce_a` dice `(non trovato)`)*: `titolo_breve` è
troncato a `100` caratteri e la spiegazione lunga non nomina la legge. ### ➜ **Quelle si LEGGONO
A MANO, e il triage non le instrada da solo.**

---

# ⛔ `②` **LA PROCEDURA, voce per voce**

```
PER OGNI voce con stato = SOSPESA-ERA-1:

  1. si legge `si_riferisce_a`.
     SE dice `(non trovato)`  ->  SI LEGGE A MANO la voce in doc/STATO_RUN.md.
                                  ### NON si instrada per somiglianza.

  2. SI CERCA quella legge nella versione NUOVA, per FORMA e non per nome
     (lo stesso metodo di csv/_test_fork/_censimento_leggi.py).

     SE NON ESISTE PIU'                     ->  `S` SUPERATA
     SE ESISTE, tradotta                    ->  `T` TRASPORTATA
     SE la voce non parlava della dinamica  ->  `V` ANCORA VALIDA

  3. SOLO per `T`: SI RIFA' LA MISURA che aveva trovato il difetto.
     ### Il difetto o c'e' o non c'e', e lo dice un numero.
     SE la misura non si puo' rifare (lo strumento dipendeva dal secondo ordine)
        ->  SI SCRIVE QUALE MISURA MANCA, e la voce RESTA APERTA.

  4. SI SCRIVE l'esito in `stato_da`, con il rimando: la decisione (per `S`),
     il numero (per `T`), il motivo (per `V`).
```

### ⛔ **TRE REGOLE CHE IL TRIAGE NON PUO' VIOLARE**

| | |
|---|---|
| ### **nessuna voce si cancella** | come nella sospensione: il conto delle righe ### **prima e dopo** si asserisce |
| ### **`T` NON si chiude senza un numero** | *«la legge è stata tradotta, quindi il difetto è passato»* è ### **un'argomentazione, non una misura.** ### **Il difetto si ricontrolla MISURANDO** |
| ### **`S` cita la DECISIONE, non l'opinione** | una voce superata deve puntare alla ### **scheda** di `doc/REGISTRO_FISICA.md` che ha tolto quella legge. ### **Se non c'è una scheda, la legge non è stata tolta per decisione** — e allora non è `S` |

---

# 📌 `③` **IL COMANDO, che parte dall'indice**

### **Lo strumento esiste già a metà:** `csv/_sospendi_era1.py` legge il TSV, classifica e
scrive le due colonne. ### ➜ **Il triage è il suo gemello**, e il comando previsto è:

```
python csv/_triage_era1.py --collaudo              # conta e NON scrive
python csv/_triage_era1.py --proponi               # scrive le PROPOSTE in un .md, NON nel TSV
python csv/_triage_era1.py --applica --solo S      # una classe alla volta
```

| | perché così |
|---|---|
| ### **`--collaudo` prima** | lo stesso patto di `_sospendi_era1.py`: ### **si conta senza scrivere** |
| ### ⭐ **`--proponi` SEPARATO da `--applica`** | il triage ### **propone** e Luca ### **conferma**, come per l'elenco delle `METODO`. ### ⛔ **`629` voci non si chiudono in automatico** |
| ### **`--solo S` / `T` / `V`** | ### **una classe alla volta** — è la regola d'oro del par.3 *(un interruttore alla volta)* applicata al triage |

### ⚠ **E IL COMANDO NON ESISTE ANCORA:** questo documento dice ### **che forma avrà**, non che
sia scritto. ### **Scriverlo adesso sarebbe uno strumento che non si può collaudare**, perché
la versione nuova delle leggi ### **non c'è.**

---

# ⭐ `④` **CHE COSA SI PUO' GIA' DIRE, con i numeri di oggi**

### **Tre gruppi di voci hanno già il loro esito PREVISTO** — e la previsione sta scritta
### **prima** del triage, per poterla perdere:

| | le voci | l'esito previsto | ### **la decisione che lo giustifica** |
|---|---|---|---|
| ### **le voci della SINCRONIZZAZIONE** | quelle che nominano `K_SYNC` o la sync | ### **`S` SUPERATA** | `sincronizzazione-si-toglie` *(decisione `(B)`, PRESA)* |
| ### **le voci di `phivel` e del TERMOSTATO** | quelle che nominano `phivel`, `xi_termo`, il bagno | ### **`S` SUPERATA** | `A16.2` *(primo ordine: `phivel` non esiste)* e `A14.1` |
| ### **l'EREDITA' DI `pos` ALLA NASCITA** | `_rn_div_pos`, `_rn_sch_pos` | ### **`V` ANCORA VALIDA** | ### **non dipende dalla dinamica:** è una ### **regola di nascita**, e `A17` la vieta comunque |

### ⛔ **E UNA VOCE CHE MERITA UN NOME, perché la decisione `(A)` la chiude per costruzione:**
`U1` — *«`massacriticacollasso`: `21` usi DENTRO le leggi»*, ### **bloccante**. La decisione
`(A)` *(il calore paga la nascita, e la soglia è ### **il bilancio**)* ### **fa sparire quella
costante**. ### ➜ **Esito previsto: `S` SUPERATA** — ### ⚠ **ma SOLO quando il vuoto locale sarà
scritto**, perché finché la soglia non è calcolabile la costante ### **non è stata sostituita da
niente.**

---

# ⛔ **CHE COSA QUESTO PIANO NON DICE**

| | |
|---|---|
| ### **quando** si esegue | ### **a riscrittura finita**, e «finita» vuol dire: ### **la `H` scelta** *(le `13` decisioni, oggi `3` prese)* e ### **le leggi portate**. Non prima |
| che le `411` senza riferimento ### **si instradino** | ### ⛔ **no: si LEGGONO A MANO.** Il piano lo dice invece di prometterlo |
| che le `86` lezioni di ### **METODO** entrino nel triage | ### ⛔ **no: non sono sospese.** Valgono nell'era `2` così come sono, e il loro elenco aspetta ### **la conferma di Luca** |
| che il triage ### **chiuda** l'indice | ### ⛔ **no.** Alcune voci resteranno ### **aperte con una misura che manca**, ed è l'esito giusto per una `T` che non si può ricontrollare |
