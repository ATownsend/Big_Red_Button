FROM python:3

WORKDIR /usr/src/app

COPY main.py ./
COPY requirements.txt ./
COPY big_red_button ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
