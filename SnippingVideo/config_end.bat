@echo off
set /a time=8
for /f "tokens=*" %%a in ('bin\ffprobe -show_format -i %1 ^| find "duration"') do set _duration=%%a
set _duration=%_duration:~9%
for /f "delims=. tokens=1*" %%b in ('echo %_duration%') do set /a "_durS=%%b"
for /f "delims=. tokens=2*" %%c in ('echo %_duration%') do set "_durMS=%%c"
rem following line is seconds to cut
set /a "_durS-=%time%"
set "_newduration=%_durS%.%_durMS%"
set "_output=%~n1"
md output
bin\ffmpeg -ss 0 -i %1 -t %_newduration% -c copy "C:\Users\dmt\Desktop\TEST\%_output%.mp4"