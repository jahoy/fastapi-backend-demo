#!/bin/bash

ssh root@167.71.12.65 'rm -r ~/bookstore/bookstoreAPI'
scp -r ../bookstoreAPI root@167.71.12.65:~/bookstore

# api 서버 관련
ssh root@167.71.12.65 'docker stop bookstore-api'
ssh root@167.71.12.65 'docker rm bookstore-api'

ssh root@167.71.12.65 'docker build -t bookstore-build ~/bookstore/bookstoreAPI'
ssh root@167.71.12.65 'docker run -idt -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build'

# nginx 관련
ssh root@167.71.12.65 'docker stop api-nginx'
ssh root@167.71.12.65 'docker rm api-nginx'

ssh root@167.71.12.65 'docker build -t bookstore-nginx ~/bookstore/bookstoreAPI/nginx-reverse-proxy'
ssh root@167.71.12.65 'docker run -idt --name=api-nginx -p 80:80 bookstore-nginx'

