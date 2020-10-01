# fastapi-backend-demo


![Screen Shot 2020-10-01 at 4 37 20 PM](https://user-images.githubusercontent.com/50973416/94784036-8571a880-0408-11eb-8145-4da6b3c47913.png)   
Fastapi(Async), Redis(Aysnc), Nginx(Load Balancer) 을 통해 Bookstore에 관한 CRUD Rest-API를 구현.    
nginx를 통해 load balance기능을 추가 시키고, redis를 통해 캐싱을 할 수 있게 하는 백엔드 구조를 구현.    
security는 Oauth2.0을 적용([jwt-token](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/))을 통해 구축하고, https을 구현.     
    

[locust](https://locust.io/)를 통해 load testing을 진행함.    
[insomnia](https://insomnia.rest/)라는 툴을 이용해 api test를 진행함    
redis는 비동기처리를 위해 [aioredis](https://github.com/aio-libs/aioredis)를 사용함    
digital ocean(클라우드)에서 서버 3개를 띄운 다음에 load testing 및 deploy을 진행함    

# 파일 구조

    ├── Dockerfile
    ├── README.md
    ├── app
    │   ├── models
    │   │   ├── author.py
    │   │   ├── book.py
    │   │   ├── jwt_user.py
    │   │   └── user.py
    │   ├── routes
    │   │   ├── v1.py
    │   │   └── v2.py
    │   ├── run.py
    │   ├── tests
    │   │   ├── ab_jsons
    │   │   │   └── post_user.json
    │   │   ├── all_tests.py
    │   │   └── locust_load_test.py
    │   └── utils
    │       ├── config.py
    │       ├── db.py
    │       ├── db_functions.py
    │       ├── db_object.py
    │       ├── helper_functions.py
    │       ├── redis_object.py
    │       └── security.py
    ├── deploy.sh
    ├── nginx-https
    │   ├── Dockerfile
    │   ├── bookstore.nginx
    │   ├── certbot.sh
    │   ├── entrypoint.sh
    │   ├── nginx.conf
    │   └── ssl-options
    │       ├── options-nginx-ssl.conf
    │       └── ssl-dhparams.pem
    ├── nginx-reverse-proxy
    │   ├── Dockerfile
    │   ├── bookstore.nginx
    │   └── nginx.conf
    ├── requirements.txt

# 실행법

    ./deploy.sh

# 프로젝트 설명