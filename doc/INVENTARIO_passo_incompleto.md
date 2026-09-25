# INVENTARIO — **chi avanza con `net.step()` senza le altre chiamate del passo**

> **Generato da `csv/_inventario_passo.py`. Non ricopiato.**
> **L'ordine del passo è letto da `csv/_passo.py`**, che lo legge per AST da `update()` e lo
> verifica contro il driver.

```
passo = scuoti_vuoto() -> step() -> mitosi() -> rilassa_disegno() -> memoria_hebbiana_moto()   (letto per AST da `update()` e verificato contro il driver)
```

**Trovati `103` file sotto `csv/` che CHIAMANO `step()`** *(per AST, non per testo)*.

**⚠ DUE CORREZIONI AL PRIMO CONTEGGIO, ed erano difetti miei:**
1. **i nomi erano cercati NEL TESTO** *(`(nome + "(") in src`)*: **un file che MENZIONA
   `mitosi` in un commento veniva contato come se la CHIAMASSE.** È `STANDARD 9` al
   contrario, e **non era teorico**: ogni referto che spiega «la mitosi resta morta»
   contiene `mitosi(`, e quei file risultavano «completi». **Ora è AST.**
2. **i figli GENERATI erano contati:** `csv/**/_tmp/_br_*.py` sono scritti dai sigilli a ogni
   corsa. **Contarli gonfia il conto senza aggiungere un file da curare** — si cura il
   GENITORE. **Saltati `22`**, e il numero è detto invece di essere nascosto.

**⚠ `1` file NON si sono potuti analizzare** *(sintassi non valida per l'AST di questa
   versione di Python)*: ``csv/_test_53a/_analisi_pilota.py``. **Non contano né come completi né come incompleti, e va
   detto.**
**Di questi, `24` NON hanno tutte le altre chiamate e NON usano il modulo condiviso.**

## IL CRITERIO DI CLASSIFICAZIONE, dichiarato — e il suo LIMITE

`STRUTTURALE` = contiene segni di identità di byte *(`tobytes`, `sha1`, `firma_byte`,
`array_equal`, …)* e non di statistica. **Un'identità di byte fra due bracci che avanzano ALLO
STESSO MODO non dipende dal ciclo:** se il ciclo è sbagliato, è sbagliato in entrambi.

`MISURA` = contiene percentili, medie, correlazioni, pendenze.

> **⚠ È UN'EURISTICA SUI NOMI PRESENTI NEL FILE, NON UNA DIMOSTRAZIONE.** Un file marcato
> `STRUTTURALE` potrebbe contenere una misura. **Non è un inventario certificato: è la prima
> tabella generata**, e va letta come tale — la stessa onestà che par.9 impone al conteggio
> dei blob nelle voci *(«non è un presidio: è una MISURA»)*.

## LA TABELLA — i file che avanzano in modo INCOMPLETO

| file | `.step()` | manca | classe | chi lo cita |
|---|--:|---|---|---|
| `csv/_seal_53rel/_test_segno_olonomia.py` | 4 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **ENTRAMBI** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fase1/_sigillo_fase1.py` | 1 | `memoria_hebbiana_moto` | **ENTRAMBI** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_test_fork/_lettura_torsione_spinore.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **ENTRAMBI** | `RELAZIONE_PER_CLAUDE.md`, `doc/INVENTARIO_passo_incompleto.md`, `doc/LETTURA_accensione_e_torsione.md` |
| `csv/_seal_53rel/_candidato_Bpp.py` | 3 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_check_5_3b_magnitudine.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_ritest_depurato.py` | 4 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_test_materialita.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_test_materialita_peq.py` | 3 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_test_materialita_stab.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_test_s3b.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fase2/_sigillo_fase2.py` | 1 | `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_test_fork/_scale_tw.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md`, `doc/SCALE_TW_lettura.md` |
| `csv/_test_fork/_verifiche_inerzia.py` | 1 | `scuoti_vuoto`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/ASSIOMI.md`, `doc/INVENTARIO_passo_incompleto.md`, `doc/INVENTARIO_strumenti.md` |
| `csv/_test_fork/_verifiche_ramp.py` | 1 | `scuoti_vuoto`, `rilassa_disegno`, `memoria_hebbiana_moto` | **MISURA** | `doc/INVENTARIO_passo_incompleto.md`, `doc/INVENTARIO_strumenti.md` |
| `csv/_seal_53rel/_check_sk_limite.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_53rel/_verifica_cecita_antimateria.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fase3/_sigillo_fase3.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fase4/_diag_gate.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fork/_sig_traccia_peq/_prova_stop.py` | 1 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_test_fork/_diagnosi_peq_nascita.py` | 1 | `scuoti_vuoto`, `rilassa_disegno`, `memoria_hebbiana_moto` | **NON CLASSIFICATO** | `doc/INVENTARIO_passo_incompleto.md`, `doc/INVENTARIO_strumenti.md` |
| `csv/_seal_fase4/_sigillo_fase4.py` | 3 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **STRUTTURALE** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fase5/_sigillo_fase5.py` | 2 | `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto` | **STRUTTURALE** | `doc/INVENTARIO_passo_incompleto.md` |
| `csv/_seal_fork/_sigillo_contatori_guardie.py` | 1 | `scuoti_vuoto`, `rilassa_disegno`, `memoria_hebbiana_moto` | **STRUTTURALE** | `RELAZIONE_PER_CLAUDE.md`, `doc/INVENTARIO_passo_incompleto.md`, `doc/INVENTARIO_strumenti.md` |
| `csv/_seal_fork/_sigillo_passo1_dieci.py` | 4 | `mitosi`, `rilassa_disegno` | **STRUTTURALE** | `RELAZIONE_PER_CLAUDE.md`, `doc/INVENTARIO_passo_incompleto.md`, `doc/INVENTARIO_strumenti.md`, `doc/RAMIFICAZIONI.md` |

## E I FILE CHE VANNO BENE, o che usano il modulo condiviso

| file | `.step()` | come avanza |
|---|--:|---|
| `csv/_seal_53a/_sigillo_53a.py` | 2 | ha tutte le chiamate |
| `csv/_seal_53c/_old_sim.py` | 5 | ha tutte le chiamate |
| `csv/_seal_53c/_verifica_carica.py` | 2 | ha tutte le chiamate |
| `csv/_seal_53rel/_test_phicrit4pi.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_runner_sim.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | 5 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_Y5_riscritto.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_Z1c.py` | 3 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_anello.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_anom_simm.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_chicoop.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_coes_causale.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_coorti.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_correzioni.py` | 4 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_denominatore.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_fix_cache.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_invarianti.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_mem_moto.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_mem_moto_tutto.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_peq_esatto.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_peq_nascita.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_psi_spin_prec.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_ramo_D.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_rumore_colorato.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_spegni_grav.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_tau_luce.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_traccia_d0.py` | 1 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_traccia_peq.py` | 2 | ha tutte le chiamate |
| `csv/_seal_fork/_sigillo_twist_nodo.py` | 2 | ha tutte le chiamate |
| `csv/_seal_k2/_old_sim.py` | 5 | ha tutte le chiamate |
| `csv/_test_fork/_Z33_due_vie.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_Z36_cucitura.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_anello_sfasato.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_arco_innesco.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_canali_disordine.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_chi_non_ruota.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_conta_psi_spin_prec.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_controllo_semi.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_crescita_omega.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_dove_spinge_la_gravita.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_estensivita_grado.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_freq_riferimento.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_gauge_degenere.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_gauge_vuoto.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_maturazione.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_mediana_ritmo.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_misura_Z24.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_misura_denominatore.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_parentela_bloch.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_peq_dentro_1126.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_pilota_sep.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_retroazione_r.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_rigiocata_0_120.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_rigiocata_1200_1230.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_rimisura_Z9.py` | 3 | ha tutte le chiamate |
| `csv/_test_fork/_rimisura_t3.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_scelta_denominatore.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_scena_video.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_scena_video_ripresa.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_somma_per_scrittore_d0.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_sonda_2706.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_sonda_eta_ramp.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_sonda_fallback_psispin.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_sonda_rho_zero.py` | 2 | ha tutte le chiamate |
| `csv/_test_fork/_tassi_coppie.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_tracing_omega.py` | 1 | ha tutte le chiamate |
| `csv/_test_fork/_video_val600.py` | 1 | ha tutte le chiamate |

## ❗ E DUE SITI **NEL SIMULATORE STESSO**

| riga | sequenza spezzata? | altri nomi vicini | testo |
|--:|---|---|---|
| `6846` | **sì** *(è il passo completo, interrotto dalle assegnazioni)* | `memoria_hebbiana_moto`, `mitosi`, `rilassa_disegno`, `scuoti_vuoto` | `t0 = _t.time(); net.step();                  acc["step"]    += _t.time() - t0` |
| `8404` | **NO — È UN AVANZAMENTO INCOMPLETO** | `rilassa_disegno` | `for _ in range(300): net.step()` |

> ### ❗ **`:8404` È UN DIFETTO VERO, E STA NEL SIMULATORE:**
> `for _ in range(300): net.step()` nel percorso di ricostruzione con `--seed`/`--nodi`.
> **Trecento passi senza mitosi, senza scuotimento e senza memoria del moto**, per
> «invecchiare» la rete. **È lo stesso difetto delle sonde, dentro il codice che le sonde
> imitano.** → va in coda.

## RIEPILOGO PER CLASSE

| classe | quanti |
|---|--:|
| **ENTRAMBI** | 3 |
| **MISURA** | 11 |
| **NON CLASSIFICATO** | 6 |
| **STRUTTURALE** | 4 |

**I `MISURA` e gli `ENTRAMBI` sono quelli le cui conclusioni possono dipendere dal ciclo.**
La colonna «chi lo cita» dice **dove cercare quelle conclusioni**; il legame è una ricerca
per NOME, non una lettura del merito — e va detto.
