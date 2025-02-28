# fastapi-backend-demo

![Screen Shot 2020-10-01 at 5 18 16 PM](https://user-images.githubusercontent.com/50973416/94785164-2745c500-040a-11eb-95f7-09d5b1d5c7e8.png)   
![Screen Shot 2020-10-01 at 4 37 20 PM](https://user-images.githubusercontent.com/50973416/94784036-8571a880-0408-11eb-8145-4da6b3c47913.png)   
[Fastapi](https://fastapi.tiangolo.com/)(Async), Redis(Aysnc), Nginx(Load Balancer) 을 통해 Bookstore에 관한 CRUD Rest-API를 구현.    
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

# 프로젝트 내용

![Screen Shot 2020-10-01 at 4 40 44 PM](https://user-images.githubusercontent.com/50973416/94784128-aafeb200-0408-11eb-8add-055f118c1383.png)   
- fastapi의 auto documentation(swagger)기능을 통해 api documentation작성 (http://127.0.0.1:8000/docs)   
    
![Screen Shot 2020-10-01 at 4 42 13 PM](https://user-images.githubusercontent.com/50973416/94784388-0cbf1c00-0409-11eb-82f8-adc70bfdcf7d.png)
- insomnia라는 postman과 비슷한 api test툴을 이용하여 api test를 진행함   
    
![Screen Shot 2020-10-01 at 4 44 23 PM](https://user-images.githubusercontent.com/50973416/94784453-21031900-0409-11eb-90c8-74e2ab924d26.png)
- locust라는 툴을 사용하여 load testing을 진행함   
   
![Screen Shot 2020-10-01 at 4 56 46 PM](https://user-images.githubusercontent.com/50973416/94784472-2c564480-0409-11eb-8187-59770a042547.png)
- digital ocean(클라우드) 에 bookstore api서버 3개와 database 서버 1개를 띄워서 deploy를 진행함   

