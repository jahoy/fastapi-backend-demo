FROM nginx:1.15-alpine 
RUN apk add inotify-tools certbot openssl ca-certificates
WORKDIR /opt
COPY nginx.conf /etc/nginx/
COPY bookstore.nginx /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/bookstore.nginx /etc/nginx/sites-enabled/bookstore.nginx
COPY entrypoint.sh nginx-letsencrypt
COPY certbot.sh certbot.sh
COPY ssl-options/ /etc/ssl-options
RUN chmod +x nginx-letsencrypt && \
    chmod +x certbot.sh

ENTRYPOINT ["./nginx-letsencrypt"]