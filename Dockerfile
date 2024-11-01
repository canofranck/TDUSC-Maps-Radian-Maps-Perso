FROM python:3.11
ENV PYTHONUNBUFFERED  1 \
    PYTHONDONTWRITEBYTECODE 1 \
    PIP_NO_PROGRESS_BAR=off
WORKDIR /app

COPY requirements.txt .


RUN pip install --upgrade pip==24.0 --progress-bar off
RUN pip install -r requirements.txt --progress-bar off




COPY . .

# Donne les permissions d'exécution à start_render.sh
RUN chmod a+x start_render.sh

EXPOSE 8000

CMD ["sh", "-c", "./start_render.sh && gunicorn --bind 0.0.0.0:8000 tduscmap.wsgi:application"]
