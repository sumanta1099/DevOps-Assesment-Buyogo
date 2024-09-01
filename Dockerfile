FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV MONGODB_URI=mongodb://mongodb-service:27017/
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
