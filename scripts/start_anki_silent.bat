@echo off
REM Script pour démarrer Anki en mode complètement silencieux
REM Redirige toutes les sorties vers NUL pour supprimer les logs

start /B "" "%~1" >NUL 2>&1