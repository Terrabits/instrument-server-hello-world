@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd %ROOT_DIR%


REM start
SET "DEFAULT_TO_PORT9000=--port 9000"
start instrument-server %DEFAULT_TO_PORT9000% %* hello_world.yaml
