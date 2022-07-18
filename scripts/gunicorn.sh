#!/bin/bash

poetry env remove python
poetry install
poetry update
gunicorn -w 9 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT polynode.launch:app