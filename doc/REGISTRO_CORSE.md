# IL REGISTRO DELLE CORSE DELL'ERA 2

> **APPEND-ONLY. Si scrive SOLO con `csv/solitone/_registro_corse.py`** *(`apri`, `tappa`, `chiudi`)*, **mai a mano.** Il task history: `doc/TASK_HISTORY/2026-11-13_registro_corse.md`; la skill: `.claude/skills/registro-corse/SKILL.md`.
>
> - **una riga per evento, `- {json}`:** `ev` = `APERTO` *(l'ora, `HEAD`, l'impronta dei file del nucleo di `doc/NUCLEO_CONGELATO.md`, il comando verbatim)*, `TAPPA` *(il punto raggiunto)*, `CHIUSO` *(`FINITO`, `FERMATO`, `FALLITO`, il punto esatto)*;
> - **al piu' UNA `lunga` e UNA `breve` aperte insieme; mai lo stesso nome aperto due volte; `forza` solo con una decisione di Luca, scritta nella voce;**
> - **dopo un riavvio una voce rimasta APERTA si chiude `FERMATO (riavvio)` all'ultima tappa SOLO dopo che Luca l'ha vista: fino ad allora blocca le corse del suo tipo.**

## GLI EVENTI

- {"comando": "python csv/solitone/s5_g1_tre_partenze.py > /c/Users/lpeano/AppData/Local/Temp/claude/b9208eb8a2665aad/a1f276e8-bac6-4d71-a5b8-87072b85f545/scratchpad/video_triplo_referto.txt (poi copiato in doc/referti_l2/campo_g1_tre/referto.txt a corsa finita: un file non tracciato sotto doc/ bloccherebbe i commit nel frattempo)", "ev": "APERTO", "git": {"file_modificati": 0, "head": "adeca755", "ramo": "primo-ordine"}, "nome": "video-triplo", "note": "la voce 8 della coda (Luca 2026-11-13 10:20; il mandato del 2026-11-12 20:10); il codice a bea419ba; HEAD adeca755; 3 x 4000 tick", "nucleo": {"diversi": [], "file": 12, "sha1_byte": {"primo_ordine/_collauda_motore.py": "4d60d2f2", "primo_ordine/_collauda_r60.py": "1ee3f0eb", "primo_ordine/_mappa.yaml": "f3bb3fdc", "primo_ordine/_misura_hw.py": "98c1d34b", "primo_ordine/_misura_mb2.py": "48269077", "primo_ordine/energia_pesata.py": "43bce8ad", "primo_ordine/flussi_parziali.py": "d43b1cf8", "primo_ordine/leggi/leggi.yaml": "1c0eac29", "primo_ordine/termini/camm_grover.py": "10b70489", "primo_ordine/termini/camm_grover_vuoto.py": "8f88bc20", "primo_ordine/termini/camm_spostamento.py": "d58a753f", "primo_ordine/termini/camm_spostamento_vuoto.py": "a58a55ea"}, "uguali_alla_tabella": true}, "ora": "2026-11-13T12:34:06+01:00", "tipo": "breve"}
- {"esito": "FINITO", "ev": "CHIUSO", "nome": "video-triplo", "ora": "2026-11-13T12:50:10+01:00", "punto": "4000 tick per (A), (B), (C); uscita 0 alle 12:49:42; 8/8"}
