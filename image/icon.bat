@ECHO OFF
REM ---------------------------------
REM Script by Paullux Waffle
REM ©1996-2023 Paullux Waffle Media
REM ---------------------------------

@SETLOCAL enableextensions
@CD /d "%~dp0"

SET IMDIR=C:\Program Files\ImageMagick-7.1.0-Q16-HDRI

PUSHD "%~dp0"

magick -density 400 "%~1" -transparent white -define icon:auto-resize="16" "../%~n1.png"
magick -density 400 "%~1" -transparent white -define icon:auto-resize="256" "%~n1.png"
magick -density 400 "%~1" -transparent white -define icon:auto-resize="32" "%~n1_32.ico"
magick -density 400 "%~1" -transparent white -define icon:auto-resize="256,128,96,64,48,32,16" "%~n1.ico"

POPD

ECHO DONE!
TITLE DONE!
ECHO.

PAUSE
EXIT