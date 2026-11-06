# 2026-11-06 — `cs` COL SOLITONE *(Luca `2026-11-06` `10:14`; la voce `5-bis` della coda)* -- ### **FERMO PRIMA DEL CODICE: la forma di `dtau` la sceglie Luca**

> **Le premesse di Luca:** `F3` e' il vuoto piu' simmetrico della famiglia, col ramo a `pi` piatto e un Goldstone quadratico; la parte dal vuoto dell'interazione della coppia matura e' attrattiva, uguale nelle due fasi, e si spegne entro `~50` nodi. **`cs` e' SPENTO in tutte le corse fatte.** **Le attese (IPOTESI):** un'attrazione indipendente dalla fase, come la gravita'; una velocita' limite locale; **probabilmente non a lungo raggio da sola.** **La `U` dinamica** *(il posto `A2`)* **resta in attesa.** **Un calcolo alla volta; il nucleo non si tocca senza Luca; nessun peso si regola.**
> **Raccolta dal repo:** con un agente di sola lettura; **i punti su cui poggia la proposta li ho riverificati io dal codice** *(segnati ✔)*.

## 1. CHE COSA E' `cs` OGGI NEL CODICE *(cercato per nome; le righe sono di oggi)*
- ✔ **`cs_k = Lambda_k / (Lambda_k + Lambda_c)`** -- `primo_ordine/flussi_parziali.py`, `def cs(lam, lambda_c, fuori)` *(`lambda_c > 0` asserito, nessun default)*; **la sua derivata** `cs'(Lambda) = Lambda_c / (Lambda + Lambda_c)^2` -- `primo_ordine/energia_pesata.py`, `def cs_primo`.
- ✔ **IL POSTO UNICO dove `cs` entra nel tempo:** `flussi_parziali.dtau_nodo(mot)`: **`mot.cs is None` -> `mot.dtau` tale e quale** *(il passo di oggi al bit)*; **altrimenti `dtau_k = cs_k x mot.dtau_k`.** **Da li'** `s_nodo = dtau_nodo / dtau_rif`, **`s_arco` la media armonica** *(`B-3`)*, `theta = pi dtau_arco / dtau_rif` *(`CAMM-SPOSTAMENTO`, `CAMM-GROVER`)*, **il cono `0 < s <= 1` asserito** *(`_nel_cono`, «non e' un clip»)*, **`dtau_rif = 1`** *(l'unita')*.
- ✔ **IL GENERATORE PESATO:** `CAMM-FASE-VUOTO` *(`leggi.yaml`)*, `cs_primo(Lambda) x (H_nodo + somma_archi(dw_dcs x H_arco))`; ### **«A FORMA SPENTA QUESTA LEGGE NON ESISTE»**: `energia_pesata.applica` **esce subito se `mot.cs is None or mot.lambda_c is None`**, e **asserisce `mot.dtau` uniforme.**
- ✔ **IL TICK CON `cs` ESISTE GIA' NEL NUCLEO:** `primo_ordine/tick.py`, **`tick_con_cs(st, mot, par, lambda_c, salta)`**, con **`cs_al_centro`** *(il punto fisso di `cs` sullo stato al CENTRO del palindromo, fino a `GIRI_MAX = 120` giri)*; `flussi_parziali.accendi_cs` *(la variante «all'inizio del passo»: il caso che DEVE fallire)*, `spegni_cs`.
- ✔ **LA SCENA DEL SOLITONE OGGI** *(misurato su `costruisci(V.N, V.L)`)*: **`mot.cs = 0.15` su ogni nodo, `mot.lambda_c = None`, `mot.dtau = 1`** -- ### **cioe' `dtau_nodo = 0.15` UNIFORME e `CAMM-FASE-VUOTO` inerte** *(`csv/_energia_del_legame.py`: `mot.cs = np.full(n, VC.S)`, `mot.lambda_c = None`; `_vuoto_vivo_B` lo asserisce: «cs spento»)*. **Il `0.15` e' l'`s` della corsa** *(`BG-F-0.15`, `V.CORSE`)*.

## 2. LE FORME GIA' PROPOSTE O PROVATE, CON GLI ESITI *(dai referti; non rigirati)*
| che cosa | dove | l'esito registrato |
|---|---|---|
| **`D0`:** `cs` spento = il passo di oggi al bit; «la forma spenta non e' `Lambda_c = 0`» | `primo_ordine/_collauda_cs.py` | il criterio del collaudo |
| **`D2`:** `cs` al centro del palindromo contro `cs` all'inizio del passo | `_collauda_cs_centro.py`; `doc/referti_l2/cs_al_centro.txt` | **la pendenza `2.001` al centro** *(PASSA)* contro `0.997` all'inizio *(il caso che deve fallire)*; `11`-`47` giri, `Lambda_c` `0.8`, `8`, `80` |
| **la convergenza del punto fisso** | `doc/referti_l2/ciclo_cs.txt` | **a `Lambda_c / Lambda = 0.01`: taglia `32` NON converge, `16` converge** |
| **`D3`:** `cs` acceso sul primo livello | `doc/referti_l2/cs_l1_d3.txt` | `0` violatori del tempo PASSA; ### **`M-B2` (la pendenza di `H_tot`) `-0.003` FALLISCE**; `cs` uniforme `1.951` / `2.009` |
| `D3` col termine di fase | `cs_l1_d3_con_la_fase.txt` | la pendenza di `G` `1.254` FALLISCE |
| `C1` | `strada_d_c1_c2_c5.txt` | `1.002` FALLISCE *(poi detto «un artefatto» di `g_pesata`: `energia_pesata.py`; `leggi.yaml` registra `2.030` per `G`)* |
| la regressione `D0` | `energia_pesata.py`; `doc/TASK_HISTORY/2026-10-21_regressione_d0.md` | `GIRI_MAX_OMEGA` da `120` a `200`: `D0` con `cs` acceso ne chiede `~137` *(`Lambda_c = 8`)* |
| la forza da un gradiente di `cs` imposto a mano | `csv/_forza_da_cs.py`; `doc/referti_l2/forza_da_cs.txt` | i controlli (`eta = 0`, lo specchio, la linearita', le taglie) FALLISCONO |
| l'era `1` | `doc/REPERTO_cs_dinamico_spento.md` | «`--cs-dinamico` era SPENTO nel braccio OFF. E accenderlo non basterebbe» |
- ### **«La voce `cs` <-> clock della roadmap»: NON TROVATA per nome** *(cercati «cs» con «orologio»/«clock» in `doc/ROADMAP_fork_SU2.md`, `MAPPA.md`, `PIANO_era2.md`, `REGISTRO_FISICA.md`)*. **Le domande aperte nell'indice:** [[DOMANDA-IL-VALORE-DI-LAMBDA-C]] *(AGENDA)*; [[DOMANDA-DOVE-VIVE-LAMBDA-C-SENZA-UN-VALORE]] *(AGENDA)*.
- **Il posto `A1`** *(`leggi.yaml`, la moneta di spin)*: «`eps * dtau` e' cio' che conta, e la forma di `dtau` NON e' decisa»; *(`motore.py`, l'intestazione: «la sua forma non e' decisa: qui entra come dato»)*. **Il posto `A2`:** «`U` e' FERMA finche' la `U` dinamica non si deriva».

## 3. ACCENDERE `cs` TOCCA IL NUCLEO?
- ### **NO, per la forma che c'e':** **il tick con `cs` e' gia' nel nucleo** *(`tick.tick_con_cs`)*; ### **la corsa lo chiamerebbe invece di `percorri_tick`** *(un cambio in `csv/solitone/accensione.tick`, con un flag spento di default: le corse vecchie al bit)*. **Nessuna configurazione o flag esiste oggi** *(`primo_ordine/config/prova.yaml` non ha chiavi di `cs`; nessun `--cs` nel CLI dell'era `2`)*.
- ### **MA NON E' «UN PARAMETRO»: servono DUE cose, e una e' un numero:** **`Lambda_c`** *(il valore e' la domanda aperta [[DOMANDA-IL-VALORE-DI-LAMBDA-C]])*, ### ⚠ **e con `Lambda_c` dato si accendono INSIEME il tempo locale E `CAMM-FASE-VUOTO`** *(il generatore pesato esiste solo con `lambda_c`)*: ### **due meccanismi con un interruttore solo** *(la regola d'oro: uno alla volta)*.
- ### **Una forma diversa da `Lambda / (Lambda + Lambda_c)` toccherebbe il nucleo** *(`flussi_parziali.cs`, `energia_pesata.cs_primo`, e la tabella)*: **decisione di Luca.**

## 4. LA PROPOSTA, MOTIVATA *(per la prima prova; la SCELTA e' di Luca)*
- ### **(P) LA FORMA CHE C'E', `cs = Lambda / (Lambda + Lambda_c)`, con `Lambda_c` RICAVATO dalla continuita' col vuoto di oggi:** **nel vuoto `F3` `Lambda = 6` esatto** *(misurato su `TBS_stato_000000`: min = max = `6.000000000000`)*; **chiedere che l'orologio del vuoto resti quello di tutte le corse, `cs_vuoto = 0.15`**, ### **da' `Lambda_c = 6 x (1 - 0.15) / 0.15 = 34`** -- **non tarato sui risultati: e' l'unico valore per cui lontano dal solitone NIENTE cambia.** ### ⚠ **Ma eredita lo `0.15`, che e' a sua volta un numero della corsa** *(`BG-F-0.15`)*: **dichiarato.**
  - **Che cosa farebbe vicino al solitone** *(dallo stato di `TBS` a `t 30000`: `Lambda` da `0.121` a `14.50`)*: **`cs` da `0.0036` a `0.30`** -- ### **l'orologio rallenta di `~40` volte dove il vuoto e' svuotato e accelera di `~2` dove e' gonfio**: **un effetto GRANDE, non una perturbazione.** **Il cono regge per costruzione** *(`cs < 1`)*. **A `t 0` `Lambda = 6` ovunque, quindi `cs = 0.15` ovunque: la partenza e' identica a quella di `TB3`.**
  - **La convergenza:** **`Lambda_c / Lambda` fra `2.3` e `280`** *(lontano dallo `0.01` che non convergeva)*.
- ### **LE ALTERNATIVE:**
  - **(A1) `Lambda_c` come parametro dichiarato e scelto da Luca** *(la domanda dell'indice)*: un numero, quindi `A1`.
  - **(A2) il solo tempo locale, SENZA `CAMM-FASE-VUOTO`** *(`mot.cs` dal `Lambda` di ogni tick, `lambda_c` lasciato `None`)*: ### **un interruttore alla volta, come vuole la regola** -- **ma `mot.cs` si scriverebbe da fuori del nucleo** *(come `csv/_forza_da_cs.py`)*, **e la conservazione dell'energia col generatore NON pesato non e' garantita** *(`D3`, `M-B2` fallito)*: **da misurare, non da supporre.**
  - **(A3) `cs` proporzionale, `0.15 x Lambda / 6`:** **nessun `Lambda_c`, ma il cono non e' garantito** *(sopra `Lambda = 40`)* **e la forma e' nuova** *(il nucleo)*.
- ### **LA MIA RACCOMANDAZIONE:** **(P) con l'ordine (A2) prima** -- **il tempo locale da solo** *(un interruttore)*, **poi `CAMM-FASE-VUOTO`** *(il secondo)*: ### **cosi' se il singolo cambia si sa quale dei due lo ha cambiato.** **Ma (A2) scrive `mot.cs` da fuori del nucleo:** **se Luca preferisce il tick del nucleo cosi' com'e', (P) intero, dichiarando che sono due meccanismi.**

## 5. LE LETTURE *(di Luca, scritte prima)*
- **(s1)** `cs` non cambia nulla entro il rumore; **(s2)** il singolo cambia *(stabilita', forma, emissione)*; **(s3)** la coppia con `cs` si attrae dove quella senza no, o piu' lontano, in tutte e due le fasi: **un'attrazione come la gravita'**; **(s4)** altro.

## 6. LE DOMANDE A LUCA *(il FERMO; il criterio di chiusura: le sue risposte, scritte qui)*
1. ### **La forma:** (P) *(`Lambda_c = 34` dalla continuita' col vuoto)*, (A1), (A3), o altra?
2. ### **Uno o due interruttori:** prima il solo tempo locale (A2), poi il generatore pesato -- o tutti e due insieme col tick del nucleo?
3. **Da quando:** **`cs` acceso dal tick `1`** *(a `t 0` e' `0.15` ovunque, la stessa partenza)* **o dopo la rampa** *(`K` tick)*? **La mia proposta: dal tick `1`.**

## 7. TODO
1. Questo task history, un commit. **FERMO.** 2. Dopo le risposte: il codice *(il flag spento di default)*, `D6`, la cassetta, `TCS`.
