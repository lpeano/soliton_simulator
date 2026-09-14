# PREDIZIONE — lo scuotimento contiene gia' una DISSIPAZIONE ALLINEANTE? (Kuramoto emergente?)

> **Scritta e committata PRIMA dell'analisi e dei test.** Branch `fork-su2`, blob **2277e9a0**.
> Data: 2026-09-14. **Nessuna modifica a `soliton_simulator.py`**: qui non si aggiunge niente al
> sistema, si misura cosa c'e' gia' dentro.

---

## 0. LA DOMANDA

Misurato finora: la dinamica dei Bloch e' **precessione pura** (Rodrigues, `:2021` — ruota
*attorno* al campo, **conserva** l'angolo fra `n` e l'asse, non allinea) **+ rumore + normalizzazione**.
Manca il termine **dissipativo** `n -> B` (il "tira verso", tipo Gilbert / Kuramoto). Senza quello:
congelato o rumore, e nient'altro.

**Ipotesi (fluttuazione-dissipazione):** un rumore porta con se' una dissipazione compagna, col
coefficiente **fissato dal rumore**, non scelto. Lo scuotimento fa `_nb += rumore` e **poi
normalizza** (`:1803-1804`). La normalizzazione di un versore perturbato **non e' neutra**: puo'
introdurre un drift sistematico. La domanda e' se quel drift **allinea ai vicini** (= Kuramoto
emergente, zero manopole) o se e' solo contrazione/isotropizzazione.

---

## 1. I TRE ESITI (definiti prima)

- **A (EMERGENTE):** il drift e' `~ -(coef)(n - <n_vicini>)`, cioe' un rilassamento **verso la media
  dei vicini**, col coefficiente fissato da `amp^2`. -> Kuramoto emergente, zero manopole.
- **B (CONTRAZIONE ISOTROPA):** il drift e' funzione **del solo `n`** (es. `-(coef)n`), senza
  direzione privilegiata dai vicini. -> nessuna dissipazione allineante nel rumore.
- **C (NESSUN DRIFT):** neutro all'ordine dominante. -> il FDT non morde qui.

> **DICHIARAZIONE: "Kuramoto emergente" e' confermato SOLO nell'esito A, e solo se il coefficiente
> ha SEGNO allineante e scala non trascurabile.** Un drift che esiste ma non guarda i vicini non e'
> un Kuramoto, comunque lo si chiami.

---

## 2. LA MIA PREDIZIONE, E UNA DICHIARAZIONE DI ONESTA' SUL "PRIMA"

**Sul rumore da solo (Test 3a) non ho un vero dubbio, e devo dirlo.** L'espansione a `O(amp^2)` di
`(n + a g)/|n + a g|` e' un calcolo di poche righe che so gia' fare, e soprattutto **c'e' un
argomento strutturale che non richiede nemmeno il calcolo**:

> Nel codice lo scuotimento del singolo nodo **non legge i vicini** (`:1803`: rumore locale
> indipendente per nodo, ampiezza da `I2` del nodo, poi normalizzazione). Il drift e' quindi per
> forza **funzione del solo `n`**. Una cosa che non guarda i vicini **non puo'** allinearli.

Quindi **predico B/C per il rumore da solo**, e lo predico con sicurezza, non per intuizione. Sarebbe
disonesto presentare come incerta una cosa che l'algebra decide in anticipo. Scrivo comunque
l'espansione per intero (§3 dell'esito) perche' la **forma** del drift e il suo **coefficiente**
sono informativi anche quando il verdetto e' B.

**Dove invece NON so, ed e' il vero esperimento: il Test 3b (precessione + rumore).** Li'
l'accoppiamento ai vicini **c'e'**, attraverso il campo `B`. E c'e' un meccanismo noto in fisica per
cui una rotazione ad **asse fluttuante** produce un drift medio che non e' una rotazione (il
*motional narrowing*): le componenti perpendicolari all'asse medio decadono piu' in fretta di quella
parallela. Se quel decadimento agisse come un rilassamento `n -> B`, sarebbe una dissipazione
allineante **emergente dalla combinazione**, non dal rumore da solo.
**Non ho calcolato se sopravvive qui**, e non voglio scommettere per non incorniciare la lettura.
Le due baseline gia' misurate (`chi = 0` congelato, `chi = 90` rumore) dicono che **nel sistema
completo non succede** — ma il sistema completo ha anche mitosi, crescita, densita' variabile: un
test isolato a due nodi puo' rivelare un effetto debole che li' e' sommerso. **E' per questo che 3b
si fa.**

---

## 3. IL CRITERIO NUMERICO (fissato prima)

Riferimenti sempre accanto al misurato:

| stato | angolo medio fra due Bloch |
|---|---|
| allineato | **0 gradi** |
| isotropo (casuale) | **90.000 gradi** (media di `sin(chi)/2`) |
| antipodale | 180 gradi |

- **3a (solo rumore+norm):** due Bloch a 60 gradi, iterare `n -> (n + a g)/|n + a g|`. L'angolo
  medio -> 0 (allinea), -> 90 (isotropizza), o resta?
  **Analitico e numerico DEVONO coincidere**: se non coincidono, la discrepanza e' essa stessa il
  reperto e ci si ferma (par.5 di CLAUDE.md).
- **3b (precessione + rumore + norm):** stessa cosa piu' la precessione di Rodrigues con `B` dai
  vicini. Allinea, disordina, o resta?
- In entrambi: controllare **`|<n>|` globale**, perche' `chi -> 0` da solo non distingue *domini* da
  *collasso* (lezione dell'esperimento Kuramoto, `doc/PREDIZIONE_kuramoto.md`).

---

## 4. SE L'ESITO E' B/C — il messaggio onesto, scritto prima

Non e' un fallimento, e non va presentato come tale:

> **"Lo scuotimento NON contiene una dissipazione allineante. Un Kuramoto in questo sistema sarebbe
> IMPOSTO, non emergente."**

E' un risultato **pulito e definitivo** su una domanda ben posta, e chiude una via: dice che la
struttura non si puo' ottenere gratis dal rumore che c'e' gia'. Sapere che una porta e' chiusa vale
quanto trovarla aperta — di piu', se evita di cercarci dietro per settimane.

---

## 5. COSA QUESTO TEST NON FARA'

Non aggiunge un termine `n -> B` al simulatore: sarebbe **Kuramoto imposto con un altro nome**, cioe'
esattamente cio' che il test deve saper distinguere. Non accende `KURAMOTO_SU2`. Non modifica lo
scuotimento. Non conclude su olonomia o gravita'. E un test a due nodi **non e' il sistema**: dice
cosa fa il meccanismo isolato, non cosa fa dentro la dinamica completa — dove infatti ci sono gia'
tre stati misurati, tutti senza struttura.
