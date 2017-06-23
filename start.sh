#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn url_shortener.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
