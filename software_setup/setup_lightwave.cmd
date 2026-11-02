rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

if not "%LIGHTWAVE_LOCATION%"=="" goto :lw_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\NewTek\LightWave_*" 2^>nul') Do set "LIGHTWAVE_LOCATION=C:\Program Files\Newtek\%%I"

rem Define location:
set "locate_file=%CGRU_LOCATION%\software_setup\locate_lightwave.cmd"
if exist %locate_file% call %locate_file%

set APP_DIR=%LIGHTWAVE_LOCATION%
set APP_EXE=%LIGHTWAVE_LOCATION%\bin\layout.exe
if not "%APP_DIR%"=="" set "LIGHTWAVE_LOCATION=%APP_DIR%"
goto :lw_done

:lw_located
echo LIGHTWAVE_LOCATION from environment: %LIGHTWAVE_LOCATION%
set APP_DIR=%LIGHTWAVE_LOCATION%
set APP_EXE=%LIGHTWAVE_LOCATION%\bin\layout.exe

:lw_done
