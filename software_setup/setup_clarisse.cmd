@echo off

rem Source general for all soft directives:
call "%CGRU_LOCATION%\software_setup\setup__all.cmd"

if not "%CLARISSE_LOCATION%"=="" goto :clarisse_located

rem Search for Clarisse installation:
set "ISOTROPIX=%SystemDrive%\Program Files\Isotropix"
For /F "Tokens=*" %%I in ('dir /b "%ISOTROPIX%\Clarisse*" 2^>nul') Do set "CLARISSE_LOCATION=%%I"
set "CLARISSE_LOCATION=%ISOTROPIX%\%CLARISSE_LOCATION%\Clarisse"

rem For export:
set "APP_DIR=%CLARISSE_LOCATION%"
set "APP_EXE=%APP_DIR%\clarisse.exe"

rem Customize location:
set "locate_file=%CGRU_LOCATION%\software_setup\locate_clarisse.cmd"
if exist "%locate_file%" call "%locate_file%"
set "CLARISSE_LOCATION=%APP_DIR%"
goto :clarisse_done

:clarisse_located
echo CLARISSE_LOCATION from environment: %CLARISSE_LOCATION%
set "APP_DIR=%CLARISSE_LOCATION%"
set "APP_EXE=%APP_DIR%\clarisse.exe"

:clarisse_done
echo CLARISSE="%APP_DIR%"
