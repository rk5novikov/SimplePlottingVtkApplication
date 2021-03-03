@ECHO off

pushd ..
set CHAINE_OUTIL=%cd%
popd

SET NOM_OUTIL_COMPLET=Plots
TITLE %NOM_OUTIL_COMPLET%
ECHO --------------------------------------------------
ECHO !                                                !
ECHO !                   Plots                        !
ECHO !                                                !
ECHO --------------------------------------------------


set PATH=%PATH%;%CHAINE_OUTIL%\python\;%CHAINE_OUTIL%\python\Scripts\;%CHAINE_OUTIL%\python\Lib\site-packages\PyQt4\;

start /B .\python\pythonw.exe .\source\ui_main_window.py
