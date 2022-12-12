FROM python:3.9
WORKDIR /fastapi
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir
COPY src .
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
