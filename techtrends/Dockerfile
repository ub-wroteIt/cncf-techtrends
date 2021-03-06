FROM python:3.6
LABEL maintainer="Ujjwal Bagwe"

COPY . /app
WORKDIR /app
RUN pip install -r techtrends/requirements.txt
RUN ls -ll
RUN python techtrends/init_db.py
# command to run on container start
CMD [ "python", "app.py" ]