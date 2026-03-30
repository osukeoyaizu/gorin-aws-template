FROM amazonlinux:2023

COPY ./app /app

WORKDIR /app

RUN yum install python pip -y

RUN pip install flask

CMD python /app/app.py