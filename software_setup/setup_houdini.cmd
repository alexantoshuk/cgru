rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

rem If HOUDINI_LOCATION is already set (e.g. from Afanasy job Environment),
rem use it as-is. Otherwise auto-detect / Keeper locate for interactive launch.
rem (goto used instead of IF() blocks so %vars% expand correctly in cmd.exe)
if "%HOUDINI_LOCATION%"=="" goto :houdini_locate

echo HOUDINI_LOCATION from environment: %HOUDINI_LOCATION%
set "APP_DIR=%HOUDINI_LOCATION%"
set "APP_EXE=%HOUDINI_LOCATION%\bin\houdini.exe"
goto :houdini_cgru

:houdini_locate
For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Side Effects Software\Houdini 1*" 2^>nul') Do set "HOUDINI_LOCATION=C:\Program Files\Side Effects Software\%%I"
set "APP_DIR=%HOUDINI_LOCATION%"
set "APP_EXE=%HOUDINI_LOCATION%\bin\houdini.exe"

rem Keeper "Setup Soft" override (default version for this machine):
set "locate_file=%CGRU_LOCATION%\software_setup\locate_houdini.cmd"
if exist "%locate_file%" call "%locate_file%"
set "HOUDINI_LOCATION=%APP_DIR%"

:houdini_cgru
set HOUDINI_CGRU_PATH=%CGRU_LOCATION%\plugins\houdini

IF DEFINED HOUDINI_PATH (
    set "HOUDINI_PATH=%HOUDINI_CGRU_PATH%;%HOUDINI_PATH%;&"
) ELSE (
    set "HOUDINI_PATH=%HOUDINI_CGRU_PATH%;&"
)

set PYTHONPATH=%HOUDINI_CGRU_PATH%;%PYTHONPATH%
