# 2026-11-01 — IL CONTROLLO DI `matrice` SUI REFERTI GIA' FATTI *(UNA PROVA E UNA CORREZIONE DI STRUMENTO IN `csv/`, NESSUNA MODIFICA AL NUCLEO, NESSUNA CORSA LUNGA; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `21:03`)*

> **Lo script:** `csv/_controllo_matrice.py`. **Il referto:** `doc/referti_l2/controllo_matrice.txt`. **La guardia:** in `csv/_dove_va_la_materia.py` *(`matrice`)*, un commit a se'.

## 1. LE PREMESSE DAL CODICE

- **Il fatto** *(`baf1e5b3`, `doc/FATTI_dal_codice.md`)*: `_dove_va_la_materia.matrice(z, phi0, amp)` chiama `12` volte `un_tick(z, phi0, p)`, che **scrive** `z["st"]["psi_h"]` *(il vettore di prova)* e `z["st"]["phi_h"]` *(rimesso a `phi0`)* e poi fa un tick congelato *(`DC.tick_congelato`)*. Misurato allora: `psi_h` cambia di `2.5`, `rho` di `5060`, `Lambda` di `1.8e-15`; `phi_h`, `psi`, `h_int` no. **`autovettori(A)` non tocca `z`** *(legge solo `A`)*.
- **Un censimento AST fatto nello scratchpad** *(prima di questo file, per scrivere le premesse; **lo script lo rifa' e lo committa**)*: le funzioni di `csv/` che chiamano `DV.matrice` **o una funzione che la chiama** *(transitivamente, risolvendo gli alias degli import)*: **`39` chiamate dirette in `21` file**, piu' le `3` dentro `_dove_va_la_materia` *(`referto`: `2` a `matrice` e `1` a `un_tick`)*.
- **`un_tick` ha lo stesso effetto, ed e' la sua causa:** lo includo nel censimento *(un'estensione dichiarata: il mandato dice «o una funzione che la chiama», e `un_tick` e' chiamata da `matrice`, non la chiama)*.
- **Le costruzioni dei proiettori** *(nominate nel mandato)*: passano da `autovettori(matrice(...))`, quindi le prende il censimento per transitivita'.

### Cosa NON so

- **Quali dei `39` siti leggono lo stato DOPO la chiamata, nella stessa scena.** L'AST trova le chiamate; **la lettura la classifico A MANO**, sito per sito, con le righe.
- **Se `Lambda` e' una chiave di `z["st"]` o una grandezza derivata.** Lo script confronta **tutte le chiavi** di `z["st"]` prima e dopo, e stampa quelle che cambiano.
- **Altre `7` funzioni `matrice` diverse** stanno in `csv/` *(`_larghezza_risonanza`, `_massa_vicino_al_cono`, `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_u1_prototipo`, `_vuoto_sul_fondo`)*: **non sono `DV.matrice`**, e il mandato non le chiede. ### **Le elenco e non le controllo:** se vadano controllate e' una domanda per Luca.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `1` | **L'elenco** *(`--elenco`)*: il censimento AST *(transitivo)*; per ogni sito **le righe DOPO la chiamata**, nella stessa funzione e nei chiamanti dopo il ritorno, che leggono lo stato *(`z["st"]`, `.st[`, `DC.forma`, `CL.punto`, `SL.anelli`, `EL.densita`, e le misure dei moduli che li chiamano)*. **La classe di ogni sito la do io, a mano, con il perche'** *(nel referto e qui)*: **PULITO** *(nessuna lettura dopo; oppure lo stato e' ricaricato **interamente** prima di leggerlo)*; **SOSPETTO** *(una lettura dopo, senza ricarica)*. |
| `2` | **Per ogni SOSPETTO:** il referto e il commit che ne dipendono, i numeri toccati; **la misura rifatta nell'ordine giusto** *(lo stato misurato PRIMA di `matrice`, o in una scena sua)* e **confrontata coi numeri committati**, con le cifre stampate. Se coincidono, lo dico; **se no, la correzione del referto in un commit a se'**, e quali letture cambiano. |
| `3` | **La guardia in `matrice`:** salva **ogni array di `z["st"]`** prima, lo rimette dopo. **DEVE:** dopo la chiamata **ogni chiave di `z["st"]` identica AL BIT** a prima; **`A` identica al bit a quella senza guardia** *(la guardia non cambia cio' che `matrice` restituisce)*. **Il caso che DEVE fallire:** la `matrice` di prima *(il blob del PADRE, `git cat-file`, in binario)* **lascia lo stato diverso**. |

**La conseguenza della guardia, dichiarata prima:** le corse che hanno evoluto lo stato lasciato da `matrice` *(`_coppia_di_B.lunga`, `_consolida_B.corsa`, `_salti_nel_cuore.rigenera`: ricaricano `psi_h`, ma `Lambda` resta quello di `matrice`)* **non si rigirano piu' al bit sul blob di oggi**: si rigirano **al loro commit**, come vuole la regola dei sigilli. ### **Non e' un difetto nuovo; lo scrivo nell'inventario.**

## 3. LE LETTURE *(di Luca, scritte prima)*

- **(m1)** nessun referto toccato: l'effetto collaterale ha colpito solo le misure della partenza gia' corrette *(`baf1e5b3`)*;
- **(m2)** referti toccati: quali, quali numeri, quali letture cambiano.

## 4. LE MOTIVAZIONI

**Un difetto di strumento trovato in un posto va cercato in tutti i posti dove lo strumento si usa.** E una guardia nello strumento **impedisce** che si ripeta, invece di affidarlo alla memoria di chi scrive lo script dopo.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_controllo_matrice.py --elenco` *(e la riga nell'inventario)*, committato prima di girare; poi l'elenco nel referto, committato, e la classe di ogni sito qui *(sezione `6`)*.
3. Per ogni SOSPETTO: `--rifai <nome>`, committato prima; il confronto; se cambia, la correzione del referto **in un commit a se'**.
4. La guardia in `matrice` e `--guardia` *(il DEVE e il caso che deve fallire)*: **un commit a se'**; poi il referto.
5. `doc/FATTI_dal_codice.md` *(l'esito)*, `RELAZIONE`, `MAPPA`, l'inventario *(le corse che si rigirano al loro commit)*.
