@echo off

set PORT=5000

uvicorn "warehouse.launch:app" "--reload" "--port" "%PORT%" "--host" "0.0.0.0"