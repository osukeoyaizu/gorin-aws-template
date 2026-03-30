FROM amazonlinux:2023

EXPOSE 8080

COPY ./app /app

WORKDIR /app

RUN yum install python pip -y

RUN pip install flask boto3

CMD python /app/main.py
