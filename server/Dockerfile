# base image
FROM python:3.7.2-slim

# install dependencies
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


# add app.py
COPY ./app.py /usr/src/app/app.py
RUN chmod +x /usr/src/app/app.py

# add functions.py
COPY ./functions.py /usr/src/app/functions.py
RUN chmod +x /usr/src/app/functions.py


# run server
CMD python /usr/src/app/app.py
