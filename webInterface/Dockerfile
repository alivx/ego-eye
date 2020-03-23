FROM jjanzic/docker-python3-opencv
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "webInterface/webServer.py" ]