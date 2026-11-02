rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

if not "%AE_LOCATION%"=="" goto :ae_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Adobe\Adobe After Effects*" 2^>nul') Do set "AE_LOCATION=C:\Program Files\Adobe\%%I\Support Files"

set APP_DIR=%AE_LOCATION%
set APP_EXE=%AE_LOCATION%\aerender.exe

rem Define location:
set locate_file=%CGRU_LOCATION%\software_setup\locate_afterfx.cmd
if exist %locate_file% call %locate_file%

set AE_LOCATION=%APP_DIR%
goto :ae_done

:ae_located
echo AE_LOCATION from environment: %AE_LOCATION%
set APP_DIR=%AE_LOCATION%
set APP_EXE=%AE_LOCATION%\AfterFX.exe
if not exist "%APP_EXE%" set APP_EXE=%AE_LOCATION%\aerender.exe

:ae_done
