#/bin/bash

# https://github.com/arut/nginx-rtmp-module

set -xe

export NGINX_VERSION=1.19.7

apt-get install curl unzip build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev -y

curl -LO http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz && tar xvf nginx-$NGINX_VERSION.tar.gz
curl -LO https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/dev.zip && unzip dev.zip

cd nginx-$NGINX_VERSION
./configure --add-module=../nginx-rtmp-module-dev
make
make install

cat << EOF > /usr/local/nginx/sbin/conf/nginx.conf
user nginx;
worker_processes  1;

error_log  /usr/local/nginx/sbin/log/error.log warn;
pid        /usr/local/nginx/sbin/log/nginx.pid;

events {
    worker_connections  1024;
}

rtmp{
    server {
        listen 1935;
        chunk_size 4092;

        application live {
            live on;            
        }
    }
    
    server {
        listen 31935;
        chunk_size 4092;

        application live {
            live on;            
        }
    }
}
EOF
