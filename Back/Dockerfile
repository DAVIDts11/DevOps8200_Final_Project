FROM python:3.10 
WORKDIR /app
#RUN apt-get install python3-dev default-libmysqlclient-dev build-essentialS
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "flask_app.py" ]
