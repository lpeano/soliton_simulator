# `media` — il video della scena del pilota `PROVA 1`

> **Ramo ORFANO, SOLO media.** Il codice e i dati stanno su **`fork-su2`**: qui non c'e'
> storia condivisa, e nessun file di questo ramo entra mai in `fork-su2`.

| file | sha1 (byte grezzi) | dimensione |
|---|---|--:|
| `FOTOGRAMMA_passo000.png` | `a9959ed48811fff214bfc388590ce762cdda1c55` | 1.82 MB |
| `FOTOGRAMMA_passo040.png` | `066b5daccf0673028f5e751c11ed1ea02aacdb81` | 1.94 MB |
| `FOTOGRAMMA_passo080.png` | `2e203d0d3fb9fa6a2f7c2489b9724f3f3cfd4734` | 2.06 MB |
| `FOTOGRAMMA_passo120.png` | `677dd3ec5348f094580c6d9c08f3d921d4e7f9e0` | 2.16 MB |
| `video_scena_seme11.mp4` | `bcfb95cb2cce4a6e50c12e5ecc592a5c128128a6` | 8.56 MB |

**PRODOTTI DA `fork-su2`:** renderer al commit **`939cf78`**, run lanciato al commit
**`c8b6dd9`**, blob del simulatore **`e203f9a8`** *(sha1 dei byte grezzi)*, seme **11**,
**120 passi**, fotogrammi ogni **2** passi, `2026-09-27`.

**COME SI RIGENERANO** *(da `fork-su2`)*:

```
python csv/_test_fork/_pilota_prova1.py --salva-stati --ogni 2     # il run (4 semi, ~48 min)
python csv/_test_fork/_video_scena.py --fps 8 --dpi 120            # il video, dai 61 fotogrammi
```

> ### ⚠ **CHE COSA IL VIDEO PUO' MENTIRE: LA VICINANZA.**
> Le posizioni sono **`pos`**, che e' **il DISEGNO**. La fisica vive **sugli ARCHI** (`net.d`
> lungo il grafo), e `pos` **non entra nella dinamica** (`A3-DISEGNO`). **Due nodi possono
> apparire vicini sullo schermo ed essere lontani sul grafo.** La didascalia lo dice in ogni
> fotogramma.

**I due pannelli:** a sinistra **la vista di sempre** *(pozzo `phi_g` in magma, archi
`|dpozzo|` in plasma)* col **`vmax` FISSO al passo 2** — al passo 0 `psi` non esiste e il pozzo
e' **zero**, quindi la scala si ancora al primo fotogramma col pozzo vivo, e **senza quella
scala fissa lo scioglimento si ricalibrerebbe via**. A destra **la coerenza interna**,
`cos(phi - phibar_m(t))` col riferimento **co-rotante per massa**, scala fissa `[-1, +1]`,
contorno verde sui nodi delle tre masse **al passo 0**.

**E il video e' un DIAGNOSTICO, non una misura:** non entra in nessun referto. Se mostrasse
qualcosa che i numeri non dicono, **vincono i numeri**.
