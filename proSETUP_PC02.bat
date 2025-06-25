@echo off
echo Starting paradigm setup...

echo Launching e-prime (NIR stimulus)...
start "" "C:\Users\biochemlab\Documents\E-Prime\_NR-in-aging\.storage\NIRS_Nback (short)__NR-in-aging.es3"
timeout /t 2 /nobreak > nul

echo Launching MATLAB (EEG stimulus)...
start "" "C:\Users\biochemlab\Documents\MATLAB\EEG_nback\MAIN_nback_short.m"
timeout /t 2 /nobreak > nul

echo Launching EmotivPro (EEG recorder)...
start "" "C:\EMOTIV\EmotivApps\EmotivPRO.exe"
timeout /t 3 /nobreak > nul

echo Launching explanation video...
timeout /t 2 /nobreak > nul
start "" "C:\Users\biochemlab\Desktop\N-back instructions video.mov"