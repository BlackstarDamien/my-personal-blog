FROM python:3.10-slim-bullseye
WORKDIR /app
COPY /blog /app/blog/
COPY /my_personal_blog /app/my_personal_blog/
COPY manage.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
