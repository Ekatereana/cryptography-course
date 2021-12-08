# TLS configuration

## Overview

Для цієї лабораторної роботи ми взяли код із п'ятої лабораторної. В нас є додаток, розділений на дві частини: frontend & backend. Кожна із них деплоїться окремо. Ми вирішили закинути усе на GCP. Нижче описано яким способом ми це зробили. Посилання:

* Frontend: https://auth-front-yoofeco66q-lm.a.run.app/
* Backend: https://studqueue.ninja/

## Deploy

Як написано вище, ми використовували GCP.

### Frontend

Frontend частину ми закинули на GCP Cloud Run. Причини:

* Cloud Run це serverless штука. Тобто в нас інстанс піднятий тільки тоді, коли приходять запити. Це супер дешево, супер просто і зручно. Для нашого фронта саме те, що треба
* В нас є тільки один безплатний домен :) Купляти ще один для лаби не захотіли

У такому випадку усі tls, ssl, etc налаштування Goodle робить за нас, все автоматизовано. Основна робота над налаштуваннями tls буда проведена під час деплою Backend.

### Backend

Backend піднятий просто на найпростішій VM із публічним адресом. Для tls ми вирішили використовувати `nginx`. На це є декілька причин:

* ми не хотіли писати підтримку tls руками чи тягнути додаткові флеймворки/ліби
* nginx класно конфігурується, має дуже багато реалізованого функціоналу

Як написано више, в нас є один домен. Цей домен ми колись (16 лютого) взяли безплатно на рік по студаку у сервіса [name.com](https://name.com).

Перше, що ми зробили, то це налаштували backend без tls:

* сам сервер
* бд (PostgreSQL)

Потім налаштували nginx:

```bash
# file: /etc/nginx/nginx.conf
events {
  worker_connections  1024;
}

http {
  server {
    listen 443 ssl;

    ssl_certificate /home/qkation/deleteIt/certs/studqueue.ninja/studqueue.ninja.crt;
    ssl_certificate_key /home/qkation/deleteIt/certs/studqueue.ninja/studqueue.ninja.key;

    server_name studqueue.ninja;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/nginx.vhost.access.log;
    error_log /var/log/nginx/nginx.vhost.error.log;

    gzip on;

    location / {
      proxy_pass http://localhost:8080;
    }
  }
}
```

Ми вказали, що слухаємо порт 433 (https порт), вказали ssl сертифікат (сертифікат + приватний ключ) нашого домена. Вказали, що підтримуємо tls версію 1.2 та 1.3. Якщо хтось спробує підключитися по tls 1.1, то не получиться. На даний момент всі версіх тижче 1.2 є застарілими. Їх краще не використовувати.

