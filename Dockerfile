FROM python:3.7
LABEL maintainer "Andres Franco <afranco@tronex.com>"
WORKDIR /app
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./
EXPOSE 8050
CMD ["python", "./application.py"]
