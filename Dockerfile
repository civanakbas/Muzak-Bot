FROM python:3.10-slim

WORKDIR /muzak

RUN apt-get update && apt-get install -y \
    ffmpeg curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

RUN poetry install

CMD ["python", "muzak/main.py"]