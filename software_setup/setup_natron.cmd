rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

rem Setup CGRU common scripts if location provided
SET "NATRON_CGRU_PATH=%CGRU_LOCATION%\plugins\natron"
if defined CGRU_LOCATION (
   if defined NATRON_PLUGIN_PATH (
      SET "NATRON_PLUGIN_PATH=%NATRON_CGRU_PATH%;%NATRON_PLUGIN_PATH%"
   ) else (
      SET "NATRON_PLUGIN_PATH=%NATRON_CGRU_PATH%"
   )
)

if not "%NATRON_LOCATION%"=="" goto :natron_located

rem Find the latest Natron:
For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\INRIA\Natron*" 2^>nul') Do SET "NATRON_LOCATION=C:\Program Files\INRIA\%%I"

SET "NATRON_DIR=%NATRON_LOCATION%"
SET "APP_DIR=%NATRON_DIR%"
SET "APP_EXE=%NATRON_DIR%\bin\Natron.exe"

rem Custom locate:
SET "locate_file=%CGRU_LOCATION%\software_setup\locate_natron.cmd"
if exist %locate_file% call %locate_file%
SET "NATRON_LOCATION=%APP_DIR%"
goto :natron_done

:natron_located
echo NATRON_LOCATION from environment: %NATRON_LOCATION%
SET "NATRON_DIR=%NATRON_LOCATION%"
SET "APP_DIR=%NATRON_LOCATION%"
SET "APP_EXE=%NATRON_LOCATION%\bin\Natron.exe"

:natron_done
