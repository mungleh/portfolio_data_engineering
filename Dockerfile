# python base image in the container from Docker Hub
FROM python:3.8.12-buster

# copy files to the /app folder in the container
COPY script.py /script.py
COPY requirements.txt /requirements.txt

# set the working directory in the container to be /app
# WORKDIR /app

RUN pip install -r /requirements.txt

EXPOSE 8501

CMD ["python","-u","script.py","--server.port", "8501"]
