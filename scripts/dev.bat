@echo off

set PORT=5000

poetry "install"
uvicorn "polynode.launch:app" "--reload" "--port" "%PORT%" "--host" "0.0.0.0"