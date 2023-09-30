FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
