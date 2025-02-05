FROM python:3.11-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install fastapi uvicorn

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8000

# Run the application.
CMD [ "uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
