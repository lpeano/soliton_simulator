# Relazione sessione — 2026-09-04

## Modifiche realizzate

- Centralizzato il pozzo fisico locale in `Rete.pozzo_grafo()`:
  \[
  \Phi_i = \sum_{j\in N(i)} I_j/d_{ij}
  \]
  La dinamica gravitazionale e la visualizzazione usano la stessa grandezza `phi_g`.
- Separata la vista topologica dal rendering XYZ: il layout del grafo è astratto e non interpreta le coordinate come nodi fisici.
- La vista campo interpola `phi_g` già calcolato dalla fisica, senza ricalcolare un potenziale continuo indipendente.
- Reso `--sync` coerente con un’unica snapshot del passo precedente per fase, campo, intensità, metrica e settore spinoriale; la mitosi richiede il ricalcolo solo quando cambia la topologia.
- Aggiunta la riga `# RUN_PARAMS {...}` all’inizio dei CSV batch e dei `diaglog`, con parametri CLI, leggi attive e costanti effettive. La gestione dei resume evita duplicazioni.
- Aggiornati gli script delle campagne core, spin/chiralità e matrice CS per includere `--cs-dinamico`. Il test dedicato `test_cs_dinamico.bat` conserva il braccio OFF per l’A/B.
- I batch lunghi attivi sono stati fermati prima della modifica degli script; non sono stati rilanciati in questa sessione.

## Verifiche svolte

- `python -m py_compile soliton_simulator.py`: superato.
- `git diff --check`: superato.
- Batch minimo con `--sync --cs-dinamico`: CSV e `diaglog` verificati con metadata, header e dati nell’ordine corretto.
- Video di verifica della snapshot sync completo generato senza errori.

## Stato scientifico

I risultati delle campagne precedenti non sono conclusivi per la nuova configurazione: erano stati eseguiti prima dell’ultima correzione snapshot e prima dell’uniformazione di `--cs-dinamico`. I segnali di spin e `Lz` osservati restano quindi **in verifica**, non dimostrano ancora una precessione orbitale o un frame dragging collettivo.

## TODO — prossima sessione

1. Rilanciare le campagne aggiornate con `--cs-dinamico` e DB/output nuovi, senza riutilizzare cache di configurazioni precedenti.
2. Attendere il completamento dei run da 2000 passi su 2–3 semi.
3. Confrontare nei CSV/`diaglog` `cs_eff_*`, `dmin_nodi`, torsione, coerenza, `m*_spin`, `m*_Lz` e `Lz_orb_*`.
4. Verificare se i nodi quasi coincidenti (`dmin_nodi` molto piccolo) persistono e se alterano `phi_g`.
5. Valutare la precessione solo da serie temporali e osservabili relazionali, non da un singolo frame o dalla rotazione della camera.
6. Controllare che la riga `# RUN_PARAMS` renda ogni CSV autonomamente interpretabile.
