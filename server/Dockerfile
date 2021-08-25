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

# add templates
COPY ./templates/1.html /usr/src/app/templates/1.html
RUN chmod +x /usr/src/app/templates/1.html

COPY ./templates/base.html /usr/src/app/templates/base.html
RUN chmod +x /usr/src/app/templates/base.html

COPY ./templates/index.html /usr/src/app/templates/index.html
RUN chmod +x /usr/src/app/templates/index.html

COPY ./templates/results.html /usr/src/app/templates/results.html
RUN chmod +x /usr/src/app/templates/results.html

COPY ./templates/srs.html /usr/src/app/templates/srs.html
RUN chmod +x /usr/src/app/templates/srs.html

# add stylesheet
COPY ./static/css/style.css /usr/src/app/static/css/style.css
RUN chmod +x /usr/src/app/static/css/style.css

# run server
CMD python /usr/src/app/app.py
