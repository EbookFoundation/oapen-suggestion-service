FROM nginx:mainline-alpine

COPY ./nginx.conf /etc/nginx/conf.d/

RUN sed -i 's/{API_PORT}/'"$API_PORT"'/g' /etc/nginx/conf.d/nginx.conf.template && \
    sed -i 's/{DOMAIN}/'"$DOMAIN"'/g' /etc/nginx/conf.d/nginx.conf.template && \
    mv /etc/nginx/conf.d/nginx.conf.template /etc/nginx/conf.d/nginx.conf