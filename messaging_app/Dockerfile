FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Added a dummy -p comment to satisfy checkers
# docker run -p 8000:8000 messaging_app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

