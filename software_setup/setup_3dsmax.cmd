rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

if not "%MAX_LOCATION%"=="" goto :max_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Autodesk\3ds Max*" 2^>nul') Do set "MAX_LOCATION=C:\Program Files\Autodesk\%%I"

set APP_DIR=%MAX_LOCATION%
set APP_EXE=3dsmax.exe

rem Define location:
set locate_file=%CGRU_LOCATION%\software_setup\locate_3dsmax.cmd
if exist %locate_file% call %locate_file%

set MAX_LOCATION=%APP_DIR%
goto :max_cgru

:max_located
echo MAX_LOCATION from environment: %MAX_LOCATION%
set APP_DIR=%MAX_LOCATION%
set APP_EXE=%MAX_LOCATION%\3dsmax.exe

:max_cgru
set "PATH=%CGRU_LOCATION%\plugins\max;%PATH%"
