# CON QUALE `argv` GIRAVA OGNI MISURA — **generato**, non ricopiato

*(`csv/_config_delle_misure.py`. Mandato di Luca, 2026-09-25, punto 1. Sola lettura:
il verdetto si legge **per AST** dal sorgente dello strumento, non da un `grep` e non da
un ricordo. **La popolazione sono i sei strumenti nominati da Luca piu' ogni `.py` di
`csv/_test_fork/` e `csv/_seal_fork/` committato oggi**, cosi' quello che avrei
dimenticato entra da se'.)*

> ### PERCHE' QUESTA TABELLA ESISTE
> Il `FAIL` di `A2` (`RAMPA-1`) ha dimostrato che **la configurazione cambia il
> verdetto**: lo stesso criterio da' `PASS` sui **default di modulo** (`CS_DINAMICO =
> False`, `cs` costante) e `FAIL` sull'**argv del driver** (`cs` vivo, `cs_std/cs = 19 %`).
> **Una misura fuori dalla configurazione del driver non e' sbagliata: e' la misura di un
> ALTRO SISTEMA**, e va marcata cosi'.

| misura | strumento | **configurazione** | flag impostati A MANO | priorita' |
|---|---|---|---|---|
| SCALE-TW pieno | `_scale_tw2.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| chi comprime d0 | `_chi_comprime_d0.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA`, `TRACCIA_D0` | **DA RIFARE** |
| figli della mitosi | `_figli_della_mitosi.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| limite di accoppiamento | `_limite_accoppiamento.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` | **DA RIFARE** |
| A13 relazionale | `_a13_relazionale.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| omega estremo | `_dove_sta_omega.py` | DEFAULT DEL SORGENTE + flag a mano | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| *(committato oggi)* | `_passo_zero_scena_ii.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_sigillo_cura4_accensione.py` | DRIVER (argv catturata via `_cli_flag`) | — |  |
| *(committato oggi)* | `_sigillo_cura5_a13nascita.py` | DEFAULT DEL SORGENTE + flag a mano | `MITOSI_2LAM`, `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| *(committato oggi)* | `_sigillo_driver_accende.py` | DRIVER (argv catturata) + lancio del driver | `SEMINA_LAM` |  |
| *(committato oggi)* | `_sigillo_u2_contatori.py` | DEFAULT DEL SORGENTE (nessun flag toccato) *(1 sorgenti-figlio non parsabili)* | — |  |
| *(committato oggi)* | `_chi_parte_invecchiato.py` | DEFAULT DEL SORGENTE (nessun flag toccato) | — |  |
| *(committato oggi)* | `_diag_triangoli.py` | MISTO: driver per il run, flag a mano in-process | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| *(committato oggi)* | `_fumo_scena_ii.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_lettura_tau_a.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_lettura_torsione_spinore.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_sim_diag.py` | DEFAULT DEL SORGENTE (nessun flag toccato) | — |  |
| *(committato oggi)* | `_perche_ramp_cala.py` | DRIVER (argv catturata via `_cli_flag`) | — |  |
| *(committato oggi)* | `_rimisura_dxd.py` | MISTO: driver per il run, flag a mano in-process | `SCALA_MIN`, `SCALA_MIN_PASSO`, `SEMINA_LAM`, `SEMINA_MATURA` |  |
| *(committato oggi)* | `_scale_tw.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_scena_video.py` | DRIVER (lanciato per subprocess) | — |  |
| *(committato oggi)* | `_scene_coerenti.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM` |  |
| *(committato oggi)* | `_verifica_flag_accesi.py` | DEFAULT DEL SORGENTE + flag a mano | `SEMINA_LAM`, `SEMINA_MATURA` |  |

## IL CONTO

```
DEFAULT DEL SORGENTE (nessun flag toccato)     3
DEFAULT DEL SORGENTE + flag a mano             14
DRIVER (argv catturata via `_cli_flag`)        2
DRIVER (argv catturata) + lancio del driver    1
DRIVER (lanciato per subprocess)               1
MISTO: driver per il run, flag a mano in-process 2
TOTALE                                         23
```

## LA DISTANZA DALLA CONFIGURAZIONE DEL DRIVER — **quali leggi MANCAVANO**

*«Default del sorgente + quattro flag» non dice QUANTO manca. Qui il conto e'
MISURATO: si carica il simulatore **due volte** — una sui default, una con l'argv del
driver — e si confrontano **tutti** i booleani di modulo. Poi, per ogni strumento, si
rimettono i flag che imposta a mano e **si elenca cio' che resta**.*

```
booleani di modulo confrontati            78
DIVERSI fra default e argv del driver     31
```

**I 31 flag che il driver ACCENDE e i default NO:**

`ANOM_SIMM` · `CALORE_VETTORIALE` · `CAMPO_SPINORIALE` · `CHI_BASC` · `CHI_COOP` · `CHI_CORE` · `COES_ADIM` · `COES_CAUSALE` · `CS_DINAMICO` · `DEPARAM_OROLOGIO` · `FORK_SU2` · `FORK_SU2_MEM` · `GUSCIO_MORBIDO` · `MITOSI_2LAM` · `OLON_PART` · `PAV_COM` · `PEQ_ESATTO` · `PEQ_NASCITA_LOCALE` · `PLAST_DIN` · `RITMO_WRAP_2PI` · `RUMORE_COLORATO` · `SCALA_MIN_PASSO` · `SEMINA_LAM` · `SEMINA_MATURA` · `SPINORE_CORRETTO` · `STEP2_OROLOGIO` · `TAU_LUCE` · `TEMPO_UNICO_MITOSI` · `VERLET` · `VIRIALE` · `ZETA_VIR`

| misura | flag rimessi a mano | **leggi che RESTAVANO SPENTE** | quante |
|---|---|---|---|
| SCALE-TW pieno | 4 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |
| chi comprime d0 | 5 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |
| figli della mitosi | 4 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |
| limite di accoppiamento | 4 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |
| A13 relazionale | 4 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |
| omega estremo | 4 | `ANOM_SIMM`, `CALORE_VETTORIALE`, `CAMPO_SPINORIALE`, `CHI_BASC`, `CHI_COOP`, `CHI_CORE`, `COES_ADIM`, `COES_CAUSALE`, `CS_DINAMICO`, `DEPARAM_OROLOGIO`, `FORK_SU2`, `FORK_SU2_MEM`, `GUSCIO_MORBIDO`, `MITOSI_2LAM`, `OLON_PART`, `PAV_COM`, `PEQ_ESATTO`, `PEQ_NASCITA_LOCALE`, `PLAST_DIN`, `RITMO_WRAP_2PI`, `RUMORE_COLORATO`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `TAU_LUCE`, `TEMPO_UNICO_MITOSI`, `VERLET`, `VIRIALE`, `ZETA_VIR` | **28 su 31** |

> ### ⚠ **NESSUNA DELLE SEI GIRAVA IN CONFIGURAZIONE DEL DRIVER**, e la voce che pesa
> ### piu' di tutte e' **`CS_DINAMICO`**: e' **il flag che ha fatto cadere `A2`**.
>
> Con `CS_DINAMICO` spento `cs = CS_M` **costante**, quindi `tau = d/cs` e' `tau ∝ d`
> travestito (par.4 di `CLAUDE.md`), il tempo-luce non si muove e **ogni grandezza che
> lo divide sembra ferma**. E' esattamente il meccanismo del `FAIL` di `A2`.
## COSA QUESTA TABELLA **NON** DICE

- **non dice che una misura sia sbagliata.** Dice **in quale sistema** e' stata presa.
- **non e' un presidio** (`A9`): non impedisce a nessuno di scrivere domani un altro
  strumento che imposta i flag a mano. Il presidio corrispondente e' `P2 FLAG VIVI`
  del mandato sui presidi automatici, **ancora da cablare**.
- **le assegnazioni dentro i sorgenti-figlio** (i sigilli scrivono il figlio come TESTO)
  si leggono parsando quelle stringhe: quando una stringa non si lascia parsare **il
  numero e' dichiarato nella riga**, invece di essere contata come «nessuna assegnazione».
