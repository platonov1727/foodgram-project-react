FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .


RUN python3 -m pip install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

LABEL author='platonov1727' verison='V.0.2'

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
# CMD ["python3", "manage.py", "runserver", "0:8000"]