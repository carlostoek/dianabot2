FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Crear entorno virtual y activarlo correctamente en Docker
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
