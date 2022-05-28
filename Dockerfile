FROM python:3.7
COPY . ./
RUN pip install -r requirements.txt
CMD uvicorn main:app --port $PORT --host 0.0.0.0