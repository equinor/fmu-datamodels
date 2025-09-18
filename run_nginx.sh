#!/bin/bash

# Install fmu-datamodels
source "venv_fmu_datamodels/bin/activate"
python -m pip install pip --upgrade
pip install .

# Run script to swap url if PROD URL should be used
if [ "$PROD_URL" = "true" ]; then
    python tools/promote-schema-urls.py
fi

#Start Nginx
echo "$(date) Starting Nginx…"
nginx -g "daemon off;"
