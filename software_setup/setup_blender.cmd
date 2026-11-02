rem Source general for all soft directives:
call "%CGRU_LOCATION%\software_setup\setup__all.cmd"

if not "%BLENDER_LOCATION%"=="" goto :blender_located

For /F "Tokens=*" %%I in ('dir /b "C:\Program Files\Blender Foundation\Blender *" 2^>nul') Do set "BLENDER_LOCATION=C:\Program Files\Blender Foundation\%%I"

set "APP_DIR=%BLENDER_LOCATION%"
set "APP_EXE=%BLENDER_LOCATION%\blender.exe"

rem Define location:
set "locate_file=%CGRU_LOCATION%\software_setup\locate_blender.cmd"
if exist "%locate_file%" call "%locate_file%"
set "BLENDER_LOCATION=%APP_DIR%"
goto :blender_cgru

:blender_located
echo BLENDER_LOCATION from environment: %BLENDER_LOCATION%
set "APP_DIR=%BLENDER_LOCATION%"
set "APP_EXE=%BLENDER_LOCATION%\blender.exe"

:blender_cgru
set "BLENDER_CGRU_PATH=%CGRU_LOCATION%\plugins\blender"
set "BLENDER_USER_SCRIPTS=%BLENDER_CGRU_PATH%"
