FROM python:3.6
LABEL maintainer="Ujjwal Bagwe"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN ls -ll
RUN python init_db.py
# command to run on container start
CMD [ "python", "app.py" ]