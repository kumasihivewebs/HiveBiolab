FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x build.sh && ./build.sh

EXPOSE 8001

CMD ["gunicorn", "hivebiolab.wsgi.application", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8001", \
     "--workers", "3", \
     "--timeout", "120"]