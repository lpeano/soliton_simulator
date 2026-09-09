# [branch dev-spinoriale] RUN COVARIANTE FASE 3 (verdetto non-abeliano)
# ON vs OFF, N-appaiato, seed {1,2,3}, 10000 passi. Isola ESATTAMENTE --campo-spinoriale:
#   OFF = spinore vivo ma campo scalare U(1) (il segno NON entra nelle forze)
#   ON  = OFF + --campo-spinoriale (forze = overlap spinoriale <psi_i|psi_j>, Fase 3)
# Domanda: in ON il segno_arco_coer diventa ATTRATTORE (resta alto a N appaiato) vs OFF
# dove decade (par.48 = repulsore)? berry_firmata sale?
#
# I run sono dominati da operazioni sparse (single-thread): forziamo *_NUM_THREADS=1
# cosi' ognuno dei 6 run occupa 1 core fisico (6 core) senza strozzarsi a vicenda.
# Checkpoint DB ogni 1000 passi (ripresa) + diaglog ogni 50 passi (serie temporale per il verdetto,
# leggibile ANCHE se il run non arriva a 10000). .pkl gitignorati; CSV/log si committano a fine run.

$ErrorActionPreference = "Stop"
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"

New-Item -ItemType Directory -Force -Path db/fase3_cov, csv/fase3_cov, log/fase3_cov | Out-Null

$PASSI = 10000
$COMUNE = "--batch --nmasse 2 --sep 6 --passi $PASSI --ogni 50 --spinore-vivo --spinore-corretto --chi-core"
$seeds = 1, 2, 3

foreach ($s in $seeds) {
    foreach ($mode in "off", "on") {
        $flag = if ($mode -eq "on") { "--campo-spinoriale" } else { "" }
        $args = "soliton_simulator.py $COMUNE --seed $s $flag " +
                "--sync-db db/fase3_cov/${mode}_s$s.pkl --db-ogni 1000 " +
                "--csv csv/fase3_cov/cond_${mode}_s$s.csv " +
                "--diaglog csv/fase3_cov/diag_${mode}_s$s.csv"
        Start-Process -FilePath python -ArgumentList $args -NoNewWindow `
            -RedirectStandardOutput "log/fase3_cov/${mode}_s$s.log" `
            -RedirectStandardError  "log/fase3_cov/${mode}_s$s.err"
        Write-Host "lanciato: $mode seed $s"
    }
}
Write-Host "6 run covarianti lanciati in parallelo (ON/OFF x seed 1,2,3), $PASSI passi."
