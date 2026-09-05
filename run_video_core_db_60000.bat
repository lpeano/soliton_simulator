@echo off
REM Rendering FULL CORE da copia DB, in background.
REM Il video esistente core_full_s1.mp4 non viene toccato.
set SIM=C:\Users\lpeano\soliton_simulator\soliton_simulator.py
set DB=C:\Users\lpeano\soliton_simulator\out_video\db_core_s1_video_60000.pkl
set OUT=C:\Users\lpeano\soliton_simulator\out_video\core_full_s1_da_db_60000.mp4
set LOG=C:\Users\lpeano\soliton_simulator\log\video_core_db_60000.log

if not exist "%DB%" (
  echo DB non trovato: %DB%
  exit /b 1
)
if not exist "C:\Users\lpeano\soliton_simulator\log" mkdir "C:\Users\lpeano\soliton_simulator\log"
if not exist "C:\Users\lpeano\soliton_simulator\out_video" mkdir "C:\Users\lpeano\soliton_simulator\out_video"

start "core_full_da_db_60000" /MIN cmd /c "python "%SIM%" --test N-MASSE --nmasse 3 --sep 8 --seed 1 --giri 0 --ppf 1 --frames 60000 --fps 24 --verlet --sync --spinore-vivo --chi-core --sync-db "%DB%" --out "%OUT%" > "%LOG%" 2>&1"
echo Rendering avviato in background.
echo Output: %OUT%
echo Log: %LOG%
