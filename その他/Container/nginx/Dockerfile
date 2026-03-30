FROM amazonlinux:2023

RUN yum install -y nginx

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]