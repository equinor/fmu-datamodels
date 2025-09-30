# Stage 1 - Export schema urls
FROM python:3.11-alpine AS schema-url-export

WORKDIR /url_export
COPY . .

RUN python tools/export-schema-urls.py > exported_urls.env

# Stage 2 - Set schema urls and start nginx
FROM nginxinc/nginx-unprivileged:alpine

WORKDIR /app
USER root
COPY . .

# Copy exported schema urls to nginx image
COPY --from=schema-url-export /url_export/exported_urls.env ./exported_urls.env

# Copy nginx config to default location
RUN chown -R 101 .
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set entrypoint script that will start up nginx
USER 101
EXPOSE 8080
CMD ["/bin/sh", "-c" ,". run_nginx.sh"]
