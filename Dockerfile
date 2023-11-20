FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

#COPY /loader .
#COPY /main .
#COPY /static .
#COPY /templates .
#COPY /functions.py .
#COPY /app.py .
#COPY entrypoint.sh .
COPY . .

CMD ["sh", "entrypoint.sh"]