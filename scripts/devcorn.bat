@echo off

poetry "env" "remove" "python"
poetry "install"
poetry "update"
poetry "run" "flask" "run"