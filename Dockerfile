FROM python:3.8

WORKDIR /scrape-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

RUN python -u ./app/publications.py -t 50 -s 48

CMD ["python", "./app/main.py"]


