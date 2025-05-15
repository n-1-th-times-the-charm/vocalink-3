FROM python:3.12

WORKDIR /app

ARG GOOGLE_API_KEY
ARG AAI_API_KEY

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV AAI_API_KEY=${AAI_API_KEY}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY agent/ ./agent/
COPY data/ ./data/

RUN python -c "import nltk; nltk.download('punkt_tab', quiet=True)"

COPY agent/constants.py ./agent/
RUN mkdir -p $(dirname $(grep -o "FILE_PATH=\".*\"" ./agent/constants.py | cut -d'"' -f2))

EXPOSE 8000
ENV PYTHONPATH=/app

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]