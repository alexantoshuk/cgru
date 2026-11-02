rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

rem Setup CGRU common scripts if location provided
set NUKE_CGRU_PATH=%CGRU_LOCATION%\plugins\nuke
if defined CGRU_LOCATION (
   if defined NUKE_PATH (
      set NUKE_PATH=%NUKE_CGRU_PATH%;%NUKE_PATH%
   ) else (
      set NUKE_PATH=%NUKE_CGRU_PATH%
   )
)

rem Default number of threads for rendering:
rem SET NUKE_AF_RENDERTHREADS=2

rem Nuke render launcher:
SET NUKE_AF_RENDER=nuke

if not "%NUKE_LOCATION%"=="" goto :nuke_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Nuke*" 2^>nul') Do set "NUKE_LOCATION=C:\Program Files\%%I"

For /F "Tokens=*" %%I in ('dir /b "%NUKE_LOCATION%\Nuke*.*.exe" 2^>nul') Do set "NUKE_EXEC=%NUKE_LOCATION%\%%I"

SET NUKE_DIR=%NUKE_LOCATION%
SET APP_DIR=%NUKE_LOCATION%
SET APP_EXE=%NUKE_EXEC%

rem Locate:
set locate_file=%CGRU_LOCATION%\software_setup\locate_nuke.cmd
if exist %locate_file% call %locate_file%

SET NUKE_LOCATION=%APP_DIR%
goto :nuke_cgru

:nuke_located
echo NUKE_LOCATION from environment: %NUKE_LOCATION%
SET NUKE_DIR=%NUKE_LOCATION%
SET APP_DIR=%NUKE_LOCATION%
For /F "Tokens=*" %%I in ('dir /b "%NUKE_LOCATION%\Nuke*.*.exe" 2^>nul') Do set "APP_EXE=%NUKE_LOCATION%\%%I"
if "%APP_EXE%"=="" set "APP_EXE=%NUKE_LOCATION%\Nuke.exe"

:nuke_cgru
SET LM_LICENSE_FILE=%NUKE_LOCATION%\nuke.lic
SET LM_LICENSE_FILE=%NUKE_LOCATION%\foundry.lic
