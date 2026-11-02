rem Source general for all soft directives:
call %CGRU_LOCATION%\software_setup\setup__all.cmd

rem Setup CGRU common scripts if location provided
set "FUSION_CGRU_PATH=%CGRU_LOCATION%\plugins\fusion"
set "FUSION_CGRU_PREFS=%FUSION_CGRU_PATH%\cgru.prefs"
if defined FUSION_MasterPrefs (
	set "FUSION_MasterPrefs=%FUSION_CGRU_PREFS%;%FUSION_MasterPrefs%"
) else (
	set "FUSION_MasterPrefs=%FUSION_CGRU_PREFS%"
)

if not exist %FUSION_CGRU_PREFS% (
	"%CGRU_PYTHONEXE%" "%FUSION_CGRU_PATH%"\makeprefs.py
)
rem {Global={Paths={Map={["Scripts:"]="C:\\cgru\\plugins\\fusion\\;Fusion:Scripts",},},},}

if not "%FUSION_LOCATION%"=="" goto :fusion_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Blackmagic Design\Fusion *" 2^>nul') Do set "FUSION_LOCATION=C:\Program Files\Blackmagic Design\%%I"

SET "APP_DIR=%FUSION_LOCATION%"
SET "APP_EXE=%FUSION_LOCATION%\Fusion.exe"

rem Locate:
set "locate_file=%CGRU_LOCATION%\software_setup\locate_fusion.cmd"
if exist %locate_file% call %locate_file%
set "FUSION_LOCATION=%APP_DIR%"
goto :fusion_done

:fusion_located
echo FUSION_LOCATION from environment: %FUSION_LOCATION%
SET "APP_DIR=%FUSION_LOCATION%"
SET "APP_EXE=%FUSION_LOCATION%\Fusion.exe"

:fusion_done
