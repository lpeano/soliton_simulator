# LA TRADUZIONE DELLE LEGGI DEL SIMULATORE IN TERMINI DI `H`

> ### ⛔ **QUESTO DOCUMENTO NON CAMBIA NIENTE NEL SIMULATORE** *(resta `b8c21049`)*, e ### **non decide la forma di `H`:** ### **propone**, e marca ogni proposta ### **candidata** o ### **aperta**. ### **La forma di `H` e la regola di crescita sono DECISIONI DI LUCA.**
>
> *I numeri escono da quattro uscite, e nessuno e' ricopiato a mano* *(`L-NUMERI`)*: `_censimento_leggi` · `_prova_integrabilita` · `_crescita_conti` · `proto_primo_ordine/uscite/diagnosi_v2`. Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_traduzione-in-H.md`, committato ### **prima** *(`c6c1112`, col criterio del «no» in `2f47b75`)*.

# 📌 `⓿` **LA CONFIGURAZIONE DELLE MISURE** *(`P5`: non i flag toccati, TUTTI)*

### ⛔ **Questo documento non fa girare niente: riporta le misure di tre strumenti**, e la configurazione e' ### **quella che LORO hanno dichiarato**, non una che io ridico:

| | |
|---|---|
| booleani di modulo confrontati con l'argv ### **del DRIVER** | ### **`82`** |
| l'esito | ### **nessuna differenza. ZERO su 82.** |
| la scena | `12802` nodi, `471564` archi, `DT = 0.01`, snapshot di `3` passi ### **pieni** *(`_passo.passo_pieno`, non `net.step()`)* |
| dove sta la dichiarazione per intero | `csv/_test_fork/_prova_integrabilita/integrabilita.txt` e `csv/_test_fork/_crescita_conti/crescita.txt` |

> ### ⚠ **E IL GENERATORE DI QUESTO DOCUMENTO E' ESENTE DA `H-P5`, dichiarato:** non importa il simulatore. ### **Chiamare `dichiara_configurazione` qui vorrebbe dire caricare il simulatore in un generatore di testo, e la dichiarazione sarebbe di un modulo appena importato — NON della scena che ha misurato.** L'esenzione e' in `doc/ESENZIONI_presidi.md`.

---

# ⭐ `①` **IL METODO -- e perche' il «NO» ADESSO SI DIMOSTRA**

Il metodo ovvio *(scrivere `E` e verificare `F = −∂E/∂x`)* ### **dimostra il sì ma non il no:** non trovare `E` prova solo che ### **non l'ho trovata**. Il rilievo e' di Luca, e ha prodotto un banco che decide ### **senza indovinare `E`**:

| | il test | che cosa decide |
|---|---|---|
| ### **`(A)`** | la legge ### **legge** la variabile che scrive? | ### ⛔ **se NO, non e' il gradiente di nessuna `E(x)`**: lo spazio d'ingresso non e' quello d'uscita. ### **E il `(B)` va SALTATO**, perche' darebbe `J = 0`, che e' simmetrica — ### **un FALSO-ZERO** |
| ### **`(B)`** | `\|\|J − Jᵀ\|\| / \|\|J\|\|` contro il ### **pavimento CALCOLATO** | ### **simmetrica ⇒ `E` ESISTE** *(localmente, in quelle variabili)*; ### **asimmetrica ⇒ un «no» DIMOSTRATO** |

### ✔ **E IL BANCO E' SANO -- tre controlli, e il terzo e' quello che conta:**

| controllo | numero | esito |
|---|--:|---|
| la coppia ### **SCALARE** *(gradiente noto)* deve essere ### **simmetrica** | `5.178e-12` contro un pavimento di `4.936e-09` | ### ✔ **PASSA** |
| la coppia del ### **DRIVER** deve risultare ### **non traducibile** | `0.000e+00` perturbando `φ` | ### ✔ **PASSA** *(per il `(A)`)* |
| ### ⭐ una coppia ### **SINTETICA** col prefattore di nodo deve risultare ### **asimmetrica** | `1.463e-02` | ### ✔ **PASSA** |

> ### ⭐ **IL TERZO CONTROLLO E' QUELLO CHE VALE, e non era nel mandato:** ### **un banco che approva tutto e un banco che funziona danno lo STESSO referto sul controllo positivo.** Serviva una legge che ### **DEVE** risultare asimmetrica, e l'ho costruita: ### **non e' una legge del simulatore**, e sta dichiarata come controllo.

### ⚠ **E TRE LIMITI, dichiarati PRIMA di usare il banco:**

| | |
|---|---|
| il «sì» e' ### **LOCALE** | e' la condizione di ### **Poincaré**: `J` simmetrica ⇒ la forma e' chiusa ⇒ `E` esiste ### **in un intorno dello stato misurato**, non globalmente |
| il «sì» e' ### **SUL CAMPIONE** | `40` nodi *(`3` di base col loro vicinato)*. ### ⚠ **Un «asimmetrica» invece e' un no SUL TUTTO**, perche' una `J` simmetrica ha ### **tutte** le sottomatrici principali simmetriche |
| vale ### **nelle variabili scelte** | una legge asimmetrica in `φ` puo' essere il gradiente di qualcosa ### **in variabili diverse** — ed e' il caso della coppia del driver, che la forma `U(2)` riscrive in `ψ`. ### **La tavola lo dice invece di nasconderlo** |

# ⭐ `②` **IL CENSIMENTO -- e il difetto che ha preso DI SE STESSO**

| | |
|---|--:|
| scritture di stato trovate, ### **per FORMA** | ### **`419`** su `339` nomi |
| funzioni raggiunte dalle ### **`10` radici dichiarate** | `68` |
| flag cambiati dall'argv ### **DEL DRIVER** | `32` |

> ### ⛔ **IL MANDATO DICEVA «`step()` E LE FUNZIONI CHE CHIAMA», E NON BASTA:** il grafo chiuso dal ### **solo `step`** raggiunge `44` funzioni e ### **NON contiene `mitosi`, Schwinger, `scuoti_vuoto` ne' la memoria hebbiana** — quelle le chiama ### **il DRIVER**. ### ➜ **Con la sola radice `step` avrei perso TUTTA la classe CRESCITA**, cioe' esattamente la classe su cui il mandato chiede il conto.

> ### ⚠ **E CIO' CHE IL METODO NON VEDE, dichiarato:** le scritture per ### **mutazione** *(un `dict` aggiornato dentro una funzione a cui l'oggetto e' passato)* — e' il falso positivo gia' preso su `conc_nodi`. ### **Per quelle il censimento e' per DIFETTO.**

# ⛔ `③` **LA TAVOLA -- legge per legge, con la classe e il perche'**

### ⚠ **LA CLASSIFICAZIONE E' UN GIUDIZIO MIO, e lo dichiaro:** i numeri che la sostengono vengono dalle uscite, il giudizio no.

| la legge | ancora *(nome, MAI una riga)* | variabile | ### **classe** |
|---|---|---|---|
| la coppia d'interferenza, ramo SCALARE | `_coppia_interferenza (ramo OFF)` | `phi` | ### **TRADUCIBILE** |
| il legame elastico delle lunghezze | `step, blocco di `vd` (VERLET)` | `d` | ### **TRADUCIBILE** |
| la repulsione | `REPULS_LEGGE, `_rep`` | `d` | ### **TRADUCIBILE** |
| il rilassamento della torsione | `step, blocco `tau_tw`` | `tw` | ### **CON UNA MEMORIA** |
| il rilassamento della lunghezza di riposo | `step, `tau_p_loc`` | `d0` | ### **CON UNA MEMORIA** |
| il rilassamento della pressione di equilibrio | `step, `tau_bg_loc`, TAU_DIFF` | `peq` | ### **CON UNA MEMORIA** |
| la precessione dello spinore e l'orologio | `_passo_spinoriale, `omega_s`` | `omega_s` | ### **CON UNA MEMORIA** |
| la memoria hebbiana del moto | `memoria_hebbiana_moto, `mem_mot`` | `mem_mot` | ### **CON UNA MEMORIA** |
| la dinamica dei pesi e delle distanze | ``w`, `d`, `d0` nello step` | `w, d, d0` | ### **CON UNA MEMORIA** |
| la mitosi | `mitosi, decidi_divisione` | `tutta la struttura` | ### **CRESCITA DELLO SPAZIO** |
| la creazione di coppia (Schwinger) | `mitosi, evento `schwinger`` | `tutta la struttura` | ### **CRESCITA DELLO SPAZIO** |
| la creazione degli archi | `_allaccia` | `i, j, d, d0, peq, tw, vd` | ### **CRESCITA DELLO SPAZIO** |
| la scomparsa degli archi | `le potature nello step` | `i, j` | ### **CRESCITA DELLO SPAZIO -- ma A ROVESCIO** |
| la sincronizzazione | `K_SYNC` | `phi` | ### **NON TRADUCIBILE -- DIMOSTRATO** |
| la coppia d'interferenza del DRIVER | `_coppia_interferenza (CAMPO_SPINORIALE)` | `phi` | ### **NON TRADUCIBILE IN phi -- DIMOSTRATO** |
| il termostato | `xi_termo, REGIME` | `phivel` | ### **NON TRADUCIBILE** |
| lo scuotimento del vuoto | `scuoti_vuoto` | `phivel` | ### **NON TRADUCIBILE** |
| il freno `_smorza` | `_smorza (D31)` | `d0` | ### **NON TRADUCIBILE -- FRECCIA** |
| lo smorzamento anisotropo | `ZETA_VIR, `beta*vd`` | `vd` | ### **NON TRADUCIBILE -- DISSIPAZIONE** |
| la massa critica | `massa_critica_adattiva, massa_critica_collasso` | `la soglia` | ### **NON TRADUCIBILE -- e' una SOGLIA** |
| i contatori `_g_*`, `_taup_*`, `_sfb_*` | `i prefissi diagnostici` | `-` | ### **DIAGNOSTICA** |

### **IL CONTO PER CLASSE** *(e `9-ter` chiede che si CONTI)*:

| classe | quante | previsto | scarto |
|---|--:|--:|--:|
| ### **TRADUCIBILE** | ### **3** | `7` *(`PT-2`)* | ### **-4** |
| ### **TRADUCIBILE CON UNA MEMORIA** | ### **6** | `6` *(`PT-3`)* | ### **=** |
| ### **CRESCITA DELLO SPAZIO** | ### **4** | `4` *(`PT-4`)* | ### **=** |
| ### **NON TRADUCIBILE** | ### **7** | `5` *(`PT-5`)* | ### **+2** |
| ### **DIAGNOSTICA** | ### **1** | `3` *(`PT-6`)* | ### **-2** |
| ### **IN TUTTO** | ### **21** | `24`..`32` *(`PT-1`)* | ### **SOTTO IL MINIMO** |

> ### ⛔ **`PT-1` E' MANCATA, E DAL BASSO: `21` contro un minimo di `24`.** Il motivo non e' che le leggi sono meno: e' che ### **le ho RAGGRUPPATE piu' grosso di quanto avessi previsto.** Il censimento trova `419` ### **scritture**; la tavola ha `21` ### **righe**, perche' *«il rilassamento di `d0`»* e' una riga e ### **dieci** scritture. ### ➜ **La previsione contava una cosa e la tavola conta un'altra, e la differenza e' MIA, non del sistema.** ### **Lo scrivo invece di spezzare le righe fino a far quadrare il numero.**

> ### ⭐ **`PT-9` LA VINCE, E DI PIU' DI QUANTO AVESSI SCRITTO:** dicevo che il test avrebbe spostato ### **almeno `2`** leggi fuori da TRADUCIBILE. ### ➜ **Ne ha spostate `4`**, e `TRADUCIBILE` passa da `7` previste a ### **`3`**. ### **Le quattro:** la ### **sincronizzazione** *(dimostrata non integrabile)*, la ### **coppia del driver** *(non legge `φ`)*, il ### **freno `_smorza`** *(a senso unico, instradata dal punto `(3)`)* e la ### **massa critica** *(non e' una forza: e' un criterio)*.

> ### ⚠ **E `DIAGNOSTICA` E' `1` RIGA, NON `3`, e non e' un errore di conto:** la riga copre ### **`231` nomi** riconosciuti per forma. ### **`PT-6` contava le LEGGI, la tavola conta le RIGHE**, e le due cose non sono la stessa — lo dico invece di far quadrare il numero.

### ⛔ **E IL TERMINE DI ENERGIA, O IL MOTIVO PER CUI NON C'E', UNA PER UNA:**

| la legge | ### **`E_x` o il vincolo** | esito della verifica |
|---|---|---|
| ### **la coppia d'interferenza, ramo SCALARE** | E = -K_C * somma_archi A_ij cos(phi_i - phi_j);  i dpsi/dt = dE/dpsi* | SIMMETRICA al banco, e il gradiente coincide a 1.49e-15 (D2-BIS) |
| ### **il legame elastico delle lunghezze** | E = (1/2) somma_archi k_ij (d_ij - d0_ij)^2, con d0 CONGELATA nel termine | NON MISURATA in questo giro: la forza non e' isolabile senza riscrivere il passo |
| ### **la repulsione** | E = somma_archi V_rep(d_ij), con V_rep decrescente;  la forza e' -dV/dd | NON MISURATA: `_rep` INSEGUE un bersaglio, quindi il termine vale a `_rep` FERMA |
| ### **il rilassamento della torsione** | tw entra in H come grado lento d'ARCO: E_tw = (1/2) somma_archi tw^2 / tau_tw, e il rilassamento e' la discesa di E_tw -- ma SOLO se tau_tw non dipende da tw | la legge dipende da una VELOCITA' (\|Delta omega\|): instradata dal punto (3) |
| ### **il rilassamento della lunghezza di riposo** | d0 entra in H come grado lento d'arco: E_d0 = (1/2) somma (d - d0)^2 / tau_p_loc | 10 scritture da 4 funzioni: NON e' una legge sola, e il test va fatto sul SISTEMA |
| ### **il rilassamento della pressione di equilibrio** | E_peq = (1/2) somma (rho - peq)^2 / tau_bg + (1/2) somma_archi (peq_i - peq_j)^2 / TAU_DIFF  -- il secondo e' un LAPLACIANO, che e' simmetrico | la diffusione usa TAU_DIFF = 1.0 NUDO: una MANOPOLA, e A1 la vieta |
| ### **la precessione dello spinore e l'orologio** | omega_s e' il grado lento di NODO dell'orologio; in H sta come E_om = (1/2) somma omega_s^2 * I_nodo, con I = (d/cs)^2 | il rilassamento usa tau = d/cs, DERIVATO (`--tau-luce`): e' l'esempio di A15.2 |
| ### **la memoria hebbiana del moto** | nessun E_x scritto: la legge e' una MEDIA MOBILE, e una media mobile NON e' una discesa -- VINCE L'ULTIMO invece di bilanciare | A14 n.4 + MEM-HEBB-VERSO: la forma va CAMBIATA, non tradotta |
| ### **la dinamica dei pesi e delle distanze** | e' il punto A16.3: w e U devono essere gradi di liberta' DENTRO H. Nel prototipo sono FISSI, ed e' una violazione DICHIARATA | APERTO: la forma del termine di memoria d'arco NON e' scritta |
| ### **la mitosi** | NON e' un termine di H: e' l'unica legge che CAMBIA H. Vincoli: (1) Sigma rho conservata; (2) il Delta H pagato dal vuoto LOCALE | la tavola delle regole NON ha una classe <<il genitore cede>>: Sigma rho CRESCE |
| ### **la creazione di coppia (Schwinger)** | come sopra, piu' il vincolo di CARICA: l'antinodo nasce a fase opposta, e quello si conserva | e' il ramo che conserva N(+1) - N(-1): la carica nasce OPPOSTA |
| ### **la creazione degli archi** | un arco nuovo e' un termine NUOVO in H: il suo contributo va pagato | `peq` nasce `nan` e lo step la CALIBRA: una nascita con un marcatore, non con un valore |
| ### **la scomparsa degli archi** | NON c'e' forma: A14.2 dice che la CRESCITA e' l'unica freccia ammessa, quindi un arco che muore e' GIA' una violazione | e' un difetto, non una legge da tradurre: va nell'elenco di Luca |
| ### **la sincronizzazione** | NESSUNA. Il banco misura un'asimmetria di `1.0641` contro un pavimento di `1.438e-10` | un <<no>> DIMOSTRATO: nove ordini sopra il pavimento, identico ai tre passi h |
| ### **la coppia d'interferenza del DRIVER** | NESSUNA in phi: la legge NON LEGGE phi (0.000e+00). La forma U(2) la riscrive in psi, ma a 1.054 di scarto, cioe' il 105 % -- per il criterio del <<no>> NON e' una traduzione, e' UNA LEGGE NUOVA | test (A): spazio d'ingresso (lo spinore) diverso dallo spazio d'uscita (phi) |
| ### **il termostato** | NESSUNA: scrive `phivel` DALL'ESTERNO, ed e' GLOBALE (A2). Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.1. E il numero: senza bagno le nascite crollano da 164 a 0 |
| ### **lo scuotimento del vuoto** | NESSUNA: e' un forzante stocastico. Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.1, insieme al termostato |
| ### **il freno `_smorza`** | NESSUNA: e' un `clip` DA UN LATO, quindi a senso unico | instradata dal punto (3) del criterio del <<no>>: il test NON si fa, darebbe un FALSO-ZERO |
| ### **lo smorzamento anisotropo** | NESSUNA: dissipa. Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.2, gia' dichiarato |
| ### **la massa critica** | non e' una forza: e' un CRITERIO. In H non entra; entra nella REGOLA DI CRESCITA | U1 dice che `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE |
| ### **i contatori `_g_*`, `_taup_*`, `_sfb_*`** | nessuna: non muovono lo stato | `231` nomi riconosciuti per FORMA. ⚠ IL CRITERIO E' DI FORMA: ogni nome va verificato col <<nessun lettore>>, e questo giro NON lo fa |

# ⛔ `④` **I DUE «NO» DIMOSTRATI -- e si riconciliano con misure di prima**

| | il numero | la lettura |
|---|--:|---|
| ### **la SINCRONIZZAZIONE** | asimmetria ### **`1.0641`** contro un pavimento di `1.438e-10` | ### ⛔ **nove ordini sopra**, e ### **identica ai tre passi `h`** — non e' un artefatto. ### **Nessuna `E(φ)` esiste di cui `K_SYNC` sia il gradiente** |
| ### **la COPPIA DEL DRIVER** | `0.000e+00` | ### ⛔ **non legge `φ` AFFATTO**: scrive una coppia su `φ` leggendo ### **lo spinore**. Spazio d'ingresso ≠ spazio d'uscita |

> ### ⭐ **E LA SINCRONIZZAZIONE SI RICONCILIA CON `D2-TER`:** là la sync toglieva il ### **`93.44 %`** della crescita di `H` a `A` fissa ### **senza costare coerenza** *(`AUC400` `0.9394` → `0.9333`)*, e l'avevo scritto *«pompava senza ordinare»*. ### ➜ **È esattamente il comportamento di una forza NON CONSERVATIVA.** Quella misura era ### **il sintomo**; questa e' ### **la causa**, e le due non si scelgono: si spiegano a vicenda.

> ### ⛔ **E LA FORMA `U(2)` NON SALVA LA COPPIA DEL DRIVER:** sta a ### **`1.054`** di scarto, cioe' il ### **`105 %`**, ### **dieci volte sopra** la soglia del `10 %` che il criterio del «no» fissa. ### ➜ **Non e' una traduzione: e' UNA LEGGE NUOVA**, e va ### **nell'elenco delle decisioni di Luca**, non nella `H` candidata. ### ⚠ **Senza quella soglia l'avrei messa in `H`**, chiamando «traduzione» un cambio di fisica del `105 %`.

# ⭐ `⑤` **LA `H` CANDIDATA -- scritta per intero, e con i buchi VISIBILI**

```
H  =  - K_C * somma_archi A_ij cos(phi_i - phi_j)            <- la coppia SCALARE
      + (1/2) somma_archi k_ij (d_ij - d0_ij)^2              <- il legame elastico
      + somma_archi V_rep(d_ij)                              <- la repulsione
      + (1/2) somma_archi tw_ij^2 / tau_tw                   <- la torsione (memoria)
      + (1/2) somma_archi (d_ij - d0_ij)^2 / tau_p           <- d0 (memoria)
      + (1/2) somma_k (rho_k - peq_k)^2 / tau_bg
          + (1/2) somma_archi (peq_i - peq_j)^2 / TAU_DIFF   <- peq (memoria + LAPLACIANO)
      + (1/2) somma_k I_k omega_s_k^2,   I_k = (d_k/cs_k)^2  <- l'orologio (memoria)
```

| | ### **che cosa NON c'e', e si vede** |
|---|---|
| ### ⛔ **la sincronizzazione** | ### **NON c'e', ed e' dimostrato** che non possa esserci |
| ### ⛔ **la coppia del driver** | ### **NON c'e'**: la `H` candidata ha la coppia ### **SCALARE**. ### **Questa è la prima decisione di Luca** |
| ### ⛔ **termostato e scuotimento** | ### **NON ci sono**: vanno diventati scambio col ### **vuoto LOCALE** *(`A15.3`)*, e quella forma ### **non e' scritta** |
| ### ⛔ **la memoria hebbiana** | ### **NON c'e'**: una ### **media mobile non e' una discesa** *(vince l'ultimo)*. La forma va ### **cambiata**, non tradotta |
| ### ⚠ **`TAU_DIFF = 1.0`** | e' una ### **MANOPOLA NUDA** dentro un termine candidato: ### **`A1` la vieta**, e finche' resta tale quel termine ### **non e' ammissibile** |
| ### ⚠ **`w` e `U` dinamici** | ### **`A16.3`**: devono essere gradi di liberta' DENTRO `H`. ### **La forma del termine di memoria d'arco NON e' scritta** |

# ⭐ `⑥` **LA REGOLA DI CRESCITA -- a parte, perche' NON e' un termine di `H`**

> ### ⭐ **E' l'unica legge che CAMBIA `H`**, quindi non puo' starci dentro. ### **Si scrive accanto.**

```
QUANDO:  una grandezza della materia supera una soglia che e' UNA LEGGE, non un numero
         (A1, A15.2) -- oggi la soglia e' massa_critica_adattiva, e U1 dice che
         `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE
COME:    psi_p -> psi_p / sqrt(2)   sul genitore E sul nato, stessa fase, stessa
         direzione di Bloch                                     [CANDIDATA, S4]
CHI PAGA: il Delta H va ceduto o ricevuto dal VUOTO LOCALE      [APERTO, S5]
```

### ⛔ **LA REGOLA DI OGGI NON CONSERVA, E LA TAVOLA DEL SIMULATORE LO DICE.** Le `67` regole di nascita si leggono dalla tavola `_nascita_regola`, e fra le sue `26` classi ### **non ce n'e' NESSUNA che si chiami «il genitore cede»**:

| | |
|---|---|
| il nato prende la ### **media dei genitori** per | `phi` `phi0` `phivel` `pos` `psi` |
| ### ⛔ **e nessuno togli niente al genitore** | ### **`Σρ` CRESCE a ogni nascita** — e' la violazione ### **`6`** di `A14`, e qui e' ### **letta dalla tavola**, non dedotta |

### **IL CONTO SULLO SNAPSHOT** *(la `ρ` vera della scena, dopo `3` passi pieni; il nodo piu' denso ha `ρ = 2.9121e+01`, lo `0.0886 %` di `Σρ`)*:

| se quel nodo divide | `Σρ` | `Σρ²` |
|---|--:|--:|
| ### **la regola di OGGI** | ### **`+0.0886 %`** *(non conserva)* | `+0.2062 %` |
| ### **la regola CANDIDATA** `ψ → ψ/√2` | ### **`0.000e+00`** *(conserva AL BIT)* | ### **`-0.1031 %`** *(il `ρ²` del nodo si DIMEZZA)* |

# ⛔ `⑦` **`PT-7`: LA NASCITA FRENA IL COLLASSO? -- LA VINCE A META', E LA META' CHE PERDE E' QUELLA CHE CONTA**

La previsione, scritta ### **prima** *(`c6c1112`)*: *«la divisione impedisce il collasso, perche' conserva `Σρ` ma dimezza il contributo `ρ²` del nodo che divide»*. Il conto, sulla `H` della sonda:

```
H(un nodo)   = (g/2) N^2
H(due figli) = -2 w (N/2) + (g/2) * 2 * (N/2)^2  =  -w N + (g/4) N^2
Delta H      = -(g/4) N^2 - w N  =  (|g|/4) N^2 - w N
```

| `N` | `g` | `w` | `H` un nodo | `H` due figli | ### **`ΔH`** |
|--:|--:|--:|--:|--:|--:|
| `400` | `-5.0` | `1.0000` | `-400000.0` | `-200400.0` | ### **`+199600.0`** |
| `400` | `-5.0` | `5.6494` | `-400000.0` | `-202259.8` | ### **`+197740.2`** |
| `400` | `-10.0` | `1.0000` | `-800000.0` | `-400400.0` | ### **`+399600.0`** |
| `400` | `-10.0` | `5.6494` | `-800000.0` | `-402259.8` | ### **`+397740.2`** |

| | |
|---|---|
| ### ✔ **la META' CHE VINCE** | ### **la diluizione c'e', ed e' ESATTA:** `Σρ` si conserva al bit e il contributo `ρ²` del nodo ### **si dimezza** — cioe' la divisione toglie ### **esattamente** cio' che il collasso guadagna |
| ### ⛔ **la META' CHE PERDE** | ### **la divisione ALZA `H`**, quindi ### **NON avviene da sola:** `ΔH = +199600.0` per `N = 400`, `g = -5.0`. ### **Va PAGATA** |
| ### ⛔ ### ➜ **la conclusione** | ### **LA NASCITA E' UN FRENO SOLO SE QUALCUNO PAGA**, e chi paga e' il ### **VUOTO LOCALE** — che e' il punto ### **`S5`**, e ### **`S5` e' APERTO**. ### ⚠ **Non e' una conferma dell'ipotesi del guardiano: e' la dimostrazione che quell'ipotesi DIPENDE INTERAMENTE DAL PUNTO APERTO** |

> ### ⭐ **E IL NUMERO CHE LEGA QUESTO AL SIMULATORE:** senza bagno le nascite crollano da ### **`164`** *(`B-SCAL`, col bagno)* a ### **`0`** *(`B-SCAL-TS`, senza)*. ### ➜ **Nel simulatore di oggi chi paga la nascita E' IL BAGNO GLOBALE**, ed e' misurato. ### **La domanda di `S5` non e' accademica: e' la domanda su che cosa sostituisca quel bagno.**

# ⭐ `⑧` **IL CONFRONTO CON LA SONDA DEL PROTOTIPO, termine per termine**

| nella sonda | nel simulatore | la lettura |
|---|---|---|
| ### **l'hopping** `-w ⟨ψ_i|U|ψ_j⟩` | la ### **coppia d'interferenza** con `A = w·cos(φ⁰_i − φ⁰_j)` | ### ⚠ **il kernel del simulatore ha `φ⁰` CONGELATA** *(`PHI0-CONGELATA`)*: la sonda non ha niente di congelato, e in questo e' ### **meno** difettosa |
| ### **la COESIONE** `(g/2)|ψ|⁴` | ### ⛔ **NON esiste un `|ψ|⁴`.** La coesione viene dalla ### **coppia stessa** *(una `A` positiva lega le fasi)* piu' il ### **legame elastico** | ### ➜ **la sonda ha messo in un termine di sito cio' che nel simulatore e' un termine d'ARCO** |
| ### ⛔ **il FRENO** | la ### **repulsione** `V_rep(d)`, la ### **massa critica**, e ### **la nascita dello spazio** | ### ⛔ **LA SONDA NON HA NESSUNO DEI TRE**, ed e' per questo che collassa |
| ### **il grafo** | ### **dinamico**: nodi e archi nascono | ### ⛔ **nella sonda e' FISSO**: un'### **impalcatura del test**, dichiarata violazione provvisoria di `A16.3` |
| la ### **memoria** | `tw`, `d0`, `peq`, `omega_s`, `mem_mot` | ### ⛔ **la sonda non ha NESSUNA memoria**: `w` e `U` sono fissi |

> ### ⭐ **E IL NUMERO DEL MARE `v2` SI LEGGE ADESSO:** con la sonda, a norma fissa, lo stato piu' basso e' il ### **collasso su un nodo** per ogni `g < 0` *(a `g = -5`: `-400000.0` contro `-18533.8`)*. ### ➜ **Non e' un fatto sul modello di Luca: e' un fatto su una `H` CHE NON HA IL FRENO.** Il simulatore ne ha ### **tre**, e la tavola li nomina.

# ⛔ `⑨` **L'ELENCO DELLE DECISIONI DI LUCA** — *una per riga, con le alternative e che cosa cambierebbe*

| # | la decisione | le alternative | che cosa cambia |
|--:|---|---|---|
| `1` | ### **la forma della COESIONE e del suo FRENO** | `(a)` un termine che ### **satura** dentro `H`; `(b)` la ### **nascita dello spazio**; `(c)` ### **entrambi** | ### ⛔ **con `(a)` il freno e' dentro `H` e il collasso non avviene;** con `(b)` il freno e' una legge FUORI da `H` e ### **serve chi paga** *(`S5`)*; `(c)` e' l'unica che regge se `S5` resta aperto |
| `2` | ### **l'interferenza NORMALIZZATA sul grado, o no** | `w_ij` ### **come oggi**; oppure `w_ij/√(s_i s_j)` | il `PR` del Perron a `g = 0` passa da ### **`24.6`** a ### **`348.2`** su `400`: ### **la geometria da sola concentra, e la normalizzazione glielo toglie quasi tutto.** ### ⚠ **E tocca `A3`** *(`s_k` e' del proprio intorno — ma e' una SOMMA, non una statistica di posizione: `s̃_k` passa da `0.3856` a `0.1160` di deviazione, media `0.98`, ### **non `1`**)* |
| `3` | ### **la SINCRONIZZAZIONE: togliere o tradurre** | ### **togliere**; oppure tenerla come scambio dichiarato col vuoto | ### ⛔ **«tradurre» NON e' un'opzione: e' DIMOSTRATO che non esiste `E(φ)`** *(asimmetria `1.0641`)*. E `D2-TER` dice che toglierla costa ### **poco**: `AUC400` `0.9394` → `0.9333` |
| `4` | ### **`A` da `φ⁰` o dalla MEMORIA VIVA dei legami** | `φ⁰` ### **congelata** *(oggi)*; oppure una memoria d'arco che ### **evolve** | ### ⛔ **`φ⁰` congelata viola `A15.1`** *(non dimentica niente)* ed e' `PHI0-CONGELATA`. Con la memoria viva `A` diventa un grado di liberta' ### **dentro `H`** *(`A16.3`)*, e la `H` candidata acquista un termine |
| `5` | ### **il campo scalare a `φ/2`** | `cos(φ_i − φ_j)` ### **(oggi)**; oppure `cos((φ_i − φ_j)/2)` ### **(la direzione candidata di Luca)** | ### **cambia la periodicita'**: `φ/2` e' la doppia copertura `4π`, cioe' ### **lo spinore**. ### ⚠ **E il ramo scalare di oggi usa `cos(φ_i − φ_j)`**, non `/2`: era un test sul ### **principio**, non sulla forma |
| `6` | ### **che cosa diventano TERMOSTATO e SCUOTIMENTO** | restare forzanti ### **globali** *(oggi, e viola `A2` e `A14.1`)*; oppure ### **scambio col vuoto LOCALE** *(`A15.3`)* | ### ⛔ **e non e' indolore: senza bagno le nascite crollano da `164` a `0`.** Togliere il bagno ### **senza** mettere il vuoto locale ### **spegne la crescita** |
| `7` | ### **la forma della DIVISIONE alla nascita, e la soglia come LEGGE** | `ψ → ψ/√2` ### **(candidata)**; oppure un'altra ripartizione | ### ✔ **`ψ/√2` conserva `Σρ` al bit e dimezza il `ρ²` del nodo** — ma ### **alza `H` di `+199600.0`**, quindi serve `S5`. ### ⛔ **E la soglia di oggi NON e' una legge:** `U1` e' ### **bloccante** |
| `8` | ### **DA DOVE VIENE L'ENERGIA DELLO SPAZIO NUOVO** *(`S5`)* | il ### **bagno globale** *(oggi, misurato)*; oppure un termine di ### **vuoto LOCALE** da scrivere | ### ⛔ **E' LA DECISIONE DA CUI DIPENDONO LE ALTRE:** senza di essa la nascita non puo' essere il freno, e la `1` si riduce a `(a)` |
| `9` | ### **la forma `U(2)` della coppia** | tenerla; oppure no | ### ⛔ **NON e' una traduzione: e' UNA LEGGE NUOVA** — `1.054` di scarto, il `105 %`, dieci volte sopra la soglia del `10 %`. ### **Va decisa come fisica nuova, non adottata come riscrittura** |
| `10` | ### **la SCOMPARSA degli archi** | tenerla; oppure vietarla | ### ⛔ **`A14.2` dice che la CRESCITA e' l'unica freccia ammessa**, quindi un arco che muore e' ### **già una violazione**. ### **Non e' una legge da tradurre: e' un difetto da decidere** |

---

# ⛔ **CHE COSA QUESTO DOCUMENTO NON DICE**

| | |
|---|---|
| la ### **forma di `H`** | ### ⛔ **non la decide.** La `H` del `⑤` e' ### **candidata**, e ha ### **due buchi dichiarati** *(`TAU_DIFF` nuda, `w`/`U` fissi)* |
| che le ### **traducibili** siano verificate | ### ⛔ **NO:** ### **una sola** lo e' *(la coppia scalare)*. Le altre dicono ### **perche' non lo sono**, e il motivo e' sempre lo stesso: ### **la forza non e' isolabile senza riscrivere il passo** |
| che la nascita ### **frenerebbe** | ### ⛔ **non lo dice:** dice che ### **diluisce esattamente** e che ### **costa**, quindi dipende da `S5`, ### **che e' aperto** |
| che i ### **contatori** siano davvero diagnostici | ### ⚠ **il criterio e' di FORMA** *(prefissi e code)*, e ### **puo' sbagliare**: ogni nome va verificato col ### **«nessun lettore»**, e questo giro ### **non lo fa** |
| le ### **scale e i semi** | ### **uno snapshot, una scena, `3` passi.** ### **`P3` non e' soddisfatta**, e il documento non pretende il contrario |
