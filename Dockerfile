FROM python:3.9

ENV HOME=/home/app

WORKDIR $HOME

ADD app $HOME

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","bliz.py"]
