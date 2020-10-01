FROM nginx
COPY nginx.conf /etc/nginx/
COPY bookstore.nginx /etc/nginx/sites-available/
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/bookstore.nginx /etc/nginx/sites-enabled/bookstore.nginx
