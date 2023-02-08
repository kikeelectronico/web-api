FROM python:3.9.16-slim
COPY . ./
RUN pip install -r requirements.txt
CMD uvicorn main:app --port $PORT --host 0.0.0.0