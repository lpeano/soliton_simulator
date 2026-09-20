# 2026-09-20 -- IL CENSIMENTO DEL SOSPESO, e i TRE PRESIDI PERMANENTI

Mandato: *"DUE LAVORI DI SOLO TESTO, mentre i run girano."* Ordine imposto: **① censimento, poi
② presidi** *(i presidi sono essi stessi una voce sospesa: farli prima costringerebbe a riscriverli
nella lista dopo)*.

Stato all'avvio: i due run A/B a `sep = 4.0` **stanno girando** (ramo A frame 30, ramo B frame 25 di
500). Simulatore `edb8f844` (blob git `b44f50ce`), **e non si tocca**. HEAD `1504d9b`.

---

## 1. RAGIONAMENTO PRELIMINARE -- cosa credo PRIMA di guardare

### 1.1 La premessa del mandato che prendo sul serio piu' di tutte

> *"Questo elenco viene dalla conversazione, non dal disco. Oggi TRE premesse mie su tre erano
> false."*

**E non e' un avvertimento generico: e' successo oggi, tre volte, e due erano MIE.** I numeri su
`|tw|` *(mediana 7.9 contro 2.25 misurata)*, l'A/B di `chi_basc` *(era la finestra)*, e
`nb_grav_proiez` *(classificata male)*. **Quindi l'elenco del par.1.1 del mandato non e' la lista:
e' una LISTA DI CANDIDATI da verificare uno per uno dal disco.**

**Mi aspetto di trovare almeno una voce dell'elenco gia' CHIUSA**, e almeno una **mancante**. Se non
ne trovo nessuna delle due, **sospetto di non aver guardato abbastanza**, non che l'elenco fosse
perfetto.

### 1.2 Cosa ho gia' visto, e cosa cambia

**Ho cercato una lista esistente in `doc/STATO_RUN.md` e ne ho trovate TRE, parziali e sparse**
(righe ~96, ~161, ~237): *"DA FARE A RUN FINITO"*, *"Cosa resta da fare quando il run e'
definitivamente chiuso"*, *"La voce TODO del ② -- il pannello fedele"*.

> **Nessuna delle tre e' LA lista: sono tre code di tre lavori diversi.**
> **Il mandato vieta di crearne una seconda se una esiste. Ne esistono TRE, e nessuna e' quella.**
> **Quindi: UNA sezione nuova che le ASSORBE e le cita, e le tre vecchie rimandano a quella.**
> Creare la quarta e lasciare le tre sarebbe **esattamente il difetto** che il mandato descrive.

### 1.3 Cosa NON so

- **non so quante voci siano davvero aperte.** Il mandato ne elenca ~11; il registro
  `RAMIFICAZIONI.md` ha **151 voci** secondo la misura del 19/9, e non so quante siano `APERTA`;
- **non so se la marcatura di validita' (par.1.3) sia fattibile su tutte** in un giro. Il mandato mi
  autorizza a marcare **almeno quelle citate negli ultimi sette giorni** e a dirlo -- e **mi aspetto
  di dover usare quell'autorizzazione**, perche' 151 voci di prosa libera non si marcano a mano
  senza sbagliarne;
- **non so se esista un meccanismo praticabile per il par.2.3**, e il mandato dice esplicitamente
  che *"nessun meccanismo, resta una regola scritta"* e' un esito onesto. **Non parto dall'idea che
  ne trovero' uno.**

### 1.4 Cosa mi aspetto sul conto degli strumenti

Il mandato da' **81 su disco, 34 in inventario, 47 mancanti (42 %)**. **Verifichero' il conto dal
disco**: se il mio conteggio differisce, **il numero giusto e' quello che conto io, e lo dico**.
Mi aspetto che **la maggioranza dei 47 siano SONDE usa-e-getta, non sigilli** -- e in quel caso
*"47 mancanti"* sovrastima il problema, perche' una sonda col suo referto costa una riga.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### 2.1 PARTE ① -- i passi, e cosa decide ciascuno

| passo | cosa decide | cosa mi FERMA |
|---|---|---|
| **A** cercare le liste esistenti | se si amplia o si crea | -- *(fatto: tre parziali, nessuna e' quella)* |
| **B** verificare le 11 voci del mandato **dal disco** | quali sono vive, chiuse, o assenti | **una voce che non trovo: la dichiaro NON TROVATA, non la invento** |
| **C** cercare le voci che il mandato NON elenca | la completezza | -- |
| **D** scrivere la sezione unica | -- | -- |
| **E** la marcatura di validita' | il presidio contro le tre ritrattazioni | **se sono troppe: marco le recenti e DICHIARO il resto** |

### 2.2 Il criterio per «a che punto e'» -- e non e' un'opinione

Per ogni voce, lo stato si legge **da un fatto verificabile**, non da un ricordo:
- **CHIUSA** se il registro dice `CHIUSA` **e** cito il commit/sigillo che l'ha chiusa;
- **APERTA, mai iniziata** se non esiste nessun file/commit che la tocchi;
- **APERTA, iniziata** se esiste un referto o un task history ma nessuna chiusura;
- **DECISIONE DI LUCA** se il blocco e' una scelta di fisica, non lavoro da fare.

> **La colonna «chi decide» separa cio' che aspetta ME da cio' che aspetta LUCA.**
> **E' il punto operativo del mandato: senza, una voce aspetta l'altra per giorni.**

### 2.3 La marcatura di validita' -- il criterio, fissato PRIMA

```
VALE SEMPRE            un difetto di codice, una legge, un fatto strutturale letto dal sorgente
VALE PER QUELLA SCENA  un numero misurato su sep=8 / quattro componenti / una finestra
DA RIVERIFICARE        la premessa sotto e' cambiata (scena nuova, blob nuovo, cura applicata)
```
**Il discriminante operativo:** *«se rigirassi questo su un'altra scena, il numero cambierebbe?»*
Se si' -> `VALE PER QUELLA SCENA`. Se la domanda non ha senso perche' non c'e' un numero (e' una
lettura del codice) -> `VALE SEMPRE`.

### 2.4 PARTE ② -- e il par.2.3 e' quello che conta

Le tre regole in `CLAUDE.md` sono **scrittura**, e le scrivo. **Ma il mandato stesso dice che
scriverle NON BASTA** (`A9`), e chiede di **PROPORRE un meccanismo e FERMARSI prima di cablarlo**.

**Cosa valutero', e il criterio di valutazione e' `A9` stesso -- IMPEDISCE o RICORDA?**
- un **sigillo** che confronti disco e inventario e FALLISCA se divergono -> **ricorda**, perche'
  qualcuno deve girarlo;
- un **hook di commit** -> **impedisce**, ma e' locale alla macchina e **non vive nel repo**: chi
  clona non ce l'ha;
- **un controllo dentro `_presidio.avvia()`** -> gira **automaticamente a ogni strumento lanciato**,
  quindi **non dipende dal ricordarsene**. **E' il candidato che mi aspetto migliore**, ma ha un
  costo da misurare e un rischio da dichiarare: **un presidio che blocca un run per un difetto di
  documentazione sarebbe peggio del difetto.**

**Cosa mi FERMEREBBE dal proporne uno:** se nessuno dei tre impedisce davvero, **lo dico**. Il
mandato lo autorizza esplicitamente, e un presidio finto e' peggio di una regola dichiarata tale.

### 2.5 Il triage del par.2.2, e cosa NON e' un'omissione

```
SIGILLO        -> inventario COMPLETO: comando + blob + ri-girabilita'
SONDA          -> una riga che dice DOVE sta il referto
SONDA SENZA REFERTO -> ⚠ e' un REPERTO: una misura fatta e mai scritta
SIGILLO NON RI-GIRABILE -> ⚠ e' un `Z31` NUOVO, non un'omissione di inventario
```
**La distinzione non e' burocratica:** inventariare una sonda come se fosse un sigillo **gonfia il
conto e nasconde i sigilli veri**.

### 2.6 Il vincolo sui run, e come lo rispetto

**Nessun file del percorso in uso si tocca** -- simulatore, driver, `_presidio.py`, `_stato_run.py`
e tutto cio' che i due processi hanno importato. **`_presidio.py` E' IMPORTATO dal driver**, quindi
**il meccanismo del par.2.4, se sara' li', si scrive ma NON si applica finche' i run non chiudono.**
**Lo dichiaro qui perche' e' il punto in cui il presidio del par.9 verrebbe violato in buona fede**,
ed e' gia' successo il 19/9.

**Il controllo che i run avanzino:** *"se passa piu' del TRIPLO della cadenza attesa senza un file
nuovo, e' piantato"*. Cadenza = 20 frame x ~25 s = **~500 s**, quindi la soglia e' **~1500 s**.
**E se si pianta: `py-spy dump` PRIMA di qualunque cosa, MAI uccidere** -- il blocco del run a 6000
al passo 2700 non si sapra' mai perche' fu ucciso senza catturare lo stato.

---

## 3. TODO DEL NEXT STEP

- [x] verificare se una lista esiste -> **TRE parziali in `STATO_RUN.md`, nessuna e' quella**
- [ ] verificare **dal disco** le 11 voci del mandato, una per una
- [ ] cercare le voci **non elencate** dal mandato
- [ ] la sezione unica in `doc/STATO_RUN.md`, che **assorbe e cita** le tre parziali
- [ ] la marcatura di validita' -> **riportare quante marcate e quante no**
- [ ] **riportare il conto**: quante voci, quante decide Luca
- [ ] le tre regole in `CLAUDE.md`
- [ ] **proporre il meccanismo del par.2.3 e FERMARSI** -- non cablare
- [ ] il triage dei 47 + il conto dei flag contro il `README`
- [ ] controlli periodici sui due run (soglia **~1500 s** senza snapshot nuovo)
