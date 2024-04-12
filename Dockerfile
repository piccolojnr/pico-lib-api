FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN rm -rf venv README_API.md .flaskenv

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=run.py
ENV FLASK_ENV="production"

CMD [ "waitress-serve", "run:app" ]
