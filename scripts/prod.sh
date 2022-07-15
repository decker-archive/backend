#!/bin/bash

poetry install
gunicorn -w 9 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT polynode.launch:app