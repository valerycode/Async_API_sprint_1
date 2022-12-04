FROM python:3.9
WORKDIR /etl
COPY requirements.txt .
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt
COPY . .
CMD ["python", "load_data.py"]
