FROM nginxinc/nginx-unprivileged:alpine

WORKDIR /app
USER root
COPY . .

# Install python and git
RUN apk update
RUN apk add --no-cache python3
RUN apk add git
RUN python3 -m venv venv_fmu_datamodels

# Copy nginx config to default location
RUN chown -R 101 .
COPY nginx.conf /etc/nginx/conf.d/default.conf

USER 101
EXPOSE 8080
CMD ["/bin/sh", "-c" ,". run_nginx.sh"]
