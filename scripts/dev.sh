#!/bin/bash

uvicorn warehouse.launch:app --reload --port $PORT --host 0.0.0.0