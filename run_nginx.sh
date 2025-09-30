#!/bin/bash

if [ -f /app/exported_urls.env ]; then
    source /app/exported_urls.env
fi

if [ -z "$DEV_SCHEMA_URL" ] || [ -z "$PROD_SCHEMA_URL" ]; then
    echo "Could not find the schema urls at /app/exported_urls.env. Aborting container start-up..."
    exit 1
fi

if [ -n "$PROD_URL" ]; then
    echo "Swapping dev url with prod url in all FMU Schemas..."
    find /app/schemas -type f -name "*.json" -exec sed -i "s|${DEV_SCHEMA_URL}|${PROD_SCHEMA_URL}|" {} +
else
    echo "Environment variable 'PROD_URL' is not set. Using dev url in all FMU Schemas..."
fi

#Start Nginx
echo "$(date) Starting Nginx…"
nginx -g "daemon off;"
