@echo off

call %CGRU_LOCATION%\software_setup\setup_houdini.cmd

rem Prefer APP_EXE from setup (houdinifx when present)
if defined APP_EXE (
    start "Houdini" "%APP_EXE%" %*
) else (
    start "Houdini" "%APP_DIR%\bin\houdini.exe" %*
)
