# LE MEMORIE CHE MANCANO, E IL BILANCIO — *rapporto del 2026-10-07*

*(Mandato di Luca del 2026-10-07, punto `1`, §`2`-§`6`. ### **NESSUN CODICE DI FISICA.** Il simulatore resta ### **`b8c21049`** — `sha1` dei ### **byte grezzi**. ### **`doc/ASSIOMI.md` non toccato qui:** `A15` e' in `73d7650`.)*

> ### 📌 **LE REGOLE CHE GOVERNANO QUESTO RAPPORTO:** `A15` *(la memoria e' dinamica, locale, e cio' che dimentica si trasforma)*, ### **`L-MEMORIA-PRIMA`** *(i sette campi, in testa a `doc/RIPRESA_2026-10-07.md`)*, e i due principi ### **`P-DECADIMENTO`** e ### **`P-MEMORIA`** *(scheda in `doc/REGISTRO_FISICA.md`)*.

> ### ⛔ **E OGNI AFFERMAZIONE PORTA LA SUA EVIDENZA:** funzione, riga sul blob, e il comando con cui l'ho verificata. ### **Dove NON l'ho verificata, la riga lo dice** — `NON VERIFICATA` non e' una reticenza, e' un dato.

---

# §`2` — **IL CENSIMENTO COMPLETO DELLO STATO**

**LA LISTA NON E' SCRITTA A MANO:** viene dai due registri del simulatore, letti ### **dall'AST** — `REGISTRO_STATO` *(le forme `("m",)` sono per ARCO, le altre per NODO)* e `REGISTRO_METRI` *(che porta `phi`, `i`, `j`)*.

| | |
|---|--:|
| grandezze di stato ### **totali** | ### **34** |
| per ### **ARCO** | ### **10** |
| per ### **NODO** | ### **24** |

> ### 📌 **IL COMANDO:** un censimento `AST` che per ogni nome cerca ogni `Assign` e `AugAssign` il cui bersaglio contenga `self.<nome>` o `net.<nome>`, e registra ### **la funzione che la contiene.** ### **Prende anche le scritture per ELEMENTO** *(`self.X[idx] = ...`)*, perche' il bersaglio e' un `Subscript` su un `Attribute`.

### ⚠ **E IL LIMITE DEL CENSIMENTO, DICHIARATO — e mi ha prodotto un FALSO POSITIVO**

Un censimento di ### **assegnazioni** non vede le ### **MUTAZIONI IN LOCO** *(`.append`, `.extend`, `ufunc.at`, o un helper che muta l'oggetto ricevuto)*.

| | |
|---|---|
| cercate a parte | `self.X.append/extend/fill/...` e `np.add.at(self.X, ...)`: ### **`3` in tutto il file**, e ### **nessuna su un array di stato** |
| ### ⛔ **il falso positivo** | ### **`conc_nodi`** risultava *congelata*, e ### **NON lo e'**: si aggiorna per mutazione dentro ### **`_agg_voce`**, chiamato da `_registra_concorrenza`. ### **Il codice stesso lo dice** *(`mitosi`: «piu' la crescita per MUTAZIONE di `conc_nodi` (`.append`, che l'AST non vede)»)* |

## LA TAVOLA — **per ARCO** *(10)*

| grandezza | chi la scrive *(dall'AST)* | ha memoria? | decade verso | il suo tempo | il decadimento fa sparire energia? |
|---|---|---|---|---|---|
| `_rep` | `__init__`, `_allaccia`, `_rn_div_rep`, `_rn_sch_rep`, `decidi_divisione` *(6 scritture)* | INSEGUE un bersaglio di repulsione | il suo bersaglio | NON VERIFICATA in questo giro | SI, gia' dichiarato in `A14` n.3 |
| `d` | `__init__`, `_allaccia`, `_rn_div_d`, `_rn_sch_d`, `step` *(8 scritture)* | istantanea: la lunghezza vera, scritta dallo `step` | — | — | no |
| `d0` | `__init__`, `_allaccia`, `_rn_div_d0`, `_rn_sch_d0`, `_smp_chiudi`, `decidi_divisione`, `memoria_hebbiana_moto`, `step` *(15 scritture)* | INSEGUE `d` | `d` | `tau_p_loc = max(t_luce, t_visco)` — DERIVATO | SI: il rilassamento non cede a nessuno |
| `i` | `__init__`, `_allaccia`, `_rn_div_i`, `_rn_sch_i` *(4 scritture)* | topologia, NON una memoria | — | — | no |
| `j` | `__init__`, `_allaccia`, `_rn_div_j`, `_rn_sch_j` *(4 scritture)* | topologia, NON una memoria | — | — | no |
| `peq` | `__init__`, `_allaccia`, `_rn_div_peq`, `_rn_sch_peq`, `step` *(9 scritture)* | INSEGUE `rho` + diffonde | `rho` | `tau_bg_loc = 1/|phivel_arco|` DERIVATO, **ma la diffusione usa `TAU_DIFF = 1.0` NUDO** | SI: il rilassamento non cede a nessuno |
| `tw` | `__init__`, `_allaccia`, `_rn_div_tw`, `_rn_sch_tw`, `step` *(6 scritture)* | ⭐ **INTEGRA**: e' LA MEMORIA VERA del sistema | zero, con `-dt_e*tw/tau_tw` | ⭐ **`tau_tw = 2pi/|Delta omega|` — DERIVATO, l'esempio di `A15.2`** | ⛔ **SI, ed e' il termine n.1 del bilancio** |
| `twp` | `__init__`, `_allaccia`, `_rn_div_twp`, `_rn_sch_twp`, `step` *(6 scritture)* | la fase precedente d'arco: **un ritardo, non una memoria** | — | un passo, per costruzione | no |
| `twp_dip` | `__init__`, `_allaccia`, `_rn_div_twp_dip`, `_rn_sch_twp_dip`, `step` *(5 scritture)* | il dipolo precedente d'arco: **un ritardo** | — | un passo; `NaN` alla nascita | no |
| `vd` | `__init__`, `_allaccia`, `_rn_div_vd`, `_rn_sch_vd`, `step` *(6 scritture)* | INERZIALE (velocita' della lunghezza) | smorzata da `beta*vd` | `beta`, e la violazione e' gia' in `A14` n.2 | SI, gia' dichiarato in `A14` |

## LA TAVOLA — **per NODO** *(24)*

| grandezza | chi la scrive *(dall'AST)* | ha memoria? | decade verso | il suo tempo | il decadimento fa sparire energia? |
|---|---|---|---|---|---|
| `_cs_nodo_prev` | `__init__`, `_rn_div_cs_nodo_prev`, `step` *(3 scritture)* | ritardo di un passo | — | un passo | no |
| `_deg` | `__init__`, `_grado` *(2 scritture)* | derivata della topologia | — | — | no |
| `_nb` | `_passo_spinoriale`, `_rn_div_nb`, `memoria_hebbiana_moto`, `misura_spin_picco_massa` *(9 scritture)* | il versore di Bloch: ruotato dallo `step` | — | — | NON VERIFICATA |
| `_nb_prec` | `_passo_spinoriale`, `_rn_div_nb_prec` *(2 scritture)* | ritardo di un passo | — | un passo | no |
| `_nb_ret` | `__init__`, `_bloch_ritardato`, `_rn_div_nb_ret` *(4 scritture)* | ⭐ il Bloch RITARDATO: `slerp` verso il corrente | il Bloch corrente | `d/cs` (tempo-luce) — DERIVATO | NON VERIFICATA |
| `_psi_prec` | `__init__`, `_rn_div_psi_prec`, `step` *(3 scritture)* | ritardo di un passo | — | un passo | no |
| `_psi_spin_prec` | `_rn_div_psi_spin_prec`, `step` *(2 scritture)* | ritardo di un passo | — | un passo | no |
| `_psi_spinor` | `__init__`, `_estendi_psi_spinor`, `_passo_spinoriale`, `_rn_div_psi_spinor` *(6 scritture)* | lo spinore: evoluto dal passo spinoriale | — | — | NON VERIFICATA |
| `_spinor_lift` | `__init__`, `_aggiorna_lift_spinoriale`, `_passo_spinoriale`, `_rn_div_spinor_lift` *(4 scritture)* | il lift: aggiornato dal passo spinoriale | — | — | NON VERIFICATA |
| `conc_nodi` | `__init__`, `_rn_div_conc_nodi`, `_rn_sch_conc_nodi` *(3 scritture)* | ⚠ **il mio censimento la dava CONGELATA: FALSO POSITIVO** — si aggiorna per MUTAZIONE in `_agg_voce`, che l'AST non vede | — | — | no |
| `eta` | `__init__`, `_rn_div_eta`, `_rn_sch_eta`, `semina`, `step` *(7 scritture)* | INTEGRA l'eta' del nodo | — | — | no |
| `mem_mot` | `__init__`, `_rn_div_mem_mot`, `_rn_sch_mem_mot`, `memoria_hebbiana_moto`, `semina` *(6 scritture)* | ⭐ MEDIA MOBILE: `(1-plast)*mem + plast*grad_tw` | ⛔ **VINCE L'ULTIMO**: non e' un bilancio, e' una sostituzione | `plast = tanh(|grad_tw|)` — DERIVATO **dallo stato** | ⛔ **SI**, ed e' `A14` n.4 + `MEM-HEBB-VERSO` |
| `omega_s` | `__init__`, `_passo_spinoriale`, `_rn_div_omega_s`, `semina` *(6 scritture)* | INSEGUE una correzione | `-omega_src/_tau` | `d_nodo/cs_nodo` — DERIVATO (`--tau-luce` e' nell'argv) | ⛔ **SI**: il decadimento non cede a nessuno |
| `perc_chi` | `__init__`, `_rn_div_perc_chi`, `_rn_sch_perc_chi`, `semina`, `step` *(6 scritture)* | DISCRETA: basculamento (`int64`) | non decade: **salta** | — (nessuna isteresi) | no (e' una carica, non energia) |
| `perc_geom` | `__init__`, `_rn_div_perc_geom`, `_rn_sch_perc_geom`, `semina`, `step` *(5 scritture)* | DISCRETA: basculamento (`int64`) | non decade: **salta** | — (nessuna isteresi) | no |
| `perc_tw` | `__init__`, `_rn_div_perc_tw`, `_rn_sch_perc_tw`, `semina` *(4 scritture)* | ⛔ **CONGELATA, e NESSUNO LA LEGGE**: sempre `np.zeros` | — | — | no: e' **STATO MORTO** (`A8`), non una violazione di `A15` |
| `phi` | `__init__`, `_rn_div_phi`, `_rn_sch_phi`, `_semina_masse_coerenti`, `memoria_hebbiana_moto`, `mitosi`, `semina`, `step` *(10 scritture)* | istantanea: la fase, integrata da `phivel` | — | — | no |
| `phi0` | `__init__`, `_rn_div_phi0`, `_rn_sch_phi0`, `_semina_masse_coerenti`, `semina` *(5 scritture)* | ⛔ **CONGELATA**: `5` scritture, TUTTE alla nascita | non decade: **non si aggiorna affatto** | — | ⛔ **peggio: non dimentica NIENTE** — viola `A15.1` |
| `phi_s` | `__init__`, `_passo_spinoriale`, `_rn_div_phi_s`, `_rn_sch_phi_s`, `semina` *(5 scritture)* | la fase dello spinore | — | NON VERIFICATA in questo giro | NON VERIFICATA |
| `phivel` | `__init__`, `_big_bang`, `_rn_div_phivel`, `_rn_sch_phivel`, `scuoti_vuoto`, `semina`, `step` *(8 scritture)* | INERZIALE | il termostato | ⛔ **il termostato e' GLOBALE** (`A2`) | ⛔ **SI**, e scrive dall'esterno: `A14` n.1 |
| `pos` | `__init__`, `_rn_div_pos`, `_rn_sch_pos`, `rilassa_disegno`, `semina` *(7 scritture)* | il DISEGNO: rilassato, non dinamico | `rilassa_disegno` | — | no (non e' fisica) |
| `psi` | `__init__`, `_rn_div_psi`, `calcola_psi`, `step` *(5 scritture)* | DERIVATA: ricalcolata ogni passo | — | — | no |
| `psi_spin` | `_rn_div_psi_spin`, `calcola_psi` *(2 scritture)* | DERIVATA | — | — | no |
| `rho_spin` | `_rn_div_rho_spin`, `calcola_psi` *(2 scritture)* | DERIVATA | — | — | no |

## ⛔ **CHE COSA HA TROVATO IL CENSIMENTO, oltre a `phi0`**

**Le grandezze i cui scrittori sono TUTTI siti di nascita o costruzione: 5** — `conc_nodi`, `i`, `j`, `perc_tw`, `phi0`.

| | e che cos'e' davvero |
|---|---|
| `i`, `j` | ### ✔ **la TOPOLOGIA, e NON sono memorie.** Gli estremi di un arco non devono «aggiornarsi»: ### **`A15` parla di MEMORIE**, e queste non lo sono. ### **Non sono violazioni.** |
| `conc_nodi` | ### ⚠ **FALSO POSITIVO DEL MIO CENSIMENTO** *(si aggiorna per mutazione)*. ### **Non e' una violazione.** |
| ### ⛔ **`phi0`** | ### **LA violazione di `A15.1`**, e il §`4a` la documenta |
| ### ⛔ **`perc_tw`** | ### **TROVATA DA QUESTO CENSIMENTO, e non era nel mandato.** Un `float64` per nodo, scritto ### **sempre a `np.zeros`** da `__init__`, `semina` e le due regole di nascita — e ### **NESSUNA legge la legge**: le sole occorrenze fuori dalle scritture sono ### **la sua dichiarazione nei registri e le stringhe delle regole di nascita** *(verificato elencando ogni occorrenza nel file)*. ### ✔ **Quindi NON e' una violazione di `A15`: e' STATO MORTO** — `A8`, «un ramo silenzioso non e' un ramo» — e il suo commento *(«stato del salto di pi al mediano»)* dice ### **che cosa avrebbe dovuto portare.** Voce: `PERC-TW-MORTA` |

> ### ⚠ **E SETTE RIGHE DELLA TAVOLA DICONO `NON VERIFICATA`**, quasi tutte nel settore spinoriale. ### **Non le ho guardate in questo giro, e dirlo vale piu' che riempirle con un'impressione.**

---

# §`3` — **IL BILANCIO: i termini che violano `P-DECADIMENTO` e `A15.3`**

> ### ⛔ **NESSUNO DI QUESTI TERMINI CEDE A QUALCUNO.** Tutti si annullano, e ### **`A15.3` pretende che vadano in CALORE DEL VUOTO LOCALE.**

| | il termine | dove | che cosa perde | a chi andrebbe |
|---|---|---|---|---|
| `1` | ### **`- dt_e * tw / tau_tw`** | `step`, blocco della torsione | ### **torsione d'arco** | ### **meta' a ciascun estremo** *(proposta)* |
| `2` | `d0 += dt_e*(d - d0)/tau_p_loc` | `step` *(`:8316`)* | lunghezza di riposo | i due estremi dell'arco |
| `3` | `peq += dt_e*((rho - peq)/tau_bg_loc + flusso/TAU_DIFF)` | `step` *(`:8010`)* | pressione di equilibrio | i due estremi |
| `4` | `mem_mot = (1-plast)*mem_mot + plast*grad_tw` | `memoria_hebbiana_moto` *(`:9221`)* | ### ⛔ **la memoria vecchia, SOVRASCRITTA**: *vince l'ultimo* | il nodo stesso |
| `5` | `- omega_src/_tau` | `_passo_spinoriale` *(`:5929`)* | rotazione dello spinore | il nodo stesso |
| `6` | il ### **termostato globale** e ### **`scuoti_vuoto`** | scrivono `phivel` ### **dall'esterno** | energia ### **e** carica | ### ⛔ **gia' `A14` n.1** |

### ⛔ **CHE COSA MANCA PER SAPERE *QUANTA* ENERGIA PERDONO**

> **L'ENERGIA DELL'ARCO NON E' DEFINITA** — `ENERGIA-NON-DEFINITA`. ### **Senza quella, ognuna di queste righe e' una FORMA senza NUMERO**, e scriverne una come legge sarebbe scrivere un bilancio che ### **non si puo' nemmeno enunciare.**

**LA DESTINAZIONE DI TUTTI E SEI e' `VUOTO-LOCALE-DETERMINISTICO`**, che e' il vuoto locale che ### **oggi non esiste.**

### ⚠ **E LA REGOLA DI RIPARTIZIONE PER UN ARCO E' UNA PROPOSTA, NON UNA LEGGE**

| la proposta | ### **meta' a ciascun estremo** |
|---|---|
| un'alternativa altrettanto scrivibile | pesata su ### **`\|psi\|²`** dei due nodi: chi ha piu' materia assorbe piu' calore |
| ### ⛔ **chi decide** | ### **Luca.** ### **Una regola di ripartizione e' FISICA**, non una convenzione di misura |

---

# §`4` — **LE EVIDENZE DEL GUARDIANO, RICONTROLLATE**

## `(a)` ⛔ **`phi0` CONGELATA — CONFERMATA, e il conto è esatto**

**`AST`: `5` scritture, TUTTE alla nascita o alla costruzione** — `__init__` *(`:3981`)*,
`semina` *(`:5059`)*, `_rn_div_phi0` *(`:2092`)*, `_rn_sch_phi0` *(`:2492`)*,
`_semina_masse_coerenti` *(`:9985`, `net.phi0[idx] = net.phi[idx]`)*.
### **Nessun aggiornamento nella dinamica.**

**LE LETTRICI:** `A = w * np.cos(self.phi0[i] - self.phi0[j])` nello ### **`step`**
*(`:7566`)*, e `src = -HAM_SRC * K_C * (w/LAM) * cos(phi0_i - phi0_j) * cos(dph)`
*(`:8051`)* — ### ⚠ **inerte, perché `HAM_SRC = 0.0`** *(`:423`)*.

> ### ⛔ **QUINDI LA <<MEMORIA HEBBIANA DEI LEGAMI>> — `Legge VI` dell'intestazione
> (`:20`) — NON IMPARA E NON DIMENTICA.** ### **È una costante d'arco fissata alla
> nascita**, e chiamarla *memoria* è il nome che promette ciò che il codice non fa.
>
> ### ⚠ **E IL SEGNO NON È NEUTRO:** nelle masse `_semina_masse_coerenti` pone
> `phi0 = phi`, quindi gli accoppiamenti sono ### **positivi PER COSTRUZIONE**; nel
> ### **vuoto** il segno è ### **casuale e congelato** — ### **disordine IMMUTABILE.**

### 🔗 **IL COLLEGAMENTO CON `SCIOGLIMENTO-FASE`** *(e la voce lo dice già)*

`SCIOGLIMENTO-FASE` chiede ### **perché `coer_campo` va da `0.999` a `0.20` in `120`
passi**, e la sua ipotesi ### **`H2`** è che ### **nel ramo del driver la coppia dipenda da
`A` e dallo spinore, non dalla fase corrente.**

> ### ➜ **E `A` È ESATTAMENTE `w·cos(phi0_i − phi0_j)`:** cioè ### **la costante
> congelata.** ### **`H2` e `phi0` congelata sono lo STESSO fatto, visto da due parti.**
>
> ### ⚠ **MA `H1` RESTA, E NON LA CURA NESSUNA MEMORIA:** `SCIOGLIMENTO-FASE` ha anche
> l'ipotesi delle ### **velocità di fase casuali della scena**, che è una proprietà
> ### **dell'inizializzazione**, non di una legge. ### **Curare `phi0` curerebbe UNA delle
> due cause.**

## `(b)` ⭐ **LA MEMORIA VERA È DENTRO `tw` — l'algebra, rifatta riga per riga**

**La legge curata** *(`step`, blocco della torsione)*:

```
tw_{t+1} = tw_t + w4(dph_t - twp_t) + (td_t - twp_dip_t) - dt_e*tw_t/tau_tw
twp_{t+1}     = dph_t
twp_dip_{t+1} = td_t
```

**Definisco `delta_t = twp_t - tw_t`**, cioè ### **`dph_{t-1} - tw_t`** — ed è
### **l'accoppiamento naturale**, perché `twp_t` *è* `dph_{t-1}`.

```
delta_{t+1} = dph_t - tw_{t+1}
            = dph_t - tw_t - w4(dph_t - dph_{t-1}) - Delta_td + dt_e*tw_t/tau_tw
```

**Senza avvolgimento** *(`|dph_t - dph_{t-1}| < 2pi`, dove `w4(x) = x`)*:

```
            = dph_{t-1} - tw_t - Delta_td + dt_e*tw_t/tau_tw
            = delta_t + (dt_e/tau_tw)*(dph_{t-1} - delta_t) - Delta_td
```

> ### ✔ **È ESATTAMENTE LA FORMA DEL GUARDIANO**, e la verifica è questa derivazione.
> ### **`delta` è una MEDIA MOBILE ESPONENZIALE di `dph_prec`**, con ritmo
> ### **`dt_e/tau_tw`**, ### **perturbata da `−Δdipolo`.**

### ⚠ **E TRE PRECISAZIONI, perché i dettagli cambiano il significato**

| | |
|---|---|
| ### **l'indice** | il guardiano scrive `delta = dph - tw`; ### **l'identità esatta è `delta = dph_PREC - tw`** *(cioè `twp - tw`)*. ### **Un passo di differenza**, e conta: la media mobile inseugue ### **il passato**, non il presente |
| ### **il `mod 4pi`** | la relazione vale ### **esattamente solo senza avvolgimento**; con un avvolgimento compare un ### **`+ 4pi*k`**. ### **Quindi la media mobile vive MOD `4pi`**, come dice il guardiano |
| ### **lo sporco** | `td ∈ {−pi, 0, +pi}`, quindi `Δtd ∈ {0, ±pi, ±2pi}`: ### **ogni salto del dipolo inietta un gradino** che decade col ritmo `dt_e/tau_tw`, cioè ### **persiste ~`tau_tw`** |

### ✔ **GLI ARCHI NUOVI, e la regola del `NaN` è ciò che li salva**

Alla nascita `twp_dip = NaN`, quindi `_nuovo` è vero, `_fp = dph` e `_dp = td`: la spinta
è ### **`w4(dph − dph) + (td − td) = 0` ESATTA**, e `twp' = dph`.
### ➜ **Quindi `delta` parte da `dph − tw_nascita`**, cioè ### **dalla differenza di fase
alla nascita dell'arco.**

> ### ⛔ **E NEL RAMO `else` — quello senza `TORS_4PI` — LA REGOLA DEL `NaN` NON C'È:**
> la legge è `tw += w4(dph − twp) − dt_e*tw/tau_tw`, e ### **`_allaccia` nasce con
> `twp = 0`** *(verificato: `_allaccia` concatena zeri)*. ### ➜ **Un arco di `_allaccia`
> riceverebbe `w4(dph)` INTERA al suo primo passo**, cioè ### **tutta la differenza di
> fase in un colpo.**
>
> ### ✔ **Nel ramo del driver questo NON succede**, perché `TORS_4PI` è acceso e la regola
> del `NaN` c'è. ### **Ma il ramo `else` esiste**, e ### **è un `A8` da dichiarare**, non
> un dettaglio.

### ⭐ **E IL SUO TEMPO È DERIVATO: è l'esempio che `A15.2` cita**

`tau_tw = 2pi/|omega_i − omega_j|` *(`_tau_tw_locale`, `:596`)*.
### **Non un numero: l'inverso della dispersione di frequenza fra i due nodi.**

## `(c)` ⛔ **`mem_mot`: per NODO, legge `pos`, scrive `d0`, usa due medie GLOBALI**

**Verificato in `memoria_hebbiana_moto`** *(`:9171`)*:

| | il codice | che cosa viola |
|---|---|---|
| è ### **per NODO** | `("mem_mot", ("n", 3,), "float64")` | una memoria di ### **moto relativo** vive sull'### **ARCO** |
| legge ### **`pos`** | `v = self.pos[jj] - self.pos[ii]` | ### ⛔ **`pos` è IL DISEGNO** |
| ### **`Imed` globale** | `Imed = max(float(np.median(I)), 1e-9)` | ### ⛔ **`A2`**: statistica globale in una legge locale |
| la ### **mediana di `d0`** | *(citata in `D03`)* | ### ⛔ **`A2`** |
| ### **vince l'ultimo** | `mem_mot = (1-plast)*mem_mot + plast*grad_tw` | ### ⛔ **non è un bilancio: è una SOSTITUZIONE** *(`A14` n.4)* |
| ### ✔ il suo tempo | `plast = np.tanh(\|grad_tw\|)` *(`:9219`)* | ### ✔ **DERIVATO dallo stato** — `A15.2` è rispettato |

> ### ➜ **ANNOTATO in `MEM-HEBB-VERSO` e in `D03`**, che è la voce ### **BLOCCANTE** su
> *«le direzioni da `pos`, la normalizzazione su una media globale»*.

## `(d)` ⚠ **IL <<PLATEAU>> DELLA TORSIONE: il NUMERO è giusto, LA PAROLA no**

**Letto dal `lunga.json` committato** *(la misura da `1000` passi)*, mediana di `|tw|`:

| passo | `1` | `50` | `150` | `300` | `600` | `1000` |
|---|--:|--:|--:|--:|--:|--:|
| mediana di `\|tw\|` | `0.0` | `1.3967` | `2.2829` | `2.7026` | `3.4243` | ### **`3.9151`** |
| in unità di `2pi` | `0.0` | `0.2223` | `0.3633` | `0.4301` | `0.5450` | ### **`0.6231`** |

> ### ✔ **IL NUMERO DEL GUARDIANO È ESATTO:** ### **`3.9151` rad**, cioè
> ### **`62.31 %` di `2pi`.**
>
> ### ⛔ **MA NON È UN PLATEAU: STA ANCORA SALENDO.** `1.40 → 2.28 → 2.70 → 3.42 → 3.92`,
> ### **monotona fino all'ultimo passo misurato.** ### **La misura si ferma mentre la
> curva cresce**, ed è ### **lo stesso fatto che avevo già trovato sugli archi oltre
> `4pi`** *(crescono fino a `368` al passo `1000`, col massimo all'ULTIMO passo)*.
>
> ### ➜ **CONSEGUENZA PER LA LETTURA:** *«oggi la memoria dei legami dimentica molto»*
> ### **non si può concludere da qui.** Per dire ### **quanto** dimentica serve il
> ### **valore d'equilibrio**, e ### **l'equilibrio non è stato raggiunto in `1000`
> passi.** ### **È una delle ragioni per cui `A1` gira a `1000` passi e misura la
> frazione sopra `2pi` a OGNI passo.**

## `(e)` ⛔ **LA COLLISIONE DI NOMI: due <<Legge VI>>**

| dove | che cos'è |
|---|---|
| `soliton_simulator.py:20` | ### **la memoria hebbiana dei legami**, `cos(dphi0)` |
| `doc/FONDAZIONE_SPINORIALE.md:141` | ### **la SCHERMATURA** *(la portata dipende dalla densità)* |

> ### ⛔ **È la famiglia di `A3`**, che era ### **tre voci diverse** e l'indice ha dovuto
> separarle. ### **Finché Luca non decide quale tiene il `VI`, si cita per NOME.**

---

# §`5` — **LE MEMORIE CHE MANCANO**

> ### 📌 **Ogni scheda porta i SETTE CAMPI di `L-MEMORIA-PRIMA`**, più la grandezza
> esistente da cui nasce, i prerequisiti, la misura che la decide, il posto in coda, e i
> ### **rischi — anelli di retroazione compresi — con il caso che DEVE FALLIRE nel suo
> sigillo.**

## ⭐ `MEM-VERSO` — **il verso dell'arco dalla sua MEMORIA**

| il campo | |
|---|---|
| ### **quale memoria** | ### **`delta = twp − tw`**, la media mobile già dentro `tw` *(§`4b`)* — oppure una media mobile del ### **segno** di `tw`. ### **Vive sull'ARCO** |
| ### **tipo** | ### **MEDIA MOBILE**, non hebbiana: non si rinforza con l'attività congiunta dei due estremi, ### **inseugue una differenza di fase** |
| ### ✔ **sostituisce o aggiunge** | ### **SOSTITUISCE**: usa la memoria ### **GIÀ PRESENTE** in `tw`. ### **ZERO stato nuovo** — è la condizione `(1)` di `L-MEMORIA-PRIMA` soddisfatta per costruzione |
| ### **che verso dà** | il verso della ### **media mobile della differenza di fase**: *da che parte si stava andando*, non *dove si è* |
| ### **a chi cede** | ### ✔ **a nessuno di nuovo**: il termine `−dt_e·tw/tau_tw` ### **c'è già**, e la sua violazione di `A15.3` ### **resta dichiarata dov'è** *(§`3` n.1)* |
| ### ✔ **il suo tempo** | ### **`tau_tw = 2pi/\|Δω\|`** — ### **DERIVATO**, `A15.2` rispettato |
| ### **che altro chiuderebbe** | ### **`GEOM-SENZA-VERSO`** *(è una CANDIDATA alla sua cura)* |

**LA MISURA CHE LA DECIDE:** ### **`A1`**, dove `MEM` entra come ### **quinta opzione**
accanto ad `A`, `D` e `perc_geom`, ### **misurata col metro giusto — `Σ\|Δdipolo\|`.**

> ### ⛔ **IL RISCHIO, e va scritto: `delta` È SPORCATA DAL DIPOLO** *(§`4b`: ogni salto
> inietta un gradino che persiste `~tau_tw`)*. ### ➜ **Quindi `MEM-VERSO` ha un anello
> `tw → dipolo → delta → verso → dipolo`**, e ### **va DOPO la cura del verso o insieme a
> essa**, non prima.
>
> ### ⛔ **IL CASO CHE DEVE FALLIRE nel suo sigillo:** su un arco con ### **`Δω = 0`**
> *(due nodi in fase)* `tau_tw` diverge e la media mobile ### **non dimentica mai**: il
> verso deve ### **congelarsi**, e se non lo fa la forma non è quella che credo.

## ⭐ `M-FLUSSO` — **memoria di flusso per ARCO, al posto di `mem_mot`**

| il campo | |
|---|---|
| ### **quale memoria** | un ### **SCALARE per ARCO**, ### **antisimmetrico** per scambio dei due estremi: *quanto flusso è passato, e in che verso* |
| ### **tipo** | ### **HEBBIANA**: si rinforza con l'### **attività congiunta** dei due estremi — ed è il caso in cui il nome *hebbiano* è ### **meritato**, a differenza di `phi0` |
| ### ✔ **sostituisce o aggiunge** | ### **SOSTITUISCE `mem_mot`** *(un `(n,3)` per nodo → uno scalare per arco)*: ### **meno stato, non più** |
| ### **che verso dà** | il verso ### **dell'arco**, per antisimmetria: ### **non serve `pos`** |
| ### **a chi cede** | il suo decadimento ### **sostituisce** quello di `mem_mot`, che oggi ### *«vince l'ultimo»* e ### **non cede a nessuno** *(`A14` n.4)*: la violazione ### **non peggiora** |
| ### **il suo tempo** | ### ⚠ **DA DERIVARE**: `plast = tanh(\|grad_tw\|)` di oggi è derivato, ma è ### **per nodo**. ### **Per un arco il candidato naturale è `tau_tw`** — e va ### **verificato, non assunto** |
| ### **che altro chiuderebbe** | ### **`MEM-HEBB-VERSO`** *(scrive su un solo estremo, legge `pos`)* ### **e `D03`**, che è ### ⛔ **BLOCCANTE** |

> ### ✔ **E `D03` L'HO LETTA:** *«La memoria del moto prende le direzioni da `pos`,
> normalizza su `Imed` GLOBALE»*. ### ➜ **Una memoria d'arco antisimmetrica toglie
> ENTRAMBI i difetti** — ### **il verso viene dall'arco, non da `pos`**, e ### **non c'è
> nessuna media su cui normalizzare.**
>
> ### ⛔ **IL CASO CHE DEVE FALLIRE:** su una rete ### **simmetrica per scambio** la
> memoria deve dare ### **zero ESATTO**; se dà un valore, l'antisimmetria è solo nel nome.

## ⭐ `M-LEGAMI` — **`cos(dph − tw)` al posto di `cos(phi0_i − phi0_j)`**

| il campo | |
|---|---|
| ### **quale memoria** | ### **`delta = dph − tw` sull'ARCO**, la stessa di `MEM-VERSO` |
| ### **tipo** | ### **MEDIA MOBILE** *(quella dentro `tw`)* |
| ### ✔ **sostituisce o aggiunge** | ### **SOSTITUISCE**: ### **NESSUNO stato nuovo**, e ### ⭐ **rende VIVA una memoria oggi CONGELATA** — cioè ### **toglie la prima violazione di `A15.1`** |
| ### **che verso dà** | non un verso: ### **un accoppiamento che EVOLVE** invece di essere fissato alla nascita |
| ### **a chi cede** | ### ✔ **niente di nuovo**: non aggiunge termini |
| ### **il suo tempo** | ### **`tau_tw`** — derivato |
| ### **che altro chiuderebbe** | ### **UNA delle due cause di `SCIOGLIMENTO-FASE`** *(`H2`)*, ### ⛔ **non l'altra** *(`H1`: le velocità di fase casuali della scena, che è l'INIZIALIZZAZIONE)* |

> ### ⛔ **QUANDO: DOPO la cura del verso**, perché ### **il dipolo sporca `delta`**
> *(§`4b`)*, e un accoppiamento costruito su una `delta` sporca ### **erediterebbe i salti
> di `pi`.**
>
> ### ⛔ **IL CASO CHE DEVE FALLIRE:** con `tw = 0` su tutti gli archi *(il passo `1`)*
> `cos(dph − tw)` deve valere ### **`cos(dph)`**, e ### **NON `cos(phi0_i − phi0_j)`**: se
> i due coincidessero, la cura non cambierebbe niente ed ### **è il controllo che lo
> mostra.**

## `M-MASSA` — **pesi di appartenenza con memoria**

| il campo | |
|---|---|
| ### **quale memoria** | il peso di appartenenza di un nodo a una massa, ### **con storia** invece che ricalcolato |
| ### **tipo** | ### **INTEGRALE** |
| ### ⛔ **sostituisce o aggiunge** | ### **AGGIUNGE** |
| ### **che verso dà** | nessuno: ### **non è una memoria di verso**, è di appartenenza |
| ### **a chi cede** | ### ⛔ **DA DEFINIRE**, e per questo cade nella condizione `(3)` |
| ### **il suo tempo** | ### ⚠ **da derivare**, e non ho un candidato |
| ### **che altro chiuderebbe** | dipende da ### **`MASSA-ID`** *(le masse si identificano con `conc_nodi`, non coi nodi del passo `0`)* |

> ### ⛔ **DIPENDE DA UNA DECISIONE SU `MASSA-ID`**, e ### **AGGIUNGE dissipazione**:
> ### **solo dopo `ENERGIA-NON-DEFINITA` e `VUOTO-LOCALE-DETERMINISTICO`** — condizione
> `(3)`.

## `M-SPINORE` — **trasporto SU(2) per arco con memoria**

| il campo | |
|---|---|
| ### **quale memoria** | la connessione `U_ij` ### **con storia**: il candidato ### **campo di gauge della carica** |
| ### **tipo** | ### **INTEGRALE su SU(2)** |
| ### ⛔ **sostituisce o aggiunge** | ### **AGGIUNGE** |
| ### **che verso dà** | un verso ### **non abeliano**: non un segno, ### **un elemento di gruppo** |
| ### **a chi cede** | ### ⛔ **DA DEFINIRE** |
| ### **il suo tempo** | ### ⚠ **da derivare** |
| ### **che altro chiuderebbe** | nessuna voce aperta oggi: ### **è un fronte, non una cura** |

> ### ⛔ **LONTANA.** ### **Aggiunge stato E dissipazione**, quindi cade nella condizione
> `(3)`; e il suo oggetto — ### **un campo di gauge emergente** — è ### **esattamente ciò
> che il `par.10` di `CLAUDE.md` vuole visto EMERGERE e non innestato.**

## ⚠ `M-ISTERESI` — **l'isteresi dei basculamenti**: — **alternativa o complemento a `MEM-VERSO`?**

| il campo | |
|---|---|
| ### **quale memoria** | un'### **isteresi sui flip** di `perc_geom` e `perc_chi`: due soglie invece di una, e il salto avviene solo oltre la seconda |
| ### **tipo** | ### **ISTERESI** — non media mobile, non hebbiana |
| ### ⛔ **sostituisce o aggiunge** | ### **AGGIUNGE** uno stato *(la soglia corrente, o il segno precedente)*, ### **ma minimo**: un bit per nodo |
| ### **che verso dà** | ### **nessuno**: ### ⛔ **non dà un verso, RALLENTA i salti** |
| ### **a chi cede** | ### ⚠ **non dissipa energia**: `perc_geom` e `perc_chi` sono ### **`int64`**, cioè ### **cariche/stati discreti**, non energia |
| ### **il suo tempo** | ### ⛔ **la larghezza dell'isteresi SAREBBE UN NUMERO**, e ### **`A15.2` lo vieta**: va derivata *(un candidato: la dispersione locale di `\|tw\|`)*, e ### **non ne ho uno verificato** |
| ### **che altro chiuderebbe** | ### **nessuna voce aperta la nomina**, e questo di per sé è un dato |

> ### ➜ **LA RISPOSTA ALLA DOMANDA DEL MANDATO: È UN COMPLEMENTO, NON UN'ALTERNATIVA.**
> ### **`MEM-VERSO` cambia COME si legge il verso** *(da istantaneo a mediato)*;
> ### **l'isteresi cambia QUANDO si permette il salto.** ### **Agiscono su cose diverse:**
> una sul ### **valore**, l'altra sulla ### **transizione.**
>
> ### ⛔ **E L'ISTERESI DA SOLA NON CURA `GEOM-SENZA-VERSO`:** il difetto è che
> ### **`perc_geom` nasce da `\|tw\|` e PERDE IL VERSO**; rallentare i salti di una
> grandezza ### **che non ha verso** ### **non le dà un verso.**

## ⛔ **E DOVE NON METTERE UNA MEMORIA, col perché**

| | perché NO |
|---|---|
| `psi`, `psi_spin`, `B` | sono ### **CAMPI DERIVATI**, ricalcolati ogni passo dalla loro legge: ### **dargli memoria li farebbe diventare STATI**, e lo stato in più è esattamente ciò che `9-ter` chiede di non aggiungere |
| `lambda_nodi` | darebbe un ### **GUSCIO IMPOSTO**, mentre ### **Luca vuole vedere se il guscio EMERGE** *(`GUSCIO-ANTIFASE-EMERGENTE`)*: una memoria qui ### **inventerebbe la risposta alla domanda aperta** |
| `pos` | è ### **IL DISEGNO.** Una memoria su `pos` sarebbe memoria ### **di un artefatto di visualizzazione** |
| `phivel`, `vd` | sono ### **GIÀ INERZIALI**: portano già la storia come ### **velocità.** Aggiungere memoria su una velocità sarebbe ### **una seconda inerzia sullo stesso grado di libertà** |

---

# §`6` — **LE TENSIONI, dichiarate**

> ### ⛔ **UNA MEMORIA CHE DIMENTICA È DISSIPATIVA PER LEGGE**, anche se ### **a regime può
> non dissipare** *(l'osservazione di Luca, `M5d`)*. ### **Per rispettare `A14` e `A15.3` il
> dimenticato deve andare in CALORE DEL VUOTO LOCALE.**

### **E LA DISTINZIONE CHE DECIDE QUANDO SI PUÒ FARE**

| | le memorie | che cosa si può fare |
|---|---|---|
| ### ✔ **SOSTITUISCONO una dissipazione esistente** | ### **`MEM-VERSO`**, ### **`M-FLUSSO`**, e ### **`M-LEGAMI`** *(valutato: ### **non aggiunge termini**, usa `delta` che c'è già)* | ### ✔ **si possono fare DENTRO LE LORO CURE**, con la ### **violazione già dichiarata che RESTA tale**: non peggiora, e il bilancio non cambia di un termine |
| ### ⛔ **AGGIUNGONO una dissipazione nuova** | ### **`M-MASSA`**, ### **`M-SPINORE`** | ### ⛔ **si scrivono come leggi SOLO DOPO `ENERGIA-NON-DEFINITA` e `VUOTO-LOCALE-DETERMINISTICO`** |
| ### ⚠ **caso a sé** | ### **l'ISTERESI** | ### **aggiunge stato ma NON dissipazione** *(agisce su `int64`, stati discreti)*. ### ⛔ **Il suo ostacolo è un altro: la larghezza sarebbe un NUMERO, e `A15.2` lo vieta** |

> ### ⛔ **E LA TENSIONE PIÙ ONESTA È QUESTA: la condizione `(3)` è CIRCOLARE finché il
> vuoto locale non esiste.** Una memoria che aggiunge dissipazione ### **non si può
> scrivere**; ma ### **il vuoto locale, per sapere quanto calore riceve, ha bisogno di
> sapere quanto le memorie dissipano.**
>
> ### ✔ **LA VIA D'USCITA NON È UN'ECCEZIONE: è L'ORDINE.** `ENERGIA-NON-DEFINITA` viene
> ### **prima** — definisce l'energia dell'arco ### **senza bisogno di nessuna memoria
> nuova** — e ### **solo dopo** il bilancio si può scrivere. ### **È `B1` della ripresa**,
> ed è ### **per questo** che `B1` sta dove sta.

---

# ⭐ **LA TABELLA DIFETTI × MEMORIE**

> ### 📌 **ANCHE IL <<NO>> VA SCRITTO**, e lo dice il mandato. ### **Una tabella che elenca solo i sì sembra dire che la memoria cura tutto.**

**LA LISTA DELLE VOCI NON È SCELTA DA ME:** il controllo verifica che ### **tutte e 12 le voci BLOCCANTI** dell'indice siano in tabella, e ### **si ferma** se una manca. *(Il GIUDIZIO di ogni riga è mio.)*

| la voce | quale memoria | sostituisce / aggiunge | perché |
|---|---|---|---|
| `A3-DISEGNO` | `M-FLUSSO` | SOSTITUISCE | la voce e' *<<il disegno esce dalla dinamica: `pos` entra nelle leggi>>*. ### ✔ **`M-FLUSSO` toglie UNA delle letture di `pos`** *(quella di `mem_mot`)*, ### ⛔ **non tutte** |
| `D03` | `M-FLUSSO` | SOSTITUISCE | ### ⛔ **BLOCCANTE**, e l'ho letta: *<<le direzioni da `pos`, normalizza su `Imed` GLOBALE>>*. ### **Una memoria d'arco toglie ENTRAMBI i difetti** |
| `GEOM-SENZA-VERSO` | `MEM-VERSO` | SOSTITUISCE | il difetto E' la perdita del verso, e una media mobile di `tw` un verso **ce l'ha** |
| `MASSA-CRITICA-LOCALE` | `M-MASSA` | AGGIUNGE | un valore **dinamico e locale** legato a `lambda`: ### **i pesi con memoria sono un candidato**, e `c_k` l'altro |
| `MEM-HEBB-VERSO` | `M-FLUSSO` | SOSTITUISCE | la voce E' la memoria del moto: ### **una memoria d'arco antisimmetrica la rifa' giusta** |
| `PHI0-CONGELATA` | `M-LEGAMI` | SOSTITUISCE | ### ⭐ **e' la memoria che rende VIVA quella congelata**: e' la cura di questa voce |
| `SCIOGLIMENTO-FASE` | `M-LEGAMI` | SOSTITUISCE | cura `H2` *(la coppia da `A`, cioe' da `phi0` congelata)*, ### ⛔ **non `H1`** *(le velocita' di fase casuali della scena)* |
| `A1-COSTANTI` | ### **nessuna, MA A15.2 LA TOCCA** | — | e' l'**audit delle costanti tarate** *(90 commenti <<misurato/tarato>>)*. ### ⚠ **`TAU_DIFF = 1.0` e' una di quelle costanti**, ed e' l'unica violazione di `A15.2` che ho trovato: ### **le due liste si INCROCIANO** |
| `ARCHI-OLTRE-4PI` | ### **nessuna** | — | ### ⛔ **e per decisione NON si indaga** |
| `CARICA-DI-GAUGE` | ### **da valutare** | ? | *<<il segno di `perc_chi` dipende al 100 per cento dal rappresentante canonico>>*: ### ⚠ **e' un problema di SEGNO**, quindi `M-ISTERESI` o una memoria di carica potrebbero toccarlo. ### **Non l'ho letta a fondo in questo giro** |
| `CENS-A1` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' una **riduzione al limite** non raggiungibile |
| `CENS-A2` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **commento contro il codice** |
| `CENS-A6` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **commento contro il codice** |
| `CENS-A7` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **numero sbagliato in un commento** |
| `CENS-B7` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **default dichiarato male** |
| `CICLO-CHIUSURA-SEGNO` | ### **nessuna** | — | e' un **segno registrato al rovescio** in una routine diagnostica: ### **una convenzione sbagliata, non una grandezza senza storia** |
| `CLI-1` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **percorso non provato** nei sigilli |
| `CONSERVAZIONE-LOCALE` | ### **nessuna, E' IL REGISTRO** | — | e' la voce che **tiene l'elenco** delle violazioni di `A14` e `A15` |
| `CS-LAMBDA-GLOBALE` | ### **nessuna** | — | e' una **scala globale** in una legge locale *(`A2`)*: va **localizzata** |
| `D31` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' un **freno a senso unico** *(`fatt = max(0, 1 - LAM/prima)` solo in discesa)*: ### **la cura e' una forma SIMMETRICA**, non una memoria |
| `ENERGIA-NON-DEFINITA` | ### **nessuna** | — | ### ⛔ **e' il PREREQUISITO di tutte le altre:** definire l'energia dell'arco ### **non richiede nessuna memoria nuova** |
| `FASE-TRASCINAMENTO-3D` | ### **da valutare** | ? | ### ⚠ **non l'ho letta in questo giro**, e dirlo vale piu' che indovinare |
| `GRAVITA-POTENZIALE` | ### **nessuna** | — | serve un **riferimento di scala** e **tre controlli**: ### **una misura, non una memoria** |
| `GUSCIO-ANTIFASE-EMERGENTE` | ### **nessuna, E PER SCELTA** | — | ### ⛔ **Luca vuole vedere se il guscio EMERGE**: una memoria su `lambda_nodi` ### **inventerebbe la risposta** |
| `M1` | ### **nessuna, MA P-DECADIMENTO LA TOCCA** | — | la voce dice *<<la materia e' uno stato, non una sostanza -- e non c'e' SCARICO>>*. ### ⚠ **<<non c'e' scarico>> E' esattamente `P-DECADIMENTO`**: ### **la stessa domanda, da un'altra parte** |
| `MCRIT-RICALCOLO` | ### **nessuna** | — | e' un **ricalcolo**, e dipende da `MASSA-CRITICA-LOCALE` |
| `P-EQ-MEDIANA-ARCHI` | ### **nessuna** | — | e' una **mediana su un sottoinsieme arbitrario** *(`A3`)* |
| `PERC-TW-MORTA` | ### **nessuna** | — | e' ### **stato MORTO** *(nessuno la legge)*: ### **si toglie o si collega**, non si cura con una memoria |
| `PHI-FUORI-DOMINIO` | ### **nessuna** | — | e' un **dominio** sbagliato: una memoria non cambia un dominio |
| `PRESTAZIONI-CORSE` | ### **nessuna** | — | e' **prestazione** |
| `RELAZIONE-BINARIA` | ### **nessuna** | — | e' una **relazione di struttura** |
| `RITMO-FLAG-SENZA-OGGETTO` | ### **nessuna** | — | e' un **flag senza oggetto** |
| `S09-MEDIANA` | ### **nessuna** | — | e' una **mediana globale** in una legge locale *(`A2`)*: va localizzata |
| `SCALE-TW` | ### **nessuna, DIRETTAMENTE** | — | ### ⛔ **BLOCCANTE.** E' un **censimento delle scale in `pi`**. ### ⚠ **MA `tau_tw` e' una di quelle scale**, e `A15.2` dice che va DERIVATA: ### **si toccano** |
| `SCHED-PASSO` | ### **nessuna** | — | ### ⛔ **BLOCCANTE.** E' **architettura del passo**, non fisica |
| `SCHERMATURA-LEGGE-REVISIONE` | ### **nessuna** | — | e' la **forma** di `f(0) = 1`: ### **la cura e' approvata e non c'entra con la memoria** |
| `SCHW-SOTTO-LAM` | ### **nessuna** | — | e' un **cancello che manca** a un sito di nascita: ### **si aggiunge il cancello** |
| `SOGLIA-MITOSI-3PI` | ### **nessuna, DIRETTAMENTE** | — | la soglia va **ricavata** *(<<solo valori ricavati>>)*. ### ⚠ **MA il `dipolo` che la soglia leggerebbe dipende dal verso**, quindi `MEM-VERSO` la **tocca di rimbalzo** |
| `TETTO-CAUSALE-TEMPO-COORDINATO` | ### **nessuna** | — | e' `DT` **coordinato** contro `c_s` **locale**: ### **un difetto di TEMPO, non di memoria** |
| `TORS-SPINTA` | ### **nessuna** | — | e' una legge con **tre numeri a mano**: ### **`A1`-`A11`, non memoria** |
| `TORS-W8-AVVOLGIMENTO` | ### **nessuna** | — | ### ✔ **curata**: la chiusura e' una **decisione di Luca** |
| `U1` | ### **nessuna** | — | e' una **soglia globale tarata** *(`massa_critica_collasso`)*: ### **si ricava o si toglie**, e nessuna memoria la deriva |
| `U2` | ### **nessuna** | — | ### ✔ **CHIUSA** il 2026-10-06: curata dal commit `6b` |
| `VUOTO-LOCALE-DETERMINISTICO` | ### **nessuna, ma e' LA DESTINAZIONE** | — | e' il posto **dove il calore va**. ### **Non si cura con una memoria: si cura con una legge di vuoto locale** |

| | |
|---|--:|
| voci in tabella | ### **44** |
| con una memoria ### **candidata** | ### **7** |
| con ### **<<nessuna>>** | ### **35** |
| ### ⚠ **non lette in questo giro** | ### **2** |

> ### ⛔ **QUINDI LA MEMORIA CURA 7 VOCI SU 44, e NON È LA CURA DI TUTTO.** La maggior parte dei difetti aperti sono ### **soglie tarate, scale globali, cancelli che mancano, commenti contro il codice e architettura**: ### **cose che una memoria non tocca.**


### ⚠ **E LE ALTRE VOCI DI `B13`: UN GIUDIZIO DI GRUPPO, DICHIARATO COME TALE**

Delle ### **53 voci** che `B13` aggiunge, ### **ne ho nominate 7 qui sopra** — quelle che toccano davvero la memoria. ### **Le restanti NON le ho giudicate una per una**, e lo dico invece di scrivere cinquanta <<nessuna>> che non ho verificato.

| | |
|---|---|
| ### **`10` sono REGOLE o casi di sigillo** | `P1`-`P6` sono ### **le regole di lavoro di `CLAUDE.md`**; `Q6`, `R3`, `R5`, `U3` sono ### **casi di collaudo gia' curati.** ### **Non sono difetti aperti**, quindi la colonna <<memoria>> non si applica |
| ### **il resto** | per ### **tipo** sono `altro`, `sospetto` e `difetto` su **soglie, mediane globali, architettura del passo e commenti contro il codice**: ### ⚠ **nessuna memoria vi si applica PER QUANTO HO VISTO DAI TITOLI**, e ### **un titolo non e' una lettura** |

> ### ⛔ **QUINDI QUESTA TABELLA E' COMPLETA SULLE BLOCCANTI E SULLE VOCI DI `A` e `B`, E PARZIALE SU `B13`.** ### **Dirlo e' il dato:** una tabella che si presenta completa quando non lo e' fa prendere decisioni su una copertura che non esiste.

> ### ⚠ **E DUE RIGHE SI TOCCANO DI RIMBALZO, non direttamente:** ### **`SOGLIA-MITOSI-3PI`** *(la soglia leggerebbe il `dipolo`, che dipende dal verso)* e ### **`SCALE-TW`** *(`tau_tw` È una delle scale in `pi` che quel censimento deve guardare, e `A15.2` dice che va DERIVATA)*. ### **Scriverle come <<nessuna>> sarebbe comodo e falso.**

---

# ANNOTAZIONE *(2026-10-07 — `par.8`: si ANNOTA, non si riscrive)*

## ⛔ **UNA MIA RIGA NON REGGE: `mem_mot` È UNA SECONDA VIOLAZIONE DI `A15.2`**

*(Rilievo del guardiano, verificato sul codice del blob ### **`b8c21049`** prima di
scriverlo.)*

> ### ⛔ **CHE COSA AVEVO SCRITTO, in tre posti:** *«`mem_mot`: il suo tempo è
> `plast = tanh(|grad_tw|)` — ### **DERIVATO dallo stato**, `A15.2` è rispettato»*
> — nella riga `mem_mot` del §`2`, nel §`4c`, e nella scheda `M-FLUSSO`.
>
> ### ⛔ **NON REGGE**, e per ### **due** ragioni ### **indipendenti.**

## `1` ⛔ **IL TEMPO È CONTATO IN TICK GLOBALI: `memoria_hebbiana_moto` NON USA IL TEMPO PROPRIO**

**Censimento `AST` della funzione** *(righe `9171`-`9636`)*, cercando ### **ogni** nome di
tempo:

| cercato | trovato? |
|---|---|
| `dt_e` *(il tempo d'arco)* | ### ⛔ **ASSENTE** |
| `dt_n` *(il tempo di nodo)* | ### ⛔ **ASSENTE** |
| `_fattore_tempo_arco` | ### ⛔ **ASSENTE** |
| `_tempo_luce_nodo` | ### ⛔ **ASSENTE** |
| `tau`, `TAU` *(qualunque costante di tempo)* | ### ⛔ **ASSENTE** |
| `DT` | ### ⚠ **PRESENTE, e SOLO nei limiti causali** — `passo_causale = c_sistema*DT` *(`:9334`, `:9390`)*, `_csa*DT` *(`:9528`)*, `LAM*sqrt(K_C)*DT` *(`:9529`, `:9539`)* |

> ### ⛔ **QUINDI L'AGGIORNAMENTO `mem_mot = (1−plast)·mem_mot + plast·grad_tw` GIRA UNA
> VOLTA PER TICK GLOBALE, SENZA NESSUN FATTORE DI TEMPO PROPRIO.**
>
> ### ➜ **IL TEMPO DI MEMORIA È CONTATO IN TICK, cioè in TEMPO COORDINATO**, e
> ### **NON RALLENTA NELLA MATERIA** — a differenza di ### **`tw`, `peq` e `d0`, che
> avanzano con `dt_e`.**
>
> ### ⛔ **È CONTRO `A15.2`**, che dice *«si ricava dalla dinamica ### **LOCALE**»*:
> ### **`plast` è derivato dallo STATO, ma l'OROLOGIO su cui ticchetta è GLOBALE** — e
> ### **sono due cose diverse.** ### **La mia riga confondeva il RITMO con l'OROLOGIO.**
>
> ### ⛔ **E È CONTRO LA DECISIONE DI LUCA** che il tick globale sia ### **solo tempo
> coordinato** e che ### **ogni nodo viva il suo tempo proprio** *(la cura `2`, «un solo
> orologio»)*.

## `2` ⛔ **`tanh(|grad_tw|)` HA UNA SCALA NASCOSTA: `grad_tw` PORTA UNITÀ**

**Dal codice** *(`:9208`-`:9219`)*, e ### **con un dettaglio che rende la cosa più netta di
come l'ho ricevuta:**

```
dtw     = twn[jj] - twn[ii]          # una DIFFERENZA DI TORSIONE  -> radianti
dirarc  = v / L                      # un VERSORE                  -> adimensionale
grad_tw = somma(dtw * dirarc) / _deg  # ...e NON si divide per L
plast   = tanh(|grad_tw|)
```

> ### ⛔ **`grad_tw` NON È UN GRADIENTE PER UNITÀ DI LUNGHEZZA: `L` viene calcolata e usata
> SOLO per normalizzare `dirarc`.** ### ➜ **Quindi `grad_tw` ha le unità della TORSIONE
> (radianti), divise per il GRADO** *(un conteggio adimensionale)*.
>
> ### ⛔ **E `tanh` VUOLE UN ARGOMENTO ADIMENSIONALE.** ### **Quindi lì dentro c'è una
> SCALA NASCOSTA di `1` radiante per unità di grado**, e nessuno l'ha scelta
> esplicitamente. ### **È la famiglia `A1`/`A11`: un numero che si comporta da legge.**

## ➜ **QUINDI: `A15.2` HA DUE VIOLAZIONI, non una**

| | la violazione | che tipo |
|---|---|---|
| `1` | ### **`TAU_DIFF = 1.0`** *(`:460`)*, usato nudo in `flusso / TAU_DIFF` *(`:8010`)* | un ### **numero** al posto di un tempo derivato |
| ### ⛔ **`2`** | ### **`mem_mot`** | il ### **ritmo** è derivato, ### **l'OROLOGIO è globale**; e ### **`tanh` di una grandezza con unità** nasconde una scala |

> ### ⚠ **E LA SECONDA È PIÙ SOTTILE DELLA PRIMA, ed è per questo che me l'ero perso:**
> `TAU_DIFF` è ### **visibilmente** un numero; `mem_mot` ### **sembra** derivato perché
> `plast` lo è. ### **Ho guardato il RITMO e non l'OROLOGIO.**

## ✔ **E LA SCHEDA `M-FLUSSO` CAMBIA DI CONSEGUENZA**

> ### ⛔ **La memoria di flusso d'arco DEVE NASCERE COL TEMPO PROPRIO DELL'ARCO** —
> ### **`dt_e/τ_tw`** o un equivalente ### **derivato** — ### **e SENZA scale nascoste.**
>
> ### ➜ **Non basta <<un ritmo derivato dallo stato>>:** serve che il ritmo sia
> ### **adimensionale** *(un rapporto fra due tempi, o fra due grandezze omogenee)* e che
> l'### **avanzamento** usi il tempo proprio dell'arco.
> ### ⚠ **E il candidato `tau_tw` va VERIFICATO, non assunto**: era già scritto nella
> scheda, e adesso è ### **un requisito, non una preferenza.**

## ⚠ **E UN'ALTRA RIGA VA ANNOTATA: `τ_BG` È DERIVATO, MA CON DUE TOPPE**

```
tau_bg_loc = np.maximum(1.0 / np.maximum(r_arco, 1e-3), 1e-3)      # :8005
```

| | |
|---|---|
| ### ✔ **derivato** | `1/\|phivel_arco\|` — ### **sì, resta vero** |
| ### ⛔ **ma con DUE pavimenti `1e-3`** | uno su ### **`r_arco`** *(che mette un TETTO a `τ` a `1000`)* e uno su ### **`τ` stesso** *(che morde quando `r_arco` è grande)*. ### **Sono `A11`: due limiti scelti, non derivati** |

> ### ➜ **Non è una violazione di `A15.2`** *(il tempo è derivato)*, ### **ma è `A11` su un
> tempo**, e ### **va elencato dove si elencano le toppe.**

---

## ⚠ **E UN ERRORE DEL GUARDIANO, che il guardiano RICONOSCE**

Nella sua evidenza `(d)` aveva chiamato ### **<<plateau>>** la torsione a `3.9` rad, e ne
aveva dedotto che la memoria dei legami ### **<<dimentica molto>>.**

| passo | `1` | `50` | `150` | `300` | `600` | `1000` |
|---|--:|--:|--:|--:|--:|--:|
| mediana di `\|tw\|` | `0.0` | `1.3967` | `2.2829` | `2.7026` | `3.4243` | ### **`3.9151`** |

> ### ⛔ **LA SERIE CRESCE FINO ALL'ULTIMO PASSO MISURATO: non è un plateau**, e
> ### **la deduzione non regge** — per dire ### **quanto** una memoria dimentica serve il
> valore ### **d'equilibrio**, e l'equilibrio ### **non è stato raggiunto in `1000`
> passi.**
>
> ### ✔ **IL NUMERO ERA ESATTO** *(`3.9151` rad, `62.31 %` di `2π`)*: ### **sbagliata era
> la parola, e con essa la conclusione.**
>
> ### 📌 **IL GUARDIANO LO RICONOSCE**, ed è registrato qui perché ### **una correzione
> che resta in una conversazione è una correzione persa.**

---

# §`7` — ⭐ **IL CENSIMENTO DELLE FRECCE IMPOSTE** *(2026-10-07)*

*(Mandato di Luca, dopo la precisazione di `A15.3`. ### **Ogni legge del passo che impone una
direzione nel tempo PER COSTRUZIONE**, trovata ### **col comando** e non a memoria. Voce:
### **`FRECCE-IMPOSTE`.**)*

> ### 📌 **IL COMANDO:** un censimento `AST` su ### **`b8c21049`** che cerca
> ### **`np.where` con una condizione DI SEGNO** *(`< 0`, `> 0`, `scende`, `sale`, `cala`,
> `cresce`)*, i ### **`clip` a UN LATO** *(un estremo a `None`)* e i
> ### **`maximum`/`minimum` applicati a una VARIAZIONE.**

## `A` — **LE FRECCE IMPOSTE, e sono NOVE**

| | la freccia | dove | quale direzione impone | reversibile? con chi | cosa serve prima | PRIMA del vuoto? |
|---|---|---|---|---|---|---|
| `1` | ### **`− dt_e · tw / τ_tw`** | `step`, blocco della torsione | la torsione ### **scende SEMPRE** verso zero | ### ✔ **sì**, scambiandola col ### **calore del vuoto locale** *(che può restituirla)* | ### ⛔ **l'energia dell'arco** *(`ENERGIA-NON-DEFINITA`)* e il ### **vuoto locale** | ### ⛔ **NO** |
| `2` | `d0 += dt_e·(d − d0)/τ_p` | `step` *(`:8316`)* | `d0` ### **inseugue `d`** e non il contrario | ### ✔ sì, col vuoto locale | idem | ### ⛔ **NO** |
| `3` | `peq += dt_e·((rho − peq)/τ_BG + …)` | `step` *(`:8010`)* | `peq` ### **inseugue `rho`** | ### ✔ sì, col vuoto locale | idem | ### ⛔ **NO** |
| `4` | `mem_mot = (1−plast)·mem_mot + plast·grad_tw` | `memoria_hebbiana_moto` *(`:9221`)* | la memoria vecchia ### **si SOVRASCRIVE**: *vince l'ultimo* | ### ⚠ **sì, MA va riscritta come SCAMBIO**, non come sostituzione | il vuoto locale, ### **e il tempo proprio** *(oggi ticchetta su `DT` globale)* | ### ⛔ **NO** |
| `5` | `− omega_src/_tau` | `_passo_spinoriale` *(`:5929`)* | la rotazione dello spinore ### **decade** | ### ✔ sì, col vuoto locale | idem | ### ⛔ **NO** |
| ### ⭐ **`6`** | ### **`np.where(scende, dx·fatt, dx)`** | ### **`_smorza`** *(`:6554`)*, chiamato da `_smp_chiudi` *(una volta per passo)* | ### ⛔ **smorza le DISCESE e lascia passare le SALITE**: `fatt = max(0, 1 − LAM/prima)` si applica ### **solo dove `dx < 0`** | ### ✔ **sì, e SENZA il vuoto**: basta un vincolo ### **SIMMETRICO** | ### ✔ **niente di nuovo**: le ### **tre candidate sono già registrate** in `D31` *(la piana, Itô, `tanh`)*, e la `tanh` ha ### **deriva ZERO esatta** | ### ⭐ ✔ **SÌ — CANDIDATO AD ANTICIPO** |
| `7` | `return np.maximum(v, LAM)` | ### **`_nasce`** | ### ⛔ **ALLUNGA e MAI accorcia**: un troncone sotto `LAM` viene ### **portato A `LAM`** | ### ⚠ **non è un rilassamento: è un CANCELLO mancato.** La via non è renderlo reversibile, è ### **non far nascere l'arco corto** | ### **il cancello allo Schwinger** *(`SCHW-SOTTO-LAM`)*, e la decisione di Luca su ### **quale lunghezza** confrontare con `LAM` | ### ✔ **SÌ**, perché è un cancello e non un bilancio |
| `8` | il ### **termostato globale** *(Nosé-Hoover)* | scrive `phivel` ### **dall'esterno** | energia ### **e** carica, a senso unico | ### ⚠ **sì in principio** *(un termostato di contatto è reversibile nel suo spazio esteso)*, ### **ma è GLOBALE** *(`A2`)* | il ### **vuoto locale**, che lo sostituirebbe | ### ⛔ **NO** |
| `9` | ### **`scuoti_vuoto`** | inietta rumore | ### **inietta** e non riassorbe | ### ✔ **sì**: è esattamente ciò che `VUOTO-LOCALE-DETERMINISTICO` deve diventare | il vuoto locale | ### ⛔ **NO** |

### ⚠ **E UNA RIGA CHE IL CENSIMENTO HA TROVATO E CHE NON E' UNA FRECCIA NEL TEMPO**

```
p_anti = np.where(s > 0, np.tanh(s), 0.0)      # mitosi, :8803
```

| | |
|---|---|
| sembra | un ### **raddrizzatore**: positivo passa, negativo diventa `0` |
| ### ✔ **non lo è** | `p_anti` è una ### **PROBABILITÀ**, e una probabilità ### **non può essere negativa**: il `0` non è una freccia nel tempo, è ### **il bordo del dominio** |
| ### ✔ **e in più NON GIRA** | è dentro `if ANTIFASE_ADD:` e ### **`ANTIFASE_ADD = False`** *(`:3092`)*, ### **assente dall'argv del driver** |

> ### ✔ **LO SCRIVO PERCHE' IL CENSIMENTO L'HA TROVATA**, non perché sia una violazione:
> ### **un censimento che tace ciò che ha scartato non si può ricontrollare.**

**E LE ALTRE SETTE RIGHE con una condizione di segno** *(`_passo_spinoriale` `:5572`,
`:5695`, `:5936`, `:6038`; `step` `:7924`, `:8027`, `:8028`)* ### **sono selettori di segno
nello SPAZIO o nella CARICA, o guardie anti-zero** — ### **non frecce nel tempo.** I `clip` a
un lato trovati stanno tutti in ### **`_diag_completa`** *(diagnostica)* e in `_celle_vive`
*(binning spaziale)*: ### **nessuno in una legge.**

## `B` — ✔ **LA FRECCIA AMMESSA, e NON è una violazione**

> ### ⭐ **LA CRESCITA DELLO SPAZIO.** Le nascite di nodi e di archi sono
> ### **a senso unico PER SCELTA DI LUCA**, e la scelta è ### **registrata.**

| | |
|---|---|
| dove è registrata | ### **`doc/REGISTRO_FISICA.md`, scheda `REVERSIBILITA-LOCALE`** *(2026-10-02)*: *«L'irreversibilita' globale EMERGE dal caos delle leggi locali reversibili (Boltzmann). ### **La SOLA freccia fondamentale ammessa e' la CRESCITA DELLO SPAZIO** — la nascita dei nodi.»* |
| il criterio che la verifica | ### **`LOSCHMIDT-ECO`**: *«L'eco di Loschmidt FALLISCE SOLO nella voce della NASCITA.»* ### **Se fallisse anche in `step`, in `chiudi` o nel termostato, la direzione NON sarebbe soddisfatta dal codice di oggi** |
| lo stato di quella scheda | era ### **«IN VALUTAZIONE, non come decisione»** |

> ### ➜ **E `A15.3` PRECISATO LA PROMUOVE: ciò che era una direzione da valutare diventa un
> VINCOLO SULLA FORMA DELLE LEGGI.** ### **Il criterio misurabile c'era già**, e ### **le
> nove frecce della tabella `A` sono esattamente ciò che l'eco di Loschmidt dovrebbe trovare
> fuori posto.**

## ⛔ **CHE COSA DICE QUESTO CENSIMENTO, in una riga**

| | |
|---|--:|
| frecce imposte trovate | ### **`9`** |
| curabili ### **SOLO dopo** il vuoto locale | ### **`7`** |
| ### ⭐ **curabili PRIMA** | ### **`2`** — ### **`_smorza`/`D31`** *(un vincolo simmetrico, tre candidate già registrate)* e ### **`_nasce`** *(un cancello, non un bilancio)* |
| righe scartate dal censimento, ### **dichiarate** | ### **`8`** *(un bordo di dominio e sette selettori di segno)* |

> ### ⛔ **E LA DECISIONE SU `D31` COME CANDIDATO AD ANTICIPO È DI LUCA.** ### **Io dico
> che si PUÒ fare prima; non che si DEBBA.**

## ⛔ **ANNOTAZIONE DEL 2026-10-07: QUALI MEMORIE SONO <<PROVVISORIE>>, e perche'**

*(Dalla precisazione di `A15.3`: una memoria della forma ### **<<insegue e dimentica>>** ### **contiene la freccia PER COSTRUZIONE**, quindi e' ### **una forma PROVVISORIA.**)*

| la memoria | come nasce | che cosa significa |
|---|---|---|
| ### **`MEM-VERSO`** | ### ⚠ **nella forma ATTUALE**, se adottata ### **prima del vuoto locale** | usa ### **`delta = twp - tw`**, che e' una media mobile *(<<insegue e dimentica>>)*: ### **si scrive SOLO come forma PROVVISORIA**, ### **da convertire in SCAMBIO REVERSIBILE col vuoto** quando arriva `VUOTO-LOCALE-DETERMINISTICO`. ### ✔ **E non peggiora il bilancio**: il termine `-dt_e*tw/tau_tw` ### **c'e' gia'** |
| ### **`M-FLUSSO`** | ### ⚠ **idem** | sostituisce `mem_mot`, che ### **dimentica sovrascrivendo**: ### **forma PROVVISORIA**, da convertire. ### ⛔ **E deve nascere col TEMPO PROPRIO dell'arco** *(`dt_e/tau_tw` o equivalente derivato)* ### **e senza scale nascoste** -- l'annotazione sopra |
| ### **`M-LEGAMI`** | ### ✔ **NASCE DIRETTAMENTE REVERSIBILE** | non aggiunge nessun termine di decadimento: ### **cambia COSA si legge** *(`cos(dph - tw)` invece di `cos(phi0_i - phi0_j)`)*, non ### **come si dimentica** |
| ### **`M-MASSA`** | ### ✔ **NASCE DIRETTAMENTE REVERSIBILE** | ### **aggiunge** dissipazione, quindi ### **viene DOPO il vuoto locale per la condizione `(3)`** -- e arrivando dopo ### **non ha ragione di nascere a senso unico** |
| ### **`M-SPINORE`** | ### ✔ **NASCE DIRETTAMENTE REVERSIBILE** | idem, e in piu' il suo oggetto *(un trasporto ### **unitario** SU(2))* e' ### **reversibile per costruzione**: `U` e' invertibile |
| `M-ISTERESI` | ### ⚠ **da valutare** | un'isteresi e' ### **dissipativa per definizione** *(l'area del ciclo)*. ### ⛔ **Non l'ho analizzata in questa chiave**, e dirlo vale piu' che classificarla a caso |

> ### ⛔ **E LA VERIFICA DI UNA FORMA REVERSIBILE E' L'ECO DI LOSCHMIDT** -- avanti, inversione, indietro, ### **il sistema deve tornare a meno del caos.** ### **Voce `LOSCHMIDT-ECO`**, e il criterio registrato dice che ### **l'eco deve fallire SOLO nella voce della NASCITA.**

---

# ⭐ **ANNOTAZIONE DEL 2026-10-07 SERA — I NUMERI DI `M5`, DALLA CORSA DA `1000` PASSI** *(`par.8`: si ANNOTA, non si riscrive)*

> ### ⛔ **TUTTO CIÒ CHE SEGUE VIENE DA UNA SOLA CORSA, CON `U1` APERTA**, e serve a
> ### **SCEGLIERE fra letture della STESSA corsa**, non a dare valori assoluti.
> ### **Le decisioni sono di Luca.** Riferimenti: referto
> `doc/REFERTO_verso_e_plaquette_2026-10-06.md`, dati
> `csv/_test_fork/_misura_verso/verso.json`, commit `67f020e`.
> ### ✔ **E IL CONTROLLO CHE LI RENDE LEGGIBILI È PASSATO:** `n` e `archi` combaciano
> ### **AL BIT con `amp0.json` su tutti i `1000` passi** *(`csv/_seal_fork/_inerzia_nascite/`)*
> — gli osservatori, involucri di nascita compresi, ### **non cambiano la dinamica.**

## `(a)` ⛔ **`phi0` È MEMORIA MORTA, E IL NUMERO NON È DI BORDO** → la scheda `PHI0-CONGELATA` e `M-LEGAMI`

Spearman fra `c0 = cos(phi0_i − phi0_j)` *(congelato)* e `c_δ = cos(dph − tw)` *(vivo)*, sugli
archi ### **VUOTO con età `> 2 τ_tw`**:

| passo | Spearman | archi |
|--:|--:|--:|
| `150` | `−0.0435` | `17174` |
| `230` | `+0.0076` | `62636` |
| `300` | `+0.0102` | `103878` |
| `400` | `+0.0006` | `138781` |
| `500` | `+0.0001` | `161099` |
| `700` | `−0.0003` | `178043` |
| ### **`1000`** | ### **`+0.0022`** | ### **`183067`** |

### **La soglia fissata PRIMA era `0.3`. Il massimo oltre il `216` è `0.0102`: TRENTA VOLTE
sotto.** ### ⭐ **Non è un esito di bordo, ed è misurato su `183067` archi.**

> ### ➜ **CONSEGUENZA PER `M-LEGAMI`:** la memoria congelata dei legami e quella viva
> ### **non sono correlate.** Sostituire `c0` con `cos(dph − tw)` ### **non è un
> raffinamento: è cambiare grandezza.** ### ⚠ **E questo NON dice quale delle due sia
> giusta** — dice che la scelta ### **non è innocua**, e che va decisa, non scivolata.

## `(b)` ⭐ **IL DIPOLO NON DOMINA `δ`, MA DOVE AGISCE VALE UN QUARTO** → la scheda `MEM-VERSO`

Mediana di `|tw_dip| / |tw|`, con `tw_dip` ### **accumulatore PARALLELO** *(non tocca `net`)*:

| | mediana su TUTTI gli archi | ### **sugli archi con un salto nei `50` passi prima** | archi |
|--:|--:|--:|--:|
| `230` | `0.0` | ### **`0.2751`** | `285` |
| `500` | `4.3e-07` | ### **`0.2780`** | `2255` |
| ### **`1000`** | ### **`2.2e-08`** | ### **`0.2289`** | ### **`9105`** |

### ⛔ **E LA MEDIANA A ZERO DA SOLA SAREBBE SOSPETTA** *(un accumulatore morto darebbe lo
stesso numero)*. ### ✔ **IL CONTROLLO POSITIVO LA SALVA: dove il dipolo agisce,
l'accumulatore PARLA** — `23–28 %` di `|tw|`.

> ### ➜ **CONSEGUENZA PER `MEM-VERSO`: il criterio è SODDISFATTO** *(mediana `< 0.5`)*,
> quindi ### **`MEM-VERSO` non leggerebbe SE STESSA** — il timore che fosse ### **un anello
> invece di una cura** ### **non si realizza.** ### ⚠ **Ma `23–28 %` dove il dipolo agisce
> non è nulla:** una memoria del verso costruita su `δ` ### **erediterebbe un quarto del
> calcio del dipolo** su quegli archi, e ### **va detto nella scheda prima di adottarla.**

## `(c)` ⛔ **L'OSSERVAZIONE DI LUCA È SMENTITA: LA DISSIPAZIONE NON STA NEL VUOTO** → `P-DECADIMENTO`, §`3`

Il criterio fissato PRIMA: *«la dissipazione sta nel VUOTO»* se la potenza per nodo
### **mediana** in MATERIA è ### **meno di UN QUARTO** di quella in VUOTO, a ### **TUTTI** i
passi pesanti dopo il `300`.

| passo | MATERIA | VUOTO | ### **rapporto** | sotto `1/4`? |
|--:|--:|--:|--:|---|
| `150` | `0.3841` | `1.5414` | ### **`0.249`** | ### ⚠ **SÌ, per un PELO** *(il quarto è `0.2500`)* |
| `230` | `0.5008` | ### **`NaN`** | — | ### ⛔ **NON DECIDIBILE** *(il veleno di un arco appena nato)* |
| `300` | `0.8397` | `2.2450` | `0.374` | ### ⛔ **no** |
| `400` | `1.8843` | `2.6261` | `0.717` | ### ⛔ **no** |
| `500` | `3.1820` | `3.0533` | ### **`1.042`** | ### ⛔ **no** |
| `700` | `4.2104` | `4.0334` | ### **`1.044`** | ### ⛔ **no** |
| ### **`1000`** | `5.2288` | `5.1395` | ### **`1.017`** | ### ⛔ **no** |

> ### ⛔ **IL RAPPORTO SALE MONOTONO E SUPERA `1`: la dissipazione NON si concentra nel
> vuoto, SI EQUALIZZA** — e dal passo `500` la ### **MATERIA dissipa leggermente PIÙ** del
> vuoto. ### **`4` passi valutati dopo il `300`, ZERO soddisfatti.**

### ⚠ **E IL PASSO `150` LA CONFERMAVA PER UN PELO** *(`0.249` contro `0.250`)*: ### **una
misura fermata al `150` avrebbe detto il CONTRARIO.** ### ⛔ **È ancora
`FINESTRA-PRE-NASCITA`, e questa volta la finestra corta avrebbe CONFERMATO un'idea invece
di romperla** — che è il modo in cui una trappola fa più danno.

> ### ➜ **CONSEGUENZA PER `P-DECADIMENTO`:** la proposta *«una memoria che dimentica dissipa
> solo quando ha qualcosa da dimenticare»* ### **non trova appoggio in questa misura.**
> ### ⚠ **E NON È UNA CONFUTAZIONE DEL PRINCIPIO:** il principio parla di ### **una memoria
> ben posta**, e `tw` oggi ### **non lo è** — `U1` è aperta e il termine di rilassamento è
> uno dei pezzi in discussione. ### **Dice che il bilancio della torsione di OGGI non è il
> costo di una memoria che rincorre**, e che ### **chi proponesse di leggerlo così deve
> prima spiegare questo rapporto che sale.**

## `(d)` ⭐ **E UNA COSA CHE NON CAMBIA MAI: LA BASE DEI CICLI** → `MEM-VERSO`, `M-SPINORE`

### **`0.00 %` di cicli di base cambiati a TUTTI gli `8` passi misurati, con `827` nascite.**
### ⭐ **Una memoria indicizzata sui cicli di base avrebbe un supporto STABILE** — e questo
era il dubbio principale su una lettura topologica del verso.

## ⚠ **E TRE NUMERI CHE NON ERANO IN NESSUNA SCHEDA, e che una scheda futura deve guardare**

| | |
|---|---|
| le spinte mediane oltre il `216` | ### **`perc_geom` `1160.8` < `D` `5260.6` < `A` `8725.8` < `MEM` `9837.0`** |
| ### ⛔ **e la legge di OGGI inietta MENO di tutte** | avevo previsto che la minore fosse `D`: ### **previsione SMENTITA.** ### **Una memoria del verso, in qualunque forma, inietterebbe PIÙ spinta di `perc_geom`** — e questo è un costo, non un dettaglio |
| la frazione con `|tw| > 2π` | sale ### **monotona** da `0` a ### **`7.64 %`** al `1000` *(avevo previsto `15–25 %`: ### **SMENTITA**, ma il verso della crescita era giusto)* |
| gli archi per origine | ### **`1130`** da divisione, ### **`524`** da Schwinger, ### **`0`** senza origine |

> ### ⛔ **IL FATTO CHE `perc_geom` INIETTI LA SPINTA MINORE NON LA RENDE GIUSTA:** inietta
> poco ### **perché perde il verso** *(`GEOM-SENZA-VERSO`)*, e una grandezza che perde
> informazione ### **è naturalmente più quieta.** ### ⚠ **Ma va scritto come COSTO delle
> alternative**, invece di essere scoperto dopo.

### ⛔ **E LA SCELTA FRA LE OPZIONI NON È IN QUESTO DOCUMENTO: È DI LUCA.**
### **Questa annotazione riporta i numeri e dice che cosa vincolano. Non sceglie.**

---

# ⛔ **ANNOTAZIONE DEL 2026-10-07 SERA — `M5d` NON È «SMENTITA»: È NON DECIDIBILE** *(decisione di Luca; `par.8`: si ANNOTA, non si riscrive)*

> ### ⛔ **L'ETICHETTA CAMBIA, IL NUMERO NO.** Il paragrafo `(c)` qui sopra resta leggibile con
> la sua tavola: ### **la tavola è giusta, la CONCLUSIONE che le ho attaccato no.**

## LA RAGIONE, ED È UNA CONDIZIONE DEL TEST CHE NON C'ERA

L'osservazione di Luca diceva che ### **la memoria non dissipa dove la struttura è STABILE.**
Il mio test confrontava la potenza per nodo fra le classi ### **MATERIA / BORDO / VUOTO** —
### ⛔ **ma quelle classi sono GEOMETRICHE: dicono dove le masse erano state SEMINATE, non dove
c'è struttura.**

E la corsa `A1` dice che ### **dal passo `400` la zona MATERIA è MENO coerente del vuoto**:

| passo | AUC MATERIA/VUOTO | `c_k` mediana MATERIA | VUOTO |
|--:|--:|--:|--:|
| `1` | `0.9992` | ### **`0.7904`** | `0.1627` |
| `300` | `0.7371` | `0.3870` | `0.2744` |
| ### **`400`** | ### **`0.4679`** | `0.2882` | `0.2972` |
| `1000` | `0.4415` | `0.2875` | ### **`0.3123`** |

### ⭐ **`c_k` di MATERIA SCENDE e quella del VUOTO SALE: si INCROCIANO attorno al `400`.**
### ➜ **Quindi i passi `400`, `500`, `700`, `1000` — cioè TUTTI quelli su cui il criterio
decideva — confrontavano «dove la materia ERA» con «il vuoto», e la prima era la MENO
strutturata delle due.** ### ⛔ **Il criterio chiedeva se la memoria dissipa dove la struttura
è stabile, e lì NON C'ERA STRUTTURA STABILE DA NESSUNA PARTE.**

> ### ✔ **IL VERDETTO: `NON DECIDIBILE`, finché non esistono masse che durano.**
> ### **I numeri restano** *(il rapporto `0.249 → 1.017`)*, e ### **vanno riletti quando il
> test avrà la sua condizione.**

## ⚠ **E IL MIO ARGOMENTO, scritto ACCANTO e senza cambiare l'etichetta**

### **Sono d'accordo sulla sostanza, e aggiungo una cosa che il cambio di etichetta non deve
far perdere:** al passo ### **`150`** — dove le masse ### **c'erano ancora** *(AUC `0.9861`,
`c_k` MATERIA `0.6483` contro VUOTO `0.2430`)* — il criterio era soddisfatto
### **per un PELO: `0.249` contro la soglia `0.2500`.**

### ➜ **Cioè: nell'UNICO passo misurato in cui la condizione del test c'era, l'osservazione
passava sul filo.** ### ⚠ **Non è una conferma** *(un passo solo, e un margine di `4e-4`)*,
### **ma non è neanche niente:** quando `A-S1` darà masse che durano, ### **il numero da
guardare è se quel `0.249` scende o sale.** ### **Lo scrivo adesso perché una previsione
scritta dopo non è una previsione.**

## ✔ **E `M5b` TOGLIE UN OSTACOLO: il vincolo su `M-LEGAMI` CADE** *(decisione di Luca)*

La scheda ### **`M-LEGAMI`** portava il vincolo *«solo DOPO la cura del verso»*, perché si
temeva che una memoria dei legami costruita su `δ` ### **leggesse il dipolo invece dello
stato.** ### ⭐ **`M5b` lo esclude con il numero:** la mediana di `|tw_dip|/|tw|` è
### **`≈ 0`** su tutti gli archi, e ### **`23–28 %` SOLO sugli archi toccati da un salto nei
`50` passi prima.**

### ➜ **Quindi `M-LEGAMI` non deve più aspettare la cura del verso, e può entrare in `A-S2`**
*(la cura di `H2`, se `H1` non basta)*.

> ### ⚠ **MA IL `23–28 %` NON SPARISCE, e la scheda lo porta:** sugli archi con un salto
> recente ### **un quarto di `|tw|` viene dal dipolo**, quindi `M-LEGAMI` su quegli archi
> ### **erediterebbe un quarto del calcio.** ### **Il vincolo cade; l'avvertenza resta.**
