rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

rem If MAYA_LOCATION already set (Keeper version / farm job) — use it.
if not "%MAYA_LOCATION%"=="" goto :maya_located

rem Set Maya version:
set "MAYA_VERSION=2015"

rem Set Maya location:
set "MAYA_LOCATION=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"

set "APP_DIR=%MAYA_LOCATION%"
set "APP_EXE=%MAYA_LOCATION%\bin\maya.exe"

rem Define location:
set "locate_file=%CGRU_LOCATION%\software_setup\locate_maya.cmd"
if exist %locate_file% call %locate_file%

set "MAYA_LOCATION=%APP_DIR%"
goto :maya_cgru

:maya_located
echo MAYA_LOCATION from environment: %MAYA_LOCATION%
set "APP_DIR=%MAYA_LOCATION%"
set "APP_EXE=%MAYA_LOCATION%\bin\maya.exe"

:maya_cgru
rem Try to derive MAYA_VERSION from folder name (Maya2024 -> 2024)
for %%I in ("%MAYA_LOCATION%") do set "MAYA_FOLDER=%%~nxI"
set "MAYA_VERSION=%MAYA_FOLDER:Maya=%"

rem Set CGRU Maya scripts location:
set "MAYA_CGRU_LOCATION=%CGRU_LOCATION%\plugins\maya"
set "PYTHONPATH=%MAYA_CGRU_LOCATION%;%PYTHONPATH%"

set "MAYA_CGRU_MENUS_NAME=CGRU"

rem Set custom values if needed here:
IF EXIST override.cmd CALL override.cmd
IF EXIST override_maya.cmd CALL override_maya.cmd

rem path to modelling, animation, rendering ... menu items
rem if not set default MAYA_CGRU_LOCATION/mel will be used
rem "set MAYA_CGRU_MENUS_LOCATION=%MAYA_CGRU_LOCATION%\settings"
set "MAYA_SCRIPT_PATH=%MAYA_CGRU_LOCATION%\mel\AETemplates;%MAYA_SCRIPT_PATH%"
set "MAYA_PLUG_IN_PATH=%MAYA_CGRU_LOCATION%\mll\%MAYA_VERSION%;%MAYA_PLUG_IN_PATH%"
set "XBMLANGPATH=%MAYA_CGRU_LOCATION%\icons"

rem Disable the Customer Improvement Program
set "MAYA_DISABLE_CIP=1"

rem Add Afanasy scripts:
set "MAYA_SCRIPT_PATH=%MAYA_CGRU_LOCATION%\afanasy;%MAYA_SCRIPT_PATH%"
