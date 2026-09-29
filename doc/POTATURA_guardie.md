# ✂ **`POTATURA-GUARDIE`: i 57 rami MORTI, in coda alla potatura generale**

> ### **Generato da uno script dalla tabella `doc/RIPIEGHI_classi.md`** *(`L-NUMERI`)*: la lista
> non e' scritta a mano. **Si rigenera quando la tabella si rigenera.**

> ### 🛑 **DECISIONE DI LUCA, 2026-09-29: la pulizia SI RIMANDA alla POTATURA GENERALE, dopo lo
> ### schedulatore** — perche' ### **il riordino della mitosi tocchera' molte di queste righe**,
> e potarle adesso vorrebbe dire farlo **due volte**. ### **Questa voce e' la lista, non il
> lavoro.**

## Perche' sono rami MORTI, e perche' nessuna misura lo verifica

| | |
|---|---|
| **sono morti** | con il **controllo unico** acceso, ai due punti del passo ogni grandezza di **STATO** ha lunghezza **esattamente** `n` o `m`: ### **la condizione di lunghezza di questi siti non puo' piu' essere falsa** |
| ### **e nessuna misura li verifica** | la prova a guasto trova **solo** cio' che il controllo **non** copre: per questi ### **il controllo spara PRIMA**. ➜ **«Zero ripieghi silenziosi» e' gia' raggiunto senza toccarli** |
| ### **quindi il rischio e' a SENSO UNICO** | un errore nella potatura puo' rompere il **percorso VIVO**, e ### **nessun braccio del sigillo lo distinguerebbe da un errore di battitura** |

## ⭐ **LA REGOLA, e vale anche per la potatura futura**

> # **IL CONTROLLO UNICO POSSIEDE LE LUNGHEZZE.**
> # **I SITI POSSIEDONO SOLO «ESISTE ANCORA?».**

| forma del sito | che cosa se ne fa |
|---|---|
| **condizione FUSA** *(`is None` / `not hasattr` **e** un test di lunghezza)* — ### **12 siti** | si **tiene** il test di **esistenza** *(e' un'inizializzazione vera, e resta)*; ### **la LUNGHEZZA SOLLEVA** |
| **sola LUNGHEZZA** — ### **45 siti** | ### **si TOGLIE**: il controllo la garantisce, e una guardia che non guarda niente e' `A9` |

### ⚠ **E si confrontano ANCHE I CONTATORI, non solo le grandezze**
Questi rami **si contano** *(`A8`)*: `_ritmo_sicurezza`, `_ritmo_guard4pi_ko`,
`_ritmo_snap_identico`, `_g_zeta_vir_*`, `_cs_in_fallback`… ### **Un contatore che cambia di UNO
e' un difetto, e le 23 grandezze del sigillo NON lo vedrebbero** — lo stato puo' restare
identico mentre il **percorso** e' cambiato. *(Il sigillo di `_sin2_vir` li confronta gia'.)*

## I 57 siti, per funzione

| funzione | siti |
|---|---|
| `step` | **23** |
| `_passo_spinoriale` | **10** |
| `memoria_hebbiana_moto` | **8** |
| `ritmo` | **6** |
| `_bloch_ritardato` | **2** |
| `_aggiorna_lift_spinoriale` | **1** |
| `_feedback_spinoriale_archi` | **1** |
| `chiralita_core_locale` | **1** |
| `_r_nodo_mitosi` | **1** |
| `_tau_arco_causale` | **1** |
| `_tempo_luce_nodo` | **1** |
| `_coppia_interferenza` | **1** |
| `pozzo_grafo` | **1** |

### ⚠ **I numeri di riga sono quelli del blob di OGGI e SHIFTERANNO** *(par.2)*: la tabella si
**rigenera**, non si aggiorna a mano.

| riga | funzione | cache | forma |
|---|---|---|---|
| `:2360` | `_aggiorna_lift_spinoriale` | `self._nb` | FUSA |
| `:2685` | `_feedback_spinoriale_archi` | `self._spinor_lift` | sola lunghezza |
| `:2732` | `chiralita_core_locale` | `self.psi` | FUSA |
| `:3668` | `ritmo` | `self._psi_prec` | FUSA |
| `:3672` | `ritmo` | `self.psi` | sola lunghezza |
| `:3684` | `ritmo` | `_ps` | FUSA |
| `:3684` | `ritmo` | `_psp` | FUSA |
| `:3693` | `ritmo` | `_ps` | sola lunghezza |
| `:3693` | `ritmo` | `_psp` | sola lunghezza |
| `:3788` | `_passo_spinoriale` | `self.phi_s` | sola lunghezza |
| `:3807` | `_passo_spinoriale` | `self.psi` | FUSA |
| `:3858` | `_passo_spinoriale` | `self._nb_prec` | FUSA |
| `:3887` | `_passo_spinoriale` | `self.perc_chi` | sola lunghezza |
| `:3922` | `_passo_spinoriale` | `self.psi` | FUSA |
| `:3954` | `_passo_spinoriale` | `_csp_in` | sola lunghezza |
| `:4291` | `_passo_spinoriale` | `psi_snapshot` | sola lunghezza |
| `:4293` | `_passo_spinoriale` | `self.psi` | sola lunghezza |
| `:4345` | `_passo_spinoriale` | `self.perc_chi` | sola lunghezza |
| `:4352` | `_passo_spinoriale` | `_csp2` | sola lunghezza |
| `:5471` | `_bloch_ritardato` | `nbr` | FUSA |
| `:5487` | `_bloch_ritardato` | `r_loc` | FUSA |
| `:5551` | `_r_nodo_mitosi` | `r` | FUSA |
| `:5591` | `_tau_arco_causale` | `csn` | FUSA |
| `:5661` | `_tempo_luce_nodo` | `csp` | sola lunghezza |
| `:5684` | `_coppia_interferenza` | `_ps` | sola lunghezza |
| `:5748` | `step` | `getattr(self, 'psi_spin', ` | sola lunghezza |
| `:5752` | `step` | `getattr(self, 'psi_spin', ` | sola lunghezza |
| `:5794` | `step` | `self.perc_chi` | sola lunghezza |
| `:5795` | `step` | `self.psi` | sola lunghezza |
| `:5799` | `step` | `self.perc_chi` | sola lunghezza |
| `:5799` | `step` | `self.psi` | sola lunghezza |
| `:5922` | `step` | `self.perc_chi` | sola lunghezza |
| `:5929` | `step` | `self.perc_chi` | sola lunghezza |
| `:5937` | `step` | `self.perc_chi` | sola lunghezza |
| `:5972` | `step` | `self.psi` | sola lunghezza |
| `:6017` | `step` | `self.phivel` | sola lunghezza |
| `:6056` | `step` | `self.phi_s` | sola lunghezza |
| `:6060` | `step` | `self.phi_s` | sola lunghezza |
| `:6070` | `step` | `self.perc_chi` | sola lunghezza |
| `:6077` | `step` | `getattr(self, _cache_tors,` | sola lunghezza |
| `:6086` | `step` | `self._deg` | sola lunghezza |
| `:6103` | `step` | `self.perc_chi` | sola lunghezza |
| `:6129` | `step` | `self.perc_chi` | sola lunghezza |
| `:6130` | `step` | `getattr(self, '_psi_spinor` | sola lunghezza |
| `:6135` | `step` | `self.perc_chi` | sola lunghezza |
| `:6136` | `step` | `getattr(self, '_psi_spinor` | sola lunghezza |
| `:6218` | `step` | `_pv_src` | sola lunghezza |
| `:6443` | `step` | `self.psi` | sola lunghezza |
| `:7178` | `pozzo_grafo` | `self.psi` | sola lunghezza |
| `:7220` | `memoria_hebbiana_moto` | `self.psi` | sola lunghezza |
| `:7333` | `memoria_hebbiana_moto` | `self._nb` | sola lunghezza |
| `:7334` | `memoria_hebbiana_moto` | `self.phi_s` | sola lunghezza |
| `:7347` | `memoria_hebbiana_moto` | `self._nb` | sola lunghezza |
| `:7351` | `memoria_hebbiana_moto` | `self._nb` | sola lunghezza |
| `:7404` | `memoria_hebbiana_moto` | `self._nb` | sola lunghezza |
| `:7546` | `memoria_hebbiana_moto` | `_csn` | sola lunghezza |
| `:7612` | `memoria_hebbiana_moto` | `self.psi` | sola lunghezza |

