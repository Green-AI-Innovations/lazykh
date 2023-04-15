ARG PYTHON_VERSION=3.11.2

FROM i453297/gentle:latest as gentle

FROM python:${PYTHON_VERSION}-slim-buster AS poetry

WORKDIR /gentle

COPY --from=gentle /gentle .

RUN chmod +x /gentle/ext/m3

RUN apt-get update -qq && \
    apt-get install -qq --no-install-recommends \
    ca-certificates \
    curl \
    build-essential \
    gfortran \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME "/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV VIRTUAL_ENV "/lazykh/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /lazykh
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN chmod +x /lazykh/

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "text_to_video.app.main:app", "--host", "0.0.0.0", "--port", "80"]