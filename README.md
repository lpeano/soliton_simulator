# `media` — il video della scena del pilota `PROVA 1`

> **Ramo ORFANO, SOLO media.** Il codice e i dati stanno su **`fork-su2`**: qui non c'e'
> storia condivisa, e nessun file di questo ramo entra mai in `fork-su2`.

| file | sha1 (byte grezzi) | dimensione |
|---|---|--:|
| `FOTOGRAMMA_passo000.png` | `b872374abe4f31c04914bd3c6e5a2c9c0413a060` | 1.68 MB |
| `FOTOGRAMMA_passo040.png` | `f4495f6baa7d84bc7228e2df72de3bc5dc97c249` | 1.79 MB |
| `FOTOGRAMMA_passo080.png` | `e9ce704aa28c28964f51f72466884954e74b2d42` | 1.88 MB |
| `FOTOGRAMMA_passo120.png` | `c563dd1c332d5fce13c49c3dec5521bdf959e5fc` | 1.95 MB |
| `video_scena_seme11.mp4` | `bbeee48ddac0a8b46efce33ddd062b9467c63aff` | 8.02 MB |

**PRODOTTI DA `fork-su2`:** renderer al commit **`5836e4c`+** *(con `V12`)*, run lanciato al
commit **`c8b6dd9`**, blob del simulatore **`e203f9a8`**, seme **11**, **120 passi**,
fotogrammi ogni **2** passi, `2026-09-27`.

```
python csv/_test_fork/_pilota_prova1.py --salva-stati --ogni 2     # il run (4 semi, ~48 min)
python csv/_test_fork/_video_scena.py --fps 8 --dpi 120            # il video, dai 61 fotogrammi
```

## I due pannelli

**SINISTRA — la vista di sempre:** pozzo `phi_g` in **magma**, archi `|dpozzo|` in **plasma**,
con **`vmax` FISSO al passo 2**. *(Al passo 0 `psi` non esiste e il pozzo e' **zero**: la scala
si ancora al primo fotogramma col pozzo vivo. **Senza scala fissa lo scioglimento si
ricalibrerebbe via.**)*

> ### ⚠ **GLI ARCHI SONO DISTORTI, ED E' MISURATO: il `100 %` sta in UN quadrante.**
> La vista prende i **primi 24000 archi per indice** (`ARCHI-PRIMI`), e l'indice correla con
> l'ordine di semina, quindi con la posizione. Baricentro degli archi disegnati
> **`(-4.392, -4.283)`** contro `(0, 0)` di tutti i nodi; sono il **`5.1 %`** dei `471 564`
> validi. **E' EREDITATO dalla vista del simulatore**, e **non e' correggibile offline**: il
> sottocampione avviene al **salvataggio**, e i fotogrammi contengono solo quei 24000 archi.
> **Il campione casuale e' gia' cablato per i run FUTURI.**

**DESTRA — la coerenza interna:** `cos(phi - phibar_m(t))`, riferimento **co-rotante per massa**
*(cosi' una rotazione rigida NON sembra uno scioglimento)*, scala fissa `[-1, +1]`, contorno
verde sui nodi delle tre masse **al passo 0**, e **opacita' = `PESO-MAX`** con
`alpha = 0.08 + 0.92 w^2`, disegnati per **peso crescente**.

## ⚠ Che cosa il video puo' mentire: **LA VICINANZA**

Le posizioni sono **`pos`**, che e' **il DISEGNO**. La fisica vive **sugli ARCHI** (`net.d` lungo
il grafo), e `pos` **non entra nella dinamica** (`A3-DISEGNO`). **Due nodi possono apparire
vicini sullo schermo ed essere lontani sul grafo.** La didascalia lo dice in ogni fotogramma.

**E il video e' un DIAGNOSTICO, non una misura:** non entra in nessun referto. Se mostrasse
qualcosa che i numeri non dicono, **vincono i numeri**.
