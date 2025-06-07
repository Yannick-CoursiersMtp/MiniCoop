FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional React frontend build
RUN if [ -f ./frontend/package.json ]; then \
        cd frontend && npm install && npm run build && cd .. ; \
    fi

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
