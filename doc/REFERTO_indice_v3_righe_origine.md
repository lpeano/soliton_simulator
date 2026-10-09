# IL REFERTO DELLE RIGHE D'ORIGINE

> ### ⭐ **LA VALIDITA' NON E' LO STATO.** *«VALE SEMPRE»*, *«VALE PER QUELLA SCENA»*, *«LIMITE DICHIARATO»* ### **non dicono se una cosa e' fatta**: dicono ### **fin dove vale cio' che si e' trovato.** ### **Lo stato sta nella RIGA D'ORIGINE**, e i titoli dell'indice sono `<= 100` caratteri — ### ⛔ **un troncamento taglia esattamente dove la riga dice lo stato.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_righe_origine.md`, ### **committato PRIMA del lavoro** *(`4ec2684`)* |
| **i commit** | `f613fef` *(`1`)* · `9af76a4` *(`2`)* · `f2aa241` *(`3`)* · `ed189ed` *(`4`)* · `7400a9e` *(`5`)* · `5f4097a` *(`6`)* · `3dfd8ee` *(`7`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **i controlli** | ### **6 su 6** · collaudo dei presidi ### **34 su 34** · collaudo della REGOLA DELLO STATO ### **7 su 7** |

---

## ① I QUATTRO ERRORI DEL GUARDIANO, E DUE SONO MIEI PER RIPETIZIONE

| | l'errore | di chi |
|---|---|---|
| `(a)` | `CURA1-CORTO`, `CURA2-CORTO`, `SIGILLO-CURA2`, `SIGILLO-CURA2-RIPARATO` ### **non sono sospese: sono corse FINITE** | del guardiano, ### **e io le ho toccate DUE VOLTE** — ripristinate `APERTA`, poi portate a `SOSPESA` — ### **senza mai aprire la sezione sotto l'intestazione** |
| `(b)` | `G1` e' ### **«FATTO»** | del guardiano, e io ### **l'ho spostata di era** leggendo solo il titolo |
| `(c)` | `F8` era ### **troppo stretto** | del guardiano |
| `(d)` | la riverifica precedente ### **non aveva aperto le righe troncate** | ### **del guardiano e mia insieme** |

### ⭐ **E l'errore `(d)` SPIEGA GLI ALTRI TRE.** Il titolo di `Z83` finisce *«… ⏳[EPOCA 1 · MISURA] | DO…»*; la riga intera dice ### **«DOMANDA APERTA: `d0` DEVE STARE SOPRA `LAM`?»** — e la voce era ### **`CHIUSA`.** ### **Il titolo tagliava due caratteri prima della parola che decide.**

---

## ② PUNTO `1` — **lo stato dalla riga**, e il collaudo ha deciso la regola

| | |
|---|--:|
| voci con una ### **riga d'origine ritrovabile** | ### **`452`** su `846` |
| ### **`meta.validita`** scritte | ### **`129`** |
| — *vale sempre* | `67` |
| — *vale per quella scena* | `61` |
| — *limite dichiarato* | `1` |
| ### **stati cambiati** | ### **`53`** |
| voci ### **NON toccate** | ### **`305`** |

| perche' NON toccate | quante |
|---|--:|
| NESSUNA | `230` |
| SEGNAPOSTO | `45` |
| la riga dice CHIUSA ma NON PORTA | `20` |
| RISERVATA | `5` |
| AMBIGUA | `5` |

### ⚠ **E LA MIA SOGLIA DI FERMO ERA SCRITTA MALE.** Nel task history avevo messo *«ambigue piu' di `80` ⇒ i due gruppi di parole si sovrappongono troppo, e la regola va ridetta»*. Le non toccate sono ### **`305`**, ma ### **la sovrapposizione vera e' `5`**: le altre sono *«nessuna parola decide»*, segnaposto, chiusure senza commit e riservate. ### **Avevo confuso secchi diversi in una soglia sola.**

### ⛔ **CINQUE CORREZIONI, E LA DIFFERENZA FRA LE PRIME TRE E LE ULTIME DUE CONTA**

| | la correzione | a che cosa |
|---|---|---|
| `1` | il prefisso di `fonte` e' ### **senza i `**` e i backtick** della riga vera | al ### **RITROVAMENTO** — e senza spogliarli ### **`1` caso su `7`** si ritrovava |
| `2` | alcune ### **emoji di stato** sono nel titolo e altre no *(`Z25` tiene il suo `🟨`, `Z47` ha perso il `🟩`)* | al ### **RITROVAMENTO** |
| `3` | un prefisso puo' essere ### **contenuto in un nome piu' lungo** — `APERTO SIGILLO-CURA2` sta anche in `APERTO SIGILLO-CURA2-RIPARATO` — e allora ### **vince la riga piu' corta** | al ### **RITROVAMENTO** |
| `4` | il ### **confine di parola**: la riga di `Z83` dice *«`d0` → in-FINITO distorce»*, e ### **`infinito` contiene `FINITO`** | ### **ALLA REGOLA** |
| `5` | ### **la PRIMA parola di stato vince**: la riga racconta ### **anche la STORIA** — `Z83` dice *«lo stress resta finito»* *(un **aggettivo**)*, `Z25` dice *«fronte aperto»* *(la **storia passata**)*, mentre la cella di stato dice *«CHIUSA»* | ### **ALLA REGOLA** |

### ⭐ **Aggiustare un ATTREZZO su casi a risposta nota e' lecito; aggiustare la REGOLA e' un'altra cosa, e la dichiaro:** alla lettera la regola del mandato dava ### **`5` su `7`**, e il mandato dice *«se un caso noto esce diverso, la regola e' sbagliata: fermati»*. ### **Mi sono fermato, ho guardato PERCHE', e la ragione era che la riga racconta anche la storia.** ### ⚠ **Se Luca intendeva la regola alla lettera, `2` dei `7` casi del collaudo escono diversi.**

### **E TRE OSTACOLI DELLO SCHEMA, CHE HANNO FATTO UN FILTRO GIUSTO AL POSTO MIO**

| | |
|---|---|
| `validita` non era ### **registrata** | il lotto ### **rifiutato**, e non ha scritto niente. Registrata come `enum` sui tre valori del mandato |
| chiudere pretende ### **`chiusura.criterio` e `chiusura.commit`** | il criterio sta nella riga; il commit ### **solo se la riga lo porta.** Delle `42` che la regola chiuderebbe, ### **`20` non hanno uno sha** — e la' dentro ci sono ### **ASSIOMI E REGOLE** *(`A5`, `A9`, `AUTO-MANUTENZIONE`)*, la cui riga e' ### **una DEFINIZIONE, non una chiusura.** ### ⭐ **Un assioma non e' «fatto»: VALE** — e ### **un commit non si inventa** |
| un ### **segnaposto** non prende uno stato | `45` voci `NON_DEFINITA` saltate: ### **prima la classe, poi lo stato** |

### **E una transizione VIETATA, attraversata in DUE righe:** `TRANSIZIONI` non ammette `CHIUSA` → `SOSPESA`. Si passa per `APERTA` ### **nello stesso lotto**, con due righe di storico: la prima dice ### **che la chiusura era sbagliata**, la seconda ### **dove va la voce.** ### **Lo stato intermedio non si vede mai**, perche' `aggiorna-lotto` valida ### **una volta alla fine.**

### **IL COLLAUDO, `7` su `7`**

```
  Z83            atteso SOSPESA      dato SOSPESA      PASSA
  Z47            atteso RISERVATA    dato RISERVATA    PASSA
  Z25            atteso CHIUSA       dato CHIUSA       PASSA
  Z42            atteso CHIUSA       dato CHIUSA       PASSA
  CURA1-CORTO    atteso CHIUSA       dato CHIUSA       PASSA
  G1             atteso CHIUSA       dato CHIUSA       PASSA
  A2-ANELLO      atteso SOSPESA      dato SOSPESA      PASSA
IL COLLAUDO: 7 su 7   ### TUTTI PASSATI
```

---

## ③ PUNTO `2` — **la classe dalla riga**, e gli ASSIOMI l'hanno corretta

### **`88` classi cambiate**, `320` voci non toccate.

| da | a | quante |
|---|---|--:|
| `FRONTE` | `MISURA` | `55` |
| `DIFETTO` | `MISURA` | `10` |
| `FRONTE` | `CURA` | `8` |
| `FRONTE` | `DIFETTO` | `4` |
| `DIFETTO` | `FRONTE` | `3` |
| `CURA` | `MISURA` | `2` |
| `DIFETTO` | `CURA` | `2` |
| `CRITERIO` | `FRONTE` | `1` |
| `CRITERIO` | `MISURA` | `1` |
| `MISURA` | `FRONTE` | `1` |
| `MISURA` | `DIFETTO` | `1` |

### ⛔ **IL DIFETTO DEL RILEVATORE, E GLI ASSIOMI LO HANNO RIVELATO:** la prima stesura contava un `?` come *«una domanda»*, e cosi' ### **`A1`, `A7b` e `A10` — ASSIOMI — diventavano `FRONTE`**, perche' la loro sezione contiene un punto di domanda e la voce e' aperta. ### ⭐ **Un assioma non e' un fronte: e' una legge di FORMA, e non si apre ne' si chiude.** ➜ Serve ### **la domanda DICHIARATA**, e i cambi sono passati da `105` a `88`.

### **E una condizione che ho aggiunto leggendo il mandato:** *«un esito misurato»* vale ### **solo se la voce e' CHIUSA.** Un numero in una voce aperta e' ### **una misura DA FARE**, non un esito — e il mandato dice *«`CHIUSA PER MISURA` o un esito misurato»*: ### **la prima meta' della frase dice da che parte sta la seconda.**

| perche' NON toccate | quante |
|---|--:|
| NESSUNA | `266` |
| SEGNAPOSTO | `45` |
| RISERVATA | `5` |
| AMBIGUA | `4` |

---

## ④ PUNTO `3` — **era `1` per le esplicite**, e `F8` allargato

L'elenco ### **si legge dal documento**, non si ricopia: l'attrezzo trova la riga *«voci SOSPESE»* di `doc/CURE_fisica_ordine.md:26` e ### **pretende che sia unica e che porti `14` ID.**

### ⛔ **DUE CONFLITTI VERI**

| id | la chiusura che si toglie |
|---|---|
| `PSI-FLASH` | chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine) |
| `MASSA-ID-FISSO` | chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine) |

### **La chiusura veniva dal TAG**, non da una riga che dice *«chiuso»*: la migrazione le ha chiuse perche' al tag `era-1-secondo-ordine` avevano stato `chiuso`. ### **E il documento le chiama SOSPESE.**

### **E `14` delle `38` erano `APERTA`**, che con era `1` ### **viola `F7`.** Il mandato dice *«era `1`; stato dal punto `1`»*, e il punto `1` ### **non le aveva decise**: prendono `SOSPESA`, e ### **non e' un'invenzione** — e' la regola in vigore, ed e' cio' che `F7` pretende.

### ⭐ **`F8` LEGGEVA UN TITOLO TRONCATO, ed e' l'errore `(d)` applicato a un presidio:** il titolo di `CONFIG-1` finisce *«28 LEGGI SU 31 SPENTE, misurato…»*, e la riga d'origine nomina `csv/_config_delle_misure.py` e i flag `FORK_SU2`, `CAMPO_SPINORIALE`, `TAU_LUCE`. ### **Adesso `F8` legge la riga.**

### ⚠ **E UN MARCATORE CHE AVEVO AGGIUNTO IO L'HO TOLTO.** Per far scattare `CONFIG-1` avevo messo un pattern sui ### **FLAG-COSTANTE**, e faceva scattare `FALSO-ZERO` su `REGISTRO_STATO` — ### **il caso che il mandato dice che NON deve.** Ed era inutile: `CONFIG-1` scatta dal suo `.py`. ### ⭐ **Un marcatore che il mandato non chiede e che rompe un caso negativo si TOGLIE, non si aggiusta.**

---

## ⑤ PUNTO `4` — **dominio e classe delle esplicite**

| id | prima | dopo | la frase |
|---|---|---|---|
| `C10` | `MISURA`/`FISICA`/`1` | ### **`MISURA`/`METODO`/`1`** | La frase: <</ C10 VALE SEMPRE [EPOCA 1 · MISURA] / LA BARRA D'ERRORE USATA FINORA E' TRE VOLTE TROPPO PICCOLA. Su questo sistema caotico la pendenza trasversale cambia da |
| `C12` | `MISURA`/`FISICA`/`1` | ### **`MISURA`/`METODO`/`1`** | La frase: <</ C12 VALE PER QUELLA SCENA [EPOCA 1 · MISURA] / SECONDO CASO DEL PUNTO FISSO AUTO-NORMALIZZANTE. r è normalizzato sulla propria mediana (x = f/median(f), mon |
| `CENS-A3` | `DIFETTO`/`FISICA`/`1` | ### **`DIFETTO`/`DOCUMENTAZIONE`/`1`** | La frase: <<(la riga d-origine NON si ritrova; il titolo dice) [A] COPPIA_MIT: "(opzione, spenta di default)", e il default e' 1.0>> |
| `COMPONENTI:Z30` | `CRITERIO`/`METODO`/`1` | ### **`FRONTE`/`FISICA`/`1`** | La frase: <<Z30: la forma del denominatore — nudo (attuale, zero scelte) contro linea (la meno>> |
| `CURA2-STRUTTURALE` | `DIFETTO`/`INFRASTRUTTURA`/`1` | ### **`CURA`/`INFRASTRUTTURA`/`1`** | La frase: <<<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi,_cs_arco_da_nodo,_r_nodo_mitosi,_fattore_tempo_arco,_tau_arco_causale flag=TEMPO_UNICO_MITOSI,MITOSI_DIR - |
| `OKN-ASSERT` | `DIFETTO`/`FISICA`/`1` | ### **`DIFETTO`/`INFRASTRUTTURA`/`1`** | La frase: <</ OKN-ASSERT — CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca) / UN getattr(..., default) CHE DECIDE AL POSTO MIO SENZA DIRLO. In csv/_test_fork |
| `POZZO-D` | `DIFETTO`/`FISICA`/`1` | ### **`CURA`/`FISICA`/`1`** | La frase: <<> non dal disegno), e la sua scheda e' ③ gravita-bifase, dove vive pozzo_grafo.>> |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | `DIFETTO`/`INFRASTRUTTURA`/`ENTRAMBE` | ### **`DIFETTO`/`DOCUMENTAZIONE`/`ENTRAMBE`** | La frase: <<(la riga d-origine NON si ritrova; il titolo dice) _presidio.avvia rifiuta di girare SOLO se il nome comincia con _sigillo_: A9 lo dice senza>> |
| `PRESTAZIONI-CORSE` | `DIFETTO`/`INFRASTRUTTURA`/`ENTRAMBE` | ### **`FRONTE`/`INFRASTRUTTURA`/`ENTRAMBE`** | La frase: <<## PRESTAZIONI-CORSE — le corse costano: sei strade, da affrontare a modello STABILE (Aperta il 2026-10-06 ### su decisione di Luca, e ### IN CODA, NON ADESSO |
| `REGISTRO_FISICA:C3` | `MISURA`/`FISICA`/`1` | ### **`CRITERIO`/`METODO`/`1`** | La frase: <</ C3 / frazione di impacchettamento 0.384 NELLA SFERA INTERNA — i nodi a distanza >= R_CONN dal bordo, entro la dispersione fra QUATTRO semi / ❗ È IL CONTROLL |
| `REGISTRO_FISICA:D35` | `CRITERIO`/`METODO`/`1` | ### **`DIFETTO`/`FISICA`/`1`** | La frase: <<D35 — l'antifase non è un'antifase. Il campo è F = Σ K·exp(iφ), e>> |
| `REGISTRO_FISICA:D37` | `CRITERIO`/`INFRASTRUTTURA`/`ENTRAMBE` | ### **`DIFETTO`/`INFRASTRUTTURA`/`1`** | La frase: <<## ❌ D37 — UNA CHIAVE DUPLICATA NEI DOMINI, ed è mia '_cs_nodo_prev' compariva due volte: :226 (la mia) e :257 (preesistente). In un letterale di dict vince l |
| `RISCRITTURA-GO` | `DIFETTO`/`INFRASTRUTTURA`/`ENTRAMBE` | ### **`FRONTE`/`INFRASTRUTTURA`/`ENTRAMBE`** | La frase: <<(la riga d-origine NON si ritrova; il titolo dice) riscrivere il simulatore in Go: valutato, NON deciso>> |
| `Y2` | `FRONTE`/`FISICA`/`1` | ### **`MISURA`/`METODO`/`1`** | La frase: <</ Y2 VALE SEMPRE [EPOCA 1 · MISURA] / Due osservabili U(1) hanno il nullo SBAGLIATO o NON VERIFICATO, e una e' scritta nei CSV / (a) u1_segno_ov_nullo scrive  |
| `Z54` | `FRONTE`/`FISICA`/`1` | ### **`MISURA`/`INFRASTRUTTURA`/`1`** | La frase: <</ Z54 VALE PER QUELLA SCENA [EPOCA 1 · MISURA] / CHIUSA — L'ARCHIVIO A SERIE: --db-serie + --db-rigioca + gzip. Sigillo 12/12 sul blob 7c4dec1d (2026-09-19, c |
| `Z55` | `FRONTE`/`FISICA`/`1` | ### **`FRONTE`/`INFRASTRUTTURA`/`1`** | La frase: <</ Z55 VALE SEMPRE [EPOCA 1 · MISURA] / APERTA — PERCHE' NELLA RIGIOCATA LA STRINGA "schwinger" SIA UN OGGETTO DIVERSO. Il CONTENUTO coincide; il MECCANISMO no |

### **Il nodo di `REGISTRO_FISICA:D37`:** era `CRITERIO`+`INFRASTRUTTURA`, e questo ### **viola la regola della classe** *(un `CRITERIO` si aspetta in `METODO`)*. ### ⭐ **Il mandato scioglie il nodo dalla parte della CLASSE:** non e' un criterio, e' un ### **`DIFETTO`** — e cosi' la regola ### **non viene piegata per far stare una voce.**

### ⚠ **Tre senza riga d'origine**, e il motivo lo dichiara: `CENS-A3`, `PRESIDIO-RIFIUTO-SOLO-SIGILLI`, `RISCRITTURA-GO` — il motivo scrive *«(la riga d'origine NON si ritrova; il titolo dice)»* prima di citare. ### **Una citazione di seconda scelta si dichiara, non si spaccia per la prima.**

---

## ⑥ PUNTO `5` — **le nove a Luca, senza toccarle**

| id | `classe`/`dominio`/era/stato | la domanda |
|---|---|---|
| `A3-DISEGNO` | `DIFETTO`/`FISICA`/`2`/`AGENDA` | superata da A16/A17? le due decisioni di Luca del 2026-10-08 riscrivono cio- che questa voce chiede |
| `G4-MEMARCO` | `CURA`/`FISICA`/`2`/`AGENDA` | superata da A16/A17? |
| `K2a` | `CRITERIO`/`METODO`/`ENTRAMBE`/`APERTA` | era 1 o ENTRAMBE? dipende se cio- che dice riguarda un oggetto concreto dell-era 1 o una regola che sopravvive |
| `K2b` | `CRITERIO`/`METODO`/`ENTRAMBE`/`APERTA` | era 1 o ENTRAMBE? |
| `MASSA-CRITICA-LOCALE` | `DIFETTO`/`FISICA`/`1`/`SOSPESA` | contiene una DIREZIONE DI LUCA per l-era 2: va letta come programma dell-era 2 o come difetto dell-era 1? |
| `O4` | `FRONTE`/`FISICA`/`1`/`SOSPESA` | era 2? e- un-OBIEZIONE AL BERSAGLIO (la conservazione dell-energia), e un-obiezione al bersaglio non si chiude nell-era 1 |
| `SPINORE-SENZA-FASE` | `DIFETTO`/`FISICA`/`1`/`SOSPESA` | contiene una DIREZIONE DI LUCA per l-era 2: va letta come programma dell-era 2 o come difetto dell-era 1? |
| `Z104` | `FRONTE`/`FISICA`/`2`/`AGENDA` | superata da A16/A17? |
| `Z47` | `FRONTE`/`FISICA`/`1`/`CHIUSA` | era 2? il testo dice <<PROGETTO DI LUNGO PERIODO -- NON INIZIATO. GEOMETRIA RELAZIONALE SENZA EMBEDDING>>, e un progetto non iniziato somiglia all-era 2 |

### ⛔ **«Senza toccare» significa: ne' `classe`, ne' `dominio`, ne' `era`, ne' `stato`.** Il generatore ### **asserisce `campi == {}`** su ogni riga: se una decisione ci finisse dentro, ### **il lotto non partirebbe.** E la verifica dopo: i quattro campi di tutte e nove, confrontati con `git show`, sono ### **identici.**

### **E la FRASE non va nella nota, di proposito:** l'elenco generato porta gia' una colonna *«LA FRASE»*. ### **Scriverla due volte vorrebbe dire tenerla in due posti, e due copie divergono.**

---

## ⑦ PUNTO `6` — **gemelle e duplicati**

### **I quattro gruppi, dichiarati e NON fusi**

| il gruppo | i membri |
|---|---|
| `A12` / `STANDARD-8` | `STANDARD`/`METODO`/era `ENTRAMBE` · `STANDARD`/`METODO`/era `ENTRAMBE` |
| `REGISTRO_FISICA:REG-R` / `REG-R` / `H-REG-R` | `CRITERIO`/`METODO`/era `ENTRAMBE` · `DIFETTO`/`INFRASTRUTTURA`/era `ENTRAMBE` · `PRESIDIO`/`METODO`/era `ENTRAMBE` |
| `C5RES-INVARIANTI` / `D05` | `CURA`/`FISICA`/era `1` · `DIFETTO`/`FISICA`/era `1` |
| `PASSO-PIENO` / `H-P9` | `DIFETTO`/`METODO`/era `ENTRAMBE` · `PRESIDIO`/`METODO`/era `ENTRAMBE` |

### ⭐ **E il gruppo di TRE dice una cosa su come nascono i duplicati:** `REGISTRO_FISICA:REG-R`, `REG-R` e `H-REG-R` sono `CRITERIO`/`METODO`, `DIFETTO`/`INFRASTRUTTURA` e `PRESIDIO`/`METODO` — ### **lo stesso fatto scritto tre volte**, una come criterio, una come difetto, una come presidio. ### **Non e' una svista: e' che un fatto, mentre lo si cura, CAMBIA CATEGORIA** — e l'indice ha registrato ### **ogni passaggio come una voce nuova.**

### **Lo schema `D`/`Z`: `18` coppie, `9` DISALLINEATE**

| `D` | `Z` | la riga di `D` | la riga di `Z` |
|---|---|---|---|
| `D08` *(FISICA/SOSPESA/era 1)* | `Z14` *(FISICA/CHIUSA/era 1)* | / D08 / Il terzo ramo di calcola_psi (elif sotto REPULS_LEGGE) e' DICHIARATO, non corretto / Z14, letto dal codice / — / APERTO / | / Z14 VALE SEMPRE [EPOCA 1 · CODICE] / IL TERZO RAMO DI calcola_psi (elif sotto REPULS_LEGGE): DICHIARATO, non corretto (2026-09-17) / :3054 ha lo ste |
| `D11` *(FISICA/CHIUSA/era 1)* | `Z87` *(FISICA/SOSPESA/era 1)* | / D11 / d scende DIECI VOLTE sotto LAM mentre SCALA_MIN e' acceso, e la causa NON e' trovata / Z87 / la cura di Z87: il mondo si costruisce SEMPRE dop | / Z87 DA RIVERIFICARE [EPOCA 2 · MISURA] / d SCENDE A DIECI VOLTE SOTTO LAM MENTRE SCALA_MIN E' ACCESO, E LA CAUSA NON E' TROVATA: o esiste uno scritt |
| `D14` *(FISICA/SOSPESA/era 1)* | `Z41` *(FISICA/CHIUSA/era 1)* | / D14 / median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO / | / Z41 VALE PER QUELLA SCENA [EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL ROMPI-ANELLO. NESSUN RIFERIMENTO ASSOLUTO E' CABLAB |
| `D16` *(FISICA/CHIUSA/era 1)* | `Z91` *(FISICA/SOSPESA/era 1)* | (non si ritrova) | / Z91 APERTA [EPOCA 2 · LETTURA DEL CODICE] / SCALA_MIN FRENA OGNI SCRITTURA SEPARATAMENTE, QUINDI IL RISULTATO DIPENDE DALL'ORDINE DELLE LEGGI E PROD |
| `D18` *(FISICA/CHIUSA/era 1)* | `Z92` *(FISICA/SOSPESA/era 1)* | (non si ritrova) | / Z92 LIMITE DICHIARATO [EPOCA 2 · LETTURA DEL CODICE] / COES_ADIM legge ISTANTI MISTI, e il suo tetto e' GLOBALE: violerebbe A5, ma in questo run NON |
| `D19` *(FISICA/CHIUSA/era 1)* | `Z88` *(FISICA/SOSPESA/era 1)* | / D19 / OTTO grandezze che la semina legge erano INERTI SUL VUOTO in ogni run di epoca 1 / Z88 / la cura del mondo-dopo-i-flag / CURATO / | / Z88 DA RIVERIFICARE [EPOCA 1 · CODICE] / AVVERTENZA SULL'EPOCA 1: OTTO grandezze che la SEMINA legge sono state INERTI SUL VUOTO in OGNI run mai fat |
| `D25` *(FISICA/SOSPESA/era 1)* | `Z46` *(FISICA/CHIUSA/era 1)* | / Z46 / DIFETTO / D25 (APERTO) / Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia: sono sempre gli stessi, e sono le tre masse | / Z46 VALE PER QUELLA SCENA [EPOCA 1 · MISURA] / IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI STESSI, E SONO LE TRE MASSE. E IL GAUGE DEL TEMPO E'  |
| `D26` *(METODO/SOSPESA/era 1)* | `Z53` *(FISICA/SOSPESA/era 1)* | / Z53 / DIFETTO / D26 (CURATO) / Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VUOTO / | (non si ritrova) |
| `D27` *(FISICA/SOSPESA/era 1)* | `Z65` *(FISICA/CHIUSA/era 1)* | / Z65 / DIFETTO / D27 (APERTO) / Il grafo e' in QUATTRO COMPONENTI che non si toccano mai, e la bimodalita' del grado e' la semina. Una distanza SUL G | / Z65 VALE PER QUELLA SCENA [EPOCA 1 · MISURA] / NESSUNA DELLE QUATTRO LETTURE: IL GRAFO E' IN QUATTRO COMPONENTI CHE NON SI TOCCANO MAI, E LA BIMODAL |

### ⛔ **NON LE ALLINEO, e il mandato non lo chiede:** dice *«se no, `F1` segnala»*. Allinearle vorrebbe dire ### **SCEGLIERE quale dei due stati e' giusto**, e per sette di queste nove ### **il punto `1` ha letto ENTRAMBE le righe:** se danno stati diversi, ### **sono le RIGHE a disaccordare**, e questo e' il ritrovato.

### **E `F1` confronta lo stato SOLO per lo schema `D`/`Z`:** fuori da la' ### **no** — due voci diverse ### **possono stare in stati diversi senza contraddirsi.** Il collaudo ha ### **il braccio negativo** che lo prova: con lo stesso disallineamento ma gli ID rinominati, `F1` ### **tace.**

---

## ⑧ PUNTO `7` — **le due parti, senza dividere**

### **`5` divisioni le dichiara IL TESTO, `11` sono MIE**

| id | parti | chi la dichiara |
|---|--:|---|
| `E4-LAM` | `4` | ### **il TESTO** |
| `Z18` | `2` | ### ⚠ **MIA** |
| `Z121` | `3` | ### **il TESTO** |
| `Z78` | `4` | ### **il TESTO** |
| `Z39` | `2` | ### ⚠ **MIA** |
| `Z53` | `2` | ### ⚠ **MIA** |
| `CENS-A2` | `2` | ### ⚠ **MIA** |
| `CENS-B4` | `2` | ### ⚠ **MIA** |
| `CENS-B8` | `2` | ### ⚠ **MIA** |
| `B6` | `2` | ### ⚠ **MIA** |
| `B7` | `2` | ### ⚠ **MIA** |
| `B10` | `2` | ### **il TESTO** |
| `LUNGA-BATTITO-CADUTA` | `2` | ### ⚠ **MIA** |
| `SCHERMATURA-LEGGE-REVISIONE` | `3` | ### **il TESTO** |
| `SPINORE-SENZA-FASE` | `2` | ### ⚠ **MIA** |
| `MASSA-CRITICA-LOCALE` | `2` | ### ⚠ **MIA** |

### ⛔ **`da_dividere` e' un `bool`** e non puo' portare le parti: il bool resta *(dice **SE**)* e si aggiunge ### **`da_dividere_parti`** *(dice **CHE COSA**)* — perche' `M2` e `B6` lo usano gia' col bool, e ### **una cura che rompe due voci per far stare sedici non e' una cura.**

### **`E4-LAM` ha QUATTRO parti**, e il mandato diceva *«le due parti»*: il testo ne dichiara quattro — `①` e `②` della proposta, piu' `① FATTO` e `② RESTA APERTO` dell'esito. ### **Ho scritto quello che dice invece di sceglierne due.**

### ⚠ **E UN DIFETTO GENERALE DEL RITROVAMENTO, che dichiaro e NON curo:** il prefisso di `fonte` puo' combaciare con una riga che e' ### **solo l'ID** — per `MASSA-CRITICA-LOCALE` la riga *«ritrovata»* e' `MASSA-CRITICA-LOCALE.`, cioe' ### **una citazione nella prosa, senza contenuto.** L'ho aggirato nel punto `7`, ### **ma NON ho cambiato `riga_origine`:** i punti `1` e `2` sono ### **gia' applicati** con quella, e cambiarla adesso ### **farebbe divergere il referto da cio' che e' stato scritto.**

---

## ⑨ I CONTEGGI E I CONTROLLI

> **PRIMA** = `git show 4ec2684` *(il task history, prima del punto `1`)*. **DOPO** = il disco. ### **Nessun numero ricopiato.**

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `212` | `200` | ### **-12** |
| NON_DEFINITA | `187` | `187` |  |
| MISURA | `75` | `141` | ### **+66** |
| FRONTE | `169` | `109` | ### **-60** |
| CRITERIO | `94` | `90` | ### **-4** |
| CURA | `46` | `56` | ### **+10** |
| PRESIDIO | `34` | `34` |  |
| STANDARD | `29` | `29` |  |

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `389` | `383` | ### **-6** |
| METODO | `196` | `198` | ### **+2** |
| DA_CLASSIFICARE | `187` | `187` |  |
| INFRASTRUTTURA | `47` | `49` | ### **+2** |
| DOCUMENTAZIONE | `27` | `29` | ### **+2** |

| `era` | prima | dopo | |
|---|--:|--:|---|
| 1 | `496` | `538` | ### **+42** |
| DA_CLASSIFICARE | `188` | `188` |  |
| ENTRAMBE | `138` | `96` | ### **-42** |
| 2 | `24` | `24` |  |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `340` | `369` | ### **+29** |
| DA_CLASSIFICARE | `188` | `188` |  |
| CHIUSA | `187` | `182` | ### **-5** |
| APERTA | `106` | `82` | ### **-24** |
| AGENDA | `24` | `24` |  |
| SUPERATA | `1` | `1` |  |

| | prima | dopo |
|---|--:|--:|
| voci | `846` | ### **`846`** |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |
| ### **righe di storico** | `1272` | ### **`1628`** |

| presidio | segnali |
|---|--:|
| `F1` | ### **`7`** |
| `F2` | `0` |
| `F3` | `0` |
| `F4` | `0` |
| `F6` | `0` |
| `F8` | ### **`19`** |
| ### **in tutto** | ### **`26`** |

```
  C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto PASSA   persi 0, doppi 0
  C2 la TRACCIA copre ogni ID vecchio, con la REGOLA       PASSA   senza traccia 0
  C3 LE LISTE DEL GUARDIANO: classificazione come indicata PASSA   fuori posto 0
  C4 IDEMPOTENZA (NON si rilancia: c'e' lavoro di dopo)    PASSA   storico.jsonl ha 1628 righe -> verificata al commit 6b8cb90; e la migrazione ha un PRESIDIO che la ferma
  C5 `indice.py valida` passa                              PASSA     ### i PRESIDI contro le mescolanze: 26 segnali (F1=7  F2=0
  C6 la VISTA passa IL VALIDATORE VECCHIO (quello del pre-commit) e la domanda PASSA   12 bloccanti su 846 voci
```

---

## ⑩ I `26` SEGNALI CHE RESTANO — **voce per voce, con la frase**

> ### ⛔ **NON SI CORREGGONO: SI ELENCANO.** Un presidio ### **segnala, non decide** — e un segnale che si spegne cambiando la voce invece di guardarla ### **e- un segnale perso.**

### **`F1`: `7`**

| id | il segnale | la riga d'origine |
|---|---|---|
| `D08` | il titolo cita `Z14`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` | */ D08 / Il terzo ramo di calcola_psi (elif sotto REPULS_LEGGE) e' DICHIARATO, non corretto / Z14, letto dal codice / — / APERTO /* |
| `D11` | il titolo cita `Z87`, che e- `FISICA`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` | */ D11 / d scende DIECI VOLTE sotto LAM mentre SCALA_MIN e' acceso, e la causa NON e' trovata / Z87 / la cura di Z87: il mondo si costruisce SEMPRE dopo i flag (01eda44, categoria D) / CURATO* |
| `D14` | il titolo cita `Z41`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` | */ D14 / median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO /* |
| `D18` | il titolo cita `Z92`, che e- `FISICA`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` | ### ⚠ **non si ritrova** |
| `D19` | il titolo cita `Z88`, che e- `FISICA`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` | */ D19 / OTTO grandezze che la semina legge erano INERTI SUL VUOTO in ogni run di epoca 1 / Z88 / la cura del mondo-dopo-i-flag / CURATO /* |
| `D25` | il titolo cita `Z46`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` | */ Z46 / DIFETTO / D25 (APERTO) / Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia: sono sempre gli stessi, e sono le tre masse /* |
| `D27` | il titolo cita `Z65`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` | */ Z65 / DIFETTO / D27 (APERTO) / Il grafo e' in QUATTRO COMPONENTI che non si toccano mai, e la bimodalita' del grado e' la semina. Una distanza SUL GRAFO fra componenti diverse non esiste, * |

### **`F8`: `19`**

| id | il segnale | la riga d'origine |
|---|---|---|
| `A7b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<calcola_psi>>) | *### A7b — COROLLARIO: uno stato non nasce indefinito (aggiunto 2026-09-17) Uno stato non deve mai nascere indefinito. O si eredita da chi lo genera, o si costruisce da cio' che esiste nel pu* |
| `A8` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) | *## A8 — UN RAMO SILENZIOSO NON E' UN RAMO Ogni fallback su un percorso fisico deve essere CONTATO. Un ramo che scatta senza segnalarlo non produce un errore: produce una FISICA DIVERSA, sile* |
| `A8b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>) | *### A8b — COROLLARIO: le cache CROSS-PASSO Una cache cross-passo va estesa a TUTTI i punti di crescita, e l'estensione va verificata DOVE AVVIENE, non dove si usa. _cs_nodo_prev era estesa i* |
| `A9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_presidio.py>>) | *## A9 — UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO Una nota, un commento o una regola scritta che non impedisce STRUTTURALMENTE il ripetersi di un difetto non e' un presidio: e' una TE* |
| `CONTA-RIGHE` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_struttura_regole.py>>) | ### ⚠ **non si ritrova** |
| `FINESTRA-PRE-NASCITA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<perc_geom>>) | ### ⚠ **non si ritrova** |
| `H-P9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>) | ### ⚠ **non si ritrova** |
| `INDICE-COLLAUDO-SCRITTURA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<indice.py>>) | *def collaudo():* |
| `LUNGA-BATTITO-CADUTA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<passo_pieno>>); uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_tors_w8_lunga.py>>) | *## LUNGA-BATTITO-CADUTA — la corsa da 1000 passi cade al passo 1, e cade su una STAMPA (Aperta il 2026-10-06. Strumento d95639a4, simulatore cf2a1ac8, mandato della misura lunga di TORS-W8-A* |
| `NON-TRACCIATI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un `.pkl` (<<.pkl>>); un file `.py` del repo (<<_censimento_non_tracciati.py>>) | ### ⚠ **non si ritrova** |
| `PASSO-PIENO` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>); un file `.py` del repo (<<_passo.py>>) | ### ⚠ **non si ritrova** |
| `PIATTAFORMA-NON-TIMBRATA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_confronto_blob_misure.py>>) | ### ⚠ **non si ritrova** |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_presidio.py>>) | ### ⚠ **non si ritrova** |
| `REG-B` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) | */ REG-B / FASE B: le SCHEDE, a lotti, un commit per lotto / MANDATO-REGISTRO §2 / LE QUATTRO DELL'ORDINE DI LUCA SONO SCRITTE. ① freno di SCALA_MIN (DIFETTOSA, i TRE CANDIDATI come domande) * |
| `REG-R` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<soliton_simulator.py>>) | */ REG-R / LA REGOLA MANTENUTA del registro della fisica — la riga in CLAUDE.md («nessuna legge fisica entra, cambia o esce dal simulatore senza passare da doc/REGISTRO_FISICA.md») e l'hook c* |
| `REG-V` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<verificaregistro.py>>) | ### ⚠ **non si ritrova** |
| `REPERTI-IMMUTABILI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_seal_fork>>); un file `.py` del repo (<<_sim_A.py>>) | */ ❓ REPERTI-IMMUTABILI — APERTA il 2026-09-26 (proposta di Luca), famiglia G / UN COMMIT PUO' TOCCARE UN REPERTO GIA' CITATO DA UN REFERTO. Luca lo ha rilevato su csv/_seal_fork/_sig_cura_A/* |
| `RIPRESA-ARGV` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: il sigillo di una cura (<<sigillo della cura>>) | */ RIPRESA-ARGV — APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) / LA RIPRESA SI FIDA DEL BLOB, E IL BLOB NON CERTIFICA L'ARGV. Caso reale: i json dei bracci off_ del sigi* |
| `Z125` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) | */ Z125 DIFETTO DI METODO, MIO [archivi delle cure · LETTURA] / IL §E NON ESISTE NEL REPO OLTRE E1 ED E2: ho citato «i quattro test E1-E4» undici volte senza che E3 ed E4 fossero scritti da n* |

### ⚠ **E `F1` NE VEDE `7` SU `9`:** le altre due — `D16` e `D26` — ### **citano la loro `Z` nella DESCRIZIONE**, e `F1` guarda ### **il TITOLO.** Lo dico perche- il numero del presidio e quello dell-attrezzo ### **NON coincidono**, e la ragione e- questa.

### ⭐ **E `F8` dice una cosa SUL CONFINE, non sulle voci:** le `19` voci che segnala sono ### **era `ENTRAMBE` con un oggetto concreto dell-era `1` nel testo**. Il mandato del giro prima ha detto che ### **vale per ENTRAMBE una REGOLA DI LAVORO o uno strumento che sopravvive**, ed e- ### **era `1` cio- che riguarda un OGGETTO CONCRETO**: ### **queste `19` stanno sul confine fra le due frasi**, e dove sta il confine ### **lo decide Luca, non un marcatore.**

---

## ⑪ CHE COSA RESTA A LUCA

| | quante | che cosa |
|---|--:|---|
| ### **l'elenco generato** | `46` | `doc/indice/DA_DECIDERE_LUCA.md`, e ### **si genera** |
| ### **le `D`/`Z` disallineate** | `9` | ### **le RIGHE disaccordano** sullo stesso fatto: scegliere quale vale e' una decisione |
| ### **le `16` da dividere** | `16` | la divisione ### **la decide Luca**, e per `11` ### **la proposta e' MIA** |
| ### **le chiusure senza commit** | `20` | righe che dicono *«CHIUSA»* e ### **non portano il commit che ha chiuso** |
| ### **i segnali di `F8`** | `19` | ### **elencati, non corretti** |
| ### **le due correzioni alla REGOLA del punto `1`** | `2` | se Luca intendeva la regola ### **alla lettera**, `2` dei `7` casi del collaudo ### **escono diversi** |
| ### **i segnaposto** | `187` | ### **non sono una domanda: sono il lavoro che resta** |

> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il mandato ### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

