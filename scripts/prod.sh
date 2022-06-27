#!/bin/bash

gunicorn -w 9 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT warehouse.launch:app